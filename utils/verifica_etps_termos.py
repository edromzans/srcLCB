import evapotranspiracaopotencial_era5check as etp
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# UGRHI SP
# tagname = '58220000'
# lat = -22.69
# lon = -44.98
# -------------------------
# tagname = '3D-001'
# lat = -22.68
# lon = -46.97
# -------------------------
# tagname = '4C-007'
# lat = -21.7
# lon = -47.82
# -------------------------
# tagname = '4B-015'
# lat = -20.63
# lon = -47.28
# -------------------------
# tagname = '5B-011'
lat = -20.91
lon = -48.09
# -------------------------
# tagname = '3D-002'
# lat = -22.70
# lon = -46.97
# -------------------------
##########

# diretórios
dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

dirplot = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/calibracaoBalagua/plots/'
# Arquivos
dataset_to_etps = 'dataset_to_etps_reanalysis-era5-land-monthly-means.nc'

ds_to_etps = xr.open_dataset(dirsubset+dataset_to_etps)

#Data variables:
u10 = ds_to_etps.u10
v10 = ds_to_etps.v10
d2m = ds_to_etps.d2m
t2m = ds_to_etps.t2m
pev       = ds_to_etps.pev
slhf      = ds_to_etps.slhf
ssr       = ds_to_etps.ssr
str       = ds_to_etps.str
sp        = ds_to_etps.sp
sshf      = ds_to_etps.sshf
ssrd      = ds_to_etps.ssrd
strd      = ds_to_etps.strd
tp        = ds_to_etps.tp
t2m_max   = ds_to_etps.t2m_max
t2m_min   = ds_to_etps.t2m_min
ra        = ds_to_etps.ra
daylh = ds_to_etps.daylh
Ith = ds_to_etps.Ith
ath = ds_to_etps.ath
# ndaysmonth = ds_to_etps.ndaysmonth

# (etp_fao56reference, Rn, G, u2, t2m, es_daily, ea) = etp.fao56reference(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
#                                                                         ssr, str, slhf, sshf)

# etp_asceewripenmanmonteith = etp.asceewripenmanmonteith(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
#                                                         ssr, str, slhf, sshf)

# (etp_penmanmonteith, G_pm, rs_pm, ra_pm, u2_pm) = etp.penmanmonteith(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
#                                                                      ssr, str, slhf, sshf)

# etp_hargreavessamani = etp.hargreavessamani(ra, t2m, t2m_max, t2m_min)

(etp_mhargreaves, S0) = etp.mhargreaves(ra, t2m, t2m_max, t2m_min, tp)

# etp_priestleytaylor = etp.priestleytaylor(ssr, str, slhf, sshf, t2m, sp)

# etp_thornthwaite = etp.thornthwaite(t2m, Ith, ath, daylh)

# fao56 = etp_fao56reference.sel(longitude=lon, latitude=lat, method='nearest')
# asceewri = etp_asceewripenmanmonteith.sel(longitude=lon, latitude=lat, method='nearest')
# pm = etp_penmanmonteith.sel(longitude=lon, latitude=lat, method='nearest')
# hs = etp_hargreavessamani.sel(longitude=lon, latitude=lat, method='nearest')
# mh = etp_mhargreaves.sel(longitude=lon, latitude=lat, method='nearest')
# pritay = etp_priestleytaylor.sel(longitude=lon, latitude=lat, method='nearest')
# th = etp_thornthwaite.sel(longitude=lon, latitude=lat, method='nearest')


# fao56 = etp_fao56reference.sel(longitude=lon, latitude=lat, method='nearest')
# Rn_s = Rn.sel(longitude=lon, latitude=lat, method='nearest')
# G_s = G.sel(longitude=lon, latitude=lat, method='nearest')
# u2_s = u2.sel(longitude=lon, latitude=lat, method='nearest')
# t2m_s = t2m.sel(longitude=lon, latitude=lat, method='nearest')
# es_daily_s = es_daily.sel(longitude=lon, latitude=lat, method='nearest')
# ea_s = ea.sel(longitude=lon, latitude=lat, method='nearest')

# pm = etp_penmanmonteith.sel(longitude=lon, latitude=lat, method='nearest')
# G_pm_s = G_pm.sel(longitude=lon, latitude=lat, method='nearest')
# rs_pm_s = 70.  # rs_pm.sel(longitude=lon, latitude=lat, method='nearest')
# ra_pm_s = ra_pm.sel(longitude=lon, latitude=lat, method='nearest')
# u2_pm_s = u2_pm.sel(longitude=lon, latitude=lat, method='nearest')

ra_s = ra.sel(longitude=lon, latitude=lat, method='nearest')
t2m_s = t2m.sel(longitude=lon, latitude=lat, method='nearest')
t2m_max_s = t2m_max.sel(longitude=lon, latitude=lat, method='nearest')
t2m_min_s = t2m_min.sel(longitude=lon, latitude=lat, method='nearest')
tp_s = tp.sel(longitude=lon, latitude=lat, method='nearest')



mh = etp_mhargreaves.sel(longitude=lon, latitude=lat, method='nearest')
S0_s = S0.sel(longitude=lon, latitude=lat, method='nearest')


# fao56.plot()
# plt.ylabel('fao56 ETP (mm d$^-1)$')
# plt.show()


# xtime = fao56.time.values
# xtime = pm.time.values
xtime = ra_s.time.values


# var = Rn_s.values
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('Rn (MJ m**-2 d**-1)')
# plt.savefig(dirplot+'Rn.png',
#             dpi=144, bbox_inches='tight')

# var = G_s.values
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('G (MJ m**-2 d**-1)')
# plt.savefig(dirplot+'G.png',
#             dpi=144, bbox_inches='tight')

# var = u2_s.values
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('u2 (m s**-1)')
# plt.savefig(dirplot+'u2.png',
#             dpi=144, bbox_inches='tight')

# var = t2m_s.values
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('Ta (°C)')
# plt.savefig(dirplot+'Ta.png',
#             dpi=144, bbox_inches='tight')

# var = ea_s.values
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('$\gamma$a (kPa)')
# plt.savefig(dirplot+'gama_a.png',
#             dpi=144, bbox_inches='tight')

# var = (es_daily_s.values - ea_s.values)
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('$\gamma$a* - $\gamma$a (kPa)')
# plt.savefig(dirplot+'deficit.png',
#             dpi=144, bbox_inches='tight')

# var = fao56.values
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('fao56 ETP (mm d**-1)')
# plt.savefig(dirplot+'fao56.png',
#             dpi=144, bbox_inches='tight')

# var = G_pm_s.values
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('G (MJ m**-2 d**-1)')
# plt.savefig(dirplot+'G_pm.png',
#             dpi=144, bbox_inches='tight')

# var = rs_pm_s
# fig = plt.figure()
# fig.set_figwidth(12)
# fig.set_figheight(4)
# plt.plot(xtime, var, 'black')
# plt.xlabel('tempo')
# plt.ylabel('rs (s m**-1)')
# plt.savefig(dirplot+'rs_pm.png',
#             dpi=144, bbox_inches='tight')

var = ra_s.values
fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(4)
plt.plot(xtime, var, 'black')
plt.xlabel('tempo')
plt.ylabel('Ra (MJ m**-2 day**-1)')
plt.savefig(dirplot+'ra.png',
            dpi=144, bbox_inches='tight')

var = t2m_s.values - 273.15
fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(4)
plt.plot(xtime, var, 'black')
plt.xlabel('tempo')
plt.ylabel('Ta (°C)')
plt.savefig(dirplot+'Ta.png',
            dpi=144, bbox_inches='tight')

var = t2m_max_s.values - 273.15
fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(4)
plt.plot(xtime, var, 'black')
plt.xlabel('tempo')
plt.ylabel('Tmax (°C)')
plt.savefig(dirplot+'Tmax.png',
            dpi=144, bbox_inches='tight')

var = t2m_min_s.values - 273.15
fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(4)
plt.plot(xtime, var, 'black')
plt.xlabel('tempo')
plt.ylabel('Tmin (°C)')
plt.savefig(dirplot+'Tmin.png',
            dpi=144, bbox_inches='tight')

var = S0_s.values
fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(4)
plt.plot(xtime, var, 'black')
plt.xlabel('tempo')
plt.ylabel('S$_0$ (mm d**-1)')
plt.savefig(dirplot+'S0.png',
            dpi=144, bbox_inches='tight')

var = ((t2m_max_s.values-273.15) - (t2m_min_s.values-273.15))
fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(4)
plt.plot(xtime, var, 'black')
plt.xlabel('tempo')
plt.ylabel('TD (°C)')
plt.savefig(dirplot+'TD.png',
            dpi=144, bbox_inches='tight')

var = tp_s.values*10**3  # [mm d**-1]
fig = plt.figure()
fig.set_figwidth(12)
fig.set_figheight(4)
plt.plot(xtime, var, 'black')
plt.xlabel('tempo')
plt.ylabel('P (mm d**-1)')
plt.savefig(dirplot+'P.png',
            dpi=144, bbox_inches='tight')




# xtime = ds_to_etps.time
# plt.plot(xtime, fao56, label='faoRef')
# plt.plot(xtime, asceewri, label='asceewri')
# plt.plot(xtime, pm, label='penmanmonteith')
# plt.plot(xtime, hs, label='hargreavessamani')
# plt.plot(xtime, mh, label='mhargreaves')
# plt.plot(xtime, pritay, label='priestleytaylor')
# plt.plot(xtime, th, label='th')
# plt.ylabel('mm d$^-1$')
# plt.legend()
# plt.show()

# #.sel(longitude=lon, latitude=lat, method='nearest')
# etpplot = etp_fao56reference.isel(time=50)
# etpplot.plot()
# plt.show()
