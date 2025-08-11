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
    contas = banco.contas   
    agencia = banco.AGENCIA
    
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = banco.depositar(saldo, extrato, valor)
            print(f"Depósito realizado com sucesso! Novo saldo: R$ {saldo:.2f}")

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato = banco.sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                numero_saques=numero_saques,
                limite=limite,
                LIMITE_SAQUES=limite_saques
            )

        elif opcao == "e":
            banco.extrato_conta(saldo, 
                                extrato=extrato)

        elif opcao == "nc":
            nome = input("Informe o nome do titular da conta: ")
            cpf = input("Informe o CPF do titular da conta: ")
            banco.criar_conta(nome, cpf, numero_conta=banco.numero_conta)
            print(f"Conta criada com sucesso! Número da conta: {banco.AGENCIA},{len(banco.contas)}")

        elif opcao == "lc":
            banco.listar_contas(contas)

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
