import pandas as pd

# Carrega os arquivos
df_cotacao = pd.read_excel("cotação dolar.xlsx")
df_producao = pd.read_excel("Dados Produção Nacional Editado.xlsx")

# Limpa colunas completamente em branco da planilha de produção original
df_producao = df_producao.loc[:, ~df_producao.columns.str.contains("^Unnamed")]

# Cruza as duas tabelas pela coluna 'Ano'
df_merged = pd.merge(df_producao, df_cotacao, on="Ano", how="left")

# Arruma os valores
df_merged["Valor (R$)"] = df_merged["Valor (R$)"] * 1000
df_merged["Valor (USD$)"] = (df_merged["Valor (USD$)"] * 1000) / df_merged[
    "Valor"
]

# Cria a coluna 'categoria' tratando valores numéricos/nulos (como o 0)
df_merged["categoria"] = (
    df_merged["Descrição NCM"].astype(str).str.split().str[0]
)
df_merged["categoria"] = df_merged["categoria"].replace(
    {"Partes": "Parte", "0": "", "nan": ""}
)

# Converte Toneladas para Quilogramas e multiplica a quantidade por 1000
filtro_toneladas = (
    df_merged["Unidade estatistica"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin(["toneladas", "tonelada"])
)

# Multiplica a quantidade por 1000 apenas nessas linhas
df_merged.loc[filtro_toneladas, "Quantidade estatistica"] = (
    df_merged.loc[filtro_toneladas, "Quantidade estatistica"] * 1000
)

# Altera a descrição da unidade para 'Quilogramas'
df_merged.loc[filtro_toneladas, "Unidade estatistica"] = "Quilogramas"

# Remove a coluna temporária da cotação e qualquer Unnamed restante, depois salvar
df_final = df_merged.drop(columns=["Valor"])
df_final = df_final.loc[:, ~df_final.columns.str.contains("^Unnamed")]

df_final.to_excel("producao_atualizada.xlsx", index=False)