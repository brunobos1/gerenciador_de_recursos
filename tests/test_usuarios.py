from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.model_bd import Base, session
from main import app, verify_password
from app.auth.auth_handler import signJWT

DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[session] = override_get_db

client = TestClient(app)

def test_cadastro_usuario():

    response = client.post(
        "/usuarios/cadastrar",
        json={"nome": "Orlando de Machado", "usuario": "orlando75", "senha": "753951"},
    )

    assert response.status_code == 200
    data = response.json()
    data = data['data']
    assert data["usuario"] == "orlando75"
    assert verify_password('753951', data['senha'])
    assert "id" in data
    usuario = data["usuario"]
    user_id = data["id"]

    token = (signJWT('brunobos1'))['access_token']

    response = client.delete(f"/usuarios/deletar?usuario={usuario}",
                        headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'})
    assert response.status_code == 200