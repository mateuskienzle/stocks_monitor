import pandas as pd

'''
Essa file aqui serve para o download das informações da distribuição da carteira da IBOV.
1º Baixei as infos necessárias no site -> https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm
2º O .csv fornecido vem com erros de encriptação. Abrir a file no Excel ou semelhante e salvá-lo novamente em outro CSV
3º Tendo feito isso, basta abrir com o pd.read_csv() normalmente.
'''

df = pd.read_csv('tabela_ibov.csv')

df['Qtde. Teórica'] = pd.to_numeric(df['Qtde. Teórica'].str.replace('.', ''))
df['Participação'] = df['Qtde. Teórica'] / df['Qtde. Teórica'].sum()

# df['Participação'].sum()
# df.groupby('Setor')['Participação'].sum()

df['Setor'] = df['Setor'].apply(lambda x: x.split('/')[0].rstrip())
df.groupby('Setor')['Participação'].sum() * 100     # resultado que queríamos

df