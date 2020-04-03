import pandas as pd
import numpy as np
import netCDF4 as nc4
import matplotlib.pyplot as plt
# import time

# dirInput = '/dados/ProcessoOtimizacaoModelos/' \
#     'calibracaoBalagua/dados/inputs/ugrhi_sp/'

dirInput = '/vol0/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/ugrhi_sp/'

# dirUgrhi = '/dados/ProcessoOtimizacaoModelos/' \
#     'calibracaoBalagua/dados/ugrhi/'

# dirUgrhi = '/media/hd2TB/lcbiag/ProcessoOtimizacaoModelos/' \
#     'calibracaoBalagua/dados/inputs/ugrhi_sp/'

dirUgrhi = '/vol0/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/'

# dirInput = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
#     'calibracaoBalagua/dados/inputs/ugrhi_sp/'

# UGRHI SP
# tagname = '58220000'
# lat = -22.69
# lon = -44.98
#-------------------------
# tagname = '3D-001'
# lat = -22.68
# lon = -46.97
#-------------------------
# tagname = '4C-007'
# lat = -21.7
# lon = -47.82
#-------------------------
# tagname = '4B-015'
# lat = -20.63
# lon = -47.28
#-------------------------
tagname = '5B-011'
lat = -20.91
lon = -48.09
#-------------------------
##########

# Leitura dos dados da UGRHI selecionada
aguadados_csv = tagname+'_ugrhi_sp.csv'
aguadf = pd.read_csv(dirUgrhi+aguadados_csv,
                     header=0, parse_dates=[0], sep=';',
                     names=['datatempo', 'p', 'q', 'escobas'])
# aguadf.index = aguadf['datatempo']

# corrigindo tempo
xtimeM = np.asarray(aguadf.datatempo, dtype='datetime64[M]')
corrig = xtimeM - np.timedelta64(4, 'M')
x_eixo = pd.to_datetime(corrig)

aguadf.index = x_eixo  # aguadf['datatempo']

# Dados Austin/UFES (Xavier)
#ncf_xavier_pet = '/dados/ET0_xavier/' \
#    'ETo_daily_UT_Brazil_v2_20140101_20170731_s1.nc'
ncf_xavier_pet = '/vol0/evandro/lcbiag/ET0_xavier/' \
    'ETo_daily_UT_Brazil_v2_20140101_20170731_s1.nc'

xavier = nc4.Dataset(ncf_xavier_pet, 'r')

# time.sleep(20)

xlon = xavier.variables['longitude'][:]
ylat = xavier.variables['latitude'][:]
tp = xavier.variables['time'][:]
pet = xavier.variables['ETo'][:]

xlon = np.ma.getdata(xlon)
ylat = np.ma.getdata(ylat)
tp = np.ma.getdata(tp)

datatempo_xavier = np.datetime64('2014-01-01', 'h') + tp.astype('timedelta64[h]')

nx_xavier = len(datatempo_xavier)

dislat = np.abs(ylat - lat)
dislon = np.abs(xlon - lon)

poslatgr = np.where(dislat == np.min(dislat))
print(lat, ylat[poslatgr])

poslongr = np.where(dislon == np.min(dislon))
print(lon, xlon[poslongr])

ts_pet = np.ma.getdata(pet[:, poslatgr, poslongr]).reshape(nx_xavier)
pet_diario_df = pd.DataFrame(data={'pet': ts_pet}, index=datatempo_xavier)

pet_df = pet_diario_df.resample('M').agg(np.nanmean)

# tstart = np.asarray(aguadf.index[0], dtype='datetime64[M]')
# tstop = (np.asarray(aguadf.index[-1], dtype='datetime64[M]') +
#          np.timedelta64(1, 'M'))

tstart = np.asarray(pet_df.index[0], dtype='datetime64[M]')
tstop = (np.asarray(pet_df.index[-1], dtype='datetime64[M]') +
         np.timedelta64(1, 'M'))

xtime = np.arange(tstart,
                  tstop,
                  dtype='datetime64[M]')

# xtime = np.arange(tstart.strftime('%Y-%m'),
#                   tstop.strftime('%Y-%m'),
#                   dtype='datetime64[M]')
# tsdf = pd.DatetimeIndex(xtime)

tsdf = pd.to_datetime(xtime)
nx_ts = len(tsdf)

# conta numero de dias em cada mes
xtimeD = np.arange(tstart,
                   tstop,
                   dtype='datetime64[D]')

ndiasdf = pd.DataFrame(xtimeD)
ndias = ndiasdf.set_index(0).resample('M').size()

etp_ts = np.empty(nx_ts)
etp_ts.fill(np.nan)
p_ts = np.empty(nx_ts)
p_ts.fill(np.nan)
q_ts = np.empty(nx_ts)
q_ts.fill(np.nan)

for tk in range(len(xtime)):
    posxavier = np.where((pet_df.index.year == tsdf.year[tk]) &
                         (pet_df.index.month == tsdf.month[tk]))
    posxavier = posxavier[0]

    posagua = np.where((aguadf.index.year == tsdf.year[tk]) &
                       (aguadf.index.month == tsdf.month[tk]))
    posagua = posagua[0]

    if (posxavier.size == 1) and (posagua.size == 1):
        etp_ts[tk] = pet_df.pet[posxavier] * ndias[tk]  # mm/mes
        p_ts[tk] = aguadf.p[posagua]
        q_ts[tk] = aguadf.q[posagua]

dados = {'etp': etp_ts, 'p': p_ts, 'q': q_ts}
hidmod_df = pd.DataFrame(data=dados, index=xtime)

# Salva ts to hidromodel binario
hidmod_df.to_pickle(dirInput+tagname+'_xavier_ugrhi_sp.pkl')
