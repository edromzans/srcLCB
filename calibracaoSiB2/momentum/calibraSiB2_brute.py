import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from sib2pymod import sib2
import pickle
import time

data2 = '/home/evandro/src_codes/LCB/srcLCB/calibracaoSiB2/momentum/' \
    'data2'

dadosobs = pd.read_table(
        data2, header=0, delim_whitespace=True, names=[
            'datetime', 'Ki', 'em', 'tm', 'um', 'prec',
            'Rn', 'ustar', 'Ho', 'LEo'])

ustar_o = dadosobs.ustar

# verifica dados validos
posval = np.asarray(ustar_o > -9999.).nonzero()
posval = posval[0]

ustar_o = ustar_o[posval]

nlinha = len(dadosobs)


def residualSiB2(params, ustar_o, posval, nlinha):

    z0d_param = params['z0d']
    dd_param = params['dd']
    cc1_param = params['cc1']
    cc2_param = params['cc2']

    '''
    Roda o SiB2
    '''

    ustar_c = sib2(z0d_param, dd_param, cc1_param, cc2_param, nlinha)

    ustar_c = ustar_c[posval]

    # print(len(Rn_O), len(Rn_C))
    # time.sleep(5)
    # print(params)
    modeloerro = ustar_o - ustar_c

    # remove os 30 primeiros valores calculados
    modeloerro = modeloerro[30:-1]
    # print(modeloerro)
    return modeloerro


z0d_min = 0.5
z0d_max = 2.5
z0d_ngrid = 8.
z0d_step = (z0d_max - z0d_min) / z0d_ngrid

dd_min = 20.
dd_max = 30.
dd_ngrid = 8.
dd_step = (dd_max - dd_min) / dd_ngrid

cc1_min = 1.
cc1_max = 15.
cc1_ngrid = 5.
cc1_step = (cc1_max - cc1_min) / cc1_ngrid

cc2_min = 100.
cc2_max = 1000.
cc2_ngrid = 5.
cc2_step = (cc2_max - cc2_min) / cc2_ngrid

params = Parameters()
params.add('z0d', min=z0d_min, max=z0d_max, brute_step=z0d_step)
params.add('dd', min=dd_min, max=dd_max, brute_step=dd_step)
params.add('cc1', min=cc1_min, max=cc1_max, brute_step=cc1_step)
#           value=0.110, vary=False)
params.add('cc2', min=cc2_min, max=cc2_max, brute_step=cc2_step)
#           value=0.225, vary=False)

otimiza = Minimizer(residualSiB2, params, fcn_args=(ustar_o, posval, nlinha))

out = otimiza.brute(workers=8)

# dirMR = '/vol0/evandro/resultados/'
# dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/resultados/'

dirMR = '/dados/ProcessoOtimizacaoModelos/SiB2/resultados/'

pickle.dump(out, open(dirMR+'sib2_momentum_bruteMinimizerResult.pkl', 'wb'))

report_fit(out)
