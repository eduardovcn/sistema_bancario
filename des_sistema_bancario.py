

LIMITE_SAQUES = 3
AGENCIA = "0001"

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
numero_conta = 0000
usuarios = []
contas = []


def depositar(saldo, valor, extrato, /):

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Valor inválido para depósito.")
    return saldo, extrato

def sacar(saldo, valor, extrato, numero_saques, limite, LIMITE_SAQUES):
    if valor > 0:
        if numero_saques < LIMITE_SAQUES:
            if valor <= saldo and valor <= limite:
                saldo -= valor
                extrato += f"Saque: R$ {valor:.2f}\n"
                numero_saques += 1
                print("Saque realizado com sucesso!")

def extrato_conta(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_conta(nome, cpf, numero_conta):
    if nome and cpf in usuarios:
        numero_conta = len(contas) + 1
        conta ={
            "numero_conta": numero_conta,
            "nome": nome,
            "cpf": cpf,
            "saldo": 0,
            "extrato": ""
        }

        contas.append(conta)
        
    

def listar_contas(contas):
    pass

def criar_usuario(nome, data_nasc, cpf, endereco):
    usuario = {
        "nome": nome,
        "data_nasc": data_nasc,
        "cpf": cpf,
        "endereco": endereco
    }
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")


def sair():
    print("Obrigado por usar nosso sistema bancário. Até logo!")
    return exit()
