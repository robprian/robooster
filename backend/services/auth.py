from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..models.models import User

class AuthService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifikasi password"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate hash password"""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Membuat access token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verifikasi token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """Autentikasi user"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user
    
    def register_user(self, db: Session, username: str, email: str, password: str) -> User:
        """Registrasi user baru"""
        hashed_password = self.get_password_hash(password)
        user = User(
            username=username,
            email=email,
            password_hash=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user