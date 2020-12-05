import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from lmfit.models import GaussianModel

import matplotlib.pyplot as plt


def residual(params):
    a1 = params['a1']
    a2 = params['a2']
    a22 = params['a22']
    a3 = params['a3']

    # Jaraguari Leonardo
    entradados = '/dados/ProcessoOtimizacaoModelos/' \
        'calibracaoBalagua/dados/inputs/jaraguari_obs_ecmwf/input.txt'

    # dados p1 62600000
    # entradados = '/dados/ProcessoOtimizacaoModelos/' \
    #     'calibracaoBalagua/dados/inputs/jaraguari_obs/input.txt'

    dadosobs = pd.read_table(
        entradados, header=None, delim_whitespace=True, names=[
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
        #
        # print *,  etp[kount], p2[kount], q2[kount], escb[kount]
        # print *, 'parametros: ', x_a
        # !print *, '----->', q2[kount], d2, abs(q2[kount]-d2)
        #
        m2 = m1 + p2[kount] - r2 - d2
        #
        modeloerro[kount] = np.sqrt(q2[kount]) - np.sqrt(d2)  # Wanderwiele
        # modeloerro[kount] = np.sqrt((q2[kount] - d2)**2.)  # erro quad. med.
        # modeloerro[kount] = q2[kount] - d2
        #
        # print(d2, s2, f2, m2)
        # print('---------------->', q2[kount], d2)
        print(modeloerro[kount])
        m1 = m2
    return modeloerro

params = Parameters()
params.add('a1', value=0.543, min=0., max=1.)
params.add('a2', value=0.072)
params.add('a22', value=1.0, vary=False)  # min=0.5, max=2.)
params.add('a3', value=7.5250e-04)

# params = Parameters()
# params.add('a1', value=0.905, min=0., max=1.)
# params.add('a2', value=0.168)
# params.add('a22', value=0.5, vary=False)  # min=0.5, max=2.)
# params.add('a3', value=2.75e-05)

# params = Parameters()
# params.add('a1', value=0.905, min=0., max=1.)
# params.add('a2', value=0.174)
# params.add('a22', value=0.5, vary=False)  # min=0.5, max=2.)
# params.add('a3', value=2.5e-05)

# estatistica foi calculada
# params = Parameters()
# params.add('a1', value=0.2, min=0., max=1.)
# params.add('a2', value=0.1)
# params.add('a22', min=0.5, max=2.)
# params.add('a3', value=0.000001)

# Com spin up 
# params = Parameters()
# params.add('a1', value=0., min=0., max=1.)
# params.add('a2', value=0.2)
# params.add('a22', value=0.5, min=0.5, max=2.)
# params.add('a3', value=0.0001)

# params = Parameters()
# params.add('a1', value=0.5, vary=False)
# params.add('a2',value=0.002)
# params.add('a22', value=1., vary=False)
# params.add('a3',value=0.00001)

otimiza = Minimizer(residual, params, reduce_fcn=None, calc_covar=True)

# out = otimiza.leastsq()
out = otimiza.minimize(method='leastsq')  # Levenberg-Marquardt

# report_fit(out.params)

report_fit(out)

"""
Verificacao dos parametros caculados
"""
a1 = out.params['a1']
a2 = out.params['a2']
a22 = out.params['a22']
a3 = out.params['a3']

# Jaraguari Leonardo
entradados = '/dados/ProcessoOtimizacaoModelos/' \
   'calibracaoBalagua/dados/inputs/jaraguari_obs_ecmwf/input.txt'

# dados p1 62600000
# entradados = '/dados/ProcessoOtimizacaoModelos/' \
#      'calibracaoBalagua/dados/inputs/jaraguari_obs/input_est.txt'

dadosobs = pd.read_table(
    entradados, header=None, delim_whitespace=True, names=[
        'year', 'month', 'day', 'h', 'm', 's',
        'etp', 'p2', 'q2', 'escb'])

datatempo = pd.to_datetime(dadosobs[['year', 'month', 'day', 'h', 'm', 's']])
m_func = len(dadosobs)
modeloerro = np.zeros(m_func, dtype='float64')
#
ts_mt = np.zeros(m_func, dtype='float64')
ts_dt = np.zeros(m_func, dtype='float64')
ts_u = np.zeros(m_func, dtype='float64')
ts_Dm = np.zeros(m_func, dtype='float64')
ts_r = np.zeros(m_func, dtype='float64')
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
    # print(d2, s2, f2, m2)
    ts_mt[kount] = m2
    ts_dt[kount] = d2
    ts_u[kount] = (np.sqrt(q2[kount]) - np.sqrt(d2))
    ts_Dm[kount] = m2 - m1
    ts_r[kount] = r2

    m1 = m2
    # print(s2)

print('---------------> ', np.average(ts_mt))
print('Media u---------------> ', np.average(ts_u))



'''
Graficos
'''

x_eixo = datatempo  # np.arange(m_func)

# histograma de u
minbin = -5
maxbin = 5
nx = 30.
step = (maxbin - minbin) / nx

binarr = np.arange(nx+1)*step + minbin
hist_u, edges_u = np.histogram(ts_u, bins=binarr, density='True')

xhist = np.arange(nx)*step + minbin + step

# ajuste gaussiano
gmodel = GaussianModel()

print('parameter names: {}'.format(gmodel.param_names))
print('independent variables: {}'.format(gmodel.independent_vars))

gparams = gmodel.make_params()

gresult = gmodel.fit(hist_u, gparams, x=xhist)

print(gresult.fit_report())


plt.subplot(3, 2, 1)
plt.plot(x_eixo, ts_mt, '.-')
# plt.xlabel('Unidade de tempo')
plt.ylabel('m_t')

plt.subplot(3, 2, 2)
plt.plot(x_eixo, ts_Dm, '.-')
plt.ylabel('Dm/Dt')
# plt.scatter(q2, ts_u)
# plt.xlabel('q')
# plt.ylabel('u')

plt.subplot(3, 2, 3)
plt.plot(x_eixo, q2, label='q_t')
plt.plot(x_eixo, ts_dt, label='d_t')
plt.legend()

# plt.subplot(3, 2, 4)
# plt.hist(ts_u, bins='auto')
# plt.xlabel('u')
# plt.ylabel('ocorrencias')

plt.subplot(3, 2, 4)
plt.plot(x_eixo, q2, label='q_t')
plt.plot(x_eixo, ts_dt, label='d_t')
plt.plot(x_eixo, p2, label='prec')
plt.plot(x_eixo, ts_r, label='r')

plt.legend()




plt.subplot(3, 2, 5)
plt.scatter(xhist, hist_u)
plt.plot(xhist, gresult.best_fit, 'r-', label='Gaussiana')
# plt.plot(hist_u[1], hist_u[0])
plt.legend()

print('correlacao de pearson')
print(np.corrcoef(hist_u, gresult.best_fit))

# semivariancia
plt.subplot(3, 2, 6)
dx=len(x_eixo)
semivar = np.zeros(dx)
for k in range(dx):
    semivar[k] = np.var( ts_u[0:k+1] )
semivar[0] = np.nan
plt.plot(x_eixo, semivar)
plt.ylabel('semivariancia')






plt.show()
