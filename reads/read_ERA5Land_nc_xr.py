import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import xarray as xr

dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA-5_Land/'

ds = xr.open_dataset(dirdata+'ERA5-Land_Monthly_avg_reanalysis.nc')

print(ds)

da = ds.fal
da = da.sel(time=('2000-01-01'))

plt.figure()
# Draw coastlines of the Earth
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
da.plot()
plt.show()
