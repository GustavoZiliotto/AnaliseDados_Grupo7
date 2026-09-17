import numpy as np
import pandas as pd

## Carrega o arquivo
df = pd.read_excel('Raw\tabela7752_produção naiconal.xlsx')

## Separa o que vem antes do ".", deixando só o número do mês
df['Mês'] = df['Mês'].astype(str).str.split('.').str[0]

## Cria a nova coluna dividindo entre Parte ou Empilhadeiras
df['Categoria'] = np.where(
    df['Descrição NCM'].astype(str).str.contains('Parte', case=False, na=False), 
    'Parte', 
    'Empilhadeiras'
)


df.to_excel('V_IMPORTACAO_GERAL_PROCESSADO.xlsx', index=False)

print("Novo arquivo gerado com sucesso!")