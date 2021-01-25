import mat73
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# UGRHI SP
# tagname = '58220000'
# lat = -22.69
# lon = -44.98
# -------------------------
# tagname = '3D-001'
# lat = -22.68
# lon = -46.97
# -------------------------
# tagname = '4C-007'
# lat = -21.7
# lon = -47.82
# -------------------------
# tagname = '4B-015'
# lat = -20.63
# lon = -47.28
# -------------------------
# tagname = '5B-011'
lat = -20.91
lon = -48.09
# -------------------------
# tagname = '3D-002'
# lat = -22.70
# lon = -46.97
# -------------------------
##########


matfile = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/calibracaoBalagua/dados/TAMUXavier/weather2.mat'
prec_raw = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/calibracaoBalagua/dados/TAMUXavier/prec_raw.npz'

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/calibracaoBalagua/dados/TAMUXavier/subset/'

# annots = loadmat(matfile)
# print(annots)

# ds = xr.open_dataset(matfile)

# data_dict = mat73.loadmat(matfile)

data_dict = mat73.loadmat(matfile, use_attrdict=True)
# struct = data_dict['structure']  # assuming a structure was saved in the .mat
struct = data_dict['weather2']  # assuming a structure was saved in the .mat

coordestacoes = struct['coordinates']

dic_coordestacores = {'lat': coordestacoes[:, 0],'lon': coordestacoes[:, 1]}
df_coordestacores = pd.DataFrame(data=dic_coordestacores)

local = (lat, lon)

npos = len(df_coordestacores)
dis_estacoes = np.zeros(npos)

for kount in range(0, (npos)):
    geo_estacao = (df_coordestacores.lat.values[kount],
                   df_coordestacores.lon.values[kount])
    # print(geodesic(local, geo_estacao).km)
    dis_estacoes[kount] = geodesic(local, geo_estacao).km

posmin = np.asarray((dis_estacoes == np.nanmin(dis_estacoes))).nonzero()
posmin = posmin[0]

print('---Estacoes---')
print(posmin)
print(df_coordestacores.loc[posmin])
print(lat, lon)


estacao = posmin[0]  # 0-745 (755)
# tempo =   # 0-12418  (12419)

data_estacao = struct['data'][estacao][:]

# coord_estacao = struct['coordinates'][estacao]

ti = '1980-01-01'
tf = '2014-01-01'  # '2013-12-31'
datatempo = np.arange(ti, tf, dtype='datetime64[D]')
pdts = pd.DatetimeIndex(datatempo)

dic_dadosestacoes = {'Tmax': data_estacao[:, 0],
                     'Tmin': data_estacao[:, 1],
                     'Rs'  : data_estacao[:, 2],
                     'RH'  : data_estacao[:, 3],
                     'u2'  : data_estacao[:, 4],
                     'ETo' : data_estacao[:, 5]}

df_dadosestacoes = pd.DataFrame(data=dic_dadosestacoes, index=pdts)


#dados de precipitacao
npzfile = np.load(prec_raw)
var_prec = npzfile['var']
latlon = npzfile['latlon']
days = npzfile['days']


npos = len(latlon)
dis_pluv = np.zeros(npos)

for kount in range(0, (npos)):
    geo_pluv = (latlon[kount, 0],
                latlon[kount, 1])
    # print(geodesic(local, geo_estacao).km)
    dis_pluv[kount] = geodesic(local, geo_pluv).km

posmin = np.asarray((dis_pluv == np.nanmin(dis_pluv))).nonzero()
posmin = posmin[0]

print('---Pluviometros---')
print(posmin)
print(latlon[posmin[0]])
print(lat, lon)

# ti = '1980-01-01'
# tf = '2015-12-31'
datatempo_prec = days  # np.arange(ti, tf, dtype='datetime64[D]')
pdts_prec = pd.DatetimeIndex(datatempo_prec)

dic_pluviometros = {'precipitacao': var_prec[posmin[0], :]}
df_pluv = pd.DataFrame(data=dic_pluviometros, index=pdts_prec)

# df_prec = pd.DataFrame()
# head = struct['names']
