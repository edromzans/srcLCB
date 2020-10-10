import pandas as pd
import numpy as np
from lmfit import report_fit  # Minimizer, Parameters,
from lmfit.models import GaussianModel
import matplotlib.pyplot as plt
import pickle
import calendar
from scipy import signal

# UGRHI SP
# tagname = '58220000'
# -------------------------
# tagname = '3D-001'
# -------------------------
# tagname = '4C-007'
# -------------------------
# tagname = '4B-015'
# -------------------------
tagname = '5B-011'
# -------------------------

dirInput = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/InstrucaoModBalagua/dados/ugrhi_sp/'

dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/InstrucaoModBalagua/resultados/'

dirplot = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/InstrucaoModBalagua/plots/'

# CRU
arqvminres = tagname+'_ugrhi_leastsqMinimizerResult.pkl'
input_df = pd.read_pickle(dirInput+tagname+'_ugrhi_sp.pkl')

# Xavier
# arqvminres = tagname+'_xavier_ugrhi_leastsqMinimizerResult.pkl'
# input_df = pd.read_pickle(dirInput+tagname+'_xavier_ugrhi_sp.pkl')

out_leastsq = pickle.load(open(dirMR + arqvminres, "rb"))

"""
Modelagem do balanco de agua com os parametros otimos
"""
a1 = out_leastsq.params['a1']
a2 = out_leastsq.params['a2']
a22 = out_leastsq.params['a22']
a3 = out_leastsq.params['a3']

etp = np.asarray(input_df.etp)
p2 = np.asarray(input_df.p)
q2 = np.asarray(input_df.q)

# where
posval = np.asarray(~np.isnan(etp) &
                    ~np.isnan(p2) &
                    ~np.isnan(q2)).nonzero()
posval = posval[0]

datatempo = input_df.index

nxts = len(input_df)

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
    s2 => escoamento lento
    n2 => precipitacao ativa
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
Visualicao dos dados
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

# Para agrupamentos mensais/anuais
# d_mes = dict(enumerate(calendar.month_abbr))
dados = {'ETP': etp, 'ET': ts_r, 'P': p2,
         'Qm': q2, 'Qc': ts_dt, 'S': ts_mt, 'DeltaS': ts_Dm,
         'mes': x_eixo.month}
toanual_df = pd.DataFrame(data=dados, index=x_eixo)
# totanual = toanual_df.resample('Y').sum()
totanual = toanual_df.resample('Y').agg(np.nansum)
medianual = toanual_df.resample('Y').agg(np.nanmean)
nantotanual = toanual_df.isnull().resample('Y').agg(np.sum)


'''
Plota paineis de verificacao
'''

'''
Figura series temporais
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

plt.subplot(7, 1, 1)
plt.title(tagname, fontsize=10)
plt.plot(x_eixo, ts_mt, '.-')
plt.ylabel('S\n(mm/mês)')
plt.xlim(xi, xf)

plt.subplot(7, 1, 2)
plt.plot(x_eixo, ts_Dm, '.-')
plt.ylabel('(S-S$_{-1})$\n(mm/mês)')
plt.xlim(xi, xf)

# considera os anos com falhas nas medidas menores do que 3 meses
posval9 = np.asarray((nantotanual.DeltaS < 3.)).nonzero()
posval9 = posval9[0]

x_eixo_ano_ts = totanual.index
nxano = len(x_eixo_ano_ts)
DeltaS_ano_ts = np.empty(nxano)
DeltaS_ano_ts.fill(np.nan)

DeltaS_ano_ts[posval9] = totanual.DeltaS[posval9]

plt.subplot(7, 1, 3)
#plt.plot(x_eixo, ts_mt, '.-')
plt.plot(x_eixo_ano_ts, DeltaS_ano_ts, '.-')
plt.ylabel('S\n(mm/ano)')
plt.xlim(xi, xf)

ax1 = plt.subplot(7, 1, 4)
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

# Anual
qm_anual = np.asarray(medianual.Qm)
qc_anual = np.asarray(medianual.Qc)
p_anual = np.asarray(medianual.P)

ax1 = plt.subplot(7, 1, 5)
ax1.plot(x_eixo_ano_ts, qm_anual, 'black', label='Q$_m$', linewidth=0.8)
ax1.plot(x_eixo_ano_ts, qc_anual, 'red', label='Q$_c$', linewidth=0.8)
plt.ylabel('(mm/ano)')
plt.xlim(xi, xf)

ax2 = ax1.twinx()
ax2.plot(x_eixo_ano_ts, p_anual, 'b', label='P', linewidth=0.8)
plt.ylabel('P (mm/ano)', axes=ax2)
plt.xlim(xi, xf)

ax2.legend(loc='upper right')
ax1.legend(loc='upper left')


plt.subplot(7, 1, 6)
plt.plot(x_eixo, ts_r, 'g', label='ET', linewidth=0.8)
plt.plot(x_eixo, etp, 'black', label='ETP', linewidth=0.8)
plt.ylabel('(mm/mês)')
plt.xlim(xi, xf)
plt.legend()

# Anual
ET_anual = np.asarray(medianual.ET)
ETP_anual = np.asarray(medianual.ETP)
plt.subplot(7, 1, 7)
plt.plot(x_eixo_ano_ts, ET_anual, 'g', label='ET', linewidth=0.8)
plt.plot(x_eixo_ano_ts, ETP_anual, 'black', label='ETP', linewidth=0.8)
plt.ylabel('(mm/ano)')
plt.xlim(xi, xf)
plt.legend()

plt.savefig(pngfigplot, dpi=300, bbox_inches='tight')


'''
Figura - erro do modelamento
'''

pngfigplot = dirplot+tagname+'_pltBalagua_erro.png'
fig = plt.figure()
fig.set_figwidth(7)
fig.set_figheight(4)

# semivariancia
plt.subplot(2, 1, 1)

ts_u_svar = ts_u[~np.isnan(ts_u)]

semivar = signal.correlate(ts_u_svar, ts_u_svar)
semivarplt = semivar[np.int(semivar.size/2):]
plt.plot(semivarplt)
plt.ylabel('Autocorr')
plt.xlabel('Lag')

plt.subplot(2, 1, 2)
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


# '''
# Figura anual
# '''

# pngfigplot = dirplot+tagname+'_pltBalagua_ts_anual.png'

# # considera os anos com falhas nas medidas menores do que 3 meses
# posval9 = np.asarray((nantotanual.DeltaS < 3.)).nonzero()
# posval9 = posval9[0]

# x_eixo_ano_ts = totanual.index
# nxano = len(x_eixo_ano_ts)
# DeltaS_ano_ts = np.empty(nxano)
# DeltaS_ano_ts.fill(np.nan)

# DeltaS_ano_ts[posval9] = totanual.DeltaS[posval9]

# fig = plt.figure()
# fig.set_figwidth(25)
# fig.set_figheight(18)
# # fig.suptitle(tagname)

# plt.style.use('bmh')  # ggplot dark_background classic bmh seaborn-bright

# plt.subplot(6, 1, 1)
# plt.title(tagname, fontsize=10)
# #plt.plot(x_eixo, ts_mt, '.-')
# plt.plot(x_eixo_ano_ts, DeltaS_ano_ts, '.-')
# plt.ylabel('S\n(mm/ano)')
# plt.xlim(xi, xf)


# # dados = {'ETP': etp, 'ET': ts_r, 'P': p2,
# #          'Qm': q2, 'Qc': ts_dt, 'S': ts_mt, 'DeltaS': ts_Dm,
# #          'mes': x_eixo.month}
# # toanual_df = pd.DataFrame(data=dados, index=x_eixo)
# # # totanual = toanual_df.resample('Y').sum()
# # totanual = toanual_df.resample('Y').agg(np.nansum)
# # medianual = toanual_df.resample('Y').agg(np.nanmean)
# # nantotanual = toanual_df.isnull().resample('Y').agg(np.sum)

# qm_anual = np.asarray(medianual.Qm)
# qc_anual = np.asarray(medianual.Qc)
# p_anual = np.asarray(medianual.P)

# ax1 = plt.subplot(6, 1, 2)
# ax1.plot(x_eixo_ano_ts, qm_anual, 'black', label='Q$_m$', linewidth=0.8)
# ax1.plot(x_eixo_ano_ts, qc_anual, 'red', label='Q$_c$', linewidth=0.8)
# plt.ylabel('(mm/ano)')
# plt.xlim(xi, xf)

# ax2 = ax1.twinx()
# ax2.plot(x_eixo_ano_ts, p_anual, 'b', label='P', linewidth=0.8)
# plt.ylabel('P (mm/ano)', axes=ax2)
# plt.xlim(xi, xf)

# ax2.legend(loc='upper right')
# ax1.legend(loc='upper left')


# ET_anual = np.asarray(medianual.ET)
# ETP_anual = np.asarray(medianual.ETP)

# plt.subplot(6, 1, 3)
# plt.plot(x_eixo_ano_ts, ET_anual, 'g', label='ET', linewidth=0.8)
# plt.plot(x_eixo_ano_ts, ETP_anual, 'black', label='ETP', linewidth=0.8)
# plt.ylabel('(mm/ano)')
# plt.xlim(xi, xf)
# plt.legend()

# plt.savefig(pngfigplot, dpi=300, bbox_inches='tight')


'''
Figura - ciclo anual
'''

pngfigplot = dirplot+tagname+'_pltBalagua_cicloanual.png'


canual = toanual_df.groupby('mes').agg(np.nanmean)

d_mes = dict(enumerate(calendar.month_abbr))
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

'''
Terceira figura
'''

pngfigplot = dirplot+tagname+'_pltBalagua_dispersao.png'


fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(9)

plt.subplot(221)

#  where
q2 = np.asarray(q2)
posval3 = np.asarray(~np.isnan(q2) |
                     ~np.isnan(ts_dt)).nonzero()
posval3 = posval3[0]
q2_plt = q2[posval3]
ts_dt_plt = ts_dt[posval3]

minv = np.nanmin(np.concatenate((q2_plt, ts_dt_plt)))
maxv = np.nanmax(np.concatenate((q2_plt, ts_dt_plt)))
xx = np.arange(minv, maxv)
yy = xx
plt.plot(xx, yy, c='green', linewidth=0.8)
plt.scatter(q2_plt, ts_dt_plt, c='black', marker='+', linewidth=0.8)
plt.ylabel('Q$_c$ (mm/mês)')
plt.xlabel('Q$_m$ (mm/mês)')

plt.subplot(222)
posval4 = np.asarray(~np.isnan(ts_r) |
                     ~np.isnan(etp)).nonzero()
posval4 = posval4[0]
ts_r_plt = ts_r[posval4]
etp_plt = etp[posval4]

minv = np.nanmin(np.concatenate((ts_r_plt, etp_plt)))
maxv = np.nanmax(np.concatenate((ts_r_plt, etp_plt)))
xx = np.arange(minv, maxv)
yy = xx
plt.plot(xx, yy, c='green', linewidth=0.8)
plt.scatter(etp_plt, ts_r_plt, c='black', marker='+', linewidth=0.8)
plt.xlabel('ETP (mm/mês)')
plt.ylabel('ET (mm/mês)')

plt.subplot(223)
posval5 = np.asarray((nantotanual.Qm < 1.) & (nantotanual.P < 1.)).nonzero()
posval5 = posval5[0]
Qm_ano_plt = totanual.Qm[posval5]
P_ano_plt = totanual.P[posval5]

posval6 = np.asarray((nantotanual.Qc < 1.) & (nantotanual.P < 1.)).nonzero()
posval6 = posval6[0]
Qc_ano_plt = totanual.Qc[posval6]
P_ano_plt = totanual.P[posval6]

posval7 = np.asarray((nantotanual.ET < 1.) & (nantotanual.P < 1.)).nonzero()
posval7 = posval7[0]
ET_ano_plt = totanual.ET[posval7]

minv = np.nanmin(np.concatenate((
    P_ano_plt, Qm_ano_plt, Qc_ano_plt, ET_ano_plt)))
maxv = np.nanmax(np.concatenate((
    P_ano_plt, Qm_ano_plt, Qc_ano_plt, ET_ano_plt)))
xx = np.arange(minv, maxv)
yy = xx

plt.plot(xx, yy, c='green', linewidth=0.8)
plt.scatter(P_ano_plt, ET_ano_plt, c='red', marker='1',
            linewidth=0.8, label='ET')
plt.scatter(P_ano_plt, Qc_ano_plt, c='blue', marker='.',
            linewidth=0.8, label='Q$_c$')
plt.scatter(P_ano_plt, Qm_ano_plt, c='black', marker='+',
            linewidth=0.8, label='Q$_m$')
plt.ylabel('(mm/ano)')
plt.xlabel('P (mm/ano)')
plt.legend()

plt.subplot(224)

posval8 = np.asarray((nantotanual.DeltaS < 1.)
                     & (nantotanual.P < 1.)).nonzero()
posval8 = posval8[0]
DeltaS_ano_plt = totanual.DeltaS[posval8]
P_ano_plt = totanual.P[posval8]

plt.scatter(P_ano_plt, DeltaS_ano_plt, c='black', marker='+', linewidth=0.8)
plt.ylabel('S-S$_{-ano}$ (mm/ano)')
plt.xlabel('P (mm/ano)')

plt.savefig(pngfigplot, dpi=300, bbox_inches='tight')

plt.show()



















# # Salva resultados para plots

# pickle.dump((out_leastsq,
#              x_eixo,
#              ts_mt,
#              ts_dt,
#              ts_u,
#              ts_Dm,
#              ts_r,
#              q2,
#              p2,
#              etp,
#              xhist,
#              hist_u,
#              gresult),
#             # open(dirR+tagname+'_ugrhi_leastsqMinimizerResult.pkl',
#             # 'wb'))
#             open(dirR+tagname+'_xavier_ugrhi_leastsqMinimizerResult.pkl',
#                  'wb'))
