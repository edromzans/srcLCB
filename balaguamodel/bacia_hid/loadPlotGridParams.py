import pandas as pd
import numpy as np
from lmfit import report_fit, fit_report
# from example_brute import plot_results_brute
# import matplotlib.pyplot as plt
import pickle
from gradeparamsbrute import plot_results_brute


# Bacias Hidrograficas SP
# -------------------------
tagname = 'pcj_bacia_hid_3D-002'
# -------------------------

dirInput = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/InstrucaoModBalagua/dados/ugrhi_sp/'

dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/InstrucaoModBalagua/resultados/'

arqvminres = tagname+'_ugrhi_bruteMinimizerResult.pkl'
pngfigplot = '/home/evandro/lcbiag/' \
    'ProcessoOtimizacaoModelos/calibracaoBalagua/InstrucaoModBalagua/' \
    'plots/'+tagname+'_ugrhi_pltGridParams.png'
input_df = pd.read_pickle(dirInput+tagname+'_ugrhi_sp.pkl')

# Xavier
# arqvminres = tagname+'_xavier_ugrhi_bruteMinimizerResult.pkl'
# pngfigplot = '/dados/' \
#     'ProcessoOtimizacaoModelos/calibracaoBalagua/' \
#     'plots/'+tagname+'_xavier_ugrhi_pltGridParams.png'
# input_df = pd.read_pickle(dirInput+tagname+'_xavier_ugrhi_sp.pkl')

out = pickle.load(open(dirMR+arqvminres, "rb"))

report_fit(out)

"""
Plota a grade de parametros
"""

plot_results_brute(out, best_vals=True, varlabels=None, output=pngfigplot)
#plot_results_brute(out, best_vals=True, varlabels=None, output=None)
