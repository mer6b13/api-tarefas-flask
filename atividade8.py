import sqlite3


def conectar():
  """Conecta ao banco de dados SQLite e cria a tabela se não existir."""
  conn = sqlite3.connect("usuarios.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
  conn.commit()
  return conn


def criar_usuario(conn, nome, email):
  """Create: Cadastra um novo usuário com validações."""
  if not nome.strip() or not email.strip():
    print("Erro: Nome e e-mail são obrigatórios e não podem estar vazios.")
    return

  cursor = conn.cursor()
  try:
    cursor.execute(
        "INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email)
    )
    conn.commit()
    print("Usuário cadastrado com sucesso!")
  except sqlite3.IntegrityError:
    print("Erro: Este e-mail já está cadastrado no sistema.")


def listar_usuarios(conn):
  """Read: Lista todos os usuários cadastrados."""
  cursor = conn.cursor()
  cursor.execute("SELECT id, nome, email FROM usuarios")
  usuarios = cursor.fetchall()

  if not usuarios:
    print("Nenhum usuário cadastrado.")
    return

  print("\n--- Lista de Usuários ---")
  for u in usuarios:
    print(f"ID: {u[0]} | Nome: {u[1]} | E-mail: {u[2]}")
  print("-" * 25)


def consultar_usuario(conn, termo):
  """Desafio Extra: Busca usuários por parte do nome ou e-mail."""
  cursor = conn.cursor()
  cursor.execute(
      "SELECT id, nome, email FROM usuarios WHERE nome LIKE ? OR email LIKE ?",
      (f"%{termo}%", f"%{termo}%"),
  )
  usuarios = cursor.fetchall()

  if not usuarios:
    print("Nenhum usuário encontrado com esse termo.")
    return

  print("\n--- Resultados da Busca ---")
  for u in usuarios:
    print(f"ID: {u[0]} | Nome: {u[1]} | E-mail: {u[2]}")
  print("-" * 25)


def atualizar_usuario(conn, id_usuario, novo_nome, novo_email):
  """Update: Altera os dados de um usuário existente."""
  if not novo_nome.strip() or not novo_email.strip():
    print("Erro: Nome e e-mail não podem ser vazios.")
    return

  cursor = conn.cursor()
  try:
    cursor.execute(
        "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?",
        (novo_nome, novo_email, id_usuario),
    )
    conn.commit()
    if cursor.rowcount > 0:
      print("Usuário atualizado com sucesso!")
    else:
      print("Usuário não encontrado.")
  except sqlite3.IntegrityError:
    print("Erro: O e-mail informado já pertence a outro usuário.")


def deletar_usuario(conn, id_usuario):
  """Delete: Exclui um usuário pelo ID."""
  cursor = conn.cursor()
  cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
  conn.commit()
  if cursor.rowcount > 0:
    print("Usuário excluído com sucesso!")
  else:
    print("Usuário não encontrado.")


def main():
  conn = conectar()
  while True:
    print("\n=== Sistema CRUD de Usuários ===")
    print("1. Cadastrar usuário")
    print("2. Listar usuários")
    print("3. Buscar usuário (por Nome ou E-mail)")
    print("4. Atualizar usuário")
    print("5. Excluir usuário")
    print("6. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
      nome = input("Nome: ")
      email = input("E-mail: ")
      criar_usuario(conn, nome, email)
    elif opcao == "2":
      listar_usuarios(conn)
    elif opcao == "3":
      termo = input("Digite o termo de busca (nome ou e-mail): ")
      consultar_usuario(conn, termo)
    elif opcao == "4":
      id_usuario = input("ID do usuário que deseja atualizar: ")
      novo_nome = input("Novo nome: ")
      novo_email = input("Novo e-mail: ")
      atualizar_usuario(conn, id_usuario, novo_nome, novo_email)
    elif opcao == "5":
      id_usuario = input("ID do usuário que deseja excluir: ")
      deletar_usuario(conn, id_usuario)
    elif opcao == "6":
      print("Saindo do sistema...")
      conn.close()
      break
    else:
      print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
  main()