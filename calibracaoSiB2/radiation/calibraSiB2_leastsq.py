import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from sib2pymod import sib2
import pickle
import time

# data2 = '/dados/ProcessoOtimizacaoModelos/SiB2/input/radiative/' \
#     'data2'

# dadosobs = pd.read_table('data2', header=0, delim_whitespace=True, names=[
#             'datetime', 'Ki', 'em', 'tm', 'um', 'prec', 'Rn'])

# dadosobs = pd.read_table('data3.csv', delim_whitespace=True)
dadosobs = pd.read_csv('data3.csv')

# print(dadosobs)
# time.sleep(30)

Rn_O = dadosobs.Rn
# verifica dados validos
posval = np.asarray(Rn_O > -9999.).nonzero()
posval = posval[0]
Rn_O = Rn_O[posval]

nlinha = len(dadosobs)
# print(nlinha, ' <--------- nlinha')


def residualSiB2(params, Rn_O, posval, nlinha):

    p_trans_viva_nir = params['TVN']
    p_ref_viva_nir = params['RVN']
    p_ref_solo_par = params['RSOLOP']
    p_ref_solo_nir = params['RSOLON']

    trans_viva_nir = p_trans_viva_nir * 1.
    ref_viva_nir = p_ref_viva_nir * 1.
    ref_solo_par = p_ref_solo_par * 1.
    ref_solo_nir = p_ref_solo_nir * 1.

    # print(p_trans_viva_nir, p_ref_viva_nir, p_ref_solo_par, p_ref_solo_nir)
    print(params)

    '''
    Roda o SiB2
    '''

    Rn_C = sib2(trans_viva_nir, ref_viva_nir, ref_solo_par, ref_solo_nir,
                nlinha)

    Rn_C = Rn_C[posval]

    # print(len(Rn_O), len(Rn_C))
    # time.sleep(5)
    # print(params)

    modeloerro = Rn_O - Rn_C

    # remove os 30 primeiros valores calculados
    # modeloerro = modeloerro[30:]
    # print(modeloerro)
    return modeloerro


params = Parameters()
params.add('TVN', value=0.200, max=0.9, min=0.01)
params.add('RVN', value=0.500, max=0.9, min=0.01)
params.add('RSOLOP', value=0.110, max=0.9, min=0.01)  # , vary=False)
params.add('RSOLON', value=0.225, max=0.9, min=0.01)  # , vary=False)

otimiza = Minimizer(residualSiB2, params,
                    reduce_fcn=None,
                    calc_covar=True,
                    fcn_args=(Rn_O, posval, nlinha))

# out_leastsq = otimiza.leastsq()
out_leastsq = otimiza.minimize(method='leastsq')  # Levenberg-Marquardt

# report_fit(out_leastsq.params)

print('###################################################')
print('Modulo: Radiacao')
print('---Parametros---')
params.pretty_print()
print('---Otimizacao---')
report_fit(out_leastsq)
