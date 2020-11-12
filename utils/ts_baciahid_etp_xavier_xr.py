import xarray as xr
import numpy as np
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
    'calibracaoBalagua/dados/ET0_xavier/'

xaviernc = 'ETo_daily_UT_Brazil_v2_20140101_20170731_s1.nc'

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'
dirshape_bacia = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/' \
    'chuva_vazao_shape/shape_file/shape_file_limite/'

sh_pcj = 'pcj_basin.shp'

file_et0_df = tagname+'_xavier_et0_bacia_hid.pkl'

ds = xr.open_dataset(dirdata+xaviernc)

geodf_pcj = salem.read_shapefile(dirshape_bacia+sh_pcj)

# Mask com shapefile
xavier_to_mask = ds.ETo.isel(time=2)
xavier_maskroi_geo = xavier_to_mask.salem.roi(shape=geodf_pcj)
xavier_maskroi = (~np.isnan(xavier_maskroi_geo.values))*1
ds.coords['mask'] = (('latitude', 'longitude'),
                     xavier_maskroi)

et0_xavier_bacia = ds.ETo.where(
    ds.mask == 1, drop=True).mean({'longitude', 'latitude'})
# pet_cru = ds.pet.sel(lon=lon, lat=lat, method='nearest')

# Media mensal
et0_xavier_bacia = et0_xavier_bacia.resample(time='M').mean()

xtime = et0_xavier_bacia.time.values
dados = {'et0': et0_xavier_bacia.values}

et0_xavier_df = pd.DataFrame(dados, index=xtime)

et0_xavier_df.to_pickle(dirsubset+file_et0_df)



# et0_xavier = ds.ETo.sel(longitude=lon, latitude=lat, method='nearest')

# et0_xavier = et0_xavier.resample(time='M').mean()

# pickle.dump(et0_xavier,
#             open(dirsubset+filesubset, 'wb'))
