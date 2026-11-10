import sqlite3
from datetime import datetime

def conectar():
    """Cria e retorna a conexão com o banco de dados SQLite."""
    return sqlite3.connect("sistema_tarefas.db")

def criar_tabelas():
    """Cria as tabelas de usuários e tarefas caso elas não existam."""
    conn = conectar()
    cursor = conn.cursor()
    
    # Habilitar suporte a chaves estrangeiras no SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Tabela de Usuários (Desafio Extra)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)
    
    # Tabela de Tarefas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            concluida BOOLEAN NOT NULL DEFAULT 0,
            data_criacao TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE SET NULL
        )
    """)
    
    conn.commit()
    conn.close()

def adicionar_usuario(nome):
    """Adiciona um novo usuário ao banco de dados."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
    conn.commit()
    usuario_id = cursor.lastrowid
    conn.close()
    print(f"Usuário '{nome}' cadastrado com sucesso (ID: {usuario_id}).")
    return usuario_id

def adicionar_tarefa(titulo, usuario_id=None):
    """Insere uma nova tarefa, vinculando opcionalmente a um usuário."""
    conn = conectar()
    cursor = conn.cursor()
    data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO tarefas (titulo, concluida, data_criacao, usuario_id)
        VALUES (?, 0, ?, ?)
    """, (titulo, data_criacao, usuario_id))
    
    conn.commit()
    conn.close()
    print(f"Tarefa '{titulo}' adicionada com sucesso!")

def listar_tarefas():
    """Lista todas as tarefas cadastradas com seus respectivos usuários."""
    conn = conectar()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT t.id, t.titulo, t.concluida, t.data_criacao, u.nome
        FROM tarefas t
        LEFT JOIN usuarios u ON t.usuario_id = u.id
    """)
    tarefas = cursor.fetchall()
    conn.close()
    
    print("\n--- LISTA DE TAREFAS ---")
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
    for t in tarefas:
        status = "✅ Concluída" if t[2] else "⏳ Pendente"
        usuario = t[4] if t[4] else "Não atribuído"
        print(f"ID: {t[0]} | Título: {t[1]} | Status: {status} | Criada em: {t[3]} | Responsável: {usuario}")
    print("-" * 40)

def atualizar_status(tarefa_id, concluida):
    """Atualiza o status de conclusão de uma tarefa."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET concluida = ? WHERE id = ?", (1 if concluida else 0, tarefa_id))
    conn.commit()
    conn.close()
    print(f"Status da tarefa ID {tarefa_id} atualizado.")

def excluir_tarefa(tarefa_id):
    """Exclui uma tarefa pelo ID."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conn.commit()
    conn.close()
    print(f"Tarefa ID {tarefa_id} excluída com sucesso.")

# Exemplo de fluxo de uso:
if __name__ == "__main__":
    criar_tabelas()
    
    uid = adicionar_usuario("Maria")
    adicionar_tarefa("Estudar Python e SQLite", uid)
    adicionar_tarefa("Praticar modelagem de banco de dados", uid)
    
    listar_tarefas()
    
    atualizar_status(1, True)
    
    listar_tarefas()
