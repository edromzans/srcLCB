import pandas as pd
import numpy as np
from lmfit import report_fit, fit_report
# from example_brute import plot_results_brute
# import matplotlib.pyplot as plt
import pickle
from gradeparamsbrute import plot_results_brute


# UGRHI SP ##
# tagname = '58220000'
# -------------------------
# tagname = '3D-001'
# -------------------------
# tagname = '4C-007'
# -------------------------
# tagname = '4B-015'
# -------------------------
tagname = '5B-011'
# -------------------------
############

# diresults = '/vol0/evandro/resultados/'
diresults = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/resultados/'
arqvminres = 'sib2_bruteMinimizerResult.pkl'

out = pickle.load(open(diresults+arqvminres, "rb"))

"""
Plota a grade de parametros
"""

# pngfigplot = '/dados/ProcessoOtimizacaoModelos/' \
#     'calibracaoBalagua/plots/plotaBruteParams.png'


pngfigplot = '/home/evandro/lcbiag/' \
    'ProcessoOtimizacaoModelos/calibracaoBalagua/' \
    'plots/sib2_pltGridParams.png'

plot_results_brute(out, best_vals=True, varlabels=None,
                   output=pngfigplot)
# plot_results_brute(out, best_vals=True, varlabels=None, output=None)
