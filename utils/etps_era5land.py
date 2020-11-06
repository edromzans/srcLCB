import evapotranspiracaopotencial_era5 as etp
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
    'calibracaoBalagua/dados/ECMWF_ERA5/'
dirdata_cru = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/CRU/'

era5land = 'ERA5-Land_monthly_averaged_reanalysis.nc'
era5singlev = 'ERA5_monthly_averaged_reanalysis_on_single_levels.nc'
cru_tmn = 'cru_ts4.04.1901.2019.tmn.dat.nc'
cru_tmx = 'cru_ts4.04.1901.2019.tmx.dat.nc'


dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# filesubset_penmont = tagname+'_era5_pet_penmont_subset.pkl'
# filesubset_penmont = tagname+'_era5_pet_penmont_subset.pkl'
filesubset = tagname+'_era5_etp_subset.pkl'

ds_era5land = xr.open_dataset(dirdata+era5land)
ds_era5singlev = xr.open_dataset(dirdata+era5singlev)
ds_cru_tmn = xr.open_dataset(dirdata_cru+cru_tmn)
ds_cru_tmx = xr.open_dataset(dirdata_cru+cru_tmx)

t_inicio = '1981-01-01'
t_final = '2019-12-30'

#datatempo = ds_era5land.time
u10 = ds_era5land.u10.sel(longitude=lon, latitude=lat, method='nearest')
u10 = u10.sel(time=slice(t_inicio, t_final))

v10 = ds_era5land.v10.sel(longitude=lon, latitude=lat, method='nearest')
v10 = v10.sel(time=slice(t_inicio, t_final))

t2m = ds_era5land.t2m.sel(longitude=lon, latitude=lat, method='nearest')
t2m = t2m.sel(time=slice(t_inicio, t_final))

d2m = ds_era5land.d2m.sel(longitude=lon, latitude=lat, method='nearest')
d2m = d2m.sel(time=slice(t_inicio, t_final))

sp = ds_era5land.sp.sel(longitude=lon, latitude=lat, method='nearest')
sp = sp.sel(time=slice(t_inicio, t_final))

# Para saldo de radiacao (Rn)
# str  = L_sup_down - L_sup_up [J m**-2]
# strd = L_sup_down            [J m**-2]
# ssr  = S_sup_down - S_sup_up [J m**-2]
# ssrd = S_sup_down            [J m**-2]
str = ds_era5land.str.sel(longitude=lon, latitude=lat, method='nearest')
str = str.sel(time=slice(t_inicio, t_final))

strd = ds_era5land.strd.sel(longitude=lon, latitude=lat, method='nearest')
strd = strd.sel(time=slice(t_inicio, t_final))

ssr = ds_era5land.ssr.sel(longitude=lon, latitude=lat, method='nearest')
ssr = ssr.sel(time=slice(t_inicio, t_final))

ssrd = ds_era5land.ssrd.sel(longitude=lon, latitude=lat, method='nearest')
ssrd = ssrd.sel(time=slice(t_inicio, t_final))

# LE
slhf = ds_era5land.slhf.sel(longitude=lon, latitude=lat, method='nearest')
slhf = slhf.sel(time=slice(t_inicio, t_final))

# H
sshf = ds_era5land.sshf.sel(longitude=lon, latitude=lat, method='nearest')
sshf = sshf.sel(time=slice(t_inicio, t_final))

# ERA5_monthly_averaged_reanalysis_on_single_levels
tisr = ds_era5singlev.tisr.sel(longitude=lon, latitude=lat, expver=1,
                               method='nearest')
tisr = tisr.sel(time=slice(t_inicio, t_final))

# CRU tmn tmx
tmin_cru = ds_cru_tmn.tmn.sel(lon=lon, lat=lat, method='nearest')
tmin_cru = tmin_cru.sel(time=slice(t_inicio, t_final))
tmax_cru = ds_cru_tmx.tmx.sel(lon=lon, lat=lat, method='nearest')
tmax_cru = tmax_cru.sel(time=slice(t_inicio, t_final))

# Calculos de etp
etp_penmanmontaith = etp.penmanmontaith(t2m, u10, v10, d2m, sp,
                                        ssr, str, slhf, sshf)

# k_coef = 0.4  # coeficiente mensal de consumo
# p_coef = 0.5  # percentual de horas de sol no periodo
# etp_blaneycriddle = etp.blaneycriddle(k_coef, p_coef, t2m)

# tmax = 28.
# tmin = 23.
etp_hargreavessamani = etp.hargreavessamani(tisr, tmax_cru.values,
                                            tmin_cru.values, t2m)

etp_makkink = etp.makkink(t2m, sp, ssrd)

etp_priestleytaylor = etp.priestleytaylor(ssr.values, str.values, t2m.values,
                                          sp.values)
# etp_rohwer = etp.rohwer(t2m, d2m, u10, v10)

etp_penman = etp.penman(t2m, d2m, u10, v10)

pickle.dump((etp_penmanmontaith,
             etp_hargreavessamani,
             etp_makkink,
             etp_priestleytaylor,
             etp_penman),
            open(dirsubset+filesubset, 'wb'))
