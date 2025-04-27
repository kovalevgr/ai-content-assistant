
# AI Content Assistant 🤖✍️

An AI-powered Telegram bot for aggregating, summarizing, rewriting, and assisting in posting news articles in a personalized style.

---

## 🚀 Solution Overview

**Goal:**  
Create an AI Content Assistant that automates news aggregation from trusted sources (via RSS), allows custom topic searches, summarizes the content, rewrites it in a custom style, and assists in publishing.

**Key Features:**
- Aggregate latest news articles via predefined RSS feeds.
- Allow users to specify custom topics for article search.
- Summarize and rewrite articles using OpenAI API.
- Store user search topics for reuse.
- Fully test-covered codebase.
- Modular agent-based architecture for easy extension.

---

## 🧠 System Architecture

```plaintext
[Telegram Bot]
    |
    |--- /top_news → [RSS Aggregator Agent]
    |        |
    |     [Fetch latest news from RSS sources]
    |
    |--- /custom_topic → [Topic Search Agent] (coming soon)
    |        |
    |     [Find articles related to user input]
    |
    ↓
[Summarizer Agent] → [Style Rewriter Agent] → [Return result to user]
```

> Agents are isolated modules that perform a specific task (parsing, summarizing, rewriting, etc.)

---

## 🛠️ Project Structure

```
/app
  /bots             # Telegram bot logic
  /agents           # Business logic agents (RSS aggregator, summarizer, etc.)
  /services         # External service wrappers (e.g., OpenAI API)
  /models           # Data models (topics, sources)
config.py
/tests
  /bots             # Bot tests
  /agents           # Agents tests
  /services         # Services tests
main.py             # Entry point
requirements.txt    # Production dependencies
requirements-dev.txt # Development dependencies
.env                # Environment variables (not versioned)
.gitignore
README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-content-assistant.git
cd ai-content-assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
.env\Scriptsctivate   # Windows
```

### 3. Install dependencies

- For production:

```bash
pip install -r requirements.txt
```

- For development:

```bash
pip install -r requirements-dev.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the root folder:

```dotenv
TELEGRAM_TOKEN=your-telegram-bot-token
OPENAI_API_KEY=your-openai-api-key
```

---

## 🚀 Running the Project

### Development Mode (local testing)

```bash
python main.py
```

It will start the Telegram bot locally and respond to commands.

### Production Mode (for server / deployment)

- Setup your environment (virtual machine, App Service, etc.)
- Install only production dependencies:

```bash
pip install -r requirements.txt
```
- Ensure environment variables are set (or .env file present)
- Run:

```bash
python main.py
```

*(In production, you can also use process managers like `pm2`, `supervisord`, or dockerize it.)*

---

## 🧪 Running Tests

```bash
pytest
```

Tests cover core functionality (bots and agents) and are isolated with mocks.

---

## 📚 Future Improvements

- Implement CrewAI/Agent-based dynamic action planning.
- Auto-posting to social networks.
- Admin panel to manage RSS sources and user topics.
- Deployment via Docker / Azure App Service.

---

## 👨‍💻 Author

Crafted with ❤️ by [your name or GitHub link].

---
