import xarray as xr
import salem
import numpy as np
import matplotlib.pyplot as plt

nc_etp1 = '../subsets/etp_fao56reference_regular.nc'
nc_etp2 = '../subsets/etp_thornthwaite_regular.nc'
# nc_etp3 = ''
# nc_etp4 = ''

ds_etp1 = xr.open_dataset(nc_etp1)
ds_etp2 = xr.open_dataset(nc_etp2)
# ds_etp1 =
# ds_etp2 =

# Descreva os codinomes dos metodos de etp que participam da media
etpcodname = 'fao56reference, thornthwaite'

# Faca a media conforme a quantidade de datasets de etp
da_etpm = (ds_etp1.fao56reference + ds_etp2.thornthwaite)/2

arq_nc = '../subsets/etpm.nc'

ds_etpm = da_etpm.to_dataset(name='etpm')
ds_etpm.etpm.attrs = {'units': 'mm d$^{-1}$',
                      'long_name': 'Etp média: '+etpcodname}

ds_etpm.to_netcdf(arq_nc)
print(ds_etpm)
print('Arquivo NetCDF criado: '+arq_nc)

# Verificacao grafica rapida ### ####################################
fig = plt.figure()

ds_etpm_spcmean = ds_etpm.etpm.mean({'time'})
ds_etpm_spcmean.attrs = {'units': 'mm d$^{-1}$'}
ds_etpm_spcmean.name = 'Media temporal'
ds_etpm_spcmean.salem.quick_map()

fig = plt.figure()
ds_etpm.etpm.mean({'latitude', 'longitude'}).plot()
plt.title('Média espacial')
plt.ylabel('mm d$^{-1}$')
plt.xlabel('tempo')

fig = plt.figure()
ds_etpm.etpm.groupby(ds_etpm.time.dt.month).mean(
    {'time', 'latitude', 'longitude'}).plot()
plt.title('Ciclo anual da média espacial')
plt.ylabel('mm d$^{-1}$')
plt.xlabel('mês')

plt.show()
######################################################################
