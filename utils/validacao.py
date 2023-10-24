def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        return False

    cpf = list(map(int, cpf))

    # Calcula o primeiro dígito verificador
    total = 0
    for i in range(9):
        total += cpf[i] * (10 - i)
    resto = total % 11
    digito_verificador1 = 0 if resto < 2 else 11 - resto

    if cpf[9] != digito_verificador1:
        return False

    # Calcula o segundo dígito verificador
    total = 0
    for i in range(10):
        total += cpf[i] * (11 - i)
    resto = total % 11
    digito_verificador2 = 0 if resto < 2 else 11 - resto

    if cpf[10] != digito_verificador2:
        return False

    return True


def validar_telefone(telefone):
    # Remove espaços em branco e caracteres especiais
    telefone = ''.join(filter(str.isdigit, telefone))

    # Verifica se o número de telefone tem um comprimento mínimo
    if len(telefone) >= 10:  # Neste exemplo, consideramos um número de telefone válido com pelo menos 10 dígitos
        return True

    return False


def validar_cep(cep):
    # Remove espaços em branco e caracteres especiais
    cep = ''.join(filter(str.isdigit, cep))

    # Verifica se o CEP tem um comprimento adequado
    if len(cep) == 8 or len(cep) == 9:  # 8 dígitos para a maioria dos CEPs, 9 dígitos em algumas áreas
        return True

    return False


def validar_nome(nome):
    if nome.strip() and nome.isalpha():
        return True
    return False


def validar_endereco(endereco):
    if endereco.strip():  # Verifica se o endereço não está em branco após remover espaços em branco
        return True
    return False

