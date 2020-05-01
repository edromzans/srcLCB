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

www1_o = np.asarray(dadosobs.SWC1)
# verifica dados validos
posval = np.asarray(www1_o > -9999.).nonzero()
posval = posval[0]
www1_o = www1_o[posval]

nlinha = len(dadosobs)
# print(nlinha, ' <--------- nlinha')


def residualSiB2(params, www1_o, posval, nlinha):

    bee1_param = params['bee1']
    phsat1_param = params['phsat1']
    satco1_param = params['satco1']
    poros1_param = params['poros1']

    print(params)

    '''
    Roda o SiB2
    '''

    www1_c = sib2(bee1_param, phsat1_param, satco1_param, poros1_param,
                  nlinha)
    www1_c = www1_c[posval]

    # print(len(Rn_O), len(Rn_C))
    # time.sleep(5)
    # print(params)

    modeloerro = www1_o - www1_c

    # remove os 30 primeiros valores calculados
    # modeloerro = modeloerro[30:]
    print(modeloerro)
    return modeloerro


bee1_min = 2.0
bee1_max = 15.0
bee1_ngrid = 3.
bee1_step = (bee1_max - bee1_min) / bee1_ngrid

phsat1_min = -0.5  
phsat1_max = -0.01
phsat1_ngrid = 3. 
phsat1_step = (phsat1_max - phsat1_min) / phsat1_ngrid

satco1_min = 1e-07
satco1_max = 1e-04
satco1_ngrid = 3.
satco1_step = (satco1_max - satco1_min) / satco1_ngrid

poros1_min = 0.3
poros1_max = 0.6 
poros1_ngrid = 3.
poros1_step = (poros1_max - poros1_min) / poros1_ngrid

params = Parameters()
params.add('bee1',   max=bee1_max   , min=bee1_min  , brute_step=bee1_step  )
params.add('phsat1', max=phsat1_max , min=phsat1_min, brute_step=phsat1_step)
params.add('satco1', max=satco1_max , min=satco1_min, brute_step=satco1_step)
params.add('poros1', max=poros1_max , min=poros1_min, brute_step=poros1_step)  # , vary=False)

otimiza = Minimizer(residualSiB2, params,
                    fcn_args=(www1_o, posval, nlinha))

out_brute = otimiza.brute(workers=3)

# report_fit(out_brute.params)
# report_fit(out_brute)

dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/SiB2/resultados/'
pickle.dump(out_brute,
            open(dirMR+'sib2_umidadesolo_bruteMinimizerResult.pkl', 'wb'))

# report_fit(out_brute.params)
# report_fit(out_brute)

print('###################################################')
print('Modulo: Umidade do solo')
print('---Parametros---')
params.pretty_print()
print('---Otimizacao---')
report_fit(out_brute)
