
from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

LIMITE_SAQUES = 3
AGENCIA = "01"

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
usuarios = []
lista_contas = []



class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, saldo, numero, cliente):
        self._saldo = 0
        self._numero = numero 
        self._agencia = "0001" 
        self._cliente = cliente
        self._historico = Historico()
    
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        
        elif valor > 0:
            self._saldo -= valor
            print(f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! Valor de saque inválido. @@@")
            return False
        
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! Valor de depósito inválido. @@@")
            return False

class Historico(Conta):
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, tipo, valor):
        self._transacoes.append({"tipo": tipo, "valor": valor})

    def listar_transacoes(self):
        return self._transacoes





    def criar_conta(self):
        numero_conta = len(self.contas) + 1
        numero_conta_formatado = f"{numero_conta:04d}"

        conta = {
            "numero_conta": numero_conta_formatado,
            "nome": self.nome,
            "cpf": self.cpf,
            "saldo": 0,
            "extrato": "",
            "saques": 0
        }

        self.contas.append(conta)
        print(f"Conta criada com sucesso! Agência: {AGENCIA} Conta: {numero_conta_formatado}")


def depositar(valor, numero_conta_alvo, lista_contas):
    """
    Deposita um valor em uma conta específica na lista de lista_contas.
    Retorna True se o depósito foi bem-sucedido, False caso contrário.
    """
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor do depósito deve ser positivo. @@@")
        return 

    # Percorre a lista de lista_contas UMA ÚNICA VEZ
    for conta in lista_contas:
        # Procura pela conta correta
        if conta['numero_conta'] == numero_conta_alvo:
            # Modifica o saldo e o extrato DENTRO do dicionário da conta
            conta['saldo'] += valor
            conta['extrato'] += f"Depósito: R$ {valor:.2f}\n"

            print(f"\n=== Depósito de R$ {valor:.2f} realizado com sucesso! ===")
            print(f"Extrato da conta {numero_conta_alvo}:")
            print(conta['extrato'])
            return True # Sucesso!

    # Se o loop terminar e nenhuma conta for encontrada
    print(f"\n@@@ Operação falhou! A conta {numero_conta_alvo} não foi encontrada. @@@")
    return False

def sacar(valor, numero_conta_alvo, limite, lista_contas):
    """
    Saca um valor de uma conta específica na lista de lista_contas.
    Retorna True se o saque foi bem-sucedido, False caso contrário.
    """
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor do saque deve ser positivo. @@@")
        return False

    for conta in lista_contas:
        if conta['numero_conta'] == numero_conta_alvo:
            if (conta['saldo'] >= valor) and (valor <= limite) and (conta['saques'] < LIMITE_SAQUES):
                conta['saldo'] -= valor
                conta['saques'] += 1
                conta['extrato'] += f"Saque: R$ {valor:.2f}\n"
                print(f"\n=== Saque de R$ {valor:.2f} realizado com sucesso! ===")
                return True
            
            elif conta['saques'] >= LIMITE_SAQUES:
                print("\n@@@ Operação falhou! Limite de saques atingido. @@@")
                return False
            else:
                print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
                return False

    print(f"\n@@@ Operação falhou! A conta {numero_conta_alvo} não foi encontrada. @@@")
    return False


def extrato_conta(conta_alvo, extrato, saldo):
    for conta in lista_contas:
        if conta['numero_conta'] == conta_alvo:
            extrato = conta['extrato']
            saldo = conta['saldo']
            print(f"\n================ EXTRATO ================")
            print(f"Conta: {conta_alvo}")
            print(f'{extrato}')
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")
            return

def criar_conta(nome, cpf):
    numero_conta  = len(lista_contas) + 1
    if any(usuario['cpf'] == cpf and usuario['nome'] == nome for usuario in usuarios):
        
        numero_conta_formatado = f"{numero_conta:04d}"

        conta = {
            "numero_conta": numero_conta_formatado,
            "nome": nome,
            "cpf": cpf,
            "saldo": 0,
            "extrato": "",
            "saques": 0
        }

        lista_contas.append(conta)
        print(f"Conta criada com sucesso! Agência: {AGENCIA} Conta: {numero_conta_formatado}")
        
    else:
        print("Usuário não encontrado. Tente novamente.")

def listar_contas(usuarios, lista_contas):
    print("--- LISTA DE CONTAS ---")
    # Itera sobre cada dicionário de usuário na lista de usuários
    for usuario in usuarios:
        print(f"\nContas do(a) cliente: {usuario['nome']} (CPF: {usuario['cpf']})")
        encontrou_conta = False
        # Para cada usuário, itera sobre TODAS as lista_contas procurando correspondências
        for conta in lista_contas:
            if conta['cpf'] == usuario['cpf']: # Comparar pelo CPF é mais seguro
                print(f"  -> Agência: {AGENCIA} | Conta: {conta['numero_conta']}")
                encontrou_conta = True
        
        if not encontrou_conta:
            print("  -> Nenhuma conta encontrada para este cliente.")
    print("-----------------------")

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
