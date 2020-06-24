import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'SiB2/input/FlorAtlantica/2014-2016/'

# dadosobs = pd.read_csv(dirdata+'data3.csv')

dadosobs = pd.read_csv(dirdata+'Data_SiB2_hourly_2014_2016_v5.csv')

dadosobs.index = dadosobs.Timestamp
xtime = np.asarray(dadosobs.index, dtype=np.datetime64)

# IDL where
posval = np.asarray((np.asarray(dadosobs.index, dtype=np.datetime64)
                     > np.datetime64('2015-09-23 15:00')) &
                    (np.asarray(dadosobs.index, dtype=np.datetime64)
                     <= np.datetime64('2015-11-23 07:00'))).nonzero()
posval = posval[0]

dadosobs = dadosobs.reset_index(drop=True)

dadosobs.loc[posval,
             ['SWC', 'VW1', 'VW2', 'VW3', 'VW4', 'VW5', 'VW6']] = np.nan

dadosobs.to_csv(dirdata+'data3_changed.csv', index=False)

swc = np.asarray(dadosobs.SWC)
vw1 = np.asarray(dadosobs.VW1)
vw2 = np.asarray(dadosobs.VW2)
vw3 = np.asarray(dadosobs.VW3)
vw4 = np.asarray(dadosobs.VW4)
vw5 = np.asarray(dadosobs.VW5)
vw6 = np.asarray(dadosobs.VW6)

plt.plot(xtime, swc)
plt.plot(xtime, vw1)
plt.plot(xtime, vw2)
plt.plot(xtime, vw3)
plt.plot(xtime, vw4)
plt.plot(xtime, vw5)
plt.plot(xtime, vw6)

# plt.plot(swc)
# plt.plot(vw1)
# plt.plot(vw2)
# plt.plot(vw3)
# plt.plot(vw4)
# plt.plot(vw5)
# plt.plot(vw6)

plt.show()
