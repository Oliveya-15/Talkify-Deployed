import os
import base64
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

from htmlTemplates import css, bot_template, user_template


def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


logo_img = get_base64("logo.png")


def get_pdf_text(pdf_docs):
    """Extract text from a list of uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text


def get_text_chunks(text):
    """Split text into overlapping chunks for embedding."""
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    """Create a FAISS vector store from text chunks using HuggingFace embeddings."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    """Build a conversational retrieval chain with memory."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    """Process user's question and update the chat history."""
    if st.session_state.conversation is None:
        st.warning("Please upload and process PDFs first.")
        return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(
                user_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True
            )
        else:
            st.write(
                bot_template.replace("{{MSG}}", message.content),
                unsafe_allow_html=True
            )


def main():
    load_dotenv()

    st.set_page_config(
        page_title="Talkify – Chat with your PDFs",
        page_icon="logo.png"
    )
    st.write(css, unsafe_allow_html=True)

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ---------- Custom header ----------
    st.markdown(
        f"""
        <div class="title-container">
            <img src="data:image/png;base64,{logo_img}" width="60">
            <h1>Talkify</h1>
        </div>
        <p class="subtitle">Chat intelligently with your documents – upload, process & ask anything.</p>
        """,
        unsafe_allow_html=True
    )

    # User query input
    user_question = st.text_input("Ask a question about your documents:")

    if user_question:
        handle_userinput(user_question)

    # ---------- Sidebar ----------
    with st.sidebar:
        st.subheader("📄 Your Documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'",
            accept_multiple_files=True,
            type="pdf"
        )

        if st.button("Process"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF.")
                return

            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.conversation = get_conversation_chain(vectorstore)

            st.success("✅ Done! Ask a question above.")

        # "How it Works" guide
        st.markdown("""
        <div class="how-it-works">
            <h3>🚀 How it Works</h3>
            <ol>
                <li><strong>Upload</strong> one or more PDF documents using the file uploader above.</li>
                <li><strong>Process</strong> the files by clicking the <em>Process</em> button – this extracts and indexes the text.</li>
                <li><strong>Ask questions</strong> in the main chat – the AI will answer based on your documents.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()