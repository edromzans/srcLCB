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

www1_o = np.asarray(dadosobs.VW1)
# verifica dados validos
posval = np.asarray(www1_o > -9999.).nonzero()
posval = posval[0]
www1_o = www1_o[posval]

swc_o = np.asarray(dadosobs.SWC)
posval = np.asarray(swc_o > -9999.).nonzero()
posval = posval[0]
swc_o = swc_o[posval]


nlinha = len(dadosobs)
# print(nlinha, ' <--------- nlinha')


def residualSiB2(params, www1_o, swc_o, posval, nlinha):

    bee1_param = params['bee1']
    phsat1_param = params['phsat1']
    satco1_param = params['satco1']
    poros1_param = params['poros1']

    bee26_param = params['bee26']
    phsat26_param = params['phsat26']
    satco26_param = params['satco26']
    poros26_param = params['poros26']

    print(params)

    '''
    Roda o SiB2
    '''

    # www1_c = sib2(bee1_param, phsat1_param, satco1_param, poros1_param,
    #               nlinha)

    # www1_c = www1_c[posval]

    [www1, www2, www3, www4, www5, www6, www7, www8, www9, www10] = sib2(
        bee1_param, phsat1_param, satco1_param, poros1_param,
        bee26_param, phsat26_param, satco26_param, poros26_param,
        nlinha)

    www2_c = www2[posval]
    www3_c = www3[posval]
    www4_c = www4[posval]
    www5_c = www5[posval]
    www6_c = www6[posval]

    swc_c = (www2_c + www3_c + www4_c + www5_c + www6_c) / 5.

    # print(len(Rn_O), len(Rn_C))
    # time.sleep(5)
    # print(params)

    # modeloerro = www1_o - www1_c

    modeloerro = swc_o - swc_c

    # remove os 30 primeiros valores calculados
    # modeloerro = modeloerro[30:]
    print(modeloerro)
    return modeloerro


params = Parameters()
params.add('bee1', value=9.16338009, max=15.0, min=2.0, vary=False)
params.add('phsat1', value=-0.04004558, max=-0.01, min=-0.5, vary=False)
params.add('satco1', value=2.8011e-05, max=1e-04, min=1e-07, vary=False)
params.add('poros1', value=0.3, max=0.6, min=0.3, vary=False)

params.add('bee26', value=7.12, max=15.0, min=2.0)
params.add('phsat26', value=-0.2, max=-0.01, min=-0.5)
params.add('satco26', value=5e-06, max=1e-04, min=1e-07)
params.add('poros26', value=0.530, max=0.6, min=0.3)  # , vary=False)

otimiza = Minimizer(residualSiB2, params,
                    reduce_fcn=None,
                    calc_covar=True,
                    fcn_args=(www1_o, swc_o, posval, nlinha))

# out_leastsq = otimiza.leastsq()
out_leastsq = otimiza.minimize(method='leastsq')  # Levenberg-Marquardt

# report_fit(out_leastsq.params)
# report_fit(out_leastsq)

print('###################################################')
print('Modulo: Umidade do solo')
print('---Parametros---')
params.pretty_print()
print('---Otimizacao---')
report_fit(out_leastsq)
