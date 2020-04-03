import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from sib2pymod import sib2
import pickle

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

    # print(len(ustar_o), len(ustar_c))
    # time.sleep(5)
    # print(params)
    # print(ustar_o)
    # print(ustar_c)
    modeloerro = ustar_o - ustar_c

    # remove os 30 primeiros valores calculados
    modeloerro = modeloerro[30:-1]  # ultimo valor nao calculado, entao [:-1]
    # print(modeloerro)
    return modeloerro


# Valores iniciais
params = Parameters()
params.add('z0d', value=1.571)  # , vary=False)
params.add('dd', value=26.606)  # , vary=False)
params.add('cc1', value=8.12)  # , vary=False)
params.add('cc2', value=727.80)  # , vary=False)

otimiza = Minimizer(residualSiB2, params,
                    reduce_fcn=None,
                    calc_covar=True,
                    fcn_args=(ustar_o, posval, nlinha))

# out_leastsq = otimiza.leastsq()
out_leastsq = otimiza.minimize(method='leastsq')  # Levenberg-Marquardt

# report_fit(out_leastsq.params)
report_fit(out_leastsq)
