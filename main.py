from typing import Annotated

from fastapi import FastAPI, Depends

from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel, Field, create_engine, Session
from datetime import date, datetime
from validate_docbr import CPF

app = FastAPI()

# Setup do banco de dados SQLite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Definição de modelos 
class UserBase(SQLModel):
    name: str = Field(min_length=3, max_length=255)
    email: EmailStr
    cpf: str
    birthdate: str
    
    # Validações 
    @field_validator("cpf")
    def cpf_must_be_valid(cls, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise ValueError("CPF inválido")
        return value
    
    @field_validator("birthdate")
    def birthdate_must_be_valid(cls, value):
        if isinstance(value, str):  # Caso a data venha como string
            try:
                value = datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Data de nascimento inválida. Use o formato YYYY-MM-DD.")

        if value > date.today():
            raise ValueError("A data de nascimento não pode estar no futuro.")
        return value
        
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

# Rotas de API
@app.post("/api/user", status_code=201)
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)    
    return user
