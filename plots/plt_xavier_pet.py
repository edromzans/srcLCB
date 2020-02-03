import netCDF4 as nc4
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

ncf_cru_pet = '/dados/ET0_xavier/ETo_daily_UT_Brazil_v2_20140101_20170731_s1.nc'

cru = nc4.Dataset(ncf_cru_pet, 'r')

xlon = cru.variables['longitude'][:]
ylat = cru.variables['latitude'][:]
tp = cru.variables['time'][:]
pet = cru.variables['ETo'][:]

xlon = np.ma.getdata(xlon)
ylat = np.ma.getdata(ylat)
tp = np.ma.getdata(tp)

datatempo = np.datetime64('2014-01-01', 'h') + tp.astype('timedelta64[h]')

map = Basemap(projection='ortho', lat_0=-10, lon_0=-60)
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)


xlon2d, ylat2d = np.meshgrid(xlon, ylat)
x, y = map(xlon2d, ylat2d)

# xp, yp = map(xlon, ylat)


post = 1
print(datatempo[post])

map.contourf(x, y, pet[post, :, :], 255)
# map.scatter(x, y, marker='.', color='r')
plt.colorbar()
plt.show()
