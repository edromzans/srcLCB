import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

dir_ugrhi_vazao = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/vazao/'
dir_ugrhi_prec = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/chuva/'

dir_input_model = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/ugrhi_sp/'

file_prec_txt = 'prec_3D-002.txt'
file_vazao_txt = '3D-002.txt'
file_etps_df = 'pcj_era5_etp_baciahid.pkl'
file_reanalises_df = 'pcj_era5_reanalise_baciahid.pkl'
file_cru_pet_df = 'pcj_cru_pet_bacia_hid.pkl'
file_xavier_et0_df = 'pcj_xavier_et0_bacia_hid.pkl'
file_out_balagua_model_df = 'pcj_bacia_hid_3D-002_ugrhi_sp.pkl'

df_pet_cru = pickle.load(open(dirsubset +
                              file_cru_pet_df, "rb"))
df_et0_xavier = pickle.load(open(dirsubset +
                                 file_xavier_et0_df, "rb"))

df_etps = pickle.load(open(dirsubset+file_etps_df, "rb"))

df_era5 = pickle.load(open(dirsubset+file_reanalises_df, "rb"))

df_prec = pd.read_csv(dir_ugrhi_prec+file_prec_txt, sep=';',
                      parse_dates=[0], index_col=[0],
                      usecols=[0, 1])

df_vazao = pd.read_csv(dir_ugrhi_vazao+file_vazao_txt, sep=';',
                       parse_dates=[0], index_col=[0])

# Vazao de m**3 s**-1 para mm mes**-1 3D-002 area 387 km**2
df_vazao.vazao = ((df_vazao.vazao*(10**3)
                   * (df_vazao.vazao.index.days_in_month*60*60*24))
                  / (387*(10**6)))

# Conversao etps pet_cru xavier_et0 [mm mes**-1]
ndias_era5 = np.transpose([df_etps.index.days_in_month]*5)
df_etps_mm_mes = df_etps*ndias_era5

ndias_cru = np.transpose([df_pet_cru.index.days_in_month])
df_pet_cru_mm_mes = df_pet_cru * ndias_cru
df_pet_cru_mm_mes.index = pd.to_datetime(
    df_pet_cru_mm_mes.index.strftime('%Y-%m-01'))

ndias_xavier = np.transpose([df_et0_xavier.index.days_in_month])
df_et0_xavier_mm_mes = df_et0_xavier * ndias_xavier
df_et0_xavier_mm_mes.index = pd.to_datetime(
    df_et0_xavier_mm_mes.index.strftime('%Y-%m-01'))

# #check time
# checktime = pd.concat([df_era5.tp*30.*1000.,
#                        df_prec,
#                        df_vazao*10.,
#                        df_etps.penmanmontaith*30.], axis=1)
# canual = checktime.groupby(checktime.index.month).agg(np.nanmean)

df_balagua_model = pd.concat([df_pet_cru_mm_mes,
                              df_et0_xavier_mm_mes,
                              df_etps_mm_mes,
                              df_prec,
                              df_vazao], axis=1)

df_balagua_model.to_pickle(dir_input_model +
                           file_out_balagua_model_df)
