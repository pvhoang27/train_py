from fastapi import FastAPI, HTTPException, status, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional

import models
from database import get_db

# Khởi tạo ứng dụng FastAPI
app = FastAPI(title="Blog Cá Nhân API - Day 5 (Real Database)")

# ==========================================
# 1. PYDANTIC SCHEMAS
# ==========================================
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

# Schema dùng để trả data về (có thêm id từ Database)
class PostResponse(PostBase):
    id: int

    class Config:
        from_attributes = True # Giúp Pydantic đọc được data từ object của SQLAlchemy

# ==========================================
# 2. CRUD API ENDPOINTS VỚI MYSQL (ASYNC)
# ==========================================

# [CREATE]
@app.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: AsyncSession = Depends(get_db)):
    # Chuyển pydantic model thành object SQLAlchemy
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    await db.commit() # Lưu vào DB
    await db.refresh(new_post) # Lấy lại data (bao gồm cả id tự tăng) từ DB
    return new_post

# [READ ALL]
@app.get("/posts", response_model=List[PostResponse])
async def get_posts(limit: int = 10, skip: int = 0, db: AsyncSession = Depends(get_db)):
    # Lệnh query: SELECT * FROM posts LIMIT {limit} OFFSET {skip}
    query = select(models.Post).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# [READ ONE]
@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    query = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(query)
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    return post

# [UPDATE]
@app.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, post_update: PostUpdate, db: AsyncSession = Depends(get_db)):
    # Tìm bài viết
    query = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(query)
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    
    # Cập nhật các trường có gửi lên
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value) # Cập nhật object
        
    await db.commit()
    await db.refresh(post)
    return post

# [DELETE]
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int = Path(..., gt=0), db: AsyncSession = Depends(get_db)):
    query = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(query)
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    
    await db.delete(post)
    await db.commit()
    return