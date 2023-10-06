import mysql.connector as banco
import bcrypt
import random
import string
from datetime import datetime
import re


conexao = banco.connect(
    host='localhost',
    user='root',
    password='Victor@12',
    database='banco_financeiro',
)
cursor = conexao.cursor()
acabar = False
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
    if len(telefone) < 8:
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

while(acabar == False):
    print("BEM VINDO AO DEFINIR NOME\n")

    opition = int(input("QUAL OPÇÃO VOCÊ DESEJA?\n1- LOGIN\n2- CADASTRO\n3-RECUPERAR SENHA\n"))

    if opition == 1:
        email = input("DIGITE SEU EMAIL:\n")
        senha = input("DIGITE SUA SENHA:\n")

        cursor.execute("SELECT senha_usuario FROM tbl_usuario WHERE email_usuario=%s", (email,))
      
        registro = cursor.fetchone()

        if registro:
            senha_armazenada = registro[0]
            
            if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
                print("Login bem-sucedido.")
            else:
                print("Senha incorreta.")
        else:
            print('Email incorreto.')


        

    elif opition == 2:
        emailcerto=False
        datacerta = False
        senhasiguais = False
        nomevalido = False
        cpfvalido = False
        telvalido = False

        while(emailcerto ==False):
            email = input("DIGITE O EMAIL:\n")
            regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(regex, email):
                emailcerto= True
            else:
                print("Email inválido")
                
        while(senhasiguais ==False):
            senha = input("DIGITE A SENHA:\n")
            confsenha = input("DIGITE A CONFIRMAÇÃO DE SENHA SENHA:\n")

            if(senha == confsenha):
                salt = bcrypt.gensalt(12)
                hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)
                if verificar_senha(senha):
                    senhasiguais = True
                else:
                    print("Senha deve conter: no mínimo oito caracteres, um caracter especial, um número e uma letra maiúscula")
            else:
                print("Senhas não conferem")

        while(nomevalido==False):
            regex = r'^[A-Za-z\s]{2,50}$'
            nome = input("DIGITE O NOME")
            if re.match(regex, nome):
                nomevalido= True
            else:
                print("Nome inválido")

        while (datacerta == False):
            dt = input("Digite sua data de nascimento. (dd/mm/ano)")
            try:
                data = datetime.strptime(dt, '%d/%m/%Y')
                print("Data inserida:", data)
                datacerta = True
            except ValueError:
                print("Formato de data inválido. Certifique-se de usar o formato 'dd/mm/aaaa'.")
        
        while(cpfvalido == False):
            cpf = input("Digite o cpf")
            if validar_cpf(cpf):
                cpfvalido = True
            else:
                print("CPF INVÁLIDO")
                
        while(telvalido ==  False):
            tel = input("Telefone do usuário (COM DD)")
            if validar_telefone(tel):
                telvalido = True
            else:
                print("Telefone inválido")


      
        salt = bcrypt.gensalt(12)
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)

        comand = 'INSERT INTO tbl_usuario (email_usuario, senha_usuario,cpf_usuario,telefone_usuario,data_nasc_usuario,nome_usuario,saldo_atual_usuario,status_usuario) VALUES (%s, %s,%s,%s,%s,%s,0,true)'
        valores = (email, hashed_senha,cpf,tel,data,nome)
        cursor.execute(comand, valores)
        conexao.commit()


            
    elif opition == 3:
        email = input("DIGITE O EMAIL:\n")
       
        cursor.execute("SELECT senha_usuario FROM tbl_usuario WHERE email_usuario=%s", (email,))
        registro = cursor.fetchone()

        if(registro):
            letras = ''.join(random.choice(string.ascii_lowercase) for _ in range(3))
            numeros = ''.join(random.choice(string.digits) for _ in range(3))
            codigo = letras + numeros
            print(f"Seu código é:\n---------\n{codigo}\n---------\n")
            cod = input("DIGITE O CÓDIGO:\n")
            if cod == codigo:
                
                 senhasiguais = False
                 while(senhasiguais == False):
                    novasenha = input("Digite a nova senha:")
                    confnovasenha = input("confirme a nova senha")
                    if(novasenha == confnovasenha):
                        salt = bcrypt.gensalt(12)
                        hashed_senha = bcrypt.hashpw(novasenha.encode('utf-8'), salt)
                        if verificar_senha(senha):
                            comand = f'UPDATE tbl_usuario SET senha_usuario = "{hashed_senha}" WHERE email_usuario = "{email}"'
                            senhasiguais = True
                        else:
                            print("Senha deve conter: no mínimo oito caracteres, um caracter especial, um número e uma letra maiúscula")
                    else:
                        print("Senhas não conferem!")

            valores = ()
            cursor.execute(comand)
            conexao.commit()

        else:
            print("Email não encontrado")


   

#nome_produto = "banana"
#valor = 0.5

# Use placeholders para evitar injeção de SQL
#comando = 'INSERT INTO product (NAME_PRODUCT, VALUE) VALUES (%s, %s)'
#valores = (nome_produto, valor)

#cursor.execute(comando, valores)
#conexao.commit()

#conexao.commit()
conexao.close()