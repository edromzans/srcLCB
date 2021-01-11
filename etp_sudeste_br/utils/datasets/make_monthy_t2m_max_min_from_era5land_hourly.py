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

# tagname = 'SE'

# t_inicio = '1981-01-01'
# t_final = '2019-12-30'

# diretorios
dirdata_era5 = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA5/'
# dirshape_bacia = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
#     'calibracaoBalagua/dados/ugrhi/' \
#     'chuva_vazao_shape/shape_file/shape_file_limite/'
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# Arquivos
t2m_19811990 = 'reanalysis-era5-land_t2m_hourly_SE_1981-1990.nc'
t2m_19912000 = 'reanalysis-era5-land_t2m_hourly_SE_1991-2000.nc'
t2m_20012010 = 'reanalysis-era5-land_t2m_hourly_SE_2001-2010.nc'
t2m_20112020 = 'reanalysis-era5-land_t2m_hourly_SE_2011-2020.nc'

# sh_pcj = 'pcj_basin.shp'


# file_df_t2m_maxmin = tagname+'_t2m_max_min_from_era5land_houly.pkl'
# Datasets
ds_t2m_1 = xr.open_dataset(dirdata_era5+t2m_19811990)
ds_t2m_2 = xr.open_dataset(dirdata_era5+t2m_19912000)
ds_t2m_3 = xr.open_dataset(dirdata_era5+t2m_20012010)
ds_t2m_4 = xr.open_dataset(dirdata_era5+t2m_20112020)

# ds_t2m_max_1 = ds_t2m_1.resample(time='M').max() - 273.15
# ds_t2m_min_1 = ds_t2m_1.resample(time='M').min() - 273.15
# ds_t2m_max_1.t2m.isel(time=50).plot()
# plt.show()
# ds_t2m_min_1.t2m.isel(time=50).plot()
# plt.show()

ds_t2m_max_1 = ds_t2m_1.resample(time='MS').max()
ds_t2m_min_1 = ds_t2m_1.resample(time='MS').min()

ds_t2m_max_2 = ds_t2m_2.resample(time='MS').max()
ds_t2m_min_2 = ds_t2m_2.resample(time='MS').min()

ds_t2m_max_3 = ds_t2m_3.resample(time='MS').max()
ds_t2m_min_3 = ds_t2m_3.resample(time='MS').min()

ds_t2m_max_4 = ds_t2m_4.resample(time='MS').max()
ds_t2m_min_4 = ds_t2m_4.resample(time='MS').min()

ds_t2m_max = xr.concat([ds_t2m_max_1,
                        ds_t2m_max_2,
                        ds_t2m_max_3,
                        ds_t2m_max_4], dim='time')

ds_t2m_min = xr.concat([ds_t2m_min_1,
                        ds_t2m_min_2,
                        ds_t2m_min_3,
                        ds_t2m_min_4], dim='time')

ds_t2m_max_min = ds_t2m_max.rename({'t2m': 't2m_max'})
ds_t2m_max_min = ds_t2m_max_min.assign(ds_t2m_min.rename({'t2m': 't2m_min'}))

ds_t2m_max_min.to_netcdf(
    dirsubset + 'madeLCB_reanalysis-era5-land_t2m_max_min_monthly_SE.nc')
