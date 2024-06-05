import getpass
import oracledb

def multip(matriz, pares):
    return [
        (matriz[0][0] * pares[0] + matriz[0][1] * pares[1]) % 26,
        (matriz[1][0] * pares[0] + matriz[1][1] * pares[1]) % 26
    ]

def criptografia(texto, chave):
    texto = texto.replace(" ", "").lower()
    if len(texto) % 2 != 0:
        texto += texto[-1]
    pares = []
    for i in range(0, len(texto), 2):
        p1 = cifra_hill.index(texto[i])
        p2 = cifra_hill.index(texto[i+1])
        pares.append([p1, p2])
    cripto = ""
    for par in pares:
        a = multip(chave, par)
        cripto += cifra_hill[a[0]] + cifra_hill[a[1]]
    
    return cripto

def descriptografia(cripto): 
    pares = []
    for i in range(0, len(cripto), 2):
        p1 = cifra_hill.index(cripto[i])
        p2 = cifra_hill.index(cripto[i+1])
        pares.append([p1, p2])
    descripto = ""
    for par in pares:
        b = multip(chaveinv, par)
        descripto += cifra_hill[b[0]] + cifra_hill[b[1]]
    return descripto

def menu():
    escolha = int(input('O que deseja fazer?\n[1] Inserir Produtos\n[2] Remover Produtos\n[3] Alterar Produtos\n[4] Listar Produtos\n[0] Sair\n:'))
    while escolha < 0 or escolha > 4:
        print('Opção inválida! Por favor, tente novamente.')
        escolha = int(input('O que deseja fazer?\n[1] Inserir Produtos\n[2] Remover Produtos\n[3] Alterar Produtos\n[4] Listar Produtos\n[0] Sair\n:'))        
    if escolha == 1:
        inserir()
    elif escolha == 2:
        apagar()
    elif escolha == 3:
        alterar()
    elif escolha == 4:
        listar()
    elif escolha == 0:
        print('Saindo...')
        
def inserir():
    cursor.execute("""select distinct codigo_prod from tabela_produtos""")
    tabela = cursor.fetchall()
    quant = int(input('Quantos itens deseja inserir? '))
    for i in range(1, quant+1):
        print(f'{i}° Item: ')
        cod = (len(tabela) + i)
        Inome = input("Nome do produto: ")
        Idescricao = input("Descrição: ")
        Idescricao = criptografia(Idescricao, chave)
        Icp = float(input("Custo do produto: "))
        Icf = int(input("Custo fixo: "))
        Icv = int(input("Comissão de venda: "))
        Iiv = int(input("Impostos: "))
        Iml = int(input("Margem de lucro: "))
        
        while (Icf + Icv + Iiv + Iml) >= 100:
            print("Não é possível inserir na tabela, pois a soma das porcentagens não pode ser maior ou igual a 100%. Insira novamente:")
            Icf = int(input("Custo fixo: "))
            Icv = int(input("Comissão de venda: "))
            Iiv = int(input("Impostos: "))
            Iml = int(input("Margem de lucro: "))
        cursor.execute(f"""insert into tabela_produtos (codigo_prod, nome, descricao, custo_prod, custo_fixo, comissao_venda, impostos, rentabilidade)
        values ({cod}, '{Inome}', '{Idescricao}', {Icp}, {Icf}, {Icv}, {Iiv}, {Iml})""")
        print('Item inserido com sucesso!')
        conexao.commit()
    menu()
       
def apagar():
    def apagar_produto_por_nome(cursor, nome_produto):
        try:
            cursor.execute("SELECT codigo_prod FROM tabela_produtos WHERE nome = :nome_produto", {'nome_produto': nome_produto})
            codigo_produto = cursor.fetchone()[0]
            cursor.execute("DELETE FROM tabela_produtos WHERE nome = :nome_produto", {'nome_produto': nome_produto})
            print("Produto", nome_produto, "foi removido.")
            cursor.execute("""select distinct codigo_prod from tabela_produtos""")
            tabela = cursor.fetchall()
            for cod in range (codigo_produto + 1, len(tabela) + 2):
                cursor.execute (f"""
                    update tabela_produtos 
                    set codigo_prod = '{cod - 1}'
                    where codigo_prod = '{cod}'
                    """)
            conexao.commit()
            menu()
        except cx_Oracle.Error as error:
            print("Erro ao apagar produto:", error)
            apagar()

    def apagar_produto_por_codigo(cursor, codigo_produto):
        try:
            cursor.execute("SELECT nome FROM tabela_produtos WHERE codigo_prod = :codigo_produto", {'codigo_produto': codigo_produto})
            nome_produto = cursor.fetchone()[0]
            confirmacao = input(f"Tem certeza que deseja remover o produto '{nome_produto}' com o código {codigo_produto}? (Sim/Não): ")
            if confirmacao.lower() == "sim":
                cursor.execute("DELETE FROM tabela_produtos WHERE codigo_prod = :codigo_produto", {'codigo_produto': codigo_produto})
                print("Produto", nome_produto, "de código", codigo_produto, "foi removido.")
                cursor.execute("""select distinct codigo_prod from tabela_produtos""")
                tabela = cursor.fetchall()
                for cod in range (codigo_produto + 1, len(tabela) + 2):
                    cursor.execute (f"""
                        update tabela_produtos 
                        set codigo_prod = '{cod - 1}'
                        where codigo_prod = '{cod}'
                        """)
                conexao.commit()
                menu()
            else:
                print("Operação cancelada.")
                apagar()
        except cx_Oracle.Error as error:
            print("Erro ao apagar produto:", error)
            apagar()

    def apagar_todos_produtos(cursor):
        try:
            confirmacao = input("Tem certeza que deseja remover todos os produtos? (Sim/Não): ")
            if confirmacao.lower() == "sim":
                cursor.execute("DELETE FROM tabela_produtos")
                print("Todos os produtos foram removidos.")
                conexao.commit()
                menu()
            else:
                print("Operação cancelada.")
                apagar()
        except cx_Oracle.Error as error:
            print("Erro ao apagar produtos:", error)
            apagar()

    print("Opções de remoção de produto:")
    print("1. Remover pelo nome do produto")
    print("2. Remover pelo código do produto")
    print("3. Remover todos os produtos")
    print("4. Voltar ao menu")
    opcao = int(input("Escolha a opção desejada (1, 2 ou 3): "))
        
    while opcao < 1 and opcao > 4:   
        print("Opção inválida.") 
        opcao = input("Escolha a opção desejada (1, 2, 3 ou 4): ")
        
    if opcao == 1:
        produto_nome = input("Digite o nome do produto que deseja remover: ")
        confirmacao = input(f"Tem certeza que deseja remover o produto '{produto_nome}' ? (Sim/Não): ")
        if confirmacao.lower() == "sim":
            apagar_produto_por_nome(cursor, produto_nome)
        else:
            print("Operação cancelada.")
            apagar()
        
    elif opcao == 2:
        try:
            produto_codigo = int(input("Digite o código do produto que deseja remover: "))
            apagar_produto_por_codigo(cursor, produto_codigo)
        except ValueError:
            print("Digite um número inteiro válido para o código do produto.")
            apagar()
        
    elif opcao == 3:
        apagar_todos_produtos(cursor)
        
    elif opcao == 4:
        menu()

def alterar():   
    def navegarAlteracoes():
        resposta = str (input ('Deseja alterar algo? (Sim/Não)'))
        if resposta.lower() == 'sim':
            alterarValor()
        else:
            print ('Voltando ao menu')
            menu()
                
    def alterarValor():
        print('Atributos disponíveis: "nome", "descricao", "custo_prod", "custo_fixo", "comissao_venda", "impostos" e "rentabilidade".')
        coluna = str(input('Nome do atributo (digite em minúsculo): '))
        if coluna == 'descricao':
            cursor.execute("""select distinct codigo_prod from tabela_produtos""")
            tabela = cursor.fetchall()
            for cod in range (1, len(tabela)+1):
                cursor.execute(f"""select NOME from tabela_produtos where codigo_prod = {cod}""")
                nome = cursor.fetchall()
                print(nome[0][0])
            resp = input('Escolha qual produto você deseja alterar a descrição: ')
            cripto = input('Descrição nova: ')
            valorNovo = criptografia(cripto, chave)
            cursor.execute (f"""
                            update tabela_produtos 
                            set {coluna} = '{valorNovo}'
                            where nome = '{resp}'
                            """)
            print ('Nome/Valor atualizado com sucesso!')
        elif coluna == 'custo_fixo' or coluna == 'comissao_venda' or coluna == 'impostos' or coluna == 'rentabilidade':
            cursor.execute("""select distinct codigo_prod from tabela_produtos""")
            tabela = cursor.fetchall()
            for cod in range (1, len(tabela)+1):
                cursor.execute(f"""select NOME from tabela_produtos where codigo_prod = {cod}""")
                nome = cursor.fetchall()
                print(nome[0][0])
            resp = input('Escolha qual produto você deseja alterar o valor: ')
            valorAntigo = int(input('Valor antigo: '))
            valorNovo = int(input('Valor novo: '))
            cursor.execute (f"""
                update tabela_produtos 
                set {coluna} = '{valorNovo}'
                where nome = '{resp}'
                """)
            cursor.execute(f"""select CUSTO_FIXO from tabela_produtos where nome = '{resp}'""")
            custo_fixo = cursor.fetchall()
            cursor.execute(f"""select COMISSAO_VENDA from tabela_produtos where nome = '{resp}'""")
            custo_venda = cursor.fetchall()
            cursor.execute(f"""select IMPOSTOS from tabela_produtos where nome = '{resp}'""")
            imposto = cursor.fetchall()
            cursor.execute(f"""select RENTABILIDADE from tabela_produtos where nome = '{resp}'""")
            rentabilidade = cursor.fetchall()
            if custo_fixo[0][0] + custo_venda[0][0] + imposto[0][0] + rentabilidade[0][0] >= 100:
                cursor.execute (f"""
                update tabela_produtos 
                set {coluna} = '{valorAntigo}'
                where nome = '{resp}'
                """)
                print('Não foi possível realizar a operação, a soma das porcentagens é maior ou igual a 100.')
            else:
                print ('Valor atualizado com sucesso!')
        elif coluna == 'custo_prod':
            cursor.execute("""select distinct codigo_prod from tabela_produtos""")
            tabela = cursor.fetchall()
            for cod in range (1, len(tabela)+1):
                cursor.execute(f"""select NOME from tabela_produtos where codigo_prod = {cod}""")
                nome = cursor.fetchall()
                print(nome[0][0])
            resp = input('Escolha qual produto você deseja alterar o valor: ')
            valorNovo = float(input ('Valor novo: '))
            cursor.execute (f"""
                            update tabela_produtos 
                            set {coluna} = '{valorNovo}'
                            where nome = '{resp}'
                            """)
            print ('Valor atualizado com sucesso!')
        else:
            valorAntigo = str(input ('Nome antigo: '))
            valorNovo = str(input ('Nome novo: '))
            cursor.execute (f"""
                            update tabela_produtos 
                            set {coluna} = '{valorNovo}'
                            where {coluna} = '{valorAntigo}'
                            """)                     
            print ('Nome atualizado com sucesso!')
        conexao.commit()
        navegarAlteracoes()


    navegarAlteracoes()

def listar():
    cursor.execute("""select distinct codigo_prod from tabela_produtos""")
    tabela = cursor.fetchall()

    for cod in range (1, len(tabela)+1):
        cursor.execute(f"""select NOME from tabela_produtos where codigo_prod = {cod}""")
        nome = cursor.fetchall()
        cursor.execute(f"""select DESCRICAO from tabela_produtos where codigo_prod = {cod}""")
        descricao = cursor.fetchall()
        cursor.execute(f"""select CUSTO_PROD from tabela_produtos where codigo_prod = {cod}""")
        cp = cursor.fetchall()
        cursor.execute(f"""select CUSTO_FIXO from tabela_produtos where codigo_prod = {cod}""")
        cf = cursor.fetchall()
        cursor.execute(f"""select COMISSAO_VENDA from tabela_produtos where codigo_prod = {cod}""")
        cv = cursor.fetchall()
        cursor.execute(f"""select IMPOSTOS from tabela_produtos where codigo_prod = {cod}""")
        iv = cursor.fetchall()
        cursor.execute(f"""select RENTABILIDADE from tabela_produtos where codigo_prod = {cod}""")
        ml = cursor.fetchall()
        pv = cp[0][0] / (1 - ((cf[0][0] + cv[0][0] + iv[0][0] + ml[0][0])/100))
    
        if(pv<=0):
            print('-'*45)
            print(f'Preço de venda menor ou igual a zero -> {pv}')
        else:
            print('-'*45)
            print("Código do produto:", cod)
            print("Nome do produto:", nome[0][0])
            print(f"Descrição do produto: {descriptografia(descricao[0][0])}\n")
            print(f"Descrição                      {'Valor':6} | {'  %':6}")
            print(f"A. Preço de venda              {pv:6.2f} | {'   100%':6}")
            print(f"B. Custo de aquisição          {cp[0][0]:6.2f} | {(cp[0][0] * 100) / pv:6.2f}%")
            print(f"C. Receita Bruta               {pv - cp[0][0]:6.2f} | {100 - ((cp[0][0] * 100) / pv):6.2f}%")
            print(f"D. Custo fixo/Administrativo   {(pv * cf[0][0]) / 100:6.2f} | {cf[0][0]:6.2f}%")
            print(f"E. Comissão de vendas          {(pv * cv[0][0]) / 100:6.2f} | {cv[0][0]:6.2f}%")
            print(f"F. Impostos                    {(pv * iv[0][0]) / 100:6.2f} | {iv[0][0]:6.2f}%")
            print(f"G. Outros custos               {((pv * cf[0][0]) / 100) + ((pv * cv[0][0]) / 100) + ((pv * iv[0][0]) / 100):6.2f} | {(cf[0][0] + cv[0][0] + iv[0][0]):6.2f}%")
            print(f"H. Rentabilidade               {(pv * (ml[0][0] / 100)):6.2f} | {(ml[0][0]):6.2f}%")

            if(ml[0][0]>20):
                print('-'*45)
                print('Lucro alto')
            elif(ml[0][0] > 10 and ml[0][0]<=20):
                print('-'*45)
                print('Lucro médio')
            elif(ml[0][0] > 0 and ml[0][0]<=10):
                print('-'*45)
                print('Lucro baixo')
            elif(ml[0][0]==0):
                print('-'*45)
                print('Equilíbrio')
            elif(ml[0][0]<0):
                print('-'*45)
                print('Prejuízo')
                print('-'*45)
                
    menu()

try:
    conexao = oracledb.connect(
    user = "BD150224132",
    password = "Crcud6",
    dsn = '172.16.12.14/xe')
except Exception as erro:
    print("Erro ao conectar", erro)
else:
    print("Conectado", conexao.version)
    cursor = conexao.cursor()

cifra_hill = "abcdefghijklmnopqrstuvwxyz"
chave = [[4, 3], [1, 2]]
chaveinv = [[42, -63],[-21, 84]]

menu()

print('Fim do Programa.')

cursor.close()
conexao.close()
