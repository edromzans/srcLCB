import xarray as xr
import salem
import numpy as np
import matplotlib.pyplot as plt

exec(open('config/etps_config.py').read())

ds_etps = xr.open_dataset(dataset_etps)

if flag_espc == 0:
    etp = ds_etps[etp_metodo].sel(
        time=slice(t_inicio, t_final)).salem.subset(
            corners=((xlon0, ylat0),
                     (xlon1, ylat1)))

    arq_nc = dir_subsets+'etp_'+etp_metodo+'_regular.nc'
    print(etp)
    etp.to_netcdf(arq_nc)
    print('Arquivo NetCDF criado: '+arq_nc)

elif flag_espc == 1:
    geodf_shapefile = salem.read_shapefile(extrac_shape)
    ds_etp_to_mask = ds_etps[etp_metodo].sel(time=t_inicio)
    ds_etp_maskroi_geo = ds_etp_to_mask.salem.roi(shape=geodf_shapefile)
    etp_maskroi = (~np.isnan(ds_etp_maskroi_geo.values))*1
    ds_etps.coords['mask'] = (('latitude', 'longitude'), etp_maskroi)

    etp = ds_etps[etp_metodo].sel(
        time=slice(t_inicio, t_final)).where(
            ds_etps.mask == 1, drop=True)
    arq_nc = dir_subsets+'etp_'+etp_metodo+'_shape.nc'
    print(etp)
    etp.to_netcdf(arq_nc)
    print('Arquivo NetCDF criado: '+arq_nc)

# Verificacao grafica rapida ### ####################################
fig = plt.figure()

etp_spcmean = etp.mean({'time'})
etp_spcmean.attrs = {'units': 'mm d$^{-1}$'}
etp_spcmean.name = 'Media temporal ('+etp_metodo+')'
etp_spcmean.salem.quick_map()

fig = plt.figure()
etp.mean({'latitude', 'longitude'}).plot()
plt.title('Média espacial ('+etp_metodo+')')
plt.ylabel('mm d$^{-1}$')
plt.xlabel('tempo')

fig = plt.figure()
etp.groupby(etp.time.dt.month).mean({'time', 'latitude', 'longitude'}).plot()
plt.title('Ciclo anual da média espacial ('+etp_metodo+')')
plt.ylabel('mm d$^{-1}$')
plt.xlabel('mês')

plt.show()
######################################################################
