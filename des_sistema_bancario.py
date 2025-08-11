

LIMITE_SAQUES = 3
AGENCIA = "01"

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
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

def criar_conta(nome, cpf):
    numero_conta  = len(contas) + 1
    if any(usuario['cpf'] == cpf and usuario['nome'] == nome for usuario in usuarios):
        
        numero_conta_formatado = f"{numero_conta:04d}"

        conta = {
            "numero_conta": numero_conta_formatado,
            "nome": nome,
            "cpf": cpf,
            "saldo": 0,
            "extrato": ""
        }

        contas.append(conta)
        print(f"Conta criada com sucesso! Agência: {AGENCIA} Conta: {numero_conta_formatado}")
        
    else:
        print("Usuário não encontrado. Tente novamente.")

def listar_contas(nome, contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    print("\n================ CONTAS =================")
    for n in nome:
        for conta in contas:
            if conta['nome'] == n['nome'] and conta['cpf'] == n['cpf']:
                print(f" Nome: {conta['nome']}, CPF: {conta['cpf']}, Agência: {AGENCIA} Conta: {conta['numero_conta']}, Saldo: R$ {conta['saldo']:.2f}")
    print("==========================================")

def criar_usuario(nome, data_nasc, cpf, endereco):
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Usuário já cadastrado com este CPF.")
        
    else:    
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
