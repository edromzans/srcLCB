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

arqvMR = tagname+'_ugrhi_bruteMinimizerResult.pkl'

df_balagua_model = pd.read_pickle(dirInput+tagname+'_ugrhi_sp.pkl')

etp = df_balagua_model.penmanmonteith.values
p2 = df_balagua_model.prec.values
q2 = df_balagua_model.vazao.values

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
    m1 = np.float64(500.)  # estimativa de m1 inicial
    r2 = np.float64(0.)
    s2 = np.float64(0.)
    n2 = np.float64(0.)
    d2 = np.float64(0.)
    m2 = np.float64(0.)
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


outbrute = pickle.load(open(dirMR + arqvMR, "rb"))

a1_bruteMR = outbrute.params['a1']
a2_bruteMR = outbrute.params['a2']
a22_bruteMR = outbrute.params['a22']
a3_bruteMR = outbrute.params['a3']

print(a1_bruteMR, a2_bruteMR, a22_bruteMR, a3_bruteMR,
      '<-----Resultado MR brute')

# Leastsq com resultado da grade de parametros - metodo bruto
params = Parameters()
params.add('a1', value=a1_bruteMR, min=0., max=1.)
params.add('a2', value=a2_bruteMR)
params.add('a22', value=a22_bruteMR, vary=False)
params.add('a3', value=a3_bruteMR)

otimiza = Minimizer(residual, params,
                    reduce_fcn=None,
                    calc_covar=True,
                    fcn_args=(etp, p2, q2))

# out_leastsq = otimiza.leastsq()
out_leastsq = otimiza.minimize(method='leastsq')  # Levenberg-Marquardt

# report_fit(out_leastsq.params)
report_fit(out_leastsq)

pickle.dump(out_leastsq,
            open(dirMR+tagname+'_ugrhi_leastsqMinimizerResult.pkl',
                 'wb'))

