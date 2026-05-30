# 🤖 AI Code Reviewer

> Intelligent Source Code Analysis & Optimization powered by Google Gemini AI

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)](https://flask.palletsprojects.com)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange?logo=google)](https://ai.google.dev)
[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://ai-code-reviewer-o5hf.onrender.com)

---

## ✨ Overview

AI Code Reviewer is a full-stack web application that analyzes source code and provides **actionable AI-powered feedback** across three key areas:

- 🐛 **Bug Detection** — Logical errors, security vulnerabilities & off-by-one errors
- ⚡ **Optimization** — Performance inefficiencies, memory leaks & algorithmic improvements
- 🎨 **Code Quality** — Readability, best practices, naming conventions & maintainability

Built as part of the **VISION X Hackathon** — "Turning Vision Into Reality".

---

## 🚀 Live Demo

**[https://ai-code-reviewer-o5hf.onrender.com](https://ai-code-reviewer-o5hf.onrender.com)**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Vanilla HTML, CSS, JavaScript |
| **Code Editor** | Monaco Editor (VS Code engine) |
| **Backend** | Python, Flask |
| **AI Engine** | Google Gemini API (`gemini-2.5-flash`) |
| **Production Server** | Gunicorn |
| **Hosting** | Render.com |

---

## 📋 Features

- **Multi-language support** — JavaScript, Python, Java, C++, Go
- **Tabbed results dashboard** — Clean, categorized review output
- **Cyberpunk dark UI** — Neon purple aesthetic with animated backgrounds
- **Monaco Editor** — Syntax-highlighted, VS Code-powered code input
- **Instant analysis** — Real-time AI feedback with loading states

---

## 🏃 Running Locally

### Prerequisites
- Python 3.9+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey) (free)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-code-reviewer.git
   cd ai-code-reviewer
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   ```bash
   # Create a .env file in the project root
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

5. Open your browser and navigate to **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🌍 Sharing Locally (Temporary Public URL)

To share a temporary public link from your local machine:
```bash
./share.sh
```
This uses Pinggy to create a public tunnel. The link expires after 60 minutes.

---

## 🚢 Deploying to Render (Cloud)

1. Push your code to a GitHub repository.
2. Sign up at [Render.com](https://render.com) and create a **New Web Service**.
3. Connect your GitHub repository.
4. Use these settings:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add an **Environment Variable**: `GEMINI_API_KEY` = your API key.
6. Click **Deploy** — your app will be live in ~2 minutes!

---

## 📁 Project Structure

```
ai-code-reviewer/
├── app.py                  # Flask backend & Gemini API integration
├── Procfile                # Gunicorn startup command for production
├── requirements.txt        # Python dependencies
├── share.sh                # Script to generate a temporary public URL
├── .gitignore              # Ignores .env, venv/, __pycache__/
├── templates/
│   └── index.html          # Main HTML page with Monaco Editor
└── static/
    ├── styles.css          # Dark cyberpunk UI styles
    └── script.js           # Frontend logic & API calls
```

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API key (required) |

> ⚠️ **Never commit your `.env` file to GitHub.** It's already included in `.gitignore`.

---

## 🎯 Problem Statement

This project was built for **VISION X Hackathon — Problem Statement 5: AI Code Reviewer**.

> *"Build an AI-powered tool that analyzes source code and provides suggestions for improvement, including bug detection, optimization, and code quality enhancement. The system should understand code structure and give meaningful feedback to developers."*

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
