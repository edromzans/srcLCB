import calendar
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

pet_cru_df = pickle.load(open(dirsubset+'pcj_cru_pet_bacia_hid.pkl', "rb"))

et0_xavier_df = pickle.load(open(dirsubset+'pcj_xavier_et0_bacia_hid.pkl', "rb"))

# file_etp = '5B-011_era5_etp_subset.pkl'
file_etps_df = 'pcj_era5_etp_baciahid.pkl'

# etp_penmanmontaith = pickle.load(open(
#     dirsubset+'5B-011_era5_pet_penmont_subset.pkl', "rb"))

pngfigplot = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/plots/etp/etp.png'

# (etp_penmanmontaith,
#  etp_hargreavessamani,
#  etp_makkink,
#  etp_priestleytaylor,
#  etp_penman) = pickle.load(open(
#      dirsubset+file_etp, "rb"))

etps_df = pickle.load(open(dirsubset+file_etps_df, "rb"))

# xi = np.datetime64('2013-01-01')
# xf = np.datetime64('2017-12-30')

xi = np.datetime64('1981-01-01')
xf = np.datetime64('2019-12-30')

#xtime = etp_penmanmontaith.time.values
xtime = etps_df.index.values

fig = plt.figure()
fig.set_figwidth(25)
fig.set_figheight(3)

# plt.style.use('seaborn-whitegrid')
# ggplot
# dark_background

plt.plot(pet_cru_df.index, pet_cru_df,
         label='CRU Penman-Montaith')
plt.plot(et0_xavier_df.index, et0_xavier_df.et0,
         label='Xavier Penman-Montaith')

plt.plot(xtime, etps_df.penmanmontaith,
         label='ERA5 Penman-Montaith')
plt.plot(xtime, etps_df.hargreavessamani,
         label='ERA5 Hargreaves Samani')
plt.plot(xtime, etps_df.makkink,
         label='ERA5 Makkink')
plt.plot(xtime, etps_df.priestleytaylor,
         label='ERA5 Priestley-Taylor')
plt.plot(xtime, etps_df.penman,
         label='ERA5 Penman')

plt.ylabel('ETP (mm d$^-1$)')
plt.xlim(xi, xf)

plt.legend(facecolor="white", framealpha=50)
plt.savefig(pngfigplot, dpi=200, bbox_inches='tight')
# plt.show()

canual_etps_df = etps_df.groupby(etps_df.index.month.values).agg(np.nanmean)
d_mes = dict(enumerate(calendar.month_abbr))
canual_etps_df.index = canual_etps_df.index.map(d_mes)

canual_pet_cru_df = pet_cru_df.groupby(
    pet_cru_df.index.month.values).agg(np.nanmean)
d_mes = dict(enumerate(calendar.month_abbr))
canual_pet_cru_df.index = canual_pet_cru_df.index.map(d_mes)

canual_et0_xavier_df = et0_xavier_df.groupby(
    et0_xavier_df.index.month.values).agg(np.nanmean)
d_mes = dict(enumerate(calendar.month_abbr))
canual_et0_xavier_df.index = canual_et0_xavier_df.index.map(d_mes)

pngfigplot = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/plots/etp/etp_cicloanual.png'
fig = plt.figure()
fig.set_figwidth(7)
fig.set_figheight(4)
# plt.style.use('seaborn-whitegrid')

plt.plot(canual_pet_cru_df.pet,
         label='CRU Penman-Montaith')
plt.plot(canual_et0_xavier_df.et0,
         label='Xavier Penman-Montaith')

plt.plot(canual_etps_df.penmanmontaith,
         label='ERA5 Penman-Montaith')
plt.plot(canual_etps_df.hargreavessamani,
         label='ERA5 Hargreaves Samani')
plt.plot(canual_etps_df.makkink,
         label='ERA5 Makkink')
plt.plot(canual_etps_df.priestleytaylor,
         label='ERA5 Priestley-Taylor')
plt.plot(canual_etps_df.penman,
         label='ERA5 Penman')

plt.ylabel('ETP (mm d$^-1$)')

plt.legend(facecolor="white", framealpha=50)
plt.savefig(pngfigplot, dpi=200, bbox_inches='tight')
plt.show()
