import mysql.connector as banco
import bcrypt
import random
import string
from datetime import datetime
import re
import funcoes

conexao = banco.connect(
    host='localhost',
    user='root',
    password='Victor@12',
    database='banco_financeiro',
    
)
cursor = conexao.cursor()
acabar = False

while(acabar == False):
    try:
        print("\n---------------\nBEM VINDO AO DEFINIR NOME\n")

        opition = int(input("QUAL OPÇÃO VOCÊ DESEJA?\n1- LOGIN\n2- CADASTRO\n3-RECUPERAR SENHA\n"))

        if opition == 1:
            email = input("DIGITE SEU EMAIL:\n")
            senha = input("DIGITE SUA SENHA:\n")

            cursor.execute("SELECT * FROM tbl_usuario WHERE email_usuario=%s", (email,))
            
            registro = cursor.fetchone()

            if registro:
                senha_armazenada = registro[6]
                
                if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
                    print(f"\nLOGIN BEM SUCEDIDO\n---------------\n")
                    menu = True
                    while(menu == True):
                        print(f"BEM-VINDO(A) {registro[1]}\nVOCÊ TEM R$ {registro[7]}\n")
                        try:
                            
                            opition_menu = int(input("Qual opção você deseja?\n 1- RENDAS E DESPESAS\n 2- BOLETOS\n 3- CALENDÁRIO\n 4- CARTÃO DE CRÉDITO"))
                            if opition_menu == 1:
                                print("")
                                
                            elif opition_menu == 2:
                                datacerta = False
                                valorcorreto = False
                                descricaoboleto = False
                                print("\n---------------\nADICIONAR BOLETOS\n")
                                descricao = input("DESCRIÇÃO DO BOLETO: ")
                                while (valorcorreto ==False):
                                    try:
                                        saldo = float(input("VALOR DO BOLETO: R$ "))
                                        if(saldo >= 0):
                                            valorcorreto = True
                                        else:
                                            print("SALDO INVÁLIDO")
                                    except ValueError:
                                        print("INVÁLIDO\n")
                                        
                                while (datacerta == False):
                                    dt = input("DIGITE A DATA DE VENCIMENTO DO BOLETO. (DD/MM/AAAA)")
                                    try:
                                        data = datetime.strptime(dt, '%d/%m/%Y')
                                        data_inserida = data.date()
                                        data_atual = datetime.now().date()
                                        if data_inserida < data_atual:
                                            print("DATA DE VENCIMENTO NÃO PODE SER ANTERIOR A DATA ATUAL\n")
                                        else:
                                            datacerta = True
                                    except ValueError:
                                        print("FORMATO DE DATA INCORRETO. CERTIFIQUE-SE DE USAR O FORMATO 'DD/MM/AAAA'.")
                                

                                comand = 'INSERT INTO tbl_pagamentos (desc_pagamento,valor_pagamento,data_vencimento_pagamento,fk_id_usuario) values (%s,%s,%s,%s)'
                                valores = (descricao,saldo,data,registro[0])
                                cursor.execute(comand, valores)
                                conexao.commit()
                                print("BOLETO ADICIONADO COM SUCESSO!!")
                            elif opition_menu == 3:
                                consulta_calendario = False
                                while(consulta_calendario == False):
                                    data_calendario = input("DIGITE A DATA QUE VOCÊ DESEJA CONSULTAR NO CALENDÁRIO. (DD/MM/AAAA): ")
                                    try:
                                        data = datetime.strptime(data_calendario, '%d/%m/%Y')
                                        data_inserida = data.date()
                                        data_atual = datetime.now().date()
                                        if data_inserida < data_atual:
                                            print("DATA DE CONSULTA NÃO PODE SER ANTERIOR A DATA ATUAL\n")
                                        else:
                                            cursor.execute("SELECT  u.saldo_atual_usuario - SUM(p.valor_pagamento) AS total_valor FROM tbl_pagamentos p INNER JOIN tbl_usuario u ON p.fk_id_usuario = u.id_usuario WHERE u.id_usuario = %s and p.data_vencimento_pagamento < %s and p.data_vencimento_pagamento > %s", (registro[0],data_inserida,data_atual))
                                            saldo_futuro = cursor.fetchone()

                                            print(saldo_futuro[0])
                                            consulta_calendario = True
                                    except ValueError:
                                        print("FORMATO DE DATA INCORRETO. CERTIFIQUE-SE DE USAR O FORMATO 'DD/MM/AAAA'.")
                            
                        except ValueError:
                            print("ALGO DEU ERRADO\n")
                else:
                    print("\n SENHA INCORRETA\n")
            else:
                print('\nEMAIL INCORRETO\n')


            

        elif opition == 2:
            emailcerto=False
            datacerta = False
            senhasiguais = False
            nomevalido = False
            cpfvalido = False
            telvalido = False
            saldocorreto = False

            while(emailcerto ==False):
                email = input("DIGITE O EMAIL:\n")
                regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if re.match(regex, email):
                    cursor.execute("SELECT * FROM tbl_usuario WHERE email_usuario=%s", (email,))
                    registro = cursor.fetchone()
                    if registro:
                        print("EMAIL JÁ REGISTRADO EM NOSSA BASE DE DADOS\n")
                    else: 
                        emailcerto= True
                else:
                    print("EMAIL INVÁLIDO\n")
                    
            while(senhasiguais ==False):
                senha = input("DIGITE A SENHA: ")
                confsenha = input("DIGITE A CONFIRMAÇÃO DE SENHA SENHA: ")

                if(senha == confsenha):
                    if funcoes.verificar_senha(senha):
                        senhasiguais = True
                    else:
                        print("SENHA DEVE CONTER: NO MÍNIMO 8 CARACTERES, UM CARACTER ESPECIAL, UM NÚMERO E UMA LETRA MAIÚSCULA\n")
                else:
                    print("SENHAS NÃO CONFEREM\n")

            while(nomevalido==False):
                regex = r'^[A-Za-z\s]{2,50}$'
                nome = input("DIGITE O NOME: ")
                if re.match(regex, nome):
                    nomevalido= True
                else:
                    print("NOME INVÁLIDO\n")

            while (datacerta == False):
                dt = input("DIGITE SUA DATA DE NASCIMENTO (DD/MM/AAAA): ")
                try:
                    data = datetime.strptime(dt, '%d/%m/%Y')
                    print("DATA INSERIDA:", data)
                    datacerta = True
                except ValueError:
                    print("FORMATO DE DATA INCORRETO. CERTIFIQUE-SE DE USAR O FORMATO 'DD/MM/AAAA'.\n")
            
            while(cpfvalido == False):
                cpf = input("DIGITE SEU CPF: ")
                if funcoes.validar_cpf(cpf):
                    cpfvalido = True
                else:
                    print("CPF INVÁLIDO\n")
                    
            while(telvalido ==  False):
                tel = input("TELEFONE DO USUÁRIO (COM DD): ")
                if funcoes.validar_telefone(tel):
                    telvalido = True
                else:
                    print("TELEFONE INVÁLIDO\n")
            while(saldocorreto == False):
                try:
                    saldo = float(input("SALDO ATUAL: R$ "))
                    if(saldo >= 0):
                        saldocorreto = True
                    else: 
                        print("SALDO INVÁLIDO")
                except ValueError:
                    print("INVÁLIDO\n")

        
            salt = bcrypt.gensalt(12)
            hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), salt)

            comand = 'INSERT INTO tbl_usuario (email_usuario, senha_usuario,cpf_usuario,telefone_usuario,data_nasc_usuario,nome_usuario,saldo_atual_usuario,status_usuario) VALUES (%s, %s,%s,%s,%s,%s,%s,true)'
            valores = (email, hashed_senha,cpf,tel,data,nome,saldo)
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
                        novasenha = input("DIGITE A NOVA SENHA")
                        confnovasenha = input("CONFIRME A NOVA SENHA")
                        if(novasenha == confnovasenha):
                            salt = bcrypt.gensalt(12)
                            hashed_novasenha = bcrypt.hashpw(novasenha.encode('utf-8'), salt)
                            if funcoes.verificar_senha(novasenha):
                                comand = 'UPDATE tbl_usuario SET senha_usuario = %s WHERE email_usuario = %s'
                                valores = (hashed_novasenha,email)
                                cursor.execute(comand,valores)
                                conexao.commit()
                                senhasiguais = True
                            else:
                                print("SENHA DEVE CONTER: NO MÍNIMO 8 CARACTERES, UM CARACTER ESPECIAL, UM NÚMERO E UMA LETRA MAIÚSCULA\n")
                        else:
                            print("SENHAS NÃO CONFEREM")
                    else:
                        print("CÓDIGO INCORRETO")
            else:
                print("EMAIL NÃO ENCONTRADO")

    except ValueError:

        print("\n ALGO DEU ERRADO\n")
    

   

#nome_produto = "banana"
#valor = 0.5

# Use placeholders para evitar injeção de SQL
#comando = 'INSERT INTO product (NAME_PRODUCT, VALUE) VALUES (%s, %s)'
#valores = (nome_produto, valor)

#cursor.execute(comando, valores)
#conexao.commit()

#conexao.commit()
conexao.close()