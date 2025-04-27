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