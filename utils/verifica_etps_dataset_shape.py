import evapotranspiracaopotencial_era5 as etp
import xarray as xr
import numpy as np
import salem
import matplotlib.pyplot as plt
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
# lat = -20.91  # Selecao inicial de verificacao (Rio Pardo)
# lon = -48.09
# -------------------------
# tagname = '3D-002'
lat = -22.70
lon = -46.97
# -------------------------
##########

# diretórios
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

dirshape_bacia = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/' \
    'chuva_vazao_shape/shape_file/shape_file_limite/'

dirplot = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/plots/analise_t2m/'

# Arquivos
dataset_to_etps = 'dataset_to_etps_reanalysis-era5-land-monthly-means.nc'
sh_pcj = 'pcj_basin.shp'

ds_to_etps = xr.open_dataset(dirsubset+dataset_to_etps)

geodf_shapefile = salem.read_shapefile(dirshape_bacia+sh_pcj)
ds_revar_to_mask = ds_to_etps.t2m.isel(time=2)
ds_revar_maskroi_geo = ds_revar_to_mask.salem.roi(shape=geodf_shapefile)
revar_maskroi = (~np.isnan(ds_revar_maskroi_geo.values))*1
ds_to_etps.coords['mask'] = (('latitude', 'longitude'), revar_maskroi)

# # variables media espacial bacia
ds_to_etps_sh = ds_to_etps[['t2m', 't2m_max', 't2m_min']].where(
    ds_to_etps.mask == 1, drop=True)

# varplot = ds_to_etps_sh.t2m_min.mean({'time'}) - 273.15

varplot = (ds_to_etps_sh.t2m_max.mean({'time'}) - 273.15) - (ds_to_etps_sh.t2m_min.mean({'time'}) - 273.15)



# Mapa de verificacao-----------------------------
fig, ax = plt.subplots()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_aspect('equal')
varplot.plot(ax=ax, cbar_kwargs=dict(orientation='horizontal',
                                     pad=0.15,
                                     shrink=0.7,
                                     label='t2m_max - t2m_min ($^{\circ}$C)'))
geodf_shapefile.plot(ax=ax, edgecolor="black", facecolor='none')
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.STATES)
ax.coastlines()
ax.gridlines(draw_labels=True)
ax.scatter(lon, lat, marker='o')
#plt.colorbar(fraction=0.5)
plt.savefig(dirplot+'t2m_amplitude_pcj.png',
            dpi=144, bbox_inches='tight')

#plt.show()
# -------------------------------------------------








# geodf_shapefile = salem.read_shapefile(dirshape_bacia+sh_pcj)
# ds_revar_to_mask = ds_reanalise[var].sel(time=t_inicio)
# ds_revar_maskroi_geo = ds_revar_to_mask.salem.roi(shape=geodf_shapefile)
# revar_maskroi = (~np.isnan(ds_revar_maskroi_geo.values))*1
# ds_reanalise.coords['mask'] = (('latitude', 'longitude'), revar_maskroi)

# # variables media espacial bacia
# revar = ds_reanalise[var].sel(
#     time=slice(t_inicio, t_final)).where(
#         ds_reanalise.mask == 1, drop=True)


# # Data variables:
# u10 = ds_to_etps.u10
# v10 = ds_to_etps.v10
# d2m = ds_to_etps.d2m
# t2m = ds_to_etps.t2m
# pev = ds_to_etps.pev
# slhf = ds_to_etps.slhf
# ssr = ds_to_etps.ssr
# str = ds_to_etps.str
# sp = ds_to_etps.sp
# sshf = ds_to_etps.sshf
# ssrd = ds_to_etps.ssrd
# strd = ds_to_etps.strd
# tp = ds_to_etps.tp
# t2m_max = ds_to_etps.t2m_max
# t2m_min = ds_to_etps.t2m_min
# ra = ds_to_etps.ra
# daylh = ds_to_etps.daylh
# Ith = ds_to_etps.Ith
# ath = ds_to_etps.ath
