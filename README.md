# 🔍 Azure RAG Chatbot (Flask Interface)

A simple Flask web interface for a chatbot powered by Azure Prompt Flow using Retrieval-Augmented Generation (RAG). This project demonstrates a user-friendly frontend and backend integration with a deployed flow on Azure Machine Learning.

---

<img width="959" height="448" alt="chatbot" src="https://github.com/user-attachments/assets/7dc65de5-2412-47bb-93fe-ad8ce743059a" />

---
## 🧠 Features

- Simple chat UI 
- Azure Prompt Flow integration (via REST API)
- Penguin 🐧 and robot 🤖 avatars for chat messages
- Designed to run locally with clean Flask routing

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/RAG-Operations.git
cd RAG-Operations
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### 3. Set up your secret keys

Create a file named `keys.py` in the project root (already ignored in `.gitignore`) and add the following:

```python
promptflow_api_key = "your-azure-api-key"
endpoint_url = "https://your-endpoint-url/score"
```

If using OAuth or Google APIs, place your `client_secret_*.json` file in the same directory — also ignored by Git.

---

## 🧪 Running the App

```bash
python app.py
```

Then open your browser to:

```
http://127.0.0.1:5000/
```

---

## 📁 Project Structure

```
Azure-Operations/
├── app.py                    # Main Flask application
├── templates/
│   └── chatbot.html          # Web UI
├── keys.py                   # 🔒 Contains secrets (not tracked by Git)
├── client_secret_*.json      # 🔒 Google OAuth or external secrets (not tracked)
├── .gitignore                # Git exclusions
└── README.md                 # Project documentation
```

---

## 📄 License

MIT License © 2025 Hassan Ahmed
