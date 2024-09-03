import os
import time
import pickle
from urllib.parse import urlparse
import hashlib
from datetime import datetime
import streamlit as st
from langchain.document_loaders import SitemapLoader
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import openai
from tenacity import retry, stop_after_attempt, wait_exponential
from bs4 import BeautifulSoup
import numpy as np

st.set_page_config(
    page_title="Site GPT",
    page_icon="🌐",
    layout="wide",
)

llm = ChatOpenAI(temperature=0.1)

answers_prompt = ChatPromptTemplate.from_template(
    """
    Using ONLY the following context answer the user's question. If you can't just say you don't know, don't make anything up.

    Then, give a score to the answer between 0 and 5.
    If the answer answers the user question the score should be high, else it should be low.
    Make sure to always include the answer's score even if it's 0.

    Context: {context}

    Examples:

    Question: How far away is the moon?
    Answer: The moon is 384,400 km away.
    Score: 5

    Question: How far away is the sun?
    Answer: I don't know
    Score: 0

    Your turn!
    Question: {question}"""
)


def get_answers(inputs):
    docs = inputs["docs"]
    question = inputs["question"]
    answers_chain = answers_prompt | llm
    return {
        "question": question,
        "answers": [
            {
                "answer": answers_chain.invoke(
                    {"question": question, "context": doc.page_content, }).content,
                "source": doc.metadata["source"],
                "date": doc.metadata.get("lastmod", "Unknown"),
            }
            for doc in docs
        ],
    }


choose_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
        Use ONLY the following pre-existing answers to answer the user's question.
        Use the answers that have the highest score (more helpful) and favor the most recent ones.
        Cite sources and return the sources of the answers as they are, do not change them.
        Answers: {answers}
        """,
        ),
        ("human", "{question}",)
    ]
)


def choose_answer(inputs):
    answers = inputs["answers"]
    question = inputs["question"]
    choose_chain = choose_prompt | llm
    condensed = "\n\n".join(
        f"{answer['answer']}\nSource:{answer['source']}\nDate:{answer['date']}\n"
        for answer in answers
    )
    return choose_chain.invoke(
        {
            "question": question,
            "answers": condensed,
        }
    )


def parse_page(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    return text


@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(6))
def embed_single_text(text, embeddings):
    try:
        embedded = embeddings.embed_query(text)
        if isinstance(embedded, list):
            return embedded
        elif isinstance(embedded, (int, float, np.float64)):
            # Ensure embedding is a list, even if it's a single float value
            return [float(embedded)]  # Convert to float and then to list
        else:
            raise ValueError(f"Unexpected embedding type: {type(embedded)}")
    except openai.error.RateLimitError as e:
        st.warning(f"Rate limit reached. Retrying after delay...")
        # Default to 10 seconds if retry_after is not set
        time.sleep(e.retry_after or 10)
        raise  # Re-raise to trigger the retry
    except Exception as e:
        st.error(f"Embedding error for text '{text[:50]}...': {str(e)}")
        return None


def get_cache_path(url, max_pages):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path.replace('/', '_')
    url_hash = hashlib.md5(url.encode()).hexdigest()
    cache_dir = os.path.join('gpts', '.cache', 'site_files')
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"{domain}_{path}_{url_hash}_max{max_pages}")


def load_or_create_embeddings(texts, cache_path):
    embeddings_path = f"{cache_path}_embeddings.pkl"
    cache_dir = os.path.dirname(embeddings_path)
    os.makedirs(cache_dir, exist_ok=True)

    if os.path.exists(embeddings_path):
        with open(embeddings_path, 'rb') as f:
            return pickle.load(f)

    embeddings = OpenAIEmbeddings()
    embedded = []
    for text in texts:
        try:
            emb = embed_single_text(text, embeddings)
            if emb is not None:
                embedded.append(emb)
        except openai.error.RateLimitError as e:
            st.warning(
                f"Rate limit reached. Waiting for {e.retry_after or 10} seconds.")
            time.sleep(e.retry_after or 10)
            emb = embed_single_text(text, embeddings)
            if emb is not None:
                embedded.append(emb)
        except Exception as e:
            st.warning(f"Error during embedding: {str(e)}")
        time.sleep(1)

    if not embedded:
        raise ValueError("No valid embeddings were created.")

    with open(embeddings_path, 'wb') as f:
        pickle.dump(embedded, f)

    return embedded


def parse_date(date_str):
    if not date_str:
        return datetime.min
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return datetime.min


@st.cache_resource(show_spinner="Loading website...")
def load_website(url, max_pages):
    cache_path = get_cache_path(url, max_pages)

    if os.path.exists(cache_path):
        vector_store = FAISS.load_local(cache_path, OpenAIEmbeddings())
        return vector_store.as_retriever()

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )

    loader = SitemapLoader(
        url,
        parsing_function=parse_page,
    )
    loader.requests_per_second = 2

    docs = []
    for i, doc in enumerate(loader.lazy_load()):
        if i >= max_pages:
            break
        doc.metadata['lastmod'] = parse_date(doc.metadata.get('lastmod'))
        docs.append(doc)

    docs.sort(key=lambda x: x.metadata['lastmod'], reverse=True)
    split_docs = splitter.split_documents(docs)

    texts = [doc.page_content for doc in split_docs]
    metadatas = [doc.metadata for doc in split_docs]

    try:
        embedded_texts = load_or_create_embeddings(texts, cache_path)
    except ValueError as e:
        st.error(f"Error creating embeddings: {str(e)}")
        return None

    # Ensure dtype is object
    embedded_texts = np.array(embedded_texts, dtype=object)
    vector_store = FAISS.from_embeddings(
        embedded_texts, OpenAIEmbeddings(), metadatas=metadatas)
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    vector_store.save_local(cache_path)

    return vector_store.as_retriever()


st.title("🌐 Site GPT")
st.markdown("Welcome to Site GPT!")

with st.sidebar:
    url = st.text_input("Write Down URL Here!",
                        placeholder="https://example.com/sitemap.xml")
    max_pages = st.number_input(
        "Maximum number of pages to process", min_value=1, value=100)

if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        try:
            retriever = load_website(url, max_pages)
            if retriever:
                query = st.text_input("Ask a question to Website.")
                if query:
                    chain = ({
                        "docs": retriever,
                        "question": RunnablePassthrough(),
                    } | RunnableLambda(get_answers) | RunnableLambda(choose_answer)
                    )
                    result = chain.invoke(query)
                    st.markdown(result.content)
            else:
                st.error(
                    "Failed to load the website. Please check the URL and try again.")
        except openai.error.RateLimitError as e:
            st.error(
                f"OpenAI API 사용량 제한에 도달했습니다. 잠시 후 다시 시도해주세요. 상세 오류: {str(e)}")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
