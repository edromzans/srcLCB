import netCDF4 as nc4
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ncf_cru_pet = '/dados/CRU_TS/cru_ts4.03.1901.2018.pet.dat.nc'

cru = nc4.Dataset(ncf_cru_pet, 'r')

xlon = cru.variables['lon'][:]
ylat = cru.variables['lat'][:]
tp = cru.variables['time'][:]
pet = cru.variables['pet'][:]

xlon = np.ma.getdata(xlon)
ylat = np.ma.getdata(ylat)

datatempo = np.datetime64('1900-01-01', 'D') + np.uint(np.ma.getdata(tp))

nx = len(datatempo) 

# estacao agua dados
lat = -22.88
lon = -46.63

dislat = np.abs(ylat - lat)
dislon = np.abs(xlon - lon)

poslatgr = np.where(dislat == np.min(dislat))
print(lat, ylat[poslatgr])

poslongr = np.where(dislon == np.min(dislon))
print(lon, xlon[poslongr])

ts_pet = np.ma.getdata(pet[:, poslatgr, poslongr]).reshape(nx)

pet_df = pd.DataFrame(data={'pet': ts_pet}, index=datatempo)

plt.plot(pet_df)
plt.show()
