from fastapi import FastAPI, HTTPException, status, Depends, Query, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List, Optional

import models
from database import get_db
import security

app = FastAPI(title="Blog Cá Nhân API - Day 6 (Auth & JWT)")

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

class PostResponse(PostBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================================
# 2. AUTH (REGISTER / LOGIN)
# ==========================================

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(models.User).where(models.User.username == user.username)
    result = await db.execute(query)

    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Username đã tồn tại")

    hashed_password = security.get_password_hash(user.password)

    new_user = models.User(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    await db.commit()

    return {"message": "Đăng ký thành công!"}


@app.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    query = select(models.User).where(models.User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai tài khoản hoặc mật khẩu",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(
        data={"sub": user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ==========================================
# 3. CRUD POSTS (ĐÃ KHÓA JWT)
# ==========================================

# CREATE (ĐÃ KHÓA)
@app.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostBase,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(security.get_current_user)  # 🔒 khóa
):
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


# READ (KHÔNG KHÓA - public)
@app.get("/posts", response_model=List[PostResponse])
async def get_posts(
    limit: int = Query(10, ge=1),
    skip: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Post).offset(skip).limit(limit)
    result = await db.execute(query)

    return result.scalars().all()


@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(query)

    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")

    return post


# UPDATE (ĐÃ KHÓA)
@app.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(security.get_current_user)  # 🔒 khóa
):
    query = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(query)

    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")

    update_data = post_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(post, key, value)

    await db.commit()
    await db.refresh(post)

    return post


# DELETE (ĐÃ KHÓA)
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(security.get_current_user)  # 🔒 khóa
):
    query = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(query)

    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")

    await db.delete(post)
    await db.commit()

    return