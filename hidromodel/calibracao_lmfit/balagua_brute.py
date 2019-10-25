import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
import pickle
import time


def residual(params):
    a1 = params['a1']
    a2 = params['a2']
    a22 = params['a22']
    a3 = params['a3']
    #
    dadosobs = pd.read_table(
        'input.txt', header=None, delim_whitespace=True, names=[
            'ano', 'mes', 'dia', 'hora', 'minuto', 'segundo',
            'etp', 'p2', 'q2', 'escb'])
    m_func = len(dadosobs)
    modeloerro = np.zeros(m_func, dtype='float64')
    #
    etp = np.float64(dadosobs['etp'])
    p2 = np.float64(dadosobs['p2'])
    q2 = np.float64(dadosobs['q2'])
    # escb = np.float64(dadosobs['escb'])
    #
    m1 = np.float64(np.float64(500.))  # estimativa de m1 inicial
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
        modeloerro[kount] = np.sqrt(q2[kount]) - np.sqrt(d2)  # Wanderwiele
        # modeloerro[kount] = np.sqrt((q2[kount] - d2)**2.)  # erro quad. med.
        # modeloerro[kount] = q2[kount] - d2
        # print(d2, s2, f2, m2)
        # print(kount, m_func, q2[kount], etp[kount],  d2, modeloerro[kount])
        # print(kount)
        # time.sleep(1)
        m1 = m2
    return modeloerro


"""
Processo de otimizacao de parametros
"""

params = Parameters()
params.add('a1', min=0., max=1., brute_step=0.005)
params.add('a2', min=0.0, max=2.0, brute_step=0.005)
params.add('a22', min=0.5, max=2.0, brute_step=0.5)
params.add('a3', min=0., max=1e-08, brute_step=2.5e-11)

# 9*10^6
# params = Parameters()
# params.add('a1', min=0., max=1., brute_step=0.01)
# params.add('a2', min=0.01, max=1.5, brute_step=0.0149)
# params.add('a22', min=0.5, max=2., brute_step=0.5)
# params.add('a3', min=1e-07, max=1e-02, brute_step=3.333e-05)

# params = Parameters()
# params.add('a1', min=0., max=1., brute_step=0.2)
# params.add('a2', min=0., max=1., brute_step=0.05)
# params.add('a22', min=0.5, max=2., brute_step=0.5)
# params.add('a3', min=1e-04, max=8e-04, brute_step=0.05e-04)

# params = Parameters()
# params.add('a1', min=0., max=1., brute_step=0.2)
# params.add('a2', min=0.1, max=1., brute_step=0.05)
# params.add('a22', min=0.5, max=2., brute_step=0.5)
# params.add('a3', min=9e-04, max=1e-02, brute_step=1e-04)

# # ---------------------------------------------------
# params = Parameters()
# params.add('a1', min=0., max=1., brute_step=0.2)
# params.add('a2', min=0.01, max=1., brute_step=0.01)
# params.add('a22', min=0.5, max=2., brute_step=0.5)
# params.add('a3', min=1e-04, max=9e-04, brute_step=0.01e-04)


"""
Calcula o numero de possibilidades a serem testadas
"""
pa1 = ((params['a1'].max - params['a1'].min) /
       params['a1'].brute_step)
pa2 = ((params['a2'].max - params['a2'].min) /
       params['a2'].brute_step)
pa22 = ((params['a22'].max - params['a22'].min) /
        params['a22'].brute_step)
pa3 = ((params['a3'].max - params['a3'].min) /
       params['a3'].brute_step)

print('-----------> Possibilidades <----------')
print('pa1 ', pa1)
print('pa2 ', pa2)
print('pa22 ', pa22)
print('pa3 ', pa3)
print('Total = ', pa1*pa2*pa22*pa3)




otimiza = Minimizer(residual, params, reduce_fcn=None, calc_covar=True)
out = otimiza.brute(workers=-1)

pickle.dump(out, open("save_outbruteMinimizerResult.p", "wb"))

# report_fit(out.params)
report_fit(out)
