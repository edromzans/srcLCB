import pandas as pd
import numpy as np
# from lmfit import Minimizer, Parameters, report_fit
# a1 = 0.5
# a2 = 0.001
# a22 = 1.
# a3 = 0.001
a1 = 1.0000e-04
a2 = 0.16466918
a22 = 0.52230610
a3 = 2.8401e-05
#
dadosobs = pd.read_table(
    'input.txt', header=None, delim_whitespace=True, names=[
        'ano', 'mes', 'dia', 'hora', 'minuto', 'segundo',
        'etp', 'p2', 'q2', 'escb'])
m_func = len(dadosobs)
modeloerro = np.zeros(m_func, dtype='float64')
#
var = np.zeros(m_func, dtype='float64')
#
etp = np.float64(dadosobs['etp'])
p2 = np.float64(dadosobs['p2'])
q2 = np.float64(dadosobs['q2'])
escb = np.float64(dadosobs['escb'])
#
m1 = 500.
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
    m2 = m1 + p2[kount] - r2 - d2
    print(d2, s2, f2, m2)
    var[kount] = m2
    m1 = m2
    # print(s2)
print('---------------> ', np.average(var))
