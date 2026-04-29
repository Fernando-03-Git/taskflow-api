from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Convierte el password en texto plano a hash seguro"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si el password ingresado coincide con el hash guardado"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Crea y firma un JWT con los datos del usuario"""
    to_encode = data.copy()
    
    # Calculamos cuándo expira
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    
    # Firmamos el token con SECRET_KEY y el algoritmo
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str) -> dict:
    """Decodifica y verifica un JWT — lanza excepción si es inválido"""
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])