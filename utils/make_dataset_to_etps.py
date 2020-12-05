import xarray as xr
# import numpy as np
# import pickle
# import matplotlib.pyplot as plt
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

# Datasets
ds_era5land = xr.open_dataset(dirdata_era5+era5land)
ds_t2m_maxmin = xr.open_dataset(dirsubset+t2m_maxmin)
da_ra = xr.open_dataset(dirsubset+ra)

# Dataset to etps
ds_reanalises_to_etps = ds_era5land.assign(ds_t2m_maxmin.sel(
    time=slice(t_inicio, t_final)))

ds_reanalises_to_etps = ds_reanalises_to_etps.assign(da_ra.sel(
    time=slice(t_inicio, t_final)))

ds_reanalises_to_etps.t2m_max.attrs = {'units': 'K', 'long_name': '2 metre maximum temperature'}
ds_reanalises_to_etps.t2m_min.attrs = {'units': 'K', 'long_name': '2 metre minimum temperature'}

ds_reanalises_to_etps.to_netcdf(
    dirsubset + 'dataset_to_etps_reanalysis-era5-land-monthly-means.nc')

# ds_t2m_max = xr.concat([ds_t2m_max_1,
#                         ds_t2m_max_2,
#                         ds_t2m_max_3,
#                         ds_t2m_max_4], dim='time')

# ds_t2m_min = xr.concat([ds_t2m_min_1,
#                         ds_t2m_min_2,
#                         ds_t2m_min_3,
#                         ds_t2m_min_4], dim='time')

# ds_t2m_max_min = ds_t2m_max.rename({'t2m': 't2m_max'})
# ds_t2m_max_min = ds_t2m_max_min.assign(ds_t2m_min.rename({'t2m': 't2m_min'}))

# ds_t2m_max_min.to_netcdf(
#     dirsubset + 'madeLCB_reanalysis-era5-land_t2m_max_min_monthly_SE.nc')
