import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from template import css, bot_template, user_template




try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


def get_pdf_text(pdf_docs):
    text = ""               
    for pdf in pdf_docs:    #goes through each uploaded PDF file
        pdf_reader = PdfReader(pdf) 
        for page in pdf_reader.pages: #reads all pages of each PDF
            text += page.extract_text() #joins everything into one big text string
    return text


def get_text_chunk(text): 
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000, #size of each chunk
        chunk_overlap = 200, #starts chunk from 200 char before prev chunk 
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

@st.cache_resource
def get_embeddings_client():
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        language="en",
    )


@st.cache_resource(show_spinner=False)
def get_vectorstore(text_chunks):
    embeddings = get_embeddings_client()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages= True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )
    return conversation_chain


def handle_user_input(user_question):
    response = st.session_state.conversation.invoke({'question': user_question, 'chat_history': st.session_state.chat_history})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    #load environment variables
    load_dotenv()
    st.set_page_config(page_title = "ChatPDF", page_icon=":books:", layout="wide")
    st.write(css,unsafe_allow_html=True)

    st.header(" Chat with multiple PDFs :books:")
    st.markdown("---")

    
    
    with st.form("question_form", clear_on_submit=True):
        user_question = st.text_input("\U0001F4AC Ask me anything about your document!")
        submitted = st.form_submit_button("Send")

    if submitted and user_question:
        if not st.session_state.conversation:
            st.warning("⚠️ Please upload and process PDFs before asking questions.")
        else:
            handle_user_input(user_question)


    if "conversation" not in st.session_state:
        st.session_state.conversation =  None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    with st.sidebar:
        st.subheader("documents")
        pdf_docs = st.file_uploader("Upload your PDFs here!",accept_multiple_files=True)

        #if user removes all PDFs (pdf_docs is empty or None), reset conversation
        if not pdf_docs:
            st.session_state.conversation = None
            st.session_state.chat_history = None

        if st.button("Upload PDFs"): #becomes true only when user clicks button
            if pdf_docs:
                with st.spinner("Processing"):

                    #get all the text from pdf
                    raw_text = get_pdf_text(pdf_docs)
                    
                    #get text chunks 
                    text_chunks = get_text_chunk(raw_text)

                    #create vector store
                    vectorstore = get_vectorstore(text_chunks)

                    #create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)

                st.success("✅ PDFs processed successfully!")
            else:
                st.warning("⚠️ Please upload at least one PDF before processing.")

if __name__ == "__main__":
    main()
