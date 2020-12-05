import xarray as xr
import numpy as np
import extratrad as ra
import matplotlib.pyplot as plt

t_inicio = '1981-01-01'
t_final = '2020-08-01'

# diretorios
dirdata_era5 = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA5/'
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# Arquivos
era5land = 'reanalysis-era5-land-monthly-means.nc'
t2m_maxmin = 'madeLCB_reanalysis-era5-land_t2m_max_min_monthly_SE.nc'

# Datasets
ds_era5land = xr.open_dataset(dirdata_era5+era5land)

nx = ds_era5land.dims['longitude']
ny = ds_era5land.dims['latitude']
nt = ds_era5land.dims['time']

dayofyearall = ds_era5land.time.dt.dayofyear.values

dayear = (np.ones((nt, ny, nx))*dayofyearall[:, np.newaxis, np.newaxis]) + 15

lat = np.transpose([ds_era5land.latitude.values]*nx)


da_lat = xr.DataArray(data=lat,
                      dims=['latitude', 'longitude'],
                      coords=[ds_era5land.latitude.values,
                              ds_era5land.longitude.values])

da_daysofyear = xr.DataArray(data=dayear,
                             dims=['time', 'latitude', 'longitude'],
                             coords=[ds_era5land.time.values,
                                     ds_era5land.latitude.values,
                                     ds_era5land.longitude.values])

da_ra = ra.extratrad(da_lat, da_daysofyear)

da_ra.attrs['units'] = 'MJ m**-2 day**-1'
da_ra.attrs['long_name'] = 'Extraterrestial radiation for daily periods'
da_ra.name = 'ra'

da_ra.to_netcdf(dirsubset + 'dataarray_extraterrestrial_rad.nc')

# def extratrad(lat, dayofyear):

# lat = -22.90
# dayofyear = 200

# lat = da_lat
# dayofyear = da_daysofyear

# gsc = 0.0820  # [MJ m-2 min-1]

# latrad = np.radians(lat)

# dr = 1+0.033*np.cos(((2*np.pi)/365)*dayofyear)

# soldec = 0.409*np.sin(((2*np.pi)/365)*dayofyear - 1.39)

# ws = np.arccos(-np.tan(latrad)*np.tan(soldec))

# ra = ((24*60)/np.pi)*gsc*dr*(ws*np.sin(latrad)*np.sin(soldec) +
#                              np.cos(latrad)*np.cos(soldec)*np.sin(ws))  # [MJ m**-2 day**-1]
