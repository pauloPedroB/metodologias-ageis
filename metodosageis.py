import mysql.connector as banco
import bcrypt
import random
import string


conexao = banco.connect(
    host='localhost',
    user='root',
    password='Victor@12',
    database='banco_teste',
)
cursor = conexao.cursor()
acabar = False
while(acabar == False):
    print("BEM VINDO AO DEFINIR NOME\n")

    opition = int(input("QUAL OPÇÃO VOCÊ DESEJA?\n1- LOGIN\n2- CADASTRO\n3-RECUPERAR SENHA\n"))

    if opition == 1:
        email = input("DIGITE SEU EMAIL:\n")
        senha = input("DIGITE SUA SENHA:\n")
        cursor.execute("SELECT senha FROM users WHERE email=%s", (email,))
        registro = cursor.fetchone()
        if registro:
            senha_armazenada = registro[0]
            if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
                print("Login bem-sucedido.")
            else:
                print("Senha incorreta.")
        else:
            print('Email incorreto.')
        cursor.close()

        conexao.close()

        

    elif opition == 2:
        email = input("DIGITE O EMAIL:\n")
        senha = input("DIGITE A SENHA:\n")
        confsenha = input("DIGITE A SENHA:\n")
        if(senha == confsenha):
            salt = bcrypt.gensalt(12)
            hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)

            comand = 'INSERT INTO users (email, senha) VALUES (%s, %s)'
            valores = (email, hashed_senha)
            cursor.execute(comand, valores)
            conexao.commit()

            cursor.close()

            conexao.close()
            
    elif opition == 3:
        email = input("DIGITE O EMAIL:\n")
       
        cursor.execute("SELECT senha FROM users WHERE email=%s", (email,))
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
                        comand = f'UPDATE users SET senha = "{hashed_senha}" WHERE email = "{email}"'
                        senhasiguais = True
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