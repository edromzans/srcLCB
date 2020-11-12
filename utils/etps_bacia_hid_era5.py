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
import cartopy.crs as ccrs
import cartopy.feature as cfeature

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
# lat = -20.91
# lon = -48.09
# -------------------------
# tagname = '3D-002'
lat = -22.70
lon = -46.97
# -------------------------
##########

tagname = 'pcj'

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

file_etps_df = tagname+'_era5_etp_baciahid.pkl'

ds_era5land = xr.open_dataset(dirdata+era5land)
ds_era5singlev = xr.open_dataset(dirdata+era5singlev)
ds_cru_tmn = xr.open_dataset(dirdata_cru+cru_tmn)
ds_cru_tmx = xr.open_dataset(dirdata_cru+cru_tmx)

t_inicio = '1981-01-01'
t_final = '2019-12-30'

# #datatempo = ds_era5land.time
# u10 = ds_era5land.u10.sel(longitude=lon, latitude=lat, method='nearest')
# u10 = u10.sel(time=slice(t_inicio, t_final))

# v10 = ds_era5land.v10.sel(longitude=lon, latitude=lat, method='nearest')
# v10 = v10.sel(time=slice(t_inicio, t_final))

# t2m = ds_era5land.t2m.sel(longitude=lon, latitude=lat, method='nearest')
# t2m = t2m.sel(time=slice(t_inicio, t_final))

# d2m = ds_era5land.d2m.sel(longitude=lon, latitude=lat, method='nearest')
# d2m = d2m.sel(time=slice(t_inicio, t_final))

# sp = ds_era5land.sp.sel(longitude=lon, latitude=lat, method='nearest')
# sp = sp.sel(time=slice(t_inicio, t_final))

# # Para saldo de radiacao (Rn)
# # str  = L_sup_down - L_sup_up [J m**-2]
# # strd = L_sup_down            [J m**-2]
# # ssr  = S_sup_down - S_sup_up [J m**-2]
# # ssrd = S_sup_down            [J m**-2]
# str = ds_era5land.str.sel(longitude=lon, latitude=lat, method='nearest')
# str = str.sel(time=slice(t_inicio, t_final))

# strd = ds_era5land.strd.sel(longitude=lon, latitude=lat, method='nearest')
# strd = strd.sel(time=slice(t_inicio, t_final))

# ssr = ds_era5land.ssr.sel(longitude=lon, latitude=lat, method='nearest')
# ssr = ssr.sel(time=slice(t_inicio, t_final))

# ssrd = ds_era5land.ssrd.sel(longitude=lon, latitude=lat, method='nearest')
# ssrd = ssrd.sel(time=slice(t_inicio, t_final))

# # LE
# slhf = ds_era5land.slhf.sel(longitude=lon, latitude=lat, method='nearest')
# slhf = slhf.sel(time=slice(t_inicio, t_final))

# # H
# sshf = ds_era5land.sshf.sel(longitude=lon, latitude=lat, method='nearest')
# sshf = sshf.sel(time=slice(t_inicio, t_final))

# ERA5_monthly_averaged_reanalysis_on_single_levels
# tisr = ds_era5singlev.tisr.sel(longitude=lon, latitude=lat, expver=1,
#                                method='nearest')
# tisr = tisr.sel(time=slice(t_inicio, t_final))

# # CRU tmn tmx
# tmin_cru = ds_cru_tmn.tmn.sel(lon=lon, lat=lat, method='nearest')
# tmin_cru = tmin_cru.sel(time=slice(t_inicio, t_final))
# tmax_cru = ds_cru_tmx.tmx.sel(lon=lon, lat=lat, method='nearest')
# tmax_cru = tmax_cru.sel(time=slice(t_inicio, t_final))

# Shapefile
# geodf_pcj = geopd.read_file(dirshape_bacia+sh_pcj, crs="epsg:4326")
# geodf_pcj = geopd.read_file(dirshape_bacia+sh_pcj)
# geodf_pcj_bf = salem.read_shapefile(dirshape_bacia+sh_pcj)
geodf_pcj = salem.read_shapefile(dirshape_bacia+sh_pcj)

# GeoDataFrame intersection---------------------------------
# xlon2d, ylat2d = np.meshgrid(ds_era5land.longitude.values,
#                              ds_era5land.latitude.values)
# pts_lon = xlon2d.flatten()
# pts_lat = ylat2d.flatten()
# df_era5latlon = pd.DataFrame({'lon': pts_lon,
#                               'lat': pts_lat})
# geodf_era5latlon = geopd.GeoDataFrame(
#     df_era5latlon,
#     geometry=geopd.points_from_xy(df_era5latlon.lon,
#                                   df_era5latlon.lat))
# inters = geopd.overlay(geodf_era5latlon, geodf_pcj, how='intersection')

# Mask com shapefile
ds_era5land_to_mask = ds_era5land.t2m.isel(time=2)
era5land_maskroi_geo = ds_era5land_to_mask.salem.roi(shape=geodf_pcj)
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
# -------------------------------------------------
era5land_maskroi = (~np.isnan(era5land_maskroi_geo.values))*1
ds_era5land.coords['mask'] = (('latitude', 'longitude'), era5land_maskroi)

# variables media espacial bacia
u10_bacia = ds_era5land.u10.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

v10_bacia = ds_era5land.v10.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

t2m_bacia = ds_era5land.t2m.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

d2m_bacia = ds_era5land.d2m.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

sp_bacia = ds_era5land.sp.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

# Para saldo de radiacao (Rn)
# str  = L_sup_down - L_sup_up [J m**-2]
# strd = L_sup_down            [J m**-2]
# ssr  = S_sup_down - S_sup_up [J m**-2]
# ssrd = S_sup_down            [J m**-2]
str_bacia = ds_era5land.str.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

strd_bacia = ds_era5land.strd.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

ssr_bacia = ds_era5land.ssr.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

ssrd_bacia = ds_era5land.ssrd.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

# LE
slhf_bacia = ds_era5land.slhf.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

# H
sshf_bacia = ds_era5land.sshf.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

# geodf_pcj_bf['geometry'] = geodf_pcj_bf.geometry.buffer(0.2)

# ERA5_monthly_averaged_reanalysis_on_single_levels
# Mask com shapefile
era5singlev_to_mask = ds_era5singlev.tisr.isel(time=2, expver=0)
era5singlev_maskroi_geo = era5singlev_to_mask.salem.roi(shape=geodf_pcj)
# # Mapa de verificacao-----------------------------
# fig, ax = plt.subplots()
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.set_aspect('equal')
# era5singlev_maskroi_geo.plot(ax=ax)
# geodf_pcj.plot(ax=ax, edgecolor="black", facecolor='none')
# ax.add_feature(cfeature.BORDERS)
# ax.add_feature(cfeature.STATES)
# ax.coastlines()
# ax.gridlines(draw_labels=True)
# plt.show()
# # -------------------------------------------------
era5singlev_maskroi = (~np.isnan(era5singlev_maskroi_geo.values))*1
ds_era5singlev.coords['mask'] = (('latitude', 'longitude'),
                                 era5singlev_maskroi)

tisr_bacia = ds_era5singlev.tisr.sel(
    time=slice(t_inicio, t_final), expver=1).where(
        ds_era5singlev.mask == 1, drop=True).mean({'longitude', 'latitude'})

# CRU tmn tmx
# Mask com shapefile
cru_to_mask = ds_cru_tmn.tmn.isel(time=2)
cru_maskroi_geo = cru_to_mask.salem.roi(shape=geodf_pcj)
cru_maskroi = (~np.isnan(cru_maskroi_geo.values))*1
ds_cru_tmn.coords['mask'] = (('lat', 'lon'),
                             cru_maskroi)
ds_cru_tmx.coords['mask'] = (('lat', 'lon'),
                             cru_maskroi)

tmin_cru_bacia = ds_cru_tmn.tmn.sel(
    time=slice(t_inicio, t_final)).where(
        ds_cru_tmn.mask == 1, drop=True).mean({'lon', 'lat'})

tmax_cru_bacia = ds_cru_tmx.tmx.sel(
    time=slice(t_inicio, t_final)).where(
        ds_cru_tmx.mask == 1, drop=True).mean({'lon', 'lat'})

# Calculos de etp
etp_penmanmontaith = etp.penmanmontaith(t2m_bacia,
                                        u10_bacia, v10_bacia,
                                        d2m_bacia,
                                        sp_bacia,
                                        ssr_bacia, str_bacia,
                                        slhf_bacia, sshf_bacia)

etp_hargreavessamani = etp.hargreavessamani(tisr_bacia.values,
                                            tmax_cru_bacia.values,
                                            tmin_cru_bacia.values,
                                            t2m_bacia.values)

etp_makkink = etp.makkink(t2m_bacia, sp_bacia, ssrd_bacia)

etp_priestleytaylor = etp.priestleytaylor(ssr_bacia, str_bacia, t2m_bacia,
                                          sp_bacia)

etp_penman = etp.penman(t2m_bacia, d2m_bacia, u10_bacia, v10_bacia)

# ETPs dataframe
xtime = t2m_bacia.time.values
dados_etps = {'penmanmontaith': etp_penmanmontaith.values,
              'hargreavessamani': etp_hargreavessamani,
              'makkink': etp_makkink.values,
              'priestleytaylor': etp_priestleytaylor.values,
              'penman': etp_penman.values}

etps_df = pd.DataFrame(dados_etps, index=xtime)

# Salva ts to hidromodel binario
etps_df.to_pickle(dirsubset+file_etps_df)

# pickle.dump((etp_penmanmontaith,
#              etp_hargreavessamani,
#              etp_makkink,
#              etp_priestleytaylor,
#              etp_penman),
#             open(dirsubset+filesubset, 'wb'))
