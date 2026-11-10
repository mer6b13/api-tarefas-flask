import math

def soma(a, b):
    return a + b

def subtracao(a, b):
    return a - b

def multiplicacao(a, b):
    return a * b

def divisao(a, b):
    if b == 0:
        return None  # Para indicar erro na divisão
    else:
        return a / b

def potenciacao(a, b):
    return a ** b

def raiz_quadrada(a):
    if a < 0:
        return None  # Raiz de número negativo não definida neste programas
    else:
        return math.sqrt(a)

def menu():
    print("\nEscolha a operação:")
    print("+ : Soma")
    print("- : Subtração")
    print("* : Multiplicação")
    print("/ : Divisão")
    print("% : Potenciação")
    print("r : Raiz Quadrada")
    print("s : Sair")

while True:
    menu()
    operacao = input("Digite a operação desejada: ").lower()

    if operacao == 's':
        print("Encerrando a calculadora. Até mais!")
        break

    if operacao == 'r':  # Raiz quadrada só precisa de um número
        try:
            num = float(input("Digite o número para calcular a raiz quadrada: "))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
            continue
        resultado = raiz_quadrada(num)
        if resultado is None:
            print("Não é possível calcular a raiz quadrada de número negativo.")
        else:
            print(f"Raiz quadrada de {num} = {resultado:.2f}")

    elif operacao in ['+', '-', '*', '/', '%']:
        try:
            num1 = float(input("Digite o primeiro número: "))
            num2 = float(input("Digite o segundo número: "))
        except ValueError:
            print("Entrada inválida. Por favor, digite números válidos.")
            continue

        if operacao == '+':
            print(f"{num1} + {num2} = {soma(num1, num2)}")
        elif operacao == '-':
            print(f"{num1} - {num2} = {subtracao(num1, num2)}")
        elif operacao == '*':
            print(f"{num1} * {num2} = {multiplicacao(num1, num2)}")
        elif operacao == '/':
            resultado = divisao(num1, num2)
            if resultado is None:
                print("Erro: divisão por zero não é permitida.")
            else:
                print(f"{num1} / {num2} = {resultado}")
        elif operacao == '%':
            print(f"{num1} ^ {num2} = {potenciacao(num1, num2)}")

    else:
        print("Operação inválida. Tente novamente.")