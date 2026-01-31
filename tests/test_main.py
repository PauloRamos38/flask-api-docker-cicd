"""
Testes para a API Flask
"""
import pytest
from app.main import app

@pytest.fixture
def client():
    """Fixture do cliente de teste"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Testa o endpoint principal"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'online'
    assert 'message' in data
    assert 'timestamp' in data

def test_health_endpoint(client):
    """Testa o health check"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'flask-api'
    assert data['version'] == '1.0.0'

def test_users_endpoint(client):
    """Testa o endpoint de usuários"""
    response = client.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    assert 'users' in data
    assert 'total' in data
    assert data['total'] == 3
    assert len(data['users']) == 3

def test_info_endpoint(client):
    """Testa o endpoint de informações"""
    response = client.get('/api/info')
    assert response.status_code == 200
    data = response.get_json()
    assert data['project'] == 'Flask API with Docker & CI/CD'
    assert data['author'] == 'Paulo Ramos'
    assert 'technologies' in data
    assert 'Flask' in data['technologies']
    assert 'Docker' in data['technologies']

def test_invalid_endpoint(client):
    """Testa endpoint inexistente"""
    response = client.get('/api/naoexiste')
    assert response.status_code == 404
