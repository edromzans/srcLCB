import evapotranspiracaopotencial_era5 as etp
import xarray as xr
import numpy as np
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
# tagname = '5B-011'
lat = -20.91
lon = -48.09
# -------------------------
# tagname = '3D-002'
# lat = -22.70
# lon = -46.97
# -------------------------
##########

# diretórios
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# Arquivos
dataset_to_etps = 'dataset_to_etps_reanalysis-era5-land-monthly-means.nc'

ds_to_etps = xr.open_dataset(dirsubset+dataset_to_etps)

#Data variables:
u10 = ds_to_etps.u10
v10 = ds_to_etps.v10
d2m = ds_to_etps.d2m
t2m = ds_to_etps.t2m
pev       = ds_to_etps.pev
slhf      = ds_to_etps.slhf
ssr       = ds_to_etps.ssr
str       = ds_to_etps.str
sp        = ds_to_etps.sp
sshf      = ds_to_etps.sshf
ssrd      = ds_to_etps.ssrd
strd      = ds_to_etps.strd
tp        = ds_to_etps.tp
t2m_max   = ds_to_etps.t2m_max
t2m_min   = ds_to_etps.t2m_min
ra        = ds_to_etps.ra
daylh = ds_to_etps.daylh
Ith = ds_to_etps.Ith
ath = ds_to_etps.ath
# ndaysmonth = ds_to_etps.ndaysmonth

etp_fao56reference = etp.fao56reference(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                                        ssr, str, slhf, sshf)

etp_asceewripenmanmonteith = etp.asceewripenmanmonteith(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                                                        ssr, str, slhf, sshf)

etp_penmanmonteith = etp.penmanmonteith(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                                        ssr, str, slhf, sshf)

etp_hargreavessamani = etp.hargreavessamani(ra, t2m, t2m_max, t2m_min)

etp_mhargreaves = etp.mhargreaves(ra, t2m, t2m_max, t2m_min, tp)

etp_priestleytaylor = etp.priestleytaylor(ssr, str, slhf, sshf, t2m, sp)

etp_thornthwaite = etp.thornthwaite(t2m, Ith, ath, daylh)

fao56 = etp_fao56reference.sel(longitude=lon, latitude=lat, method='nearest')
asceewri = etp_asceewripenmanmonteith.sel(longitude=lon, latitude=lat, method='nearest')
pm = etp_penmanmonteith.sel(longitude=lon, latitude=lat, method='nearest')
hs = etp_hargreavessamani.sel(longitude=lon, latitude=lat, method='nearest')
mh = etp_mhargreaves.sel(longitude=lon, latitude=lat, method='nearest')
pritay = etp_priestleytaylor.sel(longitude=lon, latitude=lat, method='nearest')
th = etp_thornthwaite.sel(longitude=lon, latitude=lat, method='nearest')

xtime = ds_to_etps.time
plt.plot(xtime, fao56, label='faoRef')
plt.plot(xtime, asceewri, label='asceewri')
plt.plot(xtime, pm, label='penmanmonteith')
plt.plot(xtime, hs, label='hargreavessamani')
plt.plot(xtime, mh, label='mhargreaves')
plt.plot(xtime, pritay, label='priestleytaylor')
plt.plot(xtime, th, label='th')
plt.legend()
plt.show()

# #.sel(longitude=lon, latitude=lat, method='nearest')
# etpplot = etp_fao56reference.isel(time=50)
# etpplot.plot()
# plt.show()
