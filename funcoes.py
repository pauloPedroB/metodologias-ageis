import re



def validar_cpf(cpf):
    # Remova caracteres de formatação do CPF, como pontos e traços
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifique se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Calcula o primeiro dígito verificador
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    resto = 11 - (total % 11)
    if resto == 10 or resto == 11:
        resto = 0
    if resto != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    resto = 11 - (total % 11)
    if resto == 10 or resto == 11:
        resto = 0
    if resto != int(cpf[10]):
        return False

    return True

def validar_telefone(telefone):
    # Remove caracteres de formatação do telefone, como espaços, parênteses, traços e pontos
    telefone = re.sub(r'[^\d]', '', telefone)

    # Verifica se o telefone possui pelo menos 8 dígitos (DDD + número local)
    if len(telefone) < 8 or len(telefone) > 11:
        return False

    # Verifica se os primeiros 2 dígitos correspondem a um DDD válido (códigos reais podem variar)
    ddd = telefone[:2]
    ddd_validos = ['11', '21', '31']  # Adicione outros DDDs válidos, se necessário

    if ddd not in ddd_validos:
        return False

    # Verifica se o restante dos dígitos são numéricos
    if not telefone[2:].isdigit():
        return False

    return True


def verificar_senha(senha):
    # Verifica se a senha tem pelo menos 8 caracteres
    if len(senha) < 8:
        return False

    # Verifica se a senha contém pelo menos uma letra maiúscula
    if not re.search(r'[A-Z]', senha):
        return False

    # Verifica se a senha contém pelo menos uma letra minúscula
    if not re.search(r'[a-z]', senha):
        return False

    # Verifica se a senha contém pelo menos um número
    if not re.search(r'\d', senha):
        return False

    # Verifica se a senha contém pelo menos um caractere especial
    if not re.search(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\-]', senha):
        return False

    return True
