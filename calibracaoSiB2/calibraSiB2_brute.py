import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from sib2pymod import sib2
import pickle
import time

import matplotlib.pyplot as plt

# data2 = '/dados/ProcessoOtimizacaoModelos/calibraSiB2/' \
#     'data2'
data2 = '/home/evandro/srcodes/LCBtools/calibracaoSiB2/' \
    'data2'

dadosobs = pd.read_table(
        data2, header=0, delim_whitespace=True, names=[
            'datetime', 'Ki', 'em', 'tm', 'um', 'prec', 'Rn', 'Ho', 'LEo'])

Rn_O = dadosobs.Rn

# nlinha = 78888
# trans_viva = 0.0170  # 0.0170
# trans_seca = 0.2000
# ref_viva = 0.0010
# ref_seca = 0.0010
# Rn_C = sib2(trans_viva, trans_seca, ref_viva, ref_seca,
#             nlinha)

nlinha = 78888

def residualSiB2(params, Rn_O, nlinha):

    p_trans_viva = params['tv']
    p_trans_seca = params['ts']
    p_ref_viva = params['rv']
    p_ref_seca = params['rs']

    trans_viva = p_trans_viva * 1.
    trans_seca = p_trans_seca * 1.
    ref_viva = p_ref_viva * 1.
    ref_seca = p_ref_seca * 1.

    # print('{:<8.3f}'.format(param_gradm), '{:<6.1f}'.format(param_vmax), ' <--')
    # time.sleep(5)

    '''
    Roda o SiB2
    '''

    Rn_C = sib2(trans_viva, trans_seca, ref_viva, ref_seca,
                nlinha)

    print(len(Rn_O), len(Rn_C))
    # time.sleep(5)
    modeloerro = Rn_O - Rn_C

    # print(modeloerro)
    # modeloerro = LE_c/(LE_c+H_c) - LE/(LE+H)  # *ABS(LE_O(I))
    # fvec(1:m) =(((LE(1:m))/(LE(1:m)+H(1:m))) - ((LE_O(1:m))/(LE_O(1:m)+H_O(1:m))))*ABS(LE_O(I))

    return modeloerro


params = Parameters()
params.add('tv', min=0.001, max=0.5, brute_step=0.01)
params.add('ts', min=0.001, max=0.5, brute_step=0.01)
params.add('rv', min=0.001, max=0.5, brute_step=0.01)
params.add('rs', min=0.001, max=0.5, brute_step=0.01)

otimiza = Minimizer(residualSiB2, params, fcn_args=(Rn_O, nlinha))

out = otimiza.brute(workers=30)

dirMR = '/vol0/evandro/resultados/'
# dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/resultados/'
pickle.dump(out, open(dirMR+'sib2_bruteMinimizerResult.pkl', 'wb'))

report_fit(out)
