import pandas as pd
import numpy as np
from lmfit import report_fit
import matplotlib.pyplot as plt
import pickle

diresults = '/dados/calibracaoBalagua/resultados/'
# arqv = 'save_outbruteMinimizerResult_9mi.p'
# arqv = 'save_outbruteMinimizerResult_20191028.p'
# arqv = 'save_outbruteMinimizerResult.p'
arqv = 'save_outbruteMinimizerResult_a.p'

out = pickle.load(open(diresults+arqv, "rb"))

report_fit(out)

"""
Verificacao dos parametros caculados
"""

# verificando os candidatos
# out.candidates[0].params['a1'] 


a1 = out.params['a1']
a2 = out.params['a2']
a22 = out.params['a22']
a3 = out.params['a3']
#
entradados = '/dados/calibracaoBalagua/dados/input.txt'
dadosobs = pd.read_table(
    entradados, header=None, delim_whitespace=True, names=[
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
    # print(kount)
print('---------------> ', np.average(ts_mt))
print('Media u---------------> ', np.average(ts_u))

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
