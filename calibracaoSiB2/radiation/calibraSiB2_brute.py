import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from sib2pymod import sib2
import pickle
import time

# data2 = '/home/evandro/src_codes/LCB/srcLCB/calibracaoSiB2/ustar/' \
#     'data2'

dadosobs = pd.read_table('data2', header=0, delim_whitespace=True, names=[
            'datetime', 'Ki', 'em', 'tm', 'um', 'prec', 'Rn'])

Rn_O = np.array(dadosobs.Rn)

nlinha = len(dadosobs)


def residualSiB2(params, Rn_O, nlinha):

    p_trans_viva_nir = params['TVN']
    p_ref_viva_nir = params['RVN']
    p_ref_solo_par = params['RSOLOP']
    p_ref_solo_nir = params['RSOLON']

    trans_viva_nir = p_trans_viva_nir * 1.
    ref_viva_nir = p_ref_viva_nir * 1.
    ref_solo_par = p_ref_solo_par * 1.
    ref_solo_nir = p_ref_solo_nir * 1.

    print(trans_viva_nir, ref_viva_nir, ref_solo_par, ref_solo_nir)

    '''
    Roda o SiB2
    '''

    Rn_C = sib2(trans_viva_nir, ref_viva_nir, ref_solo_par, ref_solo_nir,
                nlinha)

    # print(len(Rn_O), len(Rn_C))
    # time.sleep(5)
    # print(params)
    modeloerro = Rn_O - Rn_C

    # remove os 30 primeiros valores calculados
    modeloerro = modeloerro[30:]

    return modeloerro


TVN_min = 0.100
TVN_max = 0.300
TVN_ngrid = 20.
TVN_step = (TVN_max - TVN_min) / TVN_ngrid

RVN_min = 0.400
RVN_max = 0.600
RVN_ngrid = 10.
RVN_step = (RVN_max - RVN_min) / RVN_ngrid

RSOLOP_min = 0.100
RSOLOP_max = 0.300
RSOLOP_ngrid = 3.
RSOLOP_step = (RSOLOP_max - RSOLOP_min) / RSOLOP_ngrid

RSOLON_min = 0.150
RSOLON_max = 0.300
RSOLON_ngrid = 3.
RSOLON_step = (RSOLON_max - RSOLON_min) / RSOLON_ngrid

params = Parameters()
params.add('TVN', min=TVN_min, max=TVN_max, brute_step=TVN_step)
params.add('RVN', min=RVN_min, max=RVN_max, brute_step=RVN_step)
params.add('RSOLOP', min=RSOLOP_min, max=RSOLOP_max, brute_step=RSOLOP_step)
#           value=0.110, vary=False)
params.add('RSOLON', min=RSOLON_min, max=RSOLON_max, brute_step=RSOLON_step)
#           value=0.225, vary=False)

otimiza = Minimizer(residualSiB2, params, fcn_args=(Rn_O, nlinha))

out = otimiza.brute(workers=40)

dirMR = '/vol0/evandro/resultados/'
# dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/resultados/'

pickle.dump(out, open(dirMR+'sib2_rad_bruteMinimizerResult.pkl', 'wb'))

report_fit(out)
