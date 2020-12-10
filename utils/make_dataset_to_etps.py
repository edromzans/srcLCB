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
th_indxs = 'dataset_thornthwaite_indxs.nc'

# Datasets
ds_era5land = xr.open_dataset(dirdata_era5+era5land)
ds_t2m_maxmin = xr.open_dataset(dirsubset+t2m_maxmin)
da_ra = xr.open_dataarray(dirsubset+ra)
ds_th_indx = xr.open_dataset(dirsubset+th_indxs)

# Dataset to etps
ds_reanalises_to_etps = ds_era5land.assign(ds_t2m_maxmin.sel(
    time=slice(t_inicio, t_final)))

ds_reanalises_to_etps = ds_reanalises_to_etps.assign(ra=da_ra.sel(
    time=slice(t_inicio, t_final)))

ds_reanalises_to_etps = ds_reanalises_to_etps.assign(ds_th_indx.sel(
    time=slice(t_inicio, t_final)))

ds_reanalises_to_etps.t2m_max.attrs = {'units': 'K',
                                       'long_name':
                                       '2 metre maximum temperature'}
ds_reanalises_to_etps.t2m_min.attrs = {'units': 'K',
                                       'long_name':
                                       '2 metre minimum temperature'}

ds_reanalises_to_etps = ds_reanalises_to_etps.drop_vars({'fal',
                                                         'lai_hv',
                                                         'lai_lv',
                                                         'skt',
                                                         'e'})
ds_reanalises_to_etps.to_netcdf(
    dirsubset + 'dataset_to_etps_reanalysis-era5-land-monthly-means.nc')
