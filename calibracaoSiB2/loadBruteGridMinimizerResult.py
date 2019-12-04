# import pandas as pd
# import numpy as np
# from lmfit import report_fit, fit_report
# from example_brute import plot_results_brute
# import matplotlib.pyplot as plt
import pickle
from gradeparamsbrute import plot_results_brute


# diresults = '/vol0/evandro/resultados/'
diresults = '/dados/ProcessoOtimizacaoModelos/SiB2/resultados/'
arqvminres = 'sib2_bruteMinimizerResult.pkl'

out = pickle.load(open(diresults+arqvminres, "rb"))

"""
Plota a grade de parametros
"""

pngfigplot = '/dados/ProcessoOtimizacaoModelos/SiB2/plots/' \
    'sib2_pltGridParams.png'


plot_results_brute(out, best_vals=True, varlabels=None,
                   output=pngfigplot)
# plot_results_brute(out, best_vals=True, varlabels=None, output=None)
