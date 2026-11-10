def adicionar_tarefa(tarefas):
    descricao = input("Digite a descrição da tarefa: ").strip()
    if not descricao:
        print("A descrição não pode estar vazia.")
        return
    
    novo_id = len(tarefas) + 1
    
    tarefa = {
        "id": novo_id,
        "descricao": descricao,
        "status": "Pendente"
    }
    tarefas.append(tarefa)
    print(f"Tarefa '{descricao}' adicionada com sucesso (ID: {novo_id})!")

def listar_tarefas(tarefas):
    if not tarefas:
        print("\nNenhuma tarefa cadastrada.")
        return
    
    print("\n--- LISTA DE TAREFAS ---")
    for t in tarefas:
        print(f"ID: {t['id']} | Descrição: {t['descricao']} | Status: {t['status']}")
    print("-" * 25)

def concluir_tarefa(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    
    try:
        id_tarefa = int(input("Digite o ID da tarefa que deseja concluir: "))
    except ValueError:
        print("Erro: digite um número inteiro válido.")
        return
    
    encontrada = False
    for t in tarefas:
        if t["id"] == id_tarefa:
            t["status"] = "Concluída"
            print(f"Tarefa {id_tarefa} marcada como concluída!")
            encontrada = True
            break
            
    if not encontrada:
        print("Tarefa não encontrada com esse ID.")

def remover_tarefa(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    
    try:
        id_tarefa = int(input("Digite o ID da tarefa que deseja remover: "))
    except ValueError:
        print("Erro: digite um número inteiro válido.")
        return
    
    encontrada = False
    for i, t in enumerate(tarefas):
        if t["id"] == id_tarefa:
            tarefas.pop(i)
            print(f"Tarefa {id_tarefa} removida com sucesso!")
            encontrada = True
            break
            
    if not encontrada:
        print("Tarefa não encontrada com esse ID.")

def editar_tarefa(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    
    try:
        id_tarefa = int(input("Digite o ID da tarefa que deseja editar: "))
    except ValueError:
        print("Erro: digite um número inteiro válido.")
        return
    
    encontrada = False
    for t in tarefas:
        if t["id"] == id_tarefa:
            nova_desc = input(f"Nova descrição (atual: {t['descricao']}): ").strip()
            if nova_desc:
                t["descricao"] = nova_desc
                print("Descrição atualizada com sucesso!")
            else:
                print("A descrição não pode ficar vazia.")
            encontrada = True
            break
            
    if not encontrada:
        print("Tarefa não encontrada com esse ID.")

def main():
    tarefas = []
    
    while True:
        print("\n=== GERENCIADOR DE TAREFAS ===")
        print("1 - Adicionar tarefa")
        print("2 - Listar tarefas")
        print("3 - Concluir tarefa")
        print("4 - Remover tarefa")
        print("5 - Editar descrição da tarefa (Desafio extra)")
        print("6 - Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            adicionar_tarefa(tarefas)
        elif opcao == "2":
            listar_tarefas(tarefas)
        elif opcao == "3":
            concluir_tarefa(tarefas)
        elif opcao == "4":
            remover_tarefa(tarefas)
        elif opcao == "5":
            editar_tarefa(tarefas)
        elif opcao == "6":
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida! Escolha um número válido do menu.")

if __name__ == "__main__":
    main()