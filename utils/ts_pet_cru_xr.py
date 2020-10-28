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
    'calibracaoBalagua/dados/CRU_TS/'

crunc = 'cru_ts4.03.1901.2018.pet.dat.nc'

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

filesubset = tagname+'_cru_pet_subset.pkl'

# import netCDF4 as nc4
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

ds = xr.open_dataset(dirdata+crunc)

pet_cru = ds.pet.sel(lon=lon, lat=lat, method='nearest')

pickle.dump(pet_cru,
            open(dirsubset+filesubset, 'wb'))
