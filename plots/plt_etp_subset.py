import pickle
import matplotlib.pyplot as plt

dirsubset = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/subsets/'

pet_cru = pickle.load(open(
    dirsubset+'5B-011_cru_pet_subset.pkl', "rb"))

etp_penmanmontaith = pickle.load(open(
    dirsubset+'5B-011_era5_pet_penmont_subset.pkl', "rb"))

plt.plot(pet_cru.time, pet_cru, label='CRU Penman-Montaith')
plt.plot(etp_penmanmontaith.time, etp_penmanmontaith, label='ERA5 Penman-Montaith')
plt.legend()
plt.show()
