import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#Configuaração dos gráficos
sns.set_theme(style="whitegrid")  
plt.rcParams.update({'figure.max_open_warning': 0})  

#Dados
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "baseDados", "dadosCase_1.csv")

#CSV --> DataF
df = pd.read_csv(CSV_FILE)

#Padronização nomes
df.rename(columns={
    'Gênero': 'Genero',
    'Vendas Globais (milhões)': 'Vendas_Global'
}, inplace=True)

#Informações DataF
print("Formato do DataFrame:", df.shape)
print(df.head())

#Limpeza de dados e convertendo para inteiro
if 'Ano' not in df.columns:
    raise KeyError("Coluna 'Ano' não encontrada no CSV.")
missing_years = df['Ano'].isna().sum()
print(f"Linhas com Ano faltando: {missing_years}")
df = df.dropna(subset=['Ano']).copy()

df['Ano'] = df['Ano'].astype(int)


"""
Análise Descritiva
"""
#Gênero mais vendido
vendas_generos = df.groupby('Genero', as_index=False)['Vendas_Global'].sum()
vendas_generos = vendas_generos.sort_values(by='Vendas_Global', ascending=False)

most_sold_genre = vendas_generos.iloc[0]

print("\nVendas globais somadas por gênero:")
print(vendas_generos)
print(f"\nGênero mais vendido globalmente: {most_sold_genre['Genero']} — {most_sold_genre['Vendas_Global']:.2f} milhões")

#Plataforma com mais lançamentos
lancamento_plataforma = df['Plataforma'].value_counts()
most_common_platform = lancamento_plataforma.idxmax()
print(f"\nPlataforma com mais lançamentos: {most_common_platform} — {lancamento_plataforma.max()} jogos")

#Criar coluna Decada
def classify_decade(year):
    """Classifica o ano em década"""
    if 1990 <= year <= 1999:
        return 'Anos 90'
    elif 2000 <= year <= 2009:
        return 'Anos 2000'
    elif 2010 <= year <= 2016:
        return 'Anos 2010'
    else:
        return 'Fora do intervalo'

df['Decada'] = df['Ano'].apply(classify_decade)
print('\nContagem por década:')
print(df['Decada'].value_counts())

#Gráficos
RESULTS_DIR = 'resultados'
os.makedirs(RESULTS_DIR, exist_ok=True)

grafico_barra = vendas_generos.head(5).copy()
plt.figure(figsize=(8,6))
sns.barplot(data=grafico_barra, x='Vendas_Global', y='Genero')
plt.title('Top 5 Gêneros por Vendas Globais (milhões)')
plt.xlabel('Vendas Globais (milhões)')
plt.ylabel('Gênero')
plt.tight_layout()
bar_path = os.path.join(RESULTS_DIR, 'grafico_barra.png')
plt.savefig(bar_path)
plt.close()
print(f"Gráfico de barras salvo em: {bar_path}")

grafico_linha = df.groupby('Ano').size().reset_index(name='Num_Jogos')
grafico_linha = grafico_linha.sort_values('Ano')
plt.figure(figsize=(10,5))
sns.lineplot(data=grafico_linha, x='Ano', y='Num_Jogos', marker='o', color='blue')
plt.title('Número de Jogos Lançados por Ano')
plt.xlabel('Ano')
plt.ylabel('Número de Jogos')
plt.tight_layout()
line_path = os.path.join(RESULTS_DIR, 'grafico_linha.png')
plt.savefig(line_path)
plt.close()
print(f"Gráfico de linhas salvo em: {line_path}")

#Conclusão
"""
A análise das vendas globais de videogames mostra que o gênero Shooter domina o mercado, com mais de 209 milhões de unidades vendidas, seguido por Battle Royale e Role-Playing. Isso confirma, para jogadores, há a preferencia por experiências intensas e competitivas.
O PC aparece como a plataforma com maior número de lançamentos, destacando sua versatilidade e importância no desenvolvimento e distribuição de jogos.
No aspecto temporal, há uma forte concentração de lançamentos entre 2000 e 2010 — período em que grandes franquias se consolidaram e o mercado global de games se expandiu rapidamente.
Esses resultados apontam tendências estratégicas valiosas para o posicionamento na área de entretenimento digital.
"""

print("\n*Conclusão*")
print("A análise mostra que o gênero 'Shooter' domina as vendas globais, seguido por 'Battle Royale' e 'Role-Playing'.")
print("O 'PC' foi a plataforma com mais lançamentos, reforçando seu papel central no ecossistema de games.")
print("A maior concentração de lançamentos ocorreu nos anos 2000, período de expansão do mercado global de jogos.")


vendas_generos.to_csv(os.path.join(RESULTS_DIR, 'vendas_generos_summary.csv'), index=False)
lancamento_plataforma.reset_index().to_csv(os.path.join(RESULTS_DIR, 'lancamento_plataforma.csv'), index=False)





