from fastapi import Fastapi,HttpExeception  
from pydantic import BaseModel, Field
from typing import Annotated
import models
from database import engine,SesionLocal
from sqlalchemy.orm import Session

app=Fastapi()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session, Depends(get_db)]