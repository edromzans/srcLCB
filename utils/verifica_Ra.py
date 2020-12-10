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
era5land = 'reanalysis-era5-land-monthly-means.nc'
t2m_maxmin = 'madeLCB_reanalysis-era5-land_t2m_max_min_monthly_SE.nc'
ra = 'dataarray_extraterrestrial_rad.nc'
sl_era5land = 'ERA5_monthly_averaged_reanalysis_on_single_levels.nc'

# Datasets
# ds_era5land = xr.open_dataset(dirdata_era5+era5land)
# ds_t2m_maxmin = xr.open_dataset(dirsubset+t2m_maxmin)
da_ra = xr.open_dataset(dirsubset+ra)
ds_sl_era5land = xr.open_dataset(dirdata_era5+sl_era5land)


tisr = ds_sl_era5land.tisr.sel(longitude=lon, latitude=lat, expver=1,
                               method='nearest')
tisr = tisr.sel(time=slice(t_inicio, t_final))

tisr = tisr/10**6


ra = da_ra.ra.sel(longitude=lon, latitude=lat, method='nearest')
ra = ra.sel(time=slice(t_inicio, t_final))

xtime = ra.time.values
plt.plot(tisr.time.values, tisr, label='tisr')
plt.plot(ra.time.values, ra, label='Ra')
plt.legend()

plt.show()

canual_tisr = tisr.groupby(tisr.time.dt.month).mean()
canual_ra = ra.groupby(ra.time.dt.month).mean()

plt.plot(canual_tisr.month.values, canual_tisr, label='tisr')
# plt.plot(canual_ra.month.values, np.roll(canual_ra,-1), label='Ra')
plt.plot(canual_ra.month.values, canual_ra, label='Ra')
plt.legend()

plt.show()
