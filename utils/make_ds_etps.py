import evapotranspiracaopotencial_era5 as etp
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# diretórios
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

# Arquivos
dataset_to_etps = 'dataset_to_etps_reanalysis-era5-land-monthly-means.nc'

ds_to_etps = xr.open_dataset(dirsubset+dataset_to_etps)

#Data variables:
u10 = ds_to_etps.u10
v10 = ds_to_etps.v10
d2m = ds_to_etps.d2m
t2m = ds_to_etps.t2m
pev = ds_to_etps.pev
slhf = ds_to_etps.slhf
ssr = ds_to_etps.ssr
str = ds_to_etps.str
sp = ds_to_etps.sp
sshf = ds_to_etps.sshf
ssrd = ds_to_etps.ssrd
strd = ds_to_etps.strd
tp = ds_to_etps.tp
t2m_max = ds_to_etps.t2m_max
t2m_min = ds_to_etps.t2m_min
ra = ds_to_etps.ra
daylh = ds_to_etps.daylh
Ith = ds_to_etps.Ith
ath = ds_to_etps.ath

etp_fao56reference = etp.fao56reference(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                                        ssr, str, slhf, sshf)

etp_asceewripenmanmonteith = etp.asceewripenmanmonteith(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                                                        ssr, str, slhf, sshf)

etp_penmanmonteith = etp.penmanmonteith(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                                        ssr, str, slhf, sshf)

etp_hargreavessamani = etp.hargreavessamani(ra, t2m, t2m_max, t2m_min)

etp_mhargreaves = etp.mhargreaves(ra, t2m, t2m_max, t2m_min, tp)

etp_priestleytaylor = etp.priestleytaylor(ssr, str, slhf, sshf, t2m, sp)

etp_thornthwaite = etp.thornthwaite(t2m, Ith, ath, daylh)


ds_etps = etp_fao56reference.to_dataset(name='fao56reference')
ds_etps['asceewri_penmon'] = etp_asceewripenmanmonteith
ds_etps['penmanmonteith'] = etp_penmanmonteith
ds_etps['hargreavessamani'] = etp_hargreavessamani
ds_etps['mhargreaves'] = etp_mhargreaves
ds_etps['priestleytaylor'] = etp_priestleytaylor
ds_etps['thornthwaite'] = etp_thornthwaite


ds_etps.attrs = {'Description':
                 'Evapotranspiration calculated (McMahon, 2013; Allen etal, 1998)'}

ds_etps.fao56reference.attrs = {'units': 'mm day**-1',
                                 'long_name': 'FAO-56 Reference Crop Evapotranspiration'}

ds_etps.asceewri_penmon.attrs = {'units': 'mm day**-1',
                                 'long_name': 'ASCE-EWRI Standardized Penman-Monteith Equation'}

ds_etps.penmanmonteith.attrs = {'units': 'mm day**-1',
                                'long_name': 'Penman-Monteith model'}

ds_etps.hargreavessamani.attrs = {'units': 'mm day**-1',
                                  'long_name': 'Hargreaves-Samani (1985)'}

ds_etps.mhargreaves.attrs = {'units': 'mm day**-1',
                             'long_name': 'Modified Hargreaves'}

ds_etps.priestleytaylor.attrs = {'units': 'mm day**-1',
                                 'long_name': 'Priestley and Taylor (1972)'}

ds_etps.thornthwaite.attrs = {'units': 'mm day**-1',
                              'long_name': 'Thornthwaite (1948)'}

ds_etps.to_netcdf(
    dirsubset + 'dataset_etps.nc')
