import evapotranspiracaopotencial_era5 as etp
import xarray as xr
import numpy as np
import pickle
import matplotlib.pyplot as plt
import geopandas as geopd
import pandas as pd
import rioxarray
from shapely.geometry import box, mapping
import rasterio
import pyproj
from affine import Affine
import salem

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
dirshape_bacia = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/' \
    'chuva_vazao_shape/shape_file/shape_file_limite/'

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

era5land = 'ERA5-Land_monthly_averaged_reanalysis.nc'
era5singlev = 'ERA5_monthly_averaged_reanalysis_on_single_levels.nc'
cru_tmn = 'cru_ts4.04.1901.2019.tmn.dat.nc'
cru_tmx = 'cru_ts4.04.1901.2019.tmx.dat.nc'

sh_pcj = 'pcj_basin.shp'

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

# geods_era5land = rioxarray.open_rasterio(dirdata+era5land,
#                                          masked=True, chunks=True)



# geods_era5land = ds_era5land.rio.set_spatial_dims(
#     x_dim='longitude', y_dim='latitude', inplace=True)
# geods_era5land = geods_era5land.rio.write_csr("epsg:4326", inplace=True)

# geodf_pcj = geopd.read_file(dirshape_bacia+sh_pcj, crs="epsg:4326")
geodf_pcj = geopd.read_file(dirshape_bacia+sh_pcj)


xlon2d, ylat2d = np.meshgrid(ds_era5land.longitude.values,
                             ds_era5land.latitude.values)


pts_lon = xlon2d.flatten()
pts_lat = ylat2d.flatten()

df_era5latlon = pd.DataFrame({'lon': pts_lon,
                              'lat': pts_lat})

geodf_era5latlon = geopd.GeoDataFrame(
    df_era5latlon,
    geometry=geopd.points_from_xy(df_era5latlon.lon,
                                  df_era5latlon.lat))

# crs = pyproj.Proj(init='epsg:4326')

# transformed = pyproj.transform(gda94, mgaz56, longitude, latitude)

transformed = geopd.points_from_xy(df_era5latlon.lon,
                                   df_era5latlon.lat)

# def transform_from_latlon(lat, lon):
#     lat = np.asarray(lat)
#     lon = np.asarray(lon)
#     trans = Affine.translation(lon[0], lat[0])
#     scale = Affine.scale(lon[1] - lon[0], lat[1] - lat[0])
#     return trans * scale


# transform_latloproj = transform_from_latlon(pts_lat,
#                                             pts_lon)


# clipped = geods_era5land.rio.clip(geodf_pcj.geometry.apply(mapping),
#                                   drop=False, invert=True)

# clipped = geods_era5land.rio.clip(geodf_pcj.geometry.apply(mapping),
#                                   geodf_pcj.crs, drop=False)

# polygon_mask = rasterio.features.geometry_mask(
#     geodf_pcj.loc[0, 'geometry'],
#     out_shape=(ds_era5land.dims['longitude'],
#                ds_era5land.dims['latitude']),
#     transform=transform_latloproj,
#     all_touched=False,
#     invert=True)


inters = geopd.overlay(geodf_era5latlon, geodf_pcj, how='intersection')

t2m = ds_era5land.t2m.isel(time=2)

t2_roi = t2m.salem.roi(shape=geodf_pcj)

