from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from app.database import Base

class IALog(Base):
    __tablename__ = "ia_log"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    intent = Column(String)
    payload = Column(JSON)
    result = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
