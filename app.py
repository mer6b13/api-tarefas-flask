from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados SQLite local
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo da Tarefa (Banco de Dados)
class TarefaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    concluida = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "concluida": self.concluida
        }

# Cria o banco de dados antes da primeira requisição
with app.app_context():
    db.create_all()

# 1. GET /tarefas - Listar todas as tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    tarefas = TarefaModel.query.all()
    return jsonify([t.to_dict() for t in tarefas]), 200

# 2. GET /tarefas/{id} - Buscar uma tarefa específica
@app.route('/tarefas/<int:id>', methods=['GET'])
def buscar_tarefa(id):
    tarefa = TarefaModel.query.get(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify(tarefa.to_dict()), 200

# 3. POST /tarefas - Criar uma nova tarefa (com validação extra)
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.get_json()

    # Validação (Desafio Extra)
    if not dados or 'titulo' not in dados or not str(dados['titulo']).strip():
        return jsonify({"erro": "O campo 'titulo' é obrigatório e não pode estar vazio."}), 400

    nova_tarefa = TarefaModel(
        titulo=dados['titulo'],
        concluida=dados.get('concluida', False)
    )
    
    db.session.add(nova_tarefa)
    db.session.commit()

    return jsonify(nova_tarefa.to_dict()), 201

# 4. PUT /tarefas/{id} - Atualizar uma tarefa existente (com validação extra)
@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = TarefaModel.query.get(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos ou ausentes."}), 400

    # Validação opcional para atualização, caso envie o título
    if 'titulo' in dados:
        if not str(dados['titulo']).strip():
            return jsonify({"erro": "O campo 'titulo' não pode estar vazio."}), 400
        tarefa.titulo = dados['titulo']

    if 'concluida' in dados:
        if not isinstance(dados['concluida'], bool):
            return jsonify({"erro": "O campo 'concluida' deve ser booleano (true/false)."}), 400
        tarefa.concluida = dados['concluida']

    db.session.commit()
    return jsonify(tarefa.to_dict()), 200

# 5. DELETE /tarefas/{id} - Remover uma tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    tarefa = TarefaModel.query.get(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    db.session.delete(tarefa)
    db.session.commit()
    
    return jsonify({"mensagem": "Tarefa deletada com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True)