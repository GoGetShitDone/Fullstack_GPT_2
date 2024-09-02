from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import Html2TextTransformer
import streamlit as st

st.set_page_config(
	page_title="Site GPT",
	page_icon="🌐",
    layout="wide",
)

html2text_transformer = Html2TextTransformer()

st.title("🌐 Site GPT")

st.markdown("Welcome to Site GPT!")

with st.sidebar:
	url = st.text_input("Write Down URL Here!", placeholder="https://exampl.com",)

if url:
	loader = AsyncChromiumLoader([url])
	docs = loader.load()
	transformed = html2text_transformer.transform_documents(docs)
	st.write(docs)