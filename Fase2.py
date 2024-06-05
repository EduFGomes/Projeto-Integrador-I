import getpass
import oracledb

pw = getpass.getpass("Insira a senha:")

try:
    conexao = oracledb.connect(
    user = "BD150224134",
    password = pw,
    dsn = 'BD-ACD/xe')
except Exception as erro:
    print("Erro ao conectar", erro)
else:
    print("Conectado", conexao.version)
    cursor = conexao.cursor()
    
cp = []
cf = []
cv = []
iv = []
ml = []

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
        print("Nome do produto:", nome)
        print()
        print(f"Descrição                      {'Valor':6} | {'  %':6}")
        print(f"A. Preço de venda              {pv:6.2f} | {'   100%':6}")
        print(f"B. Custo de aquisição          {cp[0][0]:6.2f} | {(cp[0][0] * 100) / pv:6.2f}%")
        print(f"C. Receita Bruta               {pv - cp[0][0]:6.2f} | {100 - ((cp[0][0] * 100) / pv):6.2f}%")
        print(f"D. Custo fixo/Administrativo   {(pv * cf[0][0]) / 100:6.2f} | {cv[0][0]:6.2f}%")
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

conexao.commit()



cursor.close
conexao.close
