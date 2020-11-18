import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt

dir_input_model = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/ugrhi_sp/'

file_balagua_model_df = 'pcj_bacia_hid_3D-002_urghi_sp.pkl'

df_balagua_model = pickle.load(open(
    dir_input_model+file_balagua_model_df, "rb"))


# (df_balagua_model.index.days_in_month*60*60*24)/10**3
# df_balagua_model.vazao = df_balagua_model.vazao*(2592./387.)
# df_balagua_model.vazao = ((df_balagua_model.vazao*(10**3)
#                            * (df_balagua_model.index.days_in_month*60*60*24))
#                           / (387*(10**6)))

df_balagua_model.plot()
plt.xlabel('tempo')
plt.ylabel('mm mês$^{-1}$')
plt.title('Serie temporal - media mensal')

#canual = df_balagua_model.groupby(df_balagua_model.index.month).agg(np.nanmean)
#canual.plot()
df_balagua_model.groupby(df_balagua_model.index.month).agg(np.nanmean).plot()
plt.xlabel('mês')
plt.ylabel('mm mês$^{-1}$')
plt.title('Ciclo anual')
plt.show()
