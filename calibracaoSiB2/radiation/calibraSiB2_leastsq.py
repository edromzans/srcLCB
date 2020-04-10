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

    tran_1_1 = params['tran_11']
    tran_2_1 = params['tran_21']
    tran_1_2 = params['tran_12']
    tran_2_2 = params['tran_22']
    ref_1_1 = params['ref_11']
    ref_2_1 = params['ref_21']
    ref_1_2 = params['ref_12']
    ref_2_2 = params['ref_22']
    soref_1 = params['soref_1']
    soref_2 = params['soref_2']
    chil_param = params['chil']

    # print(p_trans_viva_nir, p_ref_viva_nir, p_ref_solo_par, p_ref_solo_nir)
    print(params)

    '''
    Roda o SiB2
    '''

    Rn_C = sib2(tran_1_1, tran_2_1, tran_1_2, tran_2_2,
                ref_1_1, ref_2_1, ref_1_2, ref_2_2, soref_1, soref_2,
                chil_param, nlinha)

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
params.add('tran_11', value=0.0170, max=0.2, min=0.01)
params.add('tran_21', value=0.2000, max=0.6, min=0.01)
params.add('tran_12', value=0.0010, max=0.5, min=0.0001)  # , vary=False)
params.add('tran_22', value=0.0010, max=0.5, min=0.0001)
params.add('ref_11', value=0.0700, max=0.2, min=0.01)
params.add('ref_21', value=0.5000, max=0.8, min=0.01)
params.add('ref_12', value=0.1600, max=0.4, min=0.01)
params.add('ref_22', value=0.3900, max=0.6, min=0.01)
params.add('soref_1', value=0.110, max=0.3, min=0.01)
params.add('soref_2', value=0.225, max=0.4, min=0.01)
params.add('chil', value=0.1, max=0.2, min=0.05)

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
