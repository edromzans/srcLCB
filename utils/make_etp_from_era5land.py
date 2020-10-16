import xarray as xr

dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA-5_Land/'

era5nc = 'ERA5-Land_Monthly_avg_reanalysis.nc'

# UGRHI SP
# tagname = '58220000'
# lat = -22.69
# lon = -44.98
#-------------------------
# tagname = '3D-001'
# lat = -22.68
# lon = -46.97
#-------------------------
# tagname = '4C-007'
# lat = -21.7
# lon = -47.82
#-------------------------
# tagname = '4B-015'
# lat = -20.63
# lon = -47.28
#-------------------------
tagname = '5B-011'
lat = -20.91
lon = -48.09
#-------------------------
##########

ds = xr.open_dataset(dirdata+era5nc)

datatempo = ds.time
uwind = ds.u10.sel(longitude=lon, latitude=lat, method='nearest')
vwind = ds.v10.sel(longitude=lon, latitude=lat, method='nearest')
temp = ds.t2m.sel(longitude=lon, latitude=lat, method='nearest')
td = ds.d2m.sel(longitude=lon, latitude=lat, method='nearest')
