from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração do Banco de Dados SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./tarefas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy (Tabela no Banco de Dados)
class TarefaModel(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)
    descricao = Column(String, nullable=True)
    concluida = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

# Esquemas Pydantic (Validação de Dados)
class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=1)
    descricao: str | None = None
    concluida: bool = False

class TarefaUpdate(BaseModel):
    titulo: str | None = Field(None, min_length=1)
    descricao: str | None = None
    concluida: bool | None = None

class TarefaResponse(TarefaCreate):
    id: int

    class Config:
        from_attributes = True

# Inicialização da API FastAPI
app = FastAPI(title="API de Tarefas", version="1.0")

# Rotas da API
@app.get("/tarefas", response_model=list[TarefaResponse])
def listar_tarefas():
    db = SessionLocal()
    try:
        tarefas = db.query(TarefaModel).all()
        return tarefas
    finally:
        db.close()

@app.get("/tarefas/{id}", response_model=TarefaResponse)
def obter_tarefa(id: int):
    db = SessionLocal()
    try:
        tarefa = db.query(TarefaModel).filter(TarefaModel.id == id).first()
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return tarefa
    finally:
        db.close()

@app.post("/tarefas", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: TarefaCreate):
    db = SessionLocal()
    try:
        nova_tarefa = TarefaModel(
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            concluida=tarefa.concluida
        )
        db.add(nova_tarefa)
        db.commit()
        db.refresh(nova_tarefa)
        return nova_tarefa
    finally:
        db.close()

@app.put("/tarefas/{id}", response_model=TarefaResponse)
def atualizar_tarefa(id: int, tarefa_data: TarefaUpdate):
    db = SessionLocal()
    try:
        tarefa = db.query(TarefaModel).filter(TarefaModel.id == id).first()
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        
        dados_atualizados = tarefa_data.dict(exclude_unset=True)
        for chave, valor in dados_atualizados.items():
            setattr(tarefa, chave, valor)
            
        db.commit()
        db.refresh(tarefa)
        return tarefa
    finally:
        db.close()

@app.delete("/tarefas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(id: int):
    db = SessionLocal()
    try:
        tarefa = db.query(TarefaModel).filter(TarefaModel.id == id).first()
        if not tarefa:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        
        db.delete(tarefa)
        db.commit()
        return None
    finally:
        db.close()