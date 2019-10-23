import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
import matplotlib.pyplot as plt


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
        m1 = m2
        return modeloerro


"""
Processo de otimizacao de parametros
"""

params = Parameters()
params.add('a1', min=0., max=1., brute_step=0.2)
params.add('a2', min=0., max=1., brute_step=0.05)
params.add('a22', min=0.5, max=2., brute_step=0.5)
params.add('a3', min=1e-04, max=8e-04, brute_step=0.05e-04)

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

otimiza = Minimizer(residual, params, reduce_fcn=None, calc_covar=True)
out = otimiza.brute(workers=-1)


# report_fit(out.params)
report_fit(out)

"""
Verificacao dos parametros caculados
"""
a1 = out.params['a1']
a2 = out.params['a2']
a22 = out.params['a22']
a3 = out.params['a3']
#
dadosobs = pd.read_table(
    'input.txt', header=None, delim_whitespace=True, names=[
        'ano', 'mes', 'dia', 'hora', 'minuto', 'segundo',
        'etp', 'p2', 'q2', 'escb'])
m_func = len(dadosobs)
modeloerro = np.zeros(m_func, dtype='float64')
#
ts_mt = np.zeros(m_func, dtype='float64')
ts_dt = np.zeros(m_func, dtype='float64')
ts_u = np.zeros(m_func, dtype='float64')
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
    # print(d2, s2, f2, m2)
    ts_mt[kount] = m2
    ts_dt[kount] = d2
    ts_u[kount] = (np.sqrt(q2[kount]) - np.sqrt(d2))
    m1 = m2
    # print(s2)
print('---------------> ', np.average(ts_mt))

x_eixo = np.arange(m_func)

plt.subplot(3, 2, 1)
plt.plot(x_eixo, ts_mt, '.-')
plt.xlabel('Unidade de tempo')
plt.ylabel('m_t')

plt.subplot(3, 2, 2)
plt.scatter(q2, ts_u)
plt.xlabel('q')
plt.ylabel('u')

plt.subplot(3, 2, 3)
plt.plot(x_eixo, q2, label='q_t')
plt.plot(x_eixo, ts_dt, label='d_t')
# plt.xlabel('q')
# plt.ylabel('d_t')
plt.legend()

plt.subplot(3, 2, 4)
plt.hist(ts_u, bins='auto')
plt.xlabel('u')
plt.ylabel('ocorrencias')

plt.show()
