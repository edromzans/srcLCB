import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
import pickle

# dirInput = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
#     'calibracaoBalagua/InstrucaoModBalagua/dados/ugrhi_sp/'

dirInput = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/ugrhi_sp/'

dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/InstrucaoModBalagua/resultados/'

# Bacias Hidrograficas SP
# -------------------------
tagname = 'pcj_bacia_hid_3D-002'
# -------------------------


df_balagua_model = pd.read_pickle(dirInput+tagname+'_ugrhi_sp.pkl')

etp = df_balagua_model.penmanmonteith
p2 = df_balagua_model.prec
q2 = df_balagua_model.vazao

# where
posval = np.asarray(~np.isnan(etp) &
                    ~np.isnan(p2) &
                    ~np.isnan(q2)).nonzero()
posval = posval[0]

etp = etp[posval]
p2 = p2[posval]
q2 = q2[posval]


def residual(params, etp, p2, q2):
    a1 = params['a1']
    a2 = params['a2']
    a22 = params['a22']
    a3 = params['a3']
    #
    m_func = len(etp)
    modeloerro = np.zeros(m_func, dtype='float64')
    #
    # etp = np.float64(dadosobs['etp'])
    # p2 = np.float64(dadosobs['p2'])
    # q2 = np.float64(dadosobs['q2'])
    # escb = np.float64(dadosobs['escb'])
    #
    m1 = np.float64(500.)  # estimativa de m1 inicial <<<<<------!!!!!
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

        m1 = m2

    return modeloerro


"""
Processo de otimizacao de parametros
"""
# (a1) entre 0 e 1.
a1_min = 0.6
a1_max = 0.9
a1_ngrid = 5.
a1_step = (a1_max - a1_min) / a1_ngrid

a2_min = 0.
a2_max = .3
a2_ngrid = 5.
a2_step = (a2_max - a2_min) / a2_ngrid

# (a22) Fixo!!!! 0.5, 1 ou 2
a22_min = 0.5
a22_max = 2.5
a22_ngrid = 4.
a22_step = (a22_max - a22_min) / a22_ngrid

a3_min = 5e-04
a3_max = 3e-03
a3_ngrid = 10.
a3_step = (a3_max - a3_min) / a3_ngrid

params = Parameters()
params.add('a1',  min=a1_min,  max=a1_max,  brute_step=a1_step)
params.add('a2',  min=a2_min,  max=a2_max,  brute_step=a2_step)
params.add('a22', min=a22_min, max=a22_max, brute_step=a22_step)
params.add('a3',  min=a3_min,  max=a3_max,  brute_step=a3_step)

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

otimiza = Minimizer(residual, params,
                    reduce_fcn=None,
                    calc_covar=True,
                    fcn_args=(etp, p2, q2))

out = otimiza.brute(workers=3)  # workers = numero de processadores

pickle.dump(out,
            open(dirMR+tagname+'_ugrhi_bruteMinimizerResult.pkl',
                 'wb'))
# report_fit(out.params)
report_fit(out)
