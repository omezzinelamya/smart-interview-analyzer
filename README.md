# 🎯 Smart Interview Analyzer

An AI-powered web application that analyzes interview videos, transcribes content, and evaluates candidates against job requirements using **Retrieval-Augmented Generation (RAG)**.

## 📌 Features
- 📤 Upload interview videos or download directly from **YouTube**
- 📝 Automatic transcription of video content
- 🤖 Candidate-job matching with **Google Gemini API**
- 🧠 **RAG pipeline** using **LangChain** + **Chroma Vector DB** for context-aware analysis
- 🎨 Modern UI with **Streamlit** (custom theme)

## 🛠 Tech Stack
- **Python**
- **Streamlit** (Frontend)
- **LangChain** (Text processing & RAG)
- **ChromaDB** (Vector store)
- **Google Gemini API** (Embedding & AI reasoning)
- **Pytube** (YouTube video download)
- **Whisper / Speech-to-Text** (Transcription)

## 📂 Project Structure

├── app.py # Main Streamlit app
├── modules/
│ ├── analysis.py # Candidate matching logic
│ ├── embedding_utils.py # Text embedding & vector store
│ ├── transcription.py # Video transcription
│ ├── video_utils.py # Upload & download helpers
├── requirements.txt
└── README.md


## 🚀 How to Run

1️⃣ Clone the repository
```bash
git clone https://github.com/omezzinelamya/smart-interview-analyzer.git
cd smart-interview-analyzer
```
2️⃣ Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```
3️⃣ Add your API keys in .env
```bash
GOOGLE_API_KEY=your_google_gemini_key
```
4️⃣ Run the app
```bash
streamlit run app.py
```
