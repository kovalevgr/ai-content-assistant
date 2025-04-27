from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db.database import Base

class UserArticleHistory(Base):
    __tablename__ = "user_article_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    topic = Column(String(255), nullable=False)
    style = Column(String(50), nullable=False)
    result = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())