import xarray as xr
import numpy as np
import extratrad as ra
import matplotlib.pyplot as plt
import evapotranspiracaopotencial_era5 as etp

# t_inicio = '1981-01-01'
# t_final = '2020-08-01'

# diretorios
dirdata_era5 = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA5/'
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# Arquivos
era5land = 'reanalysis-era5-land-monthly-means.nc'
#th_indexes = 'made_thornthwaite_indexes.nc'

# Datasets
ds_era5land = xr.open_dataset(dirdata_era5+era5land)

t2m = ds_era5land.t2m - 273.15  # [C]

nx = ds_era5land.dims['longitude']
ny = ds_era5land.dims['latitude']
nt = ds_era5land.dims['time']

latrad = np.radians(np.transpose([ds_era5land.latitude.values]*nx))

da_latrad = xr.DataArray(data=latrad,
                         dims=['latitude', 'longitude'],
                         coords=[ds_era5land.latitude.values,
                                 ds_era5land.longitude.values])

dayofyearall = np.fix(ds_era5land.time.dt.dayofyear.values +
                      ds_era5land.time.dt.daysinmonth.values/2)

dayear = (np.ones((nt, ny, nx))*dayofyearall[:, np.newaxis, np.newaxis])

da_daysofyear = xr.DataArray(data=dayear,
                             dims=['time', 'latitude', 'longitude'],
                             coords=[ds_era5land.time.values,
                                     ds_era5land.latitude.values,
                                     ds_era5land.longitude.values])


# daysofmonthall = ds_era5land.time.dt.daysinmonth.values

# data_daysinmonth = (np.ones((nt, ny, nx))
#                     * daysofmonthall[:, np.newaxis, np.newaxis])

# da_daysinmonth = xr.DataArray(data=data_daysinmonth,
#                               dims=['time', 'latitude', 'longitude'],
#                               coords=[ds_era5land.time.values,
#                                       ds_era5land.latitude.values,
#                                       ds_era5land.longitude.values])

da_soldec = 0.409*np.sin(((2*np.pi)/365)*da_daysofyear-1.39)

da_ws = np.arccos(np.tan(da_soldec)*(-np.tan(da_latrad)))

da_daylh = (24/np.pi) * da_ws

ith = (t2m/5)**1.514

Ith = ith.resample(time='AS').sum()

ath = (6.75*(10**(-7))*(Ith**3)
       - 7.71*(10**(-5))*(Ith**2)
       + 0.01792*Ith + 0.49239)

da_Ith = xr.DataArray(data=np.ones((nt, ny, nx)),
                      dims=['time', 'latitude', 'longitude'],
                      coords=[ds_era5land.time.values,
                              ds_era5land.latitude.values,
                              ds_era5land.longitude.values])
da_Ith.name = 'Ith'

da_ath = xr.DataArray(data=np.ones((nt, ny, nx)),
                      dims=['time', 'latitude', 'longitude'],
                      coords=[ds_era5land.time.values,
                              ds_era5land.latitude.values,
                              ds_era5land.longitude.values])
da_ath.name = 'ath'


for year in Ith.time.dt.year.values:

    posyear_da = np.asarray(da_Ith.time.dt.year == year).nonzero()
    posyear_da = posyear_da[0]

    posyear_index = np.asarray(Ith.time.dt.year == year).nonzero()
    posyear_index = posyear_index[0]

    nmes = len(posyear_da)

    if nmes == 12:
        da_Ith[posyear_da, :, :] = Ith[posyear_index[0], :, :]
        da_ath[posyear_da, :, :] = ath[posyear_index[0], :, :]
    else:
        da_Ith[posyear_da, :, :] = np.nan
        da_ath[posyear_da, :, :] = np.nan
        da_daylh[posyear_da, :, :] = np.nan

ds_th_indexes = da_Ith.to_dataset(name='Ith')
ds_th_indexes['ath'] = da_ath
ds_th_indexes['daylh'] = np.round(da_daylh, 1)
# ds_th_indexes['ndaysmonth'] = da_daysinmonth

ds_th_indexes.Ith.attrs = {'units': 'index',
                           'long_name': 'Thornthwaite I index'}
ds_th_indexes.ath.attrs = {'units': 'index',
                           'long_name': 'Thornthwaite a index'}
ds_th_indexes.daylh.attrs = {'units': 'daylight hours',
                             'long_name': 'Daylight hours (N)'}
# ds_th_indexes.ndaysmonth.attrs = {'units': 'number of days',
#                                   'long_name': 'Number of days in month'}

# etp_thornthwaite = etp.thornthwaite(t2m,
#                                     ds_th_indexes.Ith,
#                                     ds_th_indexes.ath,
#                                     ds_th_indexes.daylh)

ds_th_indexes.to_netcdf(
    dirsubset + 'dataset_thornthwaite_indxs.nc')
