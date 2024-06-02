#%% Bibliotecas
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, timedelta
import matplotlib.pylab as plt
from matplotlib.ticker import MaxNLocator

#%%
ticker_bonds_usa = ['DGS1MO', 'DGS3MO', 'DGS6MO', 'DGS1',
                                        'DGS2','DGS3' ,'DGS5', 'DGS7','DGS10', 'DGS20','DGS30']
start = '2000-01-01'
today = datetime.today()

df_bonds_usa = pdr.get_data_fred(ticker_bonds_usa,start,today).dropna()
df_bonds_usa.columns = ['US1MO', 'US3MO', 'US6MO', 'US1Y', 'US2Y','US3Y',
                     'US5Y', 'US7Y','US10Y', 'US20Y','US30Y']

# Data atual
# Dicionário de durações dos títulos do Tesouro dos EUA em anos e meses
durations = {
    'DGS1MO': timedelta(days=30),  # 1 mês
    'DGS3MO': timedelta(days=90),  # 3 meses
    'DGS6MO': timedelta(days=180), # 6 meses
    'DGS1': timedelta(days=365),   # 1 ano
    'DGS2': timedelta(days=365*2), # 2 anos
    'DGS3': timedelta(days=365*3), # 3 anos
    'DGS5': timedelta(days=365*5), # 5 anos
    'DGS7': timedelta(days=365*7), # 7 anos
    'DGS10': timedelta(days=365*10), # 10 anos
    'DGS20': timedelta(days=365*20), # 20 anos
    'DGS30': timedelta(days=365*30)  # 30 anos
}

# Calculando os dias para o vencimento de cada título
vencimento_dias = {title: (today + duration - today).days for title, duration in durations.items()}
vencimento_dias = list(vencimento_dias.values())
vencimento_dias
vencimento_anos = [days / 365 for days in vencimento_dias]

#%%
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.titlecolor'] = 'w'
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.labelcolor'] = 'w'
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'gray'
plt.rcParams['xtick.color'] = 'w'
plt.rcParams['ytick.color'] = 'w'
plt.rcParams['grid.color'] = 'black'
plt.rcParams['grid.linestyle'] = ':'
plt.rcParams['grid.linewidth'] = 0.5
plt.rcParams['axes.autolimit_mode'] = 'data'
plt.rcParams['axes.axisbelow'] = True

#%%
plt.figure(figsize=(12, 6))
ax = plt.subplot()

# Plotando as curvas para os índices -1, -30 e -360
indices = [-1, -30, -252, (-252*2)]
colors = ['b', 'g', 'r','y']
labels = ['Hoje', '1 mês atrás', '1 ano atrás','2 anos atrás']

for idx, color, label in zip(indices, colors, labels):
    last_day = df_bonds_usa.index[idx].strftime('%Y-%m-%d')
    ax.plot(vencimento_anos, df_bonds_usa.iloc[idx], color=color, label=f'{label}')
    ax.scatter(x=vencimento_anos, y=df_bonds_usa.iloc[idx], color='black')
    minimo = 0
    maximo = 0
    max_value = df_bonds_usa.iloc[idx].max()
    min_value = df_bonds_usa.iloc[idx].min()
    if minimo < min_value:
        minimo = min_value
    if maximo < max_value:
        maximo = max_value
last_day = df_bonds_usa.index[indices[0]].strftime('%d/%m/%Y')
ax.set_xlabel('Duração até o vencimento (anos)')
ax.set_ylabel('Taxa de Juros (%)')
ax.set_ylim(minimo * 0.7, 6* 1.06)
ax.yaxis.set_major_locator(MaxNLocator(nbins=10))
ax.grid(True)

ax.set_title(f'US - Yield Curve - {last_day}')
ax.legend()
plt.figtext(0.08,0.05,'Dados: FED',horizontalalignment='left',fontsize=12,
            color = 'w')
plt.figtext(0.95,0.05,'Elaboração: Caio Martins',horizontalalignment='right',fontsize=12,
            color = 'w')
plt.tight_layout()
plt.savefig('US - Yield Curve.png')
plt.show()