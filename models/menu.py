import time
from decimal import Decimal
from models.conta_bancaria import ContaBancaria, ContaJaCadastradaException
from utils.helpers import formatar_valor_monetario, obter_conta_por_cpf, exibir_menu_principal, exibir_extrato
from utils.validacao import validar_cpf, validar_telefone, validar_cep, validar_nome, validar_endereco

contas = {}


def mostrar_conta(cpf):
    if cpf in contas:
        conta = contas[cpf]
        print(f"Detalhes da conta:")
        print(f"Nome do titular: {conta.nome}")
        print(f"Telefone: {conta.telefone}")
        print(f"CPF: {conta.cpf}")
        print(f"Endereço: {conta.endereco}")
        print(f"CEP: {conta.cep}")
    else:
        print("Conta não encontrada.")


def criar_conta():
    nome = input("Nome do titular: ")
    telefone = input("Telefone: ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")
    cep = input("CEP: ")

    try:
        if cpf in contas:
            raise ContaJaCadastradaException()  # Lança a exceção personalizada
        if not nome.strip() or not telefone.strip() or not cpf.strip() or not endereco.strip() or not cep.strip():
            raise ValueError(
                "Todos os campos (Nome, Telefone, CPF, Endereço, CEP) são obrigatórios para criar uma conta.")
        if not validar_nome(nome) or not validar_telefone(telefone) or not validar_cpf(cpf) or not validar_endereco(
                endereco) or not validar_cep(
            cep):
            raise ValueError("Dados inválidos. Verifique os campos de entrada.")

        conta = ContaBancaria(nome, telefone, cpf, endereco, cep)
        contas[cpf] = conta
        print(f"Conta criada com sucesso para {nome}.\n")
        mostrar_conta(cpf)  # Chama a função para mostrar os dados da conta
    except ContaJaCadastradaException as e:
        print(f"Erro ao criar conta: {e}")
    except ValueError as e:
        print(f"Erro ao criar conta: {e}")


def depositar(cpf):
    try:
        valor = Decimal(input("Informe o valor a ser depositado: "))
        conta = obter_conta_por_cpf(contas, cpf)
        if conta:
            conta.depositar(valor)
            print(f"Depósito de {formatar_valor_monetario(valor)} realizado com sucesso.")
        else:
            print("Conta não encontrada.")
    except ValueError as e:
        print(f"Erro ao depositar: {e}")


def sacar(cpf):
    valor = Decimal(input("Informe o valor a ser sacado: "))
    conta = obter_conta_por_cpf(contas, cpf)
    if conta:
        conta.sacar(valor)
        print(f"Saque de {formatar_valor_monetario(valor)} realizado com sucesso.")
    else:
        print("Conta não encontrada.")


def transferir(cpf_origem, cpf_destino):
    valor = Decimal(input("Informe o valor a ser transferido: "))
    conta_origem = obter_conta_por_cpf(contas, cpf_origem)
    conta_destino = obter_conta_por_cpf(contas, cpf_destino)

    try:
        if not valor > 0:
            raise ValueError("O valor da transferência deve ser maior que zero.")
        if not conta_origem:
            raise ValueError("Conta de origem não encontrada.")
        if not conta_destino:
            raise ValueError("Conta de destino não encontrada.")
        if not conta_origem.saldo >= valor:
            raise ValueError("Saldo insuficiente na conta de origem.")

        conta_origem.transferir(conta_destino, valor)
        print(f"Transferência de {formatar_valor_monetario(valor)} realizada com sucesso.")
    except ValueError as e:
        print(f"Erro ao transferir: {e}")


def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada no momento.")
    else:
        print("Contas cadastradas:")
        numero_conta = 1  # Inicialize o número da conta
        for cpf, conta in contas.items():
            print(f"{numero_conta}. CPF: {cpf}, Titular: {conta.nome}")
            numero_conta += 1  # Incrementa o número da conta


def apagar_conta(cpf):
    global contas
    if cpf in contas:
        conta = contas[cpf]
        print("Detalhes da conta:")
        print(f"Nome do titular: {conta.nome}")
        print(f"Telefone: {conta.telefone}")
        print(f"CPF: {conta.cpf}")
        print(f"Endereço: {conta.endereco}")
        print(f"CEP: {conta.cep}")

        confirmacao = input("Tem certeza que deseja apagar esta conta? (s/n): ")
        if confirmacao.lower() == 's':
            del contas[cpf]
            print(f"A conta com o CPF {cpf} foi apagada.")
        else:
            print("Exclusão da conta cancelada.")
    else:
        print(f"A conta com o CPF {cpf} não foi encontrada.")


def menu_principal():
    while True:
        exibir_menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            criar_conta()
        elif opcao == '2':
            cpf = input("Informe o CPF da conta: ")
            depositar(cpf)
        elif opcao == '3':
            cpf = input("Informe o CPF da conta: ")
            sacar(cpf)
        elif opcao == '4':
            cpf_origem = input("Informe o CPF da conta de origem: ")
            cpf_destino = input("Informe o CPF da conta de destino: ")
            transferir(cpf_origem, cpf_destino)
        elif opcao == '5':
            cpf = input("Informe o CPF da conta: ")
            conta = obter_conta_por_cpf(contas, cpf)
            if conta:
                exibir_extrato(conta)
            else:
                print("Conta não encontrada.")
        elif opcao == '6':
            listar_contas()  # Opção para listar as contas cadastradas
        elif opcao == '7':
            cpf_a_excluir = input("Informe o CPF da conta a ser apagada: ")
            apagar_conta(cpf_a_excluir)
        elif opcao == '8':
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

        time.sleep(3)
