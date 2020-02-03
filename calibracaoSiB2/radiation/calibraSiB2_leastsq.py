import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from sib2pymod import sib2
import pickle

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

    print(p_trans_viva_nir, p_ref_viva_nir, p_ref_solo_par, p_ref_solo_nir)

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


# Leastsq com resultado da grade de parametros - metodo bruto
params = Parameters()
params.add('TVN', value=0.266)
params.add('RVN', value=0.440)
params.add('RSOLOP', value=0.110, vary=False)
params.add('RSOLON', value=0.225, vary=False)

otimiza = Minimizer(residualSiB2, params,
                    reduce_fcn=None,
                    calc_covar=True,
                    fcn_args=(Rn_O, nlinha))

# out_leastsq = otimiza.leastsq()
out_leastsq = otimiza.minimize(method='leastsq')  # Levenberg-Marquardt

# report_fit(out_leastsq.params)
report_fit(out_leastsq)
