# 📊 WhatsApp Chat Analyzer

A powerful, interactive WhatsApp Chat Analyzer built using **Python**, **Pandas**, and **Streamlit**.  
This project helps you uncover chat patterns, user activity, emoji usage, most common words, and much more — all from your exported WhatsApp chats.

---

## 🚀 Features

### 🔍 **Message Insights**
- Total messages  
- Total words  
- Media shared  
- Links shared  

### 📅 **Timeline Analysis**
- Monthly message timeline  
- Daily activity timeline  

### 📆 **Activity Patterns**
- Most active day  
- Most active month  
- Weekly activity heatmap  

### 🧑‍🤝‍🧑 **Top Contributors**
- Most active participants  
- Message percentage share  

### ☁️ **Text Analysis**
- WordCloud generation  
- Most common words  
- Stop-word filtering (Hinglish supported)  

### 😀 **Emoji Analysis**
- Total emoji usage  
- Most frequently used emojis  
- Emoji pie chart  

### 🗂️ **Supports both:**
- **24-hour timestamps**  
- **12-hour AM/PM timestamps**  
- **.txt chat files**  
- **.zip exported chats**  

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Frontend UI | Streamlit |
| Data Processing | Pandas |
| Visualization | Matplotlib, Seaborn |
| Text Handling | WordCloud, Regex |
| Emoji Analysis | emoji.py |
| URL Extraction | urlextract |

---

## 📦 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/ganesh333-wq/whatsapp-chat-analysis-main.git
cd whatsapp-chat-analysis-main

#2️⃣ Create a virtual environment
python -m venv .venv

#3️⃣ Activate environment
.venv\Scripts\activate

# 4️⃣ Install dependencies
pip install -r requirements.txt

# ▶️ Run the Application
streamlit run app.py

### whatsapp-chat-analysis/
│── app.py                 # Main Streamlit UI
│── helper.py              # All analysis functions
│── preprocessor.py        # Chat parsing & cleaning
│── stop_hinglish.txt      # Stop words for text cleaning
│── requirements.txt       # Python dependencies
│── README.md              # Documentation
│── Procfile               # Deployment file (Heroku)
│── setup.sh               # Deployment setup script






 
