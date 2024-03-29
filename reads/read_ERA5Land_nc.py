import netCDF4 as nc4
import numpy as np

dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA-5_Land/'

era5land = nc4.Dataset(
    dirdata+'ERA5-Land_Monthly_avg_reanalysis.nc', 'r')

# ncf_cru_pet = '/dados/CRU_TS/cru_ts4.03.1901.2018.pet.dat.nc'
# # '/dados/CRU_TS/cru_ts4.03.1901.1910.pet.dat.nc'


# cru = nc4.Dataset(ncf_cru_pet, 'r')

# xlon = cru.variables['lon'][:]
# ylat = cru.variables['lat'][:]
# tp = cru.variables['time'][:]
# pet = cru.variables['pet'][:]

# xlon = np.ma.getdata(xlon)
# ylat = np.ma.getdata(ylat)

# datatempo = np.datetime64('1900-01-01', 'D') + np.uint(np.ma.getdata(tp))

# map = Basemap(projection='ortho', lat_0=-10, lon_0=-60)
# map.drawcoastlines(linewidth=0.25)
# map.drawcountries(linewidth=0.25)


# xlon2d, ylat2d = np.meshgrid(xlon, ylat)
# x, y = map(xlon2d, ylat2d)

# # xp, yp = map(xlon, ylat)


# post = 1308
# print(datatempo[post])

# map.contourf(x, y, pet[post, :, :], 255)
# # map.scatter(x, y, marker='.', color='r')
# plt.colorbar()
# plt.show()
