import asyncio
from database import engine, Base
import models # Phải import models để SQLAlchemy biết cấu trúc bảng

async def force_create_tables():
    print("Đang kết nối Database và ép tạo bảng...")
    async with engine.begin() as conn:
        # Xóa hết bảng cũ (nếu có) và tạo lại bảng mới 100% dựa theo models.py
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tạo bảng THÀNH CÔNG! Hãy kiểm tra lại MySQL Workbench.")

if __name__ == "__main__":
    asyncio.run(force_create_tables())