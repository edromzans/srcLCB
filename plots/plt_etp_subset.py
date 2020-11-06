import pickle
import numpy as np
import matplotlib.pyplot as plt

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

pet_cru = pickle.load(open(
    dirsubset+'5B-011_cru_pet_subset.pkl', "rb"))

et0_xavier = pickle.load(open(
    dirsubset+'5B-011_xavier_et0_subset.pkl', "rb"))

# etp_penmanmontaith = pickle.load(open(
#     dirsubset+'5B-011_era5_pet_penmont_subset.pkl', "rb"))

pngfigplot = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/plots/etp/etp.png'

(etp_penmanmontaith,
 etp_hargreavessamani,
 etp_makkink,
 etp_priestleytaylor,
 etp_penman) = pickle.load(open(
     dirsubset+'5B-011_era5_etp_subset.pkl', "rb"))

xi = np.datetime64('2013-01-01')
xf = np.datetime64('2017-12-30')

xtime = etp_penmanmontaith.time.values


fig = plt.figure()
fig.set_figwidth(15)
fig.set_figheight(7)

plt.style.use('seaborn-whitegrid')
# ggplot
# dark_background

plt.plot(pet_cru.time, pet_cru,
         label='CRU Penman-Montaith')
plt.plot(et0_xavier.time, et0_xavier,
         label='Xavier Penman-Montaith')

plt.plot(etp_penmanmontaith.time, etp_penmanmontaith,
         label='ERA5 Penman-Montaith')

# plt.plot(etp_blaneycriddle.time, etp_blaneycriddle,
#          label='ERA5 Blaney-Criddle')

plt.plot(xtime, etp_hargreavessamani.values,
         label='ERA5 Hargreaves Samani')

plt.plot(etp_makkink.time, etp_makkink,
         label='ERA5 Makkink')
plt.plot(xtime, etp_priestleytaylor,
         label='ERA5 Priestley-Taylor')

# plt.plot(etp_rohwer.time, etp_rohwer,
#          label='ERA5 Rohwer')
plt.plot(etp_penman.time, etp_penman,
         label='ERA5 Penman')

plt.ylabel('ETP (mm d$^-1$)')
plt.xlim(xi, xf)


plt.legend()
plt.savefig(pngfigplot, dpi=150, bbox_inches='tight')
plt.show()
