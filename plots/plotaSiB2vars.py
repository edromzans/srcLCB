import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Expressao de conversao do formato de tempo
dateparse = lambda x: datetime.strptime(x, '%y%m%d%H')

# leitura do sib2dt como um dataframe
dfsib2dt = pd.read_table('sib2dt.dat', sep='\s+', dtype={'NYMD':str},
                         parse_dates=['NYMD'], date_parser=dateparse, index_col=['NYMD'])

# Lista as variaveis
print('Escolha uma variavel do SiB2 e defina no codigo python de'
      'visualizacao a variavel strvarplot:')
print(list(dfsib2dt))

# Defina o nome da variável do SiB2 que será visualizada, de
# acordo com a lista acima
strvarplot = 'u*_C'

varplot = dfsib2dt[strvarplot]

fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(5)

plt.style.use('bmh')

plt.subplot(311)
plt.title(strvarplot, fontsize=10)
plt.plot(varplot, 'black', linewidth=0.8)

# Media/soma diaria
varplot_diario = varplot.resample('D').mean()
# varplot_diario = varplot.resample('D').sum()

plt.subplot(312)
plt.title('Diário', fontsize=10)
plt.plot(varplot_diario, 'black', linewidth=0.8)

# Media/soma mensal
varplot_mensal = varplot.resample('M').mean()
# varplot_mensal = varplot.resample('M').sum()

plt.subplot(313)
plt.title('Mensal', fontsize=10)
plt.plot(varplot_mensal, 'black', linewidth=0.8)

plt.tight_layout()
plt.savefig(strvarplot+'_sib2var.png', dpi=300, bbox_inches='tight')
plt.show()
