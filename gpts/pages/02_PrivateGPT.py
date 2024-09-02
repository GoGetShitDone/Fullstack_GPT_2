from langchain.prompts import ChatPromptTemplate
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import CacheBackedEmbeddings, OllamaEmbeddings
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chat_models import ChatOllama
from langchain.callbacks.base import BaseCallbackHandler
import streamlit as st

st.set_page_config(
	page_title="🔒 Private GPT",
	page_icon="🔒",
	layout="wide",
)

class ChatCallbackHandler(BaseCallbackHandler):
    message = ""

    def on_llm_start(self, *args, **kwargs):
        self.message_box = st.empty()

    def on_llm_end(self, *args, **kwargs):
        save_message(self.message, "ai")

    def on_llm_new_token(self, token, *args, **kwargs):
        self.message += token
        self.message_box.markdown(self.message)


llm = ChatOllama(
	model="mistral:latest",
    temperature=0.1,
    streaming=True,
    callbacks=[
        ChatCallbackHandler(),
    ],
)

@st.cache_data(show_spinner="Embedding File...")
def embed_file(file):
	file_content = file.read()
	file_path = f"./.cache/private_files/{file.name}"
	with open(file_path, "wb") as f:
		f.write(file_content)
	cache_dir = LocalFileStore(f"./.cache/private_embeddings/{file.name}")
	splitter = CharacterTextSplitter.from_tiktoken_encoder(
		separator="\n",
		chunk_size=600,
		chunk_overlap=100,
	)
	loader = UnstructuredFileLoader(file_path)
	docs = loader.load_and_split(text_splitter=splitter)
	embeddings = OllamaEmbeddings(model="mistral:latest")
	cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)
	vectorstore = FAISS.from_documents(docs, cached_embeddings)
	retriever = vectorstore.as_retriever()
	return retriever

def save_message(message, role):
	st.session_state["messages"].append({"message": message, "role": role})

def send_message(message, role, save=True):
	with st.chat_message(role):
		st.markdown(message)
	if save:
		save_message(message, role)

def paint_history():
	for message in st.session_state["messages"]:
		send_message(message["message"], message["role"], save=False,)

def format_docs(docs):
	return "\n\n".join(document.page_content for document in docs)

prompt = ChatPromptTemplate.from_messages(
	[
		(
            "system",
            """
            Answer the question using ONLY the following context. If you don't know the answer just say you don't know. DON'T make anything up.
            
            Context: {context}
            """,
        ),
        ("human", "{question}"),
	]
)

st.title("🔒 Private GPT")

st.markdown("인터넷 연결을 해제하고 사용할 수 있는 챗봇입니다.<br>이 챗봇을 사용하여 사적인 파일에 대해 AI에게 질문하세요!<br>사이드바에서 파일을 업로드하세요!", unsafe_allow_html=True)

with st.sidebar:
	file = st.file_uploader("Upload a .txt, .pdf, .docs file", type=["pdf","txt","docx","md"],)

if file:
	retriever = embed_file(file)
	send_message("Good! Ask Anything!", "ai", save=False)
	paint_history()
	message = st.chat_input("Ask Anything! about your file...")
	if message:
		send_message(message, "human")
		chain = ({
			"context" : retriever | RunnableLambda(format_docs), 
			"question": RunnablePassthrough(),
			} | prompt | llm)		
		with st.chat_message("ai"):
			chain.invoke(message)
			
else:
	st.session_state["messages"] = []
