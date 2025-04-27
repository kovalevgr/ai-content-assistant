from app.models.db_models import UserArticleHistory
from app.db.database import get_session

def save_article_history(user_id: int, topic: str, style: str, result: str):
    db = get_session()
    history = UserArticleHistory(
        user_id=user_id,
        topic=topic,
        style=style,
        result=result
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    db.close()
    return history

def get_user_history(user_id: int, limit: int = 5):
    """Fetch recent article history for a specific user."""
    db = get_session()
    history = (
        db.query(UserArticleHistory)
        .filter(UserArticleHistory.user_id == user_id)
        .order_by(UserArticleHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    db.close()
    return history