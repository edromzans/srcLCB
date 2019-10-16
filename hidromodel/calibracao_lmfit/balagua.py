import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
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
    m1 = np.float64(np.float64(500.))
    r2 = np.float64(0)
    s2 = np.float64(0)
    n2 = np.float64(0)
    d2 = np.float64(0)
    m2 = np.float64(0)
    for kount in range(0, m_func):
        """
        Modelo de balanço de agua

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
        #
        # print *,  etp[kount], p2[kount], q2[kount], escb[kount]
        # print *, 'parametros: ', x_a
        # !print *, '----->', q2[kount], d2, abs(q2[kount]-d2)
        #
        m2 = m1 + p2[kount] - r2 - d2
        #
        # modeloerro[kount] = np.sqrt(q2[kount]) - np.sqrt(d2)
        #
        modeloerro[kount] = q2[kount] - d2
        #
        print(d2, s2, f2, m2)
        #
        m1 = m2
    return modeloerro
params = Parameters()
params.add('a1', min=0.0005, max=1.)
params.add('a2', value=0.002)
params.add('a22', min=0.5, max=2.)
params.add('a3', value=0.00001)
# params = Parameters()
# params.add('a1', value=0.5, vary=False)
# params.add('a2',value=0.002)
# params.add('a22', value=1., vary=False)
# params.add('a3',value=0.000001)
otimiza = Minimizer(residual, params)
out = otimiza.leastsq()
report_fit(out.params)
