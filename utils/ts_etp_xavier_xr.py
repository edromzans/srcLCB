import xarray as xr
# import numpy as np
import pickle

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

dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ET0_xavier/'

xaviernc = 'ETo_daily_UT_Brazil_v2_20140101_20170731_s1.nc'

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

filesubset = tagname+'_xavier_et0_subset.pkl'

ds = xr.open_dataset(dirdata+xaviernc)

et0_xavier = ds.ETo.sel(longitude=lon, latitude=lat, method='nearest')

et0_xavier = et0_xavier.resample(time='M').mean()

pickle.dump(et0_xavier,
            open(dirsubset+filesubset, 'wb'))
