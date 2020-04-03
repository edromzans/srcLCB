import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import calendar


# UGRHI SP
# tagname = '58220000'
# -------------------------
# tagname = '3D-001'
# -------------------------
# tagname = '4C-007'
# -------------------------
tagname = '4B-015'
# -------------------------
#tagname = '5B-011'

# dirR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/resultados/'
dirR = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/resultados/'
dirplot = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/plots/'

dirInput = '/dados/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/ugrhi_sp/'

# Xavier
input_df_x = pd.read_pickle(dirInput+tagname+'_xavier_ugrhi_sp.pkl')
# etp_x = np.asarray(input_df_x.etp)

# CRU
input_df_cru = pd.read_pickle(dirInput+tagname+'_ugrhi_sp.pkl')
# etp_cru = np.asarray(input_df_cru.etp)

plt.plot(input_df_x.etp, c='green', linewidth=0.8, label='Xavier')
plt.plot(input_df_cru.etp, c='red', linewidth=0.8, label='CRU')
plt.legend()

plt.show()
