import xarray as xr
import numpy as np
# import pickle
import pandas as pd
import salem

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
# tagname = '5B-011'
# lat = -20.91
# lon = -48.09
#-------------------------
##########
tagname = 'pcj'

dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/CRU/'
dirshape_bacia = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/' \
    'chuva_vazao_shape/shape_file/shape_file_limite/'

sh_pcj = 'pcj_basin.shp'

# crunc = 'cru_ts4.03.1901.2018.pet.dat.nc'
crunc = 'cru_ts4.04.1901.2019.pet.dat.nc'

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

file_cru_pet_df = tagname+'_cru_pet_bacia_hid.pkl'

# import netCDF4 as nc4
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

ds = xr.open_dataset(dirdata+crunc)

geodf_pcj = salem.read_shapefile(dirshape_bacia+sh_pcj)

# Mask com shapefile
cru_to_mask = ds.pet.isel(time=2)
cru_maskroi_geo = cru_to_mask.salem.roi(shape=geodf_pcj)
cru_maskroi = (~np.isnan(cru_maskroi_geo.values))*1
ds.coords['mask'] = (('lat', 'lon'),
                     cru_maskroi)

pet_cru_bacia = ds.pet.where(
    ds.mask == 1, drop=True).mean({'lon', 'lat'})
# pet_cru = ds.pet.sel(lon=lon, lat=lat, method='nearest')

xtime = pet_cru_bacia.time.values
dados = {'pet': pet_cru_bacia.values}

pet_cru_df = pd.DataFrame(dados, index=xtime)

pet_cru_df.to_pickle(dirsubset+file_cru_pet_df)

# pickle.dump(pet_cru,
#             open(dirsubset+file_cru_pet_df, 'wb'))
