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
filesubset = tagname+'_era5_pet_penmont_subset.pkl'

ds = xr.open_dataset(dirdata+era5nc)

datatempo = ds.time
uwind = ds.u10.sel(longitude=lon, latitude=lat, method='nearest')
vwind = ds.v10.sel(longitude=lon, latitude=lat, method='nearest')
temp = ds.t2m.sel(longitude=lon, latitude=lat, method='nearest')
td = ds.d2m.sel(longitude=lon, latitude=lat, method='nearest')
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

# Conversoes & cte
temp = temp - 273.15  # [C]
td = td - 273.15  # [C]

str = (str/10.**6)  # [MJ m**-2 d**-1]
strd = (strd/10.**6)  # [MJ m**-2 d**-1]
ssr = (ssr/10.**6)  # [MJ m**-2 d**-1]
ssrd = (ssrd/10.**6)  # [MJ m**-2 d**-1]

sp = sp/10.**3  # [kPa]
rs = 0.23  # Albedo - 0.23 grass reference

# Cte psicrometrica
# psi = 0.063  # [kPa C**-1]
calorlatvap = 2.501 - (2.361*10.**(-3))*temp
psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]

# Calculos
es = 0.611*np.exp((17.27*temp)/(temp+237.3))

ea = 0.611*np.exp((17.27*td)/(td+237.3))

delta = (4098*es)/((temp+237.3)**2)

u2 = np.sqrt(uwind**2+vwind**2)

tm1 = temp
tm0 = np.roll(temp, 1)
G = 0.14*(tm1-tm0)

# Saldo de radiacao de onda curta (Rns):
#
# Considerado a radiacao direta e difusa para a superficie (S_sup_down)
# e o albedo
#
# Rns = (1. - rs) * ssrd
#
# Usando o saldo de onda curta na superficie (S_sup_down - S_sup_up)
# do ERA5 Land
Rns = ssr

# Saldo de radiacao de onda longa (Rnl):
# Aqui não entra o que a Terra absorve da
# emissão de onda longa da atmosfera (L_sup_down)
Rnl = (str)*(-1)
#
# Saldo de onda longa do ERA5 Land
# Rnl_totalERA5Land = strd - str

Rn = (Rns - Rnl)

# ETP Penman-Montaith

etp_penmanmontaith = (
    (0.408*delta*(Rn-G) + psi*(900./(temp+273.))*u2*(es-ea)) /
    (delta + psi*(1.+0.34*u2)))  # [mm d**-1]




pickle.dump(etp_penmanmontaith,
            open(dirsubset+filesubset, 'wb'))
