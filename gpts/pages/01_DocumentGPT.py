import streamlit as st

st.title("📄 Document GPT")

st.markdown("""
<div class="app-block">
    <h2>Upload Your Document</h2>
    <p>Upload a document and ask questions about its content.</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("File uploaded successfully!")
    st.text_input("Ask a question about your document:")
    if st.button("Ask"):
        st.write("This is where the answer would appear.")