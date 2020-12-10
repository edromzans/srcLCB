import evapotranspiracaopotencial_era5 as etp
import xarray as xr
import numpy as np
# import pickle
import matplotlib.pyplot as plt
# import geopandas as geopd
# import pandas as pd
# import rioxarray
# from shapely.geometry import box, mapping
# import rasterio
# import pyproj
# from affine import Affine
# import salem
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature

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
##########

tagname = 'SE'

t_inicio = '1981-01-01'
t_final = '2020-08-01'

# diretorios
dirdata_era5 = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA5/'
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# Arquivos
th_indxs = 'dataset_thornthwaite_indxs.nc'
dataset_to_etps = 'dataset_to_etps_reanalysis-era5-land-monthly-means.nc'

# Datasets
ds_th_indx = xr.open_dataset(dirsubset+th_indxs)
ds_to_etps = xr.open_dataset(dirsubset+dataset_to_etps)

t2m = ds_to_etps.t2m.sel(longitude=lon, latitude=lat,
                         method='nearest')

Ith = ds_th_indx.Ith.sel(longitude=lon, latitude=lat,
                         method='nearest')

ath = ds_th_indx.ath.sel(longitude=lon, latitude=lat,
                         method='nearest')

daylh = ds_th_indx.daylh.sel(longitude=lon, latitude=lat,
                             method='nearest')

# ndaysmonth = ds_th_indx.ndaysmonth.sel(longitude=lon, latitude=lat,
#                                        method='nearest')


# tisr = ds_sl_era5land.tisr.sel(longitude=lon, latitude=lat, expver=1,
#                                method='nearest')
# tisr = tisr.sel(time=slice(t_inicio, t_final))

# tisr = tisr/10**6

# ra = da_ra.ra.sel(longitude=lon, latitude=lat, method='nearest')
# ra = ra.sel(time=slice(t_inicio, t_final))

# xtime = ra.time.values
plt.plot(Ith.time.values, Ith, label='I')
plt.legend()
plt.show()

plt.plot(ath.time.values, ath, label='a')
plt.legend()
plt.show()

plt.plot(daylh.time.values, daylh, label='daylh')
plt.legend()
plt.show()

etp_thornthwaite = etp.thornthwaite(t2m,
                                    Ith,
                                    ath,
                                    daylh)

plt.plot(etp_thornthwaite.time.values,
         etp_thornthwaite, label='etp_thornthwaite')
plt.legend()
plt.show()


# canual_tisr = tisr.groupby(tisr.time.dt.month).mean()
# canual_ra = ra.groupby(ra.time.dt.month).mean()

# plt.plot(canual_tisr.month.values, canual_tisr, label='tisr')
# # plt.plot(canual_ra.month.values, np.roll(canual_ra,-1), label='Ra')
# plt.plot(canual_ra.month.values, canual_ra, label='Ra')
# plt.legend()

# plt.show()
