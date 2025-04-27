
# AI Content Assistant

Your personal AI content assistant that helps you:

- Find real articles based on your custom topics (via RSS feeds)
- Summarize multiple articles into one
- Rewrite the content into different styles (Professional, Casual, Emotional, Technical)
- Save your article generation history in a PostgreSQL database
- Operate via a friendly Telegram bot

---

## 🛠 Project Structure

```
/app
  /agents         # AI-related agents (aggregator, summarizer, rewriter)
  /bots           # Telegram bot logic
  /db             # Database connection and CRUD operations
  /models         # Database models (SQLAlchemy)
  /scripts        # Helper scripts (e.g., database initialization)
/docker
  docker-compose.dev.yml   # Docker Compose for development
  docker-compose.prod.yml  # Docker Compose for production
```

---

## 🚀 Features

| Feature | Status |
|:--------|:-------|
| Find articles by topic (RSS feeds) | ✅ |
| Summarize articles with OpenAI | ✅ |
| Rewrite content in various styles | ✅ |
| Save request history (PostgreSQL) | ✅ |
| Dockerized setup (Dev/Prod) | ✅ |
| Unit-tested core flows | ✅ |

---

## ⚙️ How to Run

### Local Development

```bash
docker-compose -f docker-compose.dev.yml up -d
python scripts/init_db.py
python main.py
```

> Ensure you have a `.env` file with necessary environment variables:
>
> - OPENAI_API_KEY
> - OPENAI_MODEL
> - OPENAI_TEMPERATURE
> - OPENAI_MAX_TOKENS
> - POSTGRES_USER
> - POSTGRES_PASSWORD
> - POSTGRES_DB
> - POSTGRES_HOST
> - POSTGRES_PORT

---

### Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Make sure the production environment has all required environment variables set.

---

## ✅ How to Test

```bash
pytest
```

Unit tests mock external services and database interactions to ensure isolated, fast, and reliable tests.

---

## 📄 License

MIT License.
