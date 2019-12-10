import pandas as pd
import numpy as np
from lmfit import report_fit  # Minimizer, Parameters,
import matplotlib.pyplot as plt
import pickle
import calendar

# dird = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/dados/verifica/'
dird = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/dados/ugrhi/'
# arqv = '4C-007_diario.csv'
# arqv = '3D-002_mensal.csv'
arqv = 'paraiba_do_sul_58220000.txt'

aguadf = pd.read_csv(dird+arqv, header=0, parse_dates=[0], sep=';', names=[
    'datatempo', 'p', 'q', 'escobas'])

# corrigindo tempo!!!!!
xtimeM = np.asarray(aguadf.datatempo, dtype='datetime64[D]')
corrig = xtimeM #- np.timedelta64(122, 'D')  # + np.timedelta64(9, 'M') ou - np.timedelta64(3, 'M')
x_eixo = pd.to_datetime(corrig)

P = np.asarray(aguadf.p)
Qm = np.asarray(aguadf.q)


dados = {'P': P, 'Qm': Qm, 'mes': x_eixo.month}
toanual_df = pd.DataFrame(data=dados, index=x_eixo)

# canual = toanual_df.groupby('mes').agg(np.nansum)
canual = toanual_df.groupby('mes').agg(np.nanmean)

d_mes = dict(enumerate(calendar.month_abbr))
canual.index = canual.index.map(d_mes)

plt.style.use('bmh')
plt.plot(canual.P, label='P')
plt.plot(canual.Qm, label='Qm')
plt.legend()
plt.show()
