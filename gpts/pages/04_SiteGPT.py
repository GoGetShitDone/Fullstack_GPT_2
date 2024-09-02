from langchain.document_loaders import SitemapLoader, text
from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st


def parse_page(soup):
    header = soup.find("header")
    footer = soup.find("footer")
    if header:
        header.decompose()
    if footer:
        footer.decompose()
    return str(soup.get_text()).replace("/n", " ").replace("<li>", " ").replace("</li>", " ").replace("<p>", " ").replace("</p>", " ").replace("<li>", " ").replace("</li>", " ").replace("<strong>", " ").replace("</strong>", " ").replace("<figure>", " ").replace("</figure>", " ").replace("\n", " ").replace("</iframe>", " ").replace("<iframe>", " ").replace("<ul>", " ").replace("</ul>", " ").replace("<a href=", " ").replace("</a>", " ").replace("<br>", " ")


@st.cache_data(show_spinner="Loading website...")
def load_website(url):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )
    loader = SitemapLoader(
        url,
        filter_urls=[r"^(.*\/blog\/).*",], parsing_function=parse_page
    )
    loader.requests_per_second = 1
    docs = loader.load_and_split(text_splitter=splitter)
    return docs


st.set_page_config(
    page_title="Site GPT",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 Site GPT")

st.markdown("Welcome to Site GPT!")

with st.sidebar:
    url = st.text_input("Write Down URL Here!",
                        placeholder="https://exampl.com/sitemap.xml",)

if url:
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a Sitemap URL")
    else:
        docs = load_website(url)
        st.write(docs)
