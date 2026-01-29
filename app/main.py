"""
Flask API Package
"""
__version__ = "1.0.0"
"""
Flask API simples para demonstração de DevOps
"""
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Endpoint principal"""
    return jsonify({
        'message': 'Bem-vindo à API Flask!',
        'status': 'online',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'flask-api',
        'version': '1.0.0'
    }), 200

@app.route('/api/users')
def get_users():
    """Endpoint de exemplo - lista de usuários"""
    users = [
        {'id': 1, 'name': 'Paulo Ramos', 'role': 'DevOps Engineer'},
        {'id': 2, 'name': 'Maria Silva', 'role': 'Developer'},
        {'id': 3, 'name': 'João Santos', 'role': 'SRE'}
    ]
    return jsonify({
        'users': users,
        'total': len(users)
    })

@app.route('/api/info')
def get_info():
    """Informações sobre o projeto"""
    return jsonify({
        'project': 'Flask API with Docker & CI/CD',
        'author': 'Paulo Ramos',
        'github': 'https://github.com/PauloRamos38',
        'technologies': ['Flask', 'Docker', 'GitHub Actions', 'pytest'],
        'description': 'API REST demonstrando práticas DevOps'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
  Flask==3.0.0
Werkzeug==3.0.1
"""
Test Package
"""
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
  Flask==3.0.0
Werkzeug==3.0.1
pytest==7.4.3
pytest-cov==4.1.0
# Multi-stage build para otimização

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Instala dependências
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copia dependências do builder
COPY --from=builder /root/.local /root/.local

# Copia código da aplicação
COPY app/ .

# Adiciona .local/bin ao PATH
ENV PATH=/root/.local/bin:$PATH

# Expõe a porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Comando para iniciar a aplicação
CMD ["python", "main.py"]
version: '3.8'

services:
  api:
    build: .
    container_name: flask-api
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
        
    - name: Run tests with coverage
      run: |
        pytest tests/ -v --cov=app --cov-report=term-missing
        
    - name: Generate coverage report
      run: |
        pytest tests/ --cov=app --cov-report=xml
        
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
      
    - name: Build Docker image
      run: |
        docker build -t flask-api:latest .
        
    - name: Test Docker image
      run: |
        docker run -d -p 5000:5000 --name test-api flask-api:latest
        sleep 10
        curl -f http://localhost:5000/health || exit 1
        docker stop test-api
        docker rm test-api
        
  lint:
    name: Code Quality Check
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install flake8
      run: |
        pip install flake8
        
    - name: Run linting
      run: |
        flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
*.log
  # 🚀 Flask API with Docker & CI/CD

[![CI/CD Pipeline](https://github.com/PauloRamos38/flask-api-docker-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/PauloRamos38/flask-api-docker-cicd/actions/workflows/ci.yml)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

API REST simples em Flask demonstrando práticas modernas de DevOps: containerização com Docker, testes automatizados e CI/CD com GitHub Actions.

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
- [Endpoints](#endpoints)
- [Testes](#testes)
- [CI/CD Pipeline](#cicd-pipeline)
- [Docker](#docker)
- [Autor](#autor)

---

## 📖 Sobre o Projeto

Este projeto é uma API REST desenvolvida com Flask que demonstra:

- ✅ Desenvolvimento de API REST com Python/Flask
- ✅ Containerização com Docker (multi-stage build)
- ✅ Testes automatizados com pytest
- ✅ CI/CD com GitHub Actions
- ✅ Health checks e monitoramento básico
- ✅ Boas práticas de código e documentação

**Ideal para portfólio DevOps!**

---

## 🛠️ Tecnologias

- **Python 3.11** - Linguagem de programação
- **Flask 3.0** - Framework web
- **Docker** - Containerização
- **GitHub Actions** - CI/CD
- **pytest** - Framework de testes
- **Docker Compose** - Orquestração de containers

---

## 📦 Pré-requisitos

Antes de começar, você precisa ter instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

---

## 🚀 Instalação

### Opção 1: Executar Localmente (sem Docker)
```bash
# Clone o repositório
git clone https://github.com/PauloRamos38/flask-api-docker-cicd.git
cd flask-api-docker-cicd

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r app/requirements.txt

# Execute a aplicação
python app/main.py
```

A API estará disponível em: `http://localhost:5000`

---

### Opção 2: Executar com Docker
```bash
# Clone o repositório
git clone https://github.com/PauloRamos38/flask-api-docker-cicd.git
cd flask-api-docker-cicd

# Build da imagem Docker
docker build -t flask-api:latest .

# Execute o container
docker run -d -p 5000:5000 --name flask-api flask-api:latest
```

---

### Opção 3: Executar com Docker Compose
```bash
# Clone o repositório
git clone https://github.com/PauloRamos38/flask-api-docker-cicd.git
cd flask-api-docker-cicd

# Inicie os serviços
docker-compose up -d

# Visualize os logs
docker-compose logs -f

# Pare os serviços
docker-compose down
```

---

## 📡 Uso

### Endpoints Disponíveis

#### 1. **Home** - `GET /`
Endpoint principal da API.

**Exemplo:**
```bash
curl http://localhost:5000/
```

**Resposta:**
```json
{
  "message": "Bem-vindo à API Flask!",
  "status": "online",
  "timestamp": "2026-01-29T10:30:00"
}
```

---

#### 2. **Health Check** - `GET /health`
Verifica o status da aplicação.

**Exemplo:**
```bash
curl http://localhost:5000/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "service": "flask-api",
  "version": "1.0.0"
}
```

---

#### 3. **Usuários** - `GET /api/users`
Retorna lista de usuários de exemplo.

**Exemplo:**
```bash
curl http://localhost:5000/api/users
```

**Resposta:**
```json
{
  "users": [
    {"id": 1, "name": "Paulo Ramos", "role": "DevOps Engineer"},
    {"id": 2, "name": "Maria Silva", "role": "Developer"},
    {"id": 3, "name": "João Santos", "role": "SRE"}
  ],
  "total": 3
}
```

---

#### 4. **Informações** - `GET /api/info`
Informações sobre o projeto.

**Exemplo:**
```bash
curl http://localhost:5000/api/info
```

---

## 🧪 Testes

### Executar testes localmente
```bash
# Instale as dependências de desenvolvimento
pip install -r requirements-dev.txt

# Execute os testes
pytest tests/ -v

# Execute com coverage
pytest tests/ --cov=app --cov-report=term-missing

# Gere relatório HTML de coverage
pytest tests/ --cov=app --cov-report=html
```

### Estrutura dos Testes
```
tests/
├── __init__.py
└── test_main.py    # Testes dos endpoints
```

**Cobertura de testes:**
- ✅ Teste do endpoint home
- ✅ Teste do health check
- ✅ Teste do endpoint de usuários
- ✅ Teste do endpoint de informações
- ✅ Teste de endpoint inexistente (404)

---

## 🔄 CI/CD Pipeline

O projeto utiliza **GitHub Actions** para automação de CI/CD.

### Pipeline Stages:

1. **Test** - Executa testes automatizados
2. **Build** - Constrói imagem Docker
3. **Lint** - Verifica qualidade do código

### Como funciona:

- ✅ **Push/PR para `main` ou `develop`** → Pipeline é acionado
- ✅ **Testes são executados** → Verifica se o código está funcionando
- ✅ **Build do Docker** → Cria a imagem
- ✅ **Testa a imagem** → Roda container e verifica health
- ✅ **Linting** → Verifica qualidade do código

**Badge de status:** [![CI/CD](https://github.com/PauloRamos38/flask-api-docker-cicd/actions/workflows/ci.yml/badge.svg)](https://github.com/PauloRamos38/flask-api-docker-cicd/actions)

---

## 🐳 Docker

### Dockerfile Features

- ✅ **Multi-stage build** para otimização de tamanho
- ✅ **Python 3.11-slim** como base
- ✅ **Health check** integrado
- ✅ **Non-root user** (segurança)
- ✅ **Cache de dependências** otimizado

### Comandos Docker Úteis
```bash
# Build
docker build -t flask-api:latest .

# Run
docker run -d -p 5000:5000 --name flask-api flask-api:latest

# Logs
docker logs -f flask-api

# Stop
docker stop flask-api

# Remove
docker rm flask-api

# Check health
docker inspect --format='{{.State.Health.Status}}' flask-api
```

---

## 📈 Roadmap

- [ ] Adicionar autenticação JWT
- [ ] Implementar rate limiting
- [ ] Adicionar banco de dados (PostgreSQL)
- [ ] Deploy automático para cloud (AWS/Azure/GCP)
- [ ] Monitoramento com Prometheus/Grafana
- [ ] Adicionar Kubernetes manifests

---

## 👨‍💻 Autor

**Paulo Ramos**

- GitHub: [@PauloRamos38](https://github.com/PauloRamos38)
- LinkedIn: [Paulo Ramos de Oliveira](https://www.linkedin.com/in/paulo-ramos-de-liveira)
- Instagram: [@pauloramos136](https://instagram.com/pauloramos136)

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## ⭐ Deixe uma estrela!

Se este projeto foi útil para você, considere deixar uma ⭐!

---

<div align="center">

**Feito com ❤️ e ☕ por Paulo Ramos**

[![GitHub](https://img.shields.io/badge/GitHub-PauloRamos38-181717?style=for-the-badge&logo=github)](https://github.com/PauloRamos38)

</div>
          
