import xarray as xr
import numpy as np
import pickle
import matplotlib.pyplot as plt
import geopandas as geopd
import pandas as pd
# import rioxarray
# from shapely.geometry import box, mapping
# import rasterio
# import pyproj
# from affine import Affine
import salem
import cartopy.crs as ccrs
import cartopy.feature as cfeature

tagname = 'pcj'

t_inicio = '1981-01-01'
t_final = '2019-12-30'

# diretorios
dirdata_era5 = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA5/'
dirshape_bacia = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/' \
    'chuva_vazao_shape/shape_file/shape_file_limite/'
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# Arquivos
t2m_19811990 = 'reanalysis-era5-land_t2m_hourly_1981-1990.nc'
t2m_19912000 = 'reanalysis-era5-land_t2m_hourly_1991-2000.nc'
t2m_20012010 = 'reanalysis-era5-land_t2m_hourly_2001-2010.nc'
t2m_20112020 = 'reanalysis-era5-land_t2m_hourly_2011-2020.nc'

sh_pcj = 'pcj_basin.shp'

file_df_t2m_maxmin = tagname+'_t2m_max_min_from_era5land_houly.pkl'

# Datasets
ds_t2m_1 = xr.open_dataset(dirdata_era5+t2m_19811990)
ds_t2m_2 = xr.open_dataset(dirdata_era5+t2m_19912000)
ds_t2m_3 = xr.open_dataset(dirdata_era5+t2m_20012010)
ds_t2m_4 = xr.open_dataset(dirdata_era5+t2m_20112020)

geodf_pcj = salem.read_shapefile(dirshape_bacia+sh_pcj)
era5land_to_mask = ds_t2m_1.t2m.isel(time=2)
era5land_maskroi_geo = era5land_to_mask.salem.roi(shape=geodf_pcj)
era5land_maskroi = (~np.isnan(era5land_maskroi_geo.values))*1
# # Mapa de verificacao-----------------------------
# fig, ax = plt.subplots()
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.set_aspect('equal')
# era5land_maskroi_geo.plot(ax=ax)
# geodf_pcj.plot(ax=ax, edgecolor="black", facecolor='none')
# ax.add_feature(cfeature.BORDERS)
# ax.add_feature(cfeature.STATES)
# ax.coastlines()
# ax.gridlines(draw_labels=True)
# # ax.scatter(lon, lat, marker='o')
# plt.show()
# # -------------------------------------------------

ds_t2m = xr.concat([ds_t2m_1, ds_t2m_2, ds_t2m_3, ds_t2m_4], dim='time')

ds_t2m.coords['mask'] = (('latitude', 'longitude'),
                         era5land_maskroi)

ds_t2m_bacia_hourly = ds_t2m.t2m.sel(
    time=slice(t_inicio, t_final)).where(
        ds_t2m.mask == 1, drop=True).mean({'longitude', 'latitude'})

tmax = ds_t2m_bacia_hourly.resample(time='M').max()
tmin = ds_t2m_bacia_hourly.resample(time='M').min()
tmed = ds_t2m_bacia_hourly.resample(time='M').mean()

xtime = tmed.time.values
# plt.plot(xtime, tmax.values, label='tmax')
# plt.plot(xtime, tmin.values, label='tmin')
# plt.plot(xtime, tmed.values, label='tmed')
# plt.legend()
# plt.show()

dados_t2m = {'tmax': tmax,
             'tmin': tmin,
             'tmed': tmed}

df_t2m_maxmin = pd.DataFrame(dados_t2m, index=xtime)
df_t2m_maxmin.to_pickle(dirsubset+file_df_t2m_maxmin)
