from scipy.io import loadmat
import xarray as xr
import mat73
import pandas as pd
import h5py
import numpy as np

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


estacao = 500  # 0-745 (755)
# tempo =   # 0-12418  (12419)

data_estacao = struct['data'][estacao][:]

coord_estacao = struct['coordinates'][estacao]

f_data_estacao = open(dirsubset+'dadosestacao_xavier.txt', 'w')

f_estacao_latlonalt = open(dirsubset+'coord_estacao_xavier.txt', 'w')

f_estacao_latlonalt.write('latitude      longitude      altitude\n')
f_estacao_latlonalt.write('{:11.5f} {:11.5f} {:11.5f}\n'.format(coord_estacao[0],
                                                                coord_estacao[1],
                                                                coord_estacao[2]))

ti = '1980-01-01'
tf = '2013-12-31'
datatempo = np.arange(ti, tf, dtype='datetime64[D]')
pdts = pd.DatetimeIndex(datatempo)

#dados de precipitacao
npzfile = np.load(prec_raw)
var_prec = npzfile['var']
latlon = npzfile['latlon']
days = npzfile['days']

# ti = '1980-01-01'
# tf = '2015-12-31'
datatempo_prec = days  # np.arange(ti, tf, dtype='datetime64[D]')
pdts_prec = pd.DatetimeIndex(datatempo_prec)




head = struct['names']

f_data_estacao.write('{:>11} {:>11} {:>11} {:>11} {:>11} {:>11} {:>11}\n'.format(
    'tempo',
    head[0],
    head[1],
    head[2],
    head[3],
    head[4],
    head[5],))

for kline in range(0, 12418):
    strdatatempo = pdts[kline].strftime('%Y-%m-%d')
#    print(strdatatempo)
    f_data_estacao.write(
        '{:>11} {:11.1f} {:11.1f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} \n'.format(
            strdatatempo,
            data_estacao[kline][0],
            data_estacao[kline][1],
            data_estacao[kline][2],
            data_estacao[kline][3],
            data_estacao[kline][4],
            data_estacao[kline][5]))


# struct['data'][745][:]
# até 12419

# struct[0].var1 == struct[0]['var1']  # it's the same!

# df = pd.DataFrame(data=data_dict)

# with h5py.File(matfile, 'r') as file:
#     print(list(file.keys()))

#     a = list(file['weather2'])
#     b = list(file['#refs#'])

#f = h5py.File(matfile, 'r')
