# 📊 WhatsApp Chat Analyzer

A powerful and elegant Streamlit web application that analyzes WhatsApp chat exports to reveal user behavior, activity patterns, emoji usage, word frequency, and more — all in an interactive dashboard.

---

## 🚀 Features

- 📈 **Top Statistics**: Total messages, words, media, and links shared.
- 🗓 **Monthly & Daily Timeline**: Visualize messaging trends over time.
- 🗂 **Activity Maps**:
  - Day-wise and hour-wise activity heatmaps
  - Weekly and monthly activity bars
- 👥 **Most Active Users**: Identifies the most active members (in group chats).
- ☁️ **WordCloud**: Generates word clouds of frequently used words.
- 🔠 **Most Common Words**: Bar chart with stylish visuals.
- 😂 **Emoji Analysis**: Breakdown of emoji usage with charts and tables.

---

## 📂 Folder Structure

```
.
├── app.py                # Main Streamlit app
├── helper.py             # Functions for data analysis
├── preprocessor.py       # Chat text cleaning and preprocessing
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

---

## 🛠 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run app.py
```

---

## 📤 How to Export WhatsApp Chat

1. Open WhatsApp
2. Open any chat or group
3. Tap on the 3-dot menu > `More` > `Export Chat`
4. Choose **WITHOUT media**
5. Save the `.txt` file and upload it to the app

---

## 📦 Dependencies

- `streamlit`
- `pandas`
- `matplotlib`
- `seaborn`
- `wordcloud`
- `emoji`
- `plotly`

Install all using:

```bash
pip install -r requirements.txt
```

---

## 💻 Demo

Want to see it in action?  
https://whatsapp-chat-analyzer-2-d5m2.onrender.com

---

## 🙋‍♂️ Author

**Sujal Songire**  
Feel free to connect on [LinkedIn](www.linkedin.com/in/sujal-songire) or contribute via PRs!
