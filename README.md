# ChatPDF – Chat with Multiple PDFs 📚

An interactive **Streamlit** app that allows you to upload multiple PDFs, process them into vector embeddings using **LangChain + FAISS**, and query them conversationally using **Google Gemini models**.

---

## 🚀 Features
- 📂 **Upload Multiple PDFs** — Process multiple documents in one session.
- 🧩 **Chunk Text Automatically** — Splits large documents into manageable chunks.
- 🗂 **FAISS Vector Store** — Stores embeddings for fast similarity search.
- 🧠 **Conversational Memory** — Remembers previous queries in the session.
- 🤖 **Google Gemini Integration** — Uses Gemini Pro for intelligent answers.
- ⚡ **Streamlit Interface** — Easy to run locally or deploy to the web.

---

## 🛠 Prerequisites
- **Python** 3.9 or later
- **Google API Key** (Gemini model access)
- Git installed on your system

---

## 📥 Installation & Setup (Local)

1. **Clone the repository**  
   `git clone https://github.com/<your-username>/<repo-name>.git`  
   `cd <repo-name>`

2. **Install dependencies**  
   `pip install -r requirements.txt`

3. **Set up environment variables**  
   Create a `.env` file in the root directory and add your Google Gemini API key:  
   `GOOGLE_API_KEY=your_api_key_here`

4. **Run the Streamlit app**  
   `streamlit run app.py`
