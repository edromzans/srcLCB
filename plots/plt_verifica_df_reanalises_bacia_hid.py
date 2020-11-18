import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

file_reanalises_df = 'pcj_era5_reanalise_baciahid.pkl'

df_reanalises = pickle.load(open(
    dirsubset+file_reanalises_df, "rb"))

# df_reanalises[{'str', 'strd', 'ssr', 'ssrd', 'tisr', 'slhf', 'sshf'}].abs().plot()
# plt.xlabel('tempo')
# plt.ylabel('J m$^-2$ dia$^{-1}$')
# plt.title('Serie temporal - média mensal')
# df_reanalises[{'str', 'strd', 'ssr', 'ssrd', 'tisr', 'slhf', 'sshf'}].abs().groupby(
#     df_reanalises.index.month).mean().plot()
# plt.xlabel('mês')
# plt.ylabel('J m$^-2$ dia$^{-1}$')
# plt.title('Ciclo anual')


radwm2 = df_reanalises[{'str', 'strd', 'ssr', 'ssrd',
                        'tisr', 'slhf', 'sshf'}].abs() / 86400
radwm2.plot()
plt.xlabel('tempo')
plt.ylabel('W m$^-2$')
plt.title('Serie temporal - média mensal')
plt.savefig('reanalises_calor_radiacao.png', dpi=300, bbox_inches='tight')
radwm2.groupby(
    df_reanalises.index.month).mean().plot()
plt.xlabel('mês')
plt.ylabel('W m$^-2$')
plt.title('Ciclo anual')


df_reanalises.t2m = df_reanalises.t2m - 273.15
df_reanalises.d2m = df_reanalises.d2m - 273.15
df_reanalises[{'t2m', 'd2m', 'tmin_cru', 'tmax_cru'}].plot()
plt.xlabel('tempo')
plt.ylabel('$^\circ$C')
plt.title('Serie temporal - média mensal')
df_reanalises[{'t2m', 'd2m', 'tmin_cru', 'tmax_cru'}].groupby(
    df_reanalises.index.month).mean().plot()
plt.xlabel('mês')
plt.ylabel('$^\circ$C')
plt.title('Ciclo anual')


df_reanalises.sp = df_reanalises.sp/100.
df_reanalises[{'sp'}].plot()
plt.xlabel('tempo')
plt.ylabel('hPa')
plt.title('Serie temporal - média mensal')
df_reanalises[{'sp'}].groupby(
    df_reanalises.index.month).mean().plot()
plt.xlabel('mês')
plt.ylabel('hPa')
plt.title('Ciclo anual')


df_reanalises.pev = df_reanalises.pev * 10**3
df_reanalises.tp = df_reanalises.tp * 10**3
df_reanalises[{'pev', 'tp'}].abs().plot()
plt.xlabel('tempo')
plt.ylabel('mm dia$^-1$')
plt.title('Serie temporal - média mensal')
df_reanalises[{'pev', 'tp'}].abs().groupby(
    df_reanalises.index.month).mean().plot()
plt.xlabel('mês')
plt.ylabel('mm dia$^-1$')
plt.title('Ciclo anual')


vento = np.sqrt(df_reanalises.u10.values**2 + df_reanalises.v10.values**2)
xtime = df_reanalises.index.values
dados = {'vento': vento}
df_vento = pd.DataFrame(dados, index=xtime)
df_vento.plot()
# df_reanalises[{'u10', 'v10'}].plot()
plt.xlabel('tempo')
plt.ylabel('m s$^-1$')
plt.title('Serie temporal - média mensal')
# df_reanalises[{'u10', 'v10'}].groupby(
#      df_reanalises.index.month).mean().plot()
df_vento.groupby(
     df_vento.index.month).mean().plot()
plt.xlabel('mês')
plt.ylabel('m s$^-1$')
plt.title('Ciclo anual')


plt.show()
