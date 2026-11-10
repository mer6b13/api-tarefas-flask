# Peça a idade do usuário
idade = int(input("Digite a sua idade: "))

# Verifica se a idade é negativa
if idade < 0:
    print("Idade inválida! Não pode ser negativa.")
else:

    # Verifica a categoria de acordo com a idade
    if idade <= 12:
        print("Categoria: Criança.")
    elif idade <= 17:
        print("Categoria: Adolescente.")
    elif idade <= 59:
        print("Categoria: Adulto.")
    else:
        print("Categoria: Idoso.")
    
    # Verifica se pode dirigir (idade mínima 18)
    if idade >= 18:
        print("Você pode dirigir.")
    else:
        print("Você não pode dirigir.")