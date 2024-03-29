import pandas as pd
import numpy as np
from lmfit import report_fit, fit_report
# from example_brute import plot_results_brute
# import matplotlib.pyplot as plt
import pickle
from gradeparamsbrute import plot_results_brute

diresults = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/resultados/'
# diresults = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/calibracaoBalagua/resultados/'

# arqv = 'save_outbruteMinimizerResult_9mi.p'
# arqv = 'save_outbruteMinimizerResult_20191028.p'
# arqv = 'save_outbruteMinimizerResult_am.p'
arqvminres = 'save_outbruteMinimizerResult.p'

out = pickle.load(open(diresults+arqvminres, "rb"))

"""
Verificacao dos parametros candidatos caculados
"""

dirdados = '/dados/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/jaraguari_obs/'
# dirdados = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
#     'calibracaoBalagua/dados/inputs/jaraguari_obs/'

arqinput = 'input.txt'
entradados = dirdados+arqinput

ncand = len(out.candidates)

for ck in range(ncand):
    a1 = out.candidates[ck].params['a1']
    a2 = out.candidates[ck].params['a2']
    a22 = out.candidates[ck].params['a22']
    a3 = out.candidates[ck].params['a3']
    print(out.show_candidates(ck+1))
    dadosobs = pd.read_table(
        entradados, header=None, delim_whitespace=True, names=[
            'ano', 'mes', 'dia', 'hora', 'minuto', 'segundo',
            'etp', 'p2', 'q2', 'escb'])
    m_func = len(dadosobs)
    modeloerro = np.zeros(m_func, dtype='float64')
    #
    ts_mt = np.zeros(m_func, dtype='float64')
    ts_dt = np.zeros(m_func, dtype='float64')
    ts_u = np.zeros(m_func, dtype='float64')
    #
    etp = np.float64(dadosobs['etp'])
    p2 = np.float64(dadosobs['p2'])
    q2 = np.float64(dadosobs['q2'])
    escb = np.float64(dadosobs['escb'])
    #
    m1 = 500.
    r2 = np.float64(0)
    s2 = np.float64(0)
    n2 = np.float64(0)
    d2 = np.float64(0)
    m2 = np.float64(0)
    for kount in range(0, m_func):
        """
        Modelo de balanco de agua

        r2 => evapotranpiracao real
        s2 => escoamento lento
        n2 => precipitacao ativa
        f2 => escoamento rapido
        d2 => vazao com filtro
        """
        r2 = min(
            etp[kount]*(1.-a1**((p2[kount]+max(m1, 0.))/etp[kount])),
            (p2[kount]+max(m1, 0.))
        )
        s2 = a2*(max(m1, 0.)**a22)
        n2 = p2[kount]-etp[kount]*(1-np.exp(-p2[kount]/etp[kount]))
        f2 = a3*max(m1, 0.)*n2
        d2 = s2+f2
        m2 = m1 + p2[kount] - r2 - d2
        # print(d2, s2, f2, m2)
        ts_mt[kount] = m2
        ts_dt[kount] = d2
        ts_u[kount] = (np.sqrt(q2[kount]) - np.sqrt(d2))
        m1 = m2
        # print(kount)
    print('Media mt ---------------> ', np.average(ts_mt))
    print('Media u ----------------> ', np.average(ts_u),
          np.average(out.residual))

report_fit(out)

"""
Plota a grade de parametros
"""

pngfigplot = '/dados/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/plots/plotaBruteParams.png'


# pngfigplot = '/home/evandro/lcbiag/' \
#     'ProcessoOtimizacaoModelos/calibracaoBalagua/' \
#     'plots/plotaBruteParams.png'

plot_results_brute(out, best_vals=True, varlabels=None,
                   output=pngfigplot)
# plot_results_brute(out, best_vals=True, varlabels=None, output=None)
