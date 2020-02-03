# import pandas as pd
# import numpy as np
from lmfit import report_fit, fit_report
# from example_brute import plot_results_brute
# import matplotlib.pyplot as plt
import pickle
from gradeparamsbrute import plot_results_brute


# diresults = '/vol0/evandro/resultados/'
diresults = '/dados/ProcessoOtimizacaoModelos/SiB2/resultados/'
# diresults = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/SiB2/resultados/'
# diresults = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/SiB2/resultados/checkSiB2pymod/'

arqvminres = 'sib2_rad_bruteMinimizerResult.pkl'

out = pickle.load(open(diresults+arqvminres, "rb"))

report_fit(out)

"""
Plota a grade de parametros
"""

pngfigplot = '/dados/ProcessoOtimizacaoModelos/SiB2/plots/' \
    'sib2_ustar_pltGridParams_brute.png'

plot_results_brute(out, best_vals=True, varlabels=None,
                   output=pngfigplot)
# plot_results_brute(out, best_vals=True, varlabels=None, output=None)
