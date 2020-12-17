import xarray as xr
import salem
import numpy as np
import matplotlib.pyplot as plt

exec(open('config/reanalise_config.py').read())

ds_reanalise = xr.open_dataset(dataset_reanalise)

if flag_espc == 0:
    revar = ds_reanalise[var].sel(
        time=slice(t_inicio, t_final)).salem.subset(
            corners=((xlon0, ylat0),
                     (xlon1, ylat1)))

    arq_nc = dir_subsets+'revar_'+var+'_regular.nc'
    print('Arquivo NetCDF criado: '+arq_nc)
    print(revar)
    revar.to_netcdf(arq_nc)

elif flag_espc == 1:
    geodf_shapefile = salem.read_shapefile(extrac_shape)
    ds_revar_to_mask = ds_reanalise[var].sel(time=t_inicio)
    ds_revar_maskroi_geo = ds_revar_to_mask.salem.roi(shape=geodf_shapefile)
    revar_maskroi = (~np.isnan(ds_revar_maskroi_geo.values))*1
    ds_reanalise.coords['mask'] = (('latitude', 'longitude'), revar_maskroi)

    # variables media espacial bacia
    revar = ds_reanalise[var].sel(
        time=slice(t_inicio, t_final)).where(
            ds_reanalise.mask == 1, drop=True)
    arq_nc = dir_subsets+'revar_'+var+'_shape.nc'
    print('Arquivo NetCDF criado: '+arq_nc)
    print(revar)
    revar.to_netcdf(arq_nc)

# Verificacao rapida -  graficos ####################################
fig = plt.figure()

revar_spcmean = revar.mean({'time'})
revar_spcmean.attrs = {'units': revar.attrs['units']}
revar_spcmean.name = 'Media temporal ('+var+')'
revar_spcmean.salem.quick_map()

fig = plt.figure()
revar.mean({'latitude', 'longitude'}).plot()
plt.title('Média espacial ('+var+')')
plt.ylabel(revar.attrs['units'])
plt.xlabel('tempo')

fig = plt.figure()
revar.groupby(revar.time.dt.month).mean({'time', 'latitude', 'longitude'}).plot()
plt.title('Ciclo anual da média espacial ('+var+')')
plt.ylabel(revar.attrs['units'])
plt.xlabel('mês')

plt.show()
######################################################################
