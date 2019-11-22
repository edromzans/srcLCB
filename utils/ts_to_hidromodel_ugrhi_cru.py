import pandas as pd
import numpy as np
import netCDF4 as nc4


dirInput = '/dados/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/ugrhi_sp/'

# UGRHI SP
tagname = '58220000'
lat = -22.69
lon = -44.98
##########

# Leitura dos dados da UGRHI selecionada
aguadados_csv = tagname+'_ugrhi_sp.csv'
aguadf = pd.read_csv(dirInput+aguadados_csv, header=0, parse_dates=[0], names=[
    'datatempo', 'p', 'q', 'escobas'])
aguadf.index = aguadf['datatempo']

# Dados do Climatic Research Unit (CRU)
ncf_cru_pet = '/dados/CRU_TS/cru_ts4.03.1901.2018.pet.dat.nc'
cru = nc4.Dataset(ncf_cru_pet, 'r')

xlon = cru.variables['lon'][:]
ylat = cru.variables['lat'][:]
tp = cru.variables['time'][:]
pet = cru.variables['pet'][:]

xlon = np.ma.getdata(xlon)
ylat = np.ma.getdata(ylat)

datatempo_cru = np.datetime64('1900-01-01', 'D') + np.uint(np.ma.getdata(tp))

nx_cru = len(datatempo_cru)

dislat = np.abs(ylat - lat)
dislon = np.abs(xlon - lon)

poslatgr = np.where(dislat == np.min(dislat))
print(lat, ylat[poslatgr])

poslongr = np.where(dislon == np.min(dislon))
print(lon, xlon[poslongr])

ts_pet = np.ma.getdata(pet[:, poslatgr, poslongr]).reshape(nx_cru)
pet_df = pd.DataFrame(data={'pet': ts_pet}, index=datatempo_cru)

tstart = aguadf.index[0]
tstop = (aguadf.index[-1] + np.timedelta64(1, 'M'))
xtime = np.arange(tstart.strftime('%Y-%m'),
                  tstop.strftime('%Y-%m'),
                  dtype='datetime64[M]')
tsdf = pd.DatetimeIndex(xtime)
nx_ts = len(tsdf)

# conta numero de dias em cada mes
xtimeD = np.arange(tstart.strftime('%Y-%m'),
                   tstop.strftime('%Y-%m'),
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
    poscru = np.where((pet_df.index.year == tsdf.year[tk]) &
                      (pet_df.index.month == tsdf.month[tk]))
    poscru = poscru[0]

    posagua = np.where((aguadf.index.year == tsdf.year[tk]) &
                       (aguadf.index.month == tsdf.month[tk]))
    posagua = posagua[0]

    # print(poscru.size, posagua.size)
    # if (poscru.size < 1) or (posagua.size < 1):
    #     print('Falta dados: '+pdts[tk].strftime('%Y %m %d %H %M %S'))
    #     break

    if (poscru.size == 1) and (posagua.size == 1):
        etp_ts[tk] = pet_df.pet[poscru] * ndias[tk]  # mm/mes
        p_ts[tk] = aguadf.p[posagua]
        q_ts[tk] = aguadf.q[posagua]

dados = {'etp': etp_ts, 'p': p_ts, 'q': q_ts}
hidmod_df = pd.DataFrame(data=dados, index=xtime)

#Salva ts to hidromodel binario
hidmod_df.to_pickle(dirInput+tagname+'_ugrhi_sp.pkl')
