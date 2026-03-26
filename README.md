# ⚔️ Battle of Bots — Qwen3 32B vs LLaMA 3.3 70B

A real-time AI model comparison web app built with Flask.  
Ask a question, get answers from two models simultaneously, and compare their speed, token usage, and response quality — side by side.

---

## 📸 Snapshots

<table>
  <tr>
    <td align="center" width="50%">
      <img src="snapshots/snapshot1.png" width="100%" alt="Hero and Chat Interface"/>
      <br/><b>1. Hero & Chat Interface</b>
    </td>
    <td align="center" width="50%">
      <img src="snapshots/snapshot2.png" width="100%" alt="Efficiency Summary Table"/>
      <br/><b>2. Efficiency Summary Table</b>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="snapshots/snapshot3.png" width="100%" alt="Performance Graph"/>
      <br/><b>3. Performance Graph</b>
    </td>
    <td align="center" width="50%">
      <img src="snapshots/snapshot4.png" width="100%" alt="Responses for Manual Review"/>
      <br/><b>4. Responses for Manual Review</b>
    </td>
  </tr>
</table>

---

## 🚀 Features

- Side-by-side responses from **Qwen3 32B** and **LLaMA 3.3 70B**
- Real-time **response time** comparison
- **Token usage** tracking (input & output)
- **Performance graph** generated per query
- **Readability & keyword density** analysis
- Clean, responsive UI with warm cream theme

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, Flask                     |
| AI Models  | Qwen3 32B, LLaMA 3.3 70B via Groq |
| Graphs     | Matplotlib, Pandas                |
| Analysis   | Textstat                          |
| Frontend   | HTML, Tailwind CSS, Vanilla JS    |

---

## ⚙️ Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ai-model-comparison.git
cd ai-model-comparison
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free key at [console.groq.com](https://console.groq.com)

**4. Run the app**
```bash
python app.py
```

**5. Open in browser**
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
ai-model-comparison/
├── app.py                  # Flask backend, model handlers, graph generation
├── requirements.txt        # Python dependencies
├── .env                    # API key (not pushed to GitHub)
├── .gitignore
└── templates/
    └── index.html          # Frontend UI
```

---

## 🔑 Models Used

| Model | Provider | Type |
|---|---|---|
| `qwen/qwen3-32b` | Alibaba via Groq | Reasoning model |
| `llama-3.3-70b-versatile` | Meta via Groq | General purpose |

Both models are **free tier** on Groq — no billing required.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).