import evapotranspiracaopotencial_era5land as etp
import xarray as xr
import numpy as np
import pickle
import matplotlib.pyplot as plt

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
tagname = '5B-011'
lat = -20.91
lon = -48.09
# -------------------------
##########

dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA-5_Land/'
era5nc = 'ERA5-Land_monthly_averaged_reanalysis.nc'

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

filesubset_penmont = tagname+'_era5_pet_penmont_subset.pkl'

filesubset_penmont = tagname+'_era5_pet_penmont_subset.pkl'


ds = xr.open_dataset(dirdata+era5nc)

datatempo = ds.time
u10 = ds.u10.sel(longitude=lon, latitude=lat, method='nearest')
v10 = ds.v10.sel(longitude=lon, latitude=lat, method='nearest')
t2m = ds.t2m.sel(longitude=lon, latitude=lat, method='nearest')
d2m = ds.d2m.sel(longitude=lon, latitude=lat, method='nearest')
sp = ds.sp.sel(longitude=lon, latitude=lat, method='nearest')

# Para saldo de radiacao (Rn)
# str  = L_sup_down - L_sup_up [J m**-2]
# strd = L_sup_down            [J m**-2]
# ssr  = S_sup_down - S_sup_up [J m**-2]
# ssrd = S_sup_down            [J m**-2]
str = ds.str.sel(longitude=lon, latitude=lat, method='nearest')
strd = ds.strd.sel(longitude=lon, latitude=lat, method='nearest')
ssr = ds.ssr.sel(longitude=lon, latitude=lat, method='nearest')
ssrd = ds.ssrd.sel(longitude=lon, latitude=lat, method='nearest')

etp_penmanmontaith = etp.penmanmontaith(t2m, u10, v10, d2m, sp, ssr, str)

pickle.dump(etp_penmanmontaith,
            open(dirsubset+filesubset_penmont, 'wb'))


k_coef = 0.4  # coeficiente mensal de consumo
p_coef = 0.5  # percentual de horas de sol no periodo
etp_blaneycriddle = etp.blaneycriddle(k_coef, p_coef, t2m)
