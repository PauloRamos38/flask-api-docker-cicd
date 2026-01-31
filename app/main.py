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
          
