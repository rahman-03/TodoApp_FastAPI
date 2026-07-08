from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "FocusSprint API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/healthy",
    }

def test_health_check():
    response = client.get('/healthy')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'msg' : 'healthy'}

