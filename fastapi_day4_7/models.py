from sqlalchemy import Column, Integer, String, Boolean
from database import Base
from sqlalchemy import Column, Integer, String, Boolean
class Post(Base):
    __tablename__ = "posts" # Tên bảng trong MySQL

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(2000), nullable=False)
    published = Column(Boolean, server_default='1', nullable=False)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False) # Sẽ lưu mật khẩu đã băm
    role = Column(String(20), server_default="user") # Phân quyền (admin hoặc user)