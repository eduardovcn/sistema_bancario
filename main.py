import textwrap
import des_sistema_bancario as banco



def menu():
    menu =  """\n================ MENU ================
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova Conta
[lc]\tListar Contas
[nu]\tNovo Usuário
[q] \tSair
========================================
Escolha uma opção: """
    
    return input(textwrap.dedent(menu)) #ja cria um print esperando a resposta do usuário

def main ():
    numero_saques = banco.numero_saques
    limite = banco.limite
    saldo = banco.saldo
    extrato = banco.extrato
    limite_saques = banco.LIMITE_SAQUES
    usuarios = banco.usuarios
    lista_contas = banco.lista_contas
    agencia = banco.AGENCIA
    
    while True:
        opcao = menu()

        if opcao not in ["d", "s", "e", "nc", "lc", "nu", "q"]:
            print("\n@@@ Opção inválida! Tente novamente. @@@")
            continue

        elif opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta_alvo = input("Informe o número da conta_alvo(0000): ")
            
            banco.depositar(
                valor=valor,
                numero_conta_alvo=conta_alvo,
                lista_contas=lista_contas
            )

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            numero_conta_alvo = input("Informe o número da conta_alvo(0000): ")

            banco.sacar(valor, numero_conta_alvo, limite, lista_contas)

        elif opcao == "e":
            conta_alvo = input("Informe o número da conta_alvo(0000): ")
            banco.extrato_conta(conta_alvo, extrato, saldo)

        elif opcao == "nc":
            nome = input("Informe o nome do titular da conta_alvo: ")
            cpf = input("Informe o CPF do titular da conta_alvo: ")
            banco.criar_conta(nome, cpf)
            

        elif opcao == "lc":
            banco.listar_contas(usuarios, lista_contas)

        elif opcao == "nu":
            nome = input("Informe o nome do usuário: ")
            data_nasc = input("Informe a data de nascimento (DD/MM/AAAA): ")
            cpf = input("Informe o CPF (somente números): ")
            endereco = input("Informe o endereço (Logradouro - bairro - cidade/sigla estado: ): ")

            banco.criar_usuario(nome, data_nasc, cpf, endereco)

        elif opcao == "q":
            print("Saindo...")
            break


main()
