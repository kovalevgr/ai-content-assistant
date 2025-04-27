from app.db.database import Base, engine
from app.models.db_models import UserArticleHistory

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized!")

if __name__ == "__main__":
    init_db()