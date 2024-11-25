from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from dotenv import load_dotenv
import os
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

# Configuração do FastAPI
app = FastAPI()  

# Definindo um modelo Pydantic para receber as credenciais
class UserLogin(BaseModel):
    username: str
    password: str

# Função para criar hash da senha
def hash_password(password: str):
    return pwd_context.hash(password)

# Função para verificar a senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar o token JWT (agora com expiração de 1 ano)
def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=365)):  # Token válido por 1 ano
    to_encode = data.copy() 
    expire = datetime.utcnow() + expires_delta  
    to_encode.update({"exp": expire})  
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm="HS256")  # Codifica o token
    return encoded_jwt

load_dotenv()

# Configurações do Banco de Dados
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Contexto para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Definir o OAuth2PasswordBearer para pegar o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Modelo de Exemplo
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota de criação de usuário (registrar)
@app.post("/users/")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Rota de login (autenticação)
@app.post("/token/")
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    user_in_db = db.query(User).filter(User.username == user.username).first()
    if not user_in_db or not verify_password(user.password, user_in_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user_in_db.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Protegendo uma rota com autenticação JWT
@app.get("/protected/")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"message": "Welcome to the protected route!", "user": username}
