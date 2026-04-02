import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Tải các biến môi trường từ file .env
load_dotenv()

# Lấy thông tin bảo mật từ .env
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Tên database mình dùng cho bài học hôm nay
DB_NAME = "fastapi_blog"

# Tạo chuỗi kết nối (URL)
SQLALCHEMY_DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Khởi tạo Async Engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Khởi tạo Session
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Dependency để sử dụng trong FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session