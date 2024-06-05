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
    
    cursor.execute("""insert into tabela_produtos (codigo_prod, nome, descricao, custo_prod, custo_fixo, comissao_venda, impostos, rentabilidade)
values (1, 'Arroz', 'Arroz Branco Camil 5Kg', 20, 10, 5, 18, 40)""")
    
    cursor.execute("""insert into tabela_produtos (codigo_prod, nome, descricao, custo_prod, custo_fixo, comissao_venda, impostos, rentabilidade)
values (2, 'Feijão', 'Feijão Carioca Camil 1Kg', 4.50, 10, 10, 5, 25)""")
    
    cursor.execute("""insert into tabela_produtos (codigo_prod, nome, descricao, custo_prod, custo_fixo, comissao_venda, impostos, rentabilidade)
values (3, 'Caneta', 'Caneta Bic esferográfica preta', 7, 5, 5, 10, 15)""")
    
    cursor.execute("""insert into tabela_produtos (codigo_prod, nome, descricao, custo_prod, custo_fixo, comissao_venda, impostos, rentabilidade)
values (4, 'Urso Pelúcia', 'Urso de pelúcia tamanho mini', 30, 65, 15, 10, 17)""")
    
    cursor.execute("""insert into tabela_produtos (codigo_prod, nome, descricao, custo_prod, custo_fixo, comissao_venda, impostos, rentabilidade)
values (5, 'Borracha Premium', 'Borracha de alta qualidade, durável e eficiente', 1.50, 0.5, 10,
5, 30)""")
    
    conexao.commit()
    cursor.execute("select* from tabela_produtos")
    print(cursor.fetchall())
    
    cursor.close
    conexao.close
