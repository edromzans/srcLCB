import pandas as pd
import numpy as np
from lmfit import report_fit  # Minimizer, Parameters,
from lmfit.models import GaussianModel
import matplotlib.pyplot as plt
import pickle
import calendar
from scipy import signal

dirInput = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/ugrhi_sp/'

dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/InstrucaoModBalagua/resultados/'

# Bacias Hidrograficas SP
# -------------------------
tagname = 'pcj_bacia_hid_3D-002'
# -------------------------

dirplot = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/InstrucaoModBalagua/plots/'


arqvMRleastsq = tagname+'_ugrhi_leastsqMinimizerResult.pkl'
df_balagua_model = pd.read_pickle(dirInput+tagname+'_ugrhi_sp.pkl')
out_leastsq = pickle.load(open(dirMR + arqvMRleastsq, "rb"))

"""
Verificacao dos parametros caculados
"""
a1 = out_leastsq.params['a1']
a2 = out_leastsq.params['a2']
a22 = out_leastsq.params['a22']
a3 = out_leastsq.params['a3']

etp = df_balagua_model.penmanmonteith.values
p2 = df_balagua_model.prec.values
q2 = df_balagua_model.vazao.values

# where
posval = np.asarray(~np.isnan(etp) &
                    ~np.isnan(p2) &
                    ~np.isnan(q2)).nonzero()
posval = posval[0]

datatempo = df_balagua_model.index

nxts = len(df_balagua_model)

ts_mt = np.empty(nxts)
ts_dt = np.empty(nxts)
ts_u = np.empty(nxts)
ts_Dm = np.empty(nxts)
ts_r = np.empty(nxts)
ts_mt.fill(np.nan)
ts_dt.fill(np.nan)
ts_u.fill(np.nan)
ts_Dm.fill(np.nan)
ts_r.fill(np.nan)

m1 = np.float64(500.)
r2 = np.float64(0.)
s2 = np.float64(0.)
n2 = np.float64(0.)
d2 = np.float64(0.)
m2 = np.float64(0.)

m_func = len(posval)

for kount in range(0, m_func):
    """
    Modelo de balanço de agua

    r2 => evapotranpiracao real
    n2 => precipitacao ativa
    s2 => escoamento lento
    f2 => escoamento rapido
    d2 => vazao com filtro
    """
    posck = posval[kount]

    r2 = min(
        etp[posck]*(1.-a1**((p2[posck]+max(m1, 0.))/etp[posck])),
        (p2[posck]+max(m1, 0.))
    )
    s2 = a2*(max(m1, 0.)**a22)
    n2 = p2[posck]-etp[posck]*(1-np.exp(-p2[posck]/etp[posck]))
    f2 = a3*max(m1, 0.)*n2
    d2 = s2+f2
    m2 = m1 + p2[posck] - r2 - d2
    # print(d2, s2, f2, m2)
    ts_mt[posck] = m2
    ts_dt[posck] = d2
    ts_u[posck] = (np.sqrt(q2[posck]) - np.sqrt(d2))
    ts_Dm[posck] = m2 - m1
    ts_r[posck] = r2

    m1 = m2

'''
Saidas
'''

x_eixo = datatempo

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

'''
Plota paineis de verificacao
'''

# where
posval2 = np.asarray(~np.isnan(etp) &
                     ~np.isnan(p2) &
                     ~np.isnan(q2)).nonzero()
posval2 = posval2[0]

xi = x_eixo[posval2[0]]
xf = x_eixo[posval2[-1]]

# xi = np.datetime64('2014-01-01')
# xf = np.datetime64('2016-08-01')

pngfigplot = dirplot+tagname+'_pltBalagua_ts.png'

# report_fit(out_leastsq)
# print(gresult.fit_report())

fig = plt.figure()
fig.set_figwidth(25)
fig.set_figheight(18)
# fig.suptitle(tagname)

plt.style.use('bmh')  # ggplot dark_background classic bmh seaborn-bright

plt.subplot(6, 1, 1)
plt.title(tagname, fontsize=10)
plt.plot(x_eixo, ts_mt, '.-')
plt.ylabel('S\n(mm/mês)')
plt.xlim(xi, xf)

plt.subplot(6, 1, 2)
plt.plot(x_eixo, ts_Dm, '.-')
plt.ylabel('(S-S$_{-1})$\n(mm/mês)')
plt.xlim(xi, xf)

ax1 = plt.subplot(6, 1, 3)
ax1.plot(x_eixo, q2, 'black', label='Q$_m$', linewidth=0.8)
ax1.plot(x_eixo, ts_dt, 'red', label='Q$_c$', linewidth=0.8)
plt.ylabel('(mm/mês)')
plt.xlim(xi, xf)

ax2 = ax1.twinx()
ax2.plot(x_eixo, p2, 'b', label='P', linewidth=0.8)
plt.ylabel('P (mm/mês)', axes=ax2)
plt.xlim(xi, xf)

ax2.legend(loc='upper right')
ax1.legend(loc='upper left')

plt.subplot(6, 1, 4)
plt.plot(x_eixo, ts_r, 'g', label='ET', linewidth=0.8)
plt.plot(x_eixo, etp, 'black', label='ETP', linewidth=0.8)
plt.ylabel('(mm/mês)')
plt.xlim(xi, xf)
plt.legend()

# semivariancia
plt.subplot(6, 1, 5)

ts_u_svar = ts_u[~np.isnan(ts_u)]

semivar = signal.correlate(ts_u_svar, ts_u_svar)
semivarplt = semivar[np.int(semivar.size/2):]
plt.plot(semivarplt)
plt.ylabel('Autocorr')
plt.xlabel('Lag')

plt.subplot(6, 1, 6)
plt.scatter(xhist, hist_u)
plt.plot(xhist, gresult.best_fit, 'r-', label='Gaussiana')
plt.ylabel('Prob')
plt.legend()
corrperson = np.corrcoef(hist_u, gresult.best_fit)
corrperson = corrperson[0, 1]
plt.text(2.5, np.max(hist_u)/2.,
         'C(prob, gauss) = '+'{:5.3f}'.format(corrperson), wrap=True)
print('correlacao de pearson')
print(np.corrcoef(hist_u, gresult.best_fit))

plt.savefig(pngfigplot, dpi=300, bbox_inches='tight')

'''
Segunda figura
'''

pngfigplot = dirplot+tagname+'_pltBalagua_cicloanual.png'

d_mes = dict(enumerate(calendar.month_abbr))

dados = {'ETP': etp, 'ET': ts_r, 'P': p2,
         'Qm': q2, 'Qc': ts_dt, 'S': ts_mt, 'DeltaS': ts_Dm,
         'mes': x_eixo.month}
toanual_df = pd.DataFrame(data=dados, index=x_eixo)

canual = toanual_df.groupby('mes').agg(np.nanmean)

canual.index = canual.index.map(d_mes)  # .str.slice(stop=3)

fig = plt.figure()
fig.set_figwidth(6)
fig.set_figheight(6)

plt.style.use('bmh')  # ggplot dark_background classic bmh seaborn-bright
# plt.rcParams.update({'font.size': 10})

ax1 = plt.subplot(311)
ax1.plot(canual.Qm, label='Q$_m$')
ax1.plot(canual.Qc, label='Q$_c$')
plt.ylabel('(mm/mês)')

ax2 = ax1.twinx()
ax2.plot(canual.P, 'black', label='P')
plt.ylabel('(mm/mês)')
ax2.legend(loc='upper right')
ax1.legend(loc='upper left')

ax1 = plt.subplot(312)
ax1.plot(canual.ET, label='ET')
ax1.plot(canual.ETP, label='ETP')
plt.ylabel('(mm/mês)')

ax2 = ax1.twinx()
ax2.plot(canual.P, 'black', label='P')
plt.ylabel('(mm/mês)')
ax2.legend(loc='upper right')
ax1.legend(loc='upper left')

ax1 = plt.subplot(313)
ax1.plot(canual.S, label='S')
plt.ylabel('(mm/mês)')

ax2 = ax1.twinx()
ax2.plot(canual.P, 'black', label='P')
plt.ylabel('(mm/mês)')
ax2.legend(loc='upper right')
ax1.legend(loc='upper left')

plt.savefig(pngfigplot, dpi=300, bbox_inches='tight')

plt.show()
