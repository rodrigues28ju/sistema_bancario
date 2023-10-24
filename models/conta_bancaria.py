class ContaBancaria:
    def __init__(self, nome, telefone, cpf, endereco, cep):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.endereco = endereco
        self.cep = cep
        self.saldo = 0
        self.extrato = []

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f'Depósito: +{valor}')

    def sacar(self, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            self.extrato.append(f'Saque: -{valor}')

    def transferir(self, outra_conta, valor):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            outra_conta.depositar(valor)
            self.extrato.append(f'Transferência para {outra_conta.nome}: -{valor}')
            outra_conta.extrato.append(f'Transferência de {self.nome}: +{valor}')

    def visualizar_extrato(self):
        for movimento in self.extrato:
            print(movimento)
        print(f'Saldo atual: {self.saldo}')


class ContaJaCadastradaException(Exception):
    def __init__(self, mensagem="CPF já cadastrado. Não é permitido cadastrar a mesma pessoa novamente."):
        self.mensagem = mensagem
        super().__init__(self.mensagem)
