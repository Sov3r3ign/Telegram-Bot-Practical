# Telegram Bot Practical
# Si-Bone Chatbot with SpaCy Integration

## 📌 Problem Statement
Many chatbots are either too simple (keyword-based) or too complex (pure NLP without clear flow).  
This project addresses the need for a **hybrid chatbot** that combines:
- **Simple quick replies** for casual conversation.
- **Stateful conversation** using SpaCy NLP for guided interactions.

It is designed as a Telegram bot that:
- Responds to simple phrases like "hello" or "how are you".
- Can enter a conversation mode (via `/startconv`) where it analyzes the text for nouns (and can be extended to more NLP features).
- Supports `/help` and `/cancel` for usability.

---

## 🚀 How to Run & Verify
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd chatbot-project
   
## Create a virtual environment:
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

## Install dependencies:
pip install -r requirements.txt
python -m spacy download en_core_web_sm

## Insert your Telegram Bot Token in telegrambot.py:
TOKEN: Final = "YOUR_SECRET_API_TOKEN"

## Run the bot and open telegram 
