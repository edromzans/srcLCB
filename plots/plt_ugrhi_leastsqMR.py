import pandas as pd
import numpy as np
from lmfit import report_fit  # Minimizer, Parameters,
# from lmfit.models import GaussianModel
import matplotlib.pyplot as plt
import pickle
import calendar


# UGRHI SP
tagname = '58220000'
# -------------------------
# tagname = '3D-001'
# -------------------------
# tagname = '4C-007'
# -------------------------
# tagname = '4B-015'
# -------------------------
# tagname = '5B-011'

# dirR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/resultados/'
dirR = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/resultados/'
dirplot = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/plots/'
(out_leastsq,
 x_eixo, xi, xf,
 ts_mt,
 ts_dt,
 ts_u,
 ts_Dm,
 ts_r,
 q2,
 p2,
 etp,
 xhist,
 hist_u,
 gresult) = pickle.load(open(
     dirR+tagname+'_ugrhi_leastsqMinimizerResult.pkl', "rb"))

# corrigindo tempo!!!!!
xtimeM = np.array(x_eixo.to_pydatetime(), dtype='datetime64[M]')
corrig = xtimeM + np.timedelta64(9, 'M')  # + np.timedelta64(9, 'M') ou - np.timedelta64(3, 'M')
x_eixo = pd.to_datetime(corrig)

p2 = np.asarray(p2)
etp = np.asarray(etp)
q2 = np.asarray(q2)

pngfigplot = dirplot+tagname+'_pltTsBalagua_new.png'

report_fit(out_leastsq)
print(gresult.fit_report())

fig = plt.figure()
fig.set_figwidth(20)
fig.set_figheight(14)
# fig.suptitle(tagname)

plt.style.use('bmh')  # ggplot dark_background classic bmh seaborn-bright

plt.subplot(6, 1, 1)
plt.title(tagname, fontsize=10)
plt.plot(x_eixo, ts_mt, '.-')
# plt.xlabel('Unidade de tempo')
plt.ylabel('S\n(mm/mês)')
plt.xlim(xi, xf)

plt.subplot(6, 1, 2)
plt.plot(x_eixo, ts_Dm, '.-')
plt.ylabel('(S-S$_{-1})$\n(mm/mês)')
plt.xlim(xi, xf)


ax1 = plt.subplot(6, 1, 3)
# plt.plot(x_eixo, q2, label='q_t')
# plt.plot(x_eixo, ts_dt, label='d_t')
ax1.plot(x_eixo, q2, 'black', label='Q$_m$', linewidth=0.8)
ax1.plot(x_eixo, ts_dt, 'red', label='Q$_c$', linewidth=0.8)
plt.ylabel('(mm/mês)')
#ax1.plot(x_eixo, ts_r, 'g', label='ET', linewidth=0.8)
#plt.ylabel('ET (mm/mês)', axes=ax1)
plt.xlim(xi, xf)

ax2 = ax1.twinx()
ax2.plot(x_eixo, p2, 'b', label='P', linewidth=0.8)
plt.ylabel('P (mm/mês)', axes=ax2)
# fig.tight_layout()
plt.xlim(xi, xf)

ax2.legend(loc='upper right')
ax1.legend(loc='upper left')


plt.subplot(6, 1, 4)
plt.plot(x_eixo, ts_r, 'g', label='ET', linewidth=0.8)
plt.plot(x_eixo, etp, 'black', label='ETP', linewidth=0.8)
# plt.plot(x_eixo, q2, label='Q$_m$', linewidth=0.8)
# plt.plot(x_eixo, ts_dt, label='Q$_c$', linewidth=0.8)
plt.ylabel('(mm/mês)')
plt.xlim(xi, xf)
plt.legend()


# semivariancia
plt.subplot(6, 1, 5)
dx = len(x_eixo)
semivar = np.zeros(dx)
for k in range(dx):
    semivar[k] = np.nanvar(ts_u[0:k+1])
semivar[0] = np.nan
plt.plot(x_eixo, semivar)
plt.ylabel('semivar-u\n(mm/mês)')
plt.xlim(xi, xf)

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

pngfigplot = dirplot+tagname+tagname+'_pltTsBalagua_new_2.png'

d_mes = dict(enumerate(calendar.month_abbr))

dados = {'ETP': etp, 'ET': ts_r, 'P': p2,
         'Qm': q2, 'Qc': ts_dt, 'S': ts_mt, 'DeltaS': ts_Dm,
         'mes': x_eixo.month}
toanual_df = pd.DataFrame(data=dados, index=x_eixo)

canual = toanual_df.groupby('mes').agg(np.nanmean)

canual.index = canual.index.map(d_mes)  # .str.slice(stop=3)

fig = plt.figure()
# fig.set_figwidth(20)
# fig.set_figheight(14)
fig.set_figwidth(10)
fig.set_figheight(10)
# fig.suptitle(tagname)

plt.style.use('bmh')  # ggplot dark_background classic bmh seaborn-bright

plt.rcParams.update({'font.size': 12})

ax1 = plt.subplot(311)
plt.title(tagname, fontsize=10)
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

pngfigplot = dirplot+tagname+'_pltTsBalagua_new_3.png'

# totanual = toanual_df.resample('Y').sum()
totanual = toanual_df.resample('Y').agg(np.nansum)

fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(20)

plt.subplot(331)
# IDL where
q2 = np.asarray(q2)
posval = np.asarray(~np.isnan(q2) &
                    ~np.isnan(ts_dt)).nonzero()
posval = posval[0]
q2_plt = q2[posval]
ts_dt_plt = ts_dt[posval]
plt.scatter(q2_plt, ts_dt_plt)
plt.ylabel('Q$_c$ (mm/mês)')
plt.xlabel('Q$_m$ (mm/mês)')

plt.subplot(332)
plt.scatter(ts_r, etp)
plt.ylabel('ETP (mm/mês)')
plt.xlabel('ET (mm/mês)')

plt.subplot(333)
plt.scatter(totanual.Qm, totanual.P)
plt.xlabel('Q$_m$ (mm/ano)')
plt.ylabel('P (mm/ano)')

plt.subplot(334)
plt.scatter(totanual.Qc, totanual.P)
plt.xlabel('Q$_c$ (mm/ano)')
plt.ylabel('P (mm/ano)')

plt.subplot(335)
plt.scatter(totanual.ET, totanual.P)
plt.xlabel('ET (mm/ano)')
plt.ylabel('P (mm/ano)')





posjan = np.asarray(toanual_df.mes == 1).nonzero()
posjan = posjan[0]
posdez = np.asarray(toanual_df.mes == 12).nonzero()
posdez = posdez[0]

plt.subplot(336)
plt.scatter(totanual.DeltaS, totanual.P)
plt.xlabel('S-S$_{-ano}$ (mm/ano)')
plt.ylabel('P (mm/ano)')

plt.savefig(pngfigplot, dpi=300, bbox_inches='tight')

plt.show()
