import evapotranspiracaopotencial_era5 as etp
import xarray as xr
import numpy as np
import pickle
import matplotlib.pyplot as plt
import geopandas as geopd
import pandas as pd
import rioxarray
# from shapely.geometry import box, mapping
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


# diretorios
dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA5/'
dirdata_cru = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/CRU/'
dirshape_bacia = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/' \
    'chuva_vazao_shape/shape_file/shape_file_limite/'
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# Arquivos
# era5land = 'ERA5-Land_monthly_averaged_reanalysis.nc'
era5land = 'reanalysis-era5-land-monthly-means.nc'

era5singlev = 'ERA5_monthly_averaged_reanalysis_on_single_levels.nc'
cru_tmn = 'cru_ts4.04.1901.2019.tmn.dat.nc'
cru_tmx = 'cru_ts4.04.1901.2019.tmx.dat.nc'

sh_pcj = 'pcj_basin.shp'

file_etps_df = tagname+'_era5_etp_baciahid.pkl'
file_reanalises_df = tagname+'_era5_reanalise_baciahid.pkl'

file_df_t2m_maxmin = tagname+'_t2m_max_min_from_era5land_houly.pkl'

# Datasets
ds_era5land = xr.open_dataset(dirdata+era5land)
ds_era5singlev = xr.open_dataset(dirdata+era5singlev)
ds_cru_tmn = xr.open_dataset(dirdata_cru+cru_tmn)
ds_cru_tmx = xr.open_dataset(dirdata_cru+cru_tmx)
###################################################################33

t_inicio = '1981-01-01'
t_final = '2019-12-30'

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

# t2m max min from era5land hourly

df_t2m_maxmin = pickle.load(open(dirsubset +
                                 file_df_t2m_maxmin, "rb"))

# Variaveis adicionais
pev_bacia = ds_era5land.pev.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})

tp_bacia = ds_era5land.tp.sel(
    time=slice(t_inicio, t_final)).where(
        ds_era5land.mask == 1, drop=True).mean({'longitude', 'latitude'})


# Calculos de etp
etp_penmanmonteith = etp.penmanmonteith(t2m_bacia,
                                        u10_bacia, v10_bacia,
                                        d2m_bacia,
                                        sp_bacia,
                                        ssr_bacia, str_bacia,
                                        slhf_bacia, sshf_bacia)

etp_hargreavessamani = etp.hargreavessamani(tisr_bacia.values,
                                            df_t2m_maxmin.tmax.values,
                                            df_t2m_maxmin.tmin.values,
                                            t2m_bacia.values)

etp_makkink = etp.makkink(t2m_bacia, sp_bacia, ssrd_bacia)

etp_priestleytaylor = etp.priestleytaylor(ssr_bacia, str_bacia, t2m_bacia,
                                          sp_bacia)

etp_penman = etp.penman(t2m_bacia, d2m_bacia, u10_bacia, v10_bacia)

# Faz dataframes de saida
xtime = t2m_bacia.time.values

# ETPs
dados_etps = {'penmanmonteith': etp_penmanmonteith.values,
              'hargreavessamani': etp_hargreavessamani,
              'makkink': etp_makkink.values,
              'priestleytaylor': etp_priestleytaylor.values,
              'penman': etp_penman.values}
etps_df = pd.DataFrame(dados_etps, index=xtime)
etps_df.to_pickle(dirsubset+file_etps_df)

# Reanalises
dados_re = {'u10': u10_bacia,
            'v10': v10_bacia,
            't2m': t2m_bacia,
            't2m_max': df_t2m_maxmin.tmax.values,
            't2m_min': df_t2m_maxmin.tmin.values,
            'tmax_cru': tmax_cru_bacia,
            'tmin_cru': tmin_cru_bacia,
            'd2m': d2m_bacia,
            'sp': sp_bacia,
            'str': str_bacia,
            'strd': strd_bacia,
            'ssr': ssr_bacia,
            'ssrd': ssrd_bacia,
            'slhf': slhf_bacia,
            'sshf': sshf_bacia,
            'tisr': tisr_bacia,
            'pev': pev_bacia,
            'tp': tp_bacia}
reanalises_df = pd.DataFrame(dados_re, index=xtime)
reanalises_df.to_pickle(dirsubset+file_reanalises_df)
