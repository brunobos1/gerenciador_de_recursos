from fastapi.testclient import TestClient
from app.auth.auth_handler import signJWT

from main import app

client = TestClient(app)

def test_get_root():
    response = client.get("/")
    body = response.json()
    assert response.status_code == 200
    assert body["mensagem"] == "Olá, para usar a API no navegador adicione /docs na url."

def teste_post_login():
    response = client.post(
        '/token',
        headers={'Content-Type': 'application/json'},
        json={'usuario': 'brunobos1', 'senha': '673460'},
        )
    assert response.status_code == 200