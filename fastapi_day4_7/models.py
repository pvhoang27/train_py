from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Post(Base):
    __tablename__ = "posts" # Tên bảng trong MySQL

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(2000), nullable=False)
    published = Column(Boolean, server_default='1', nullable=False)