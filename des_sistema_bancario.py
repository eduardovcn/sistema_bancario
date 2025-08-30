import textwrap
from abc import ABC, abstractmethod
from datetime import datetime



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
    def __init__(self, numero, cliente):
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
            
        else:
            print("\n@@@ Operação falhou! Valor de depósito inválido. @@@")
            return False
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor): #sobescrita do metodo para fazer algumas validações com relação ao limite e quantidade de saques.
        numero_saques = len( [transacao for transacao in self._historico.listar_transacoes() if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! Limite de saque excedido. @@@")
            

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Limite de saques atingido. @@@")

        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""
        Agência: {self.agencia}
        C/C: {self.numero}
        Titular: {self.cliente.nome}
        """
   

class Historico(Conta):
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )


class Transacao(ABC):
    
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """
    ================= MENU =================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova Conta
    [lc]\tListar Contas
    [nu]\tNovo Usuário
    [q]\tSair
    ========================================
    Escolha uma opção: """
    
    return input(textwrap.dedent(menu)) #ja cria um print esperando a resposta do usuário

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return 
    #FIXME: não permite o cliente escolher conta
    return cliente.contas[0] 

def depositar(clientes):
    cpf = input("Informe o CPF do titular da conta: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):

    cpf = input("Informe o CPF do titular da conta: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do titular da conta: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")

    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n"

    print(extrato)
    print(f"Saldo: \n\tR$ {conta.saldo:.2f}")
    print("========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (DD-MM-AAAA): ")
    endereco = input("Informe o endereço (Logradouro - bairro - cidade/sigla estado: ): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta, limite=500, limite_saques=3)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n@@@ Conta criada com sucesso! @@@")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main ():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao not in ["d", "s", "e", "nc", "lc", "nu", "q"]:
            print("\n@@@ Opção inválida! Tente novamente. @@@")
            continue

        elif opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "q":
            print("Saindo...")
            break


main()
