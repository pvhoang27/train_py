from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

# Cấu hình băm mật khẩu bằng thuật toán bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Khóa bí mật dùng để ký JWT (Thực tế cái này nên giấu vào file .env)
SECRET_KEY = "hoang_super_secret_key_day_6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token có hạn 30 phút

def get_password_hash(password: str) -> str:
    """Hàm băm mật khẩu trước khi lưu vào DB"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Hàm kiểm tra mật khẩu người dùng nhập có khớp với mật khẩu đã băm trong DB không"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Hàm tạo JWT Token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Mã hóa chuỗi token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Hàm này sẽ tự động bắt Token từ Header và giải mã để kiểm tra"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Không thể xác thực danh tính (Token không hợp lệ hoặc đã hết hạn)",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Giải mã token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # Lấy username từ trong token ra
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception