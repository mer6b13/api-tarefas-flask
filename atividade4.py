notas = []

while True:
    try:
        entrada = input("Digite uma nota (-1 para encerrar): ")
        nota = float(entrada)

        if nota == -1:
            break

        if nota < 0 or nota > 10:
            print("Nota inválida! Digite uma nota entre 0 e 10.")
        else:
            notas.append(nota)
    except ValueError:
        print("Entrada inválida! Por favor, digite um número válido.")

# Opção para editar ou remover notas
if len(notas) > 0:
    while True:
        print("\nNotas cadastradas:")
        for indice, nota in enumerate(notas):
            print(f"[{indice}] -> {nota}")

        print("1 - Editar nota")
        print("2 - Remover nota")
        print("3 - Finalizar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            try:
                posicao = int(input("Digite a posição da nota que deseja editar: "))

                if 0 <= posicao < len(notas):
                    nova_nota = float(input("Digite a nova nota: "))

                    if 0 <= nova_nota <= 10:
                        notas[posicao] = nova_nota
                        print("Nota editada com sucesso!")
                    else:
                        print("Nota inválida! Deve ser entre 0 e 10.")
                else:
                    print("Posição inválida!")
            except ValueError:
                print("Entrada inválida! Digite valores numéricos.")

        elif opcao == "2":
            try:
                posicao = int(input("Digite a posição da nota que deseja remover: "))

                if 0 <= posicao < len(notas):
                    notas.pop(posicao)
                    print("Nota removida com sucesso!")
                else:
                    print("Posição inválida!")
            except ValueError:
                print("Entrada inválida! Digite um número inteiro para a posição.")

        elif opcao == "3":
            break

        else:
            print("Opção inválida!")

# Resultado final
if len(notas) > 0:
    quantidade = len(notas)
    media = sum(notas) / quantidade
    maior = max(notas)
    menor = min(notas)

    print("\n----- RESULTADO FINAL -----")
    print("Quantidade de notas:", quantidade)
    print(f"Média: {media:.2f}")
    print("Maior nota:", maior)
    print("Menor nota:", menor)

    if media >= 7:
        print("Situação: Aprovado!")
    elif media >= 5:
        print("Situação: Recuperação!")
    else:
        print("Situação: Reprovado!")

else:
    print("Nenhuma nota válida foi informada.")