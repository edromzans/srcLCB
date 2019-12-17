import pandas as pd
import numpy as np
from lmfit import report_fit  # Minimizer, Parameters,
# from lmfit.models import GaussianModel
import matplotlib.pyplot as plt
import pickle
import calendar


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

# dirR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/resultados/'
dirR = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/resultados/'
dirplot = '/dados/ProcessoOtimizacaoModelos/calibracaoBalagua/plots/'
(out_leastsq,
 x_eixo,
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

# Deslocamento de tempo para ciclo anual jan-dez em set-ago
xtimeM = np.array(x_eixo.to_pydatetime(), dtype='datetime64[M]')
corrig = xtimeM + np.timedelta64(4, 'M')
x_eixo = pd.to_datetime(corrig)

# p2 = np.asarray(p2)
# etp = np.asarray(etp)
# q2 = np.asarray(q2)


# IDL where
posval = np.asarray(~np.isnan(etp) &
                    ~np.isnan(p2) &
                    ~np.isnan(q2)).nonzero()
posval = posval[0]

xi = x_eixo[posval[0]]
xf = x_eixo[posval[-1]]


'''
Segunda figura
'''

pngfigplot = dirplot+tagname+'_pltTsBalagua_hidroano_cicloanual.png'

#d_mes = dict(enumerate(calendar.month_abbr))
d_mes = {5: 'Jan',
         6: 'Feb',
         7: 'Mar',
         8: 'Apr',
         9: 'May',
         10: 'Jun',
         11: 'Jul',
         12: 'Aug',
         1: 'Sep',
         2: 'Oct',
         3: 'Nov',
         4: 'Dec'}

dados = {'ETP': etp, 'ET': ts_r, 'P': p2,
         'Qm': q2, 'Qc': ts_dt, 'S': ts_mt, 'DeltaS': ts_Dm,
         'mes': x_eixo.month}
toanual_df = pd.DataFrame(data=dados, index=x_eixo)

canual = toanual_df.groupby('mes').agg(np.nanmean)

canual.index = canual.index.map(d_mes)  # .str.slice(stop=3)

fig = plt.figure()
fig.set_figwidth(6)
fig.set_figheight(6)
# fig.suptitle(tagname)

plt.style.use('bmh')  # ggplot dark_background classic bmh seaborn-bright

# plt.rcParams.update({'font.size': 10})

ax1 = plt.subplot(311)
# plt.title(tagname, fontsize=10)
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

pngfigplot = dirplot+tagname+'_pltTsBalagua_hidroano_dispersao.png'


# totanual = toanual_df.resample('Y').sum()
totanual = toanual_df.resample('Y').agg(np.nansum)
nantotanual = toanual_df.isnull().resample('Y').agg(np.sum)

fig = plt.figure()
fig.set_figwidth(10)
fig.set_figheight(9)

plt.subplot(221)

# IDL where
q2 = np.asarray(q2)
posval = np.asarray(~np.isnan(q2) |
                    ~np.isnan(ts_dt)).nonzero()
posval = posval[0]
q2_plt = q2[posval]
ts_dt_plt = ts_dt[posval]

minv = np.nanmin(np.concatenate((q2_plt, ts_dt_plt)))
maxv = np.nanmax(np.concatenate((q2_plt, ts_dt_plt)))
xx = np.arange(minv, maxv)
yy = xx
plt.plot(xx, yy, c='green', linewidth=0.8)
plt.scatter(q2_plt, ts_dt_plt, c='black', marker='+', linewidth=0.8)
plt.ylabel('Q$_c$ (mm/mês)')
plt.xlabel('Q$_m$ (mm/mês)')

plt.subplot(222)
posval = np.asarray(~np.isnan(ts_r) |
                    ~np.isnan(etp)).nonzero()
posval = posval[0]
ts_r_plt = ts_r[posval]
etp_plt = etp[posval]

minv = np.nanmin(np.concatenate((ts_r_plt, etp_plt)))
maxv = np.nanmax(np.concatenate((ts_r_plt, etp_plt)))
xx = np.arange(minv, maxv)
yy = xx
plt.plot(xx, yy, c='green', linewidth=0.8)
plt.scatter(etp_plt, ts_r_plt, c='black', marker='+', linewidth=0.8)
plt.xlabel('ETP (mm/mês)')
plt.ylabel('ET (mm/mês)')


plt.subplot(223)
posval = np.asarray((nantotanual.Qm < 1.) & (nantotanual.P < 1.)).nonzero()
posval = posval[0]
Qm_ano_plt = totanual.Qm[posval]
P_ano_plt = totanual.P[posval]

posval = np.asarray((nantotanual.Qc < 1.) & (nantotanual.P < 1.)).nonzero()
posval = posval[0]
Qc_ano_plt = totanual.Qc[posval]
P_ano_plt = totanual.P[posval]

posval = np.asarray((nantotanual.ET < 1.) & (nantotanual.P < 1.)).nonzero()
posval = posval[0]
ET_ano_plt = totanual.ET[posval]

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

posval = np.asarray((nantotanual.DeltaS < 1.) & (nantotanual.P < 1.)).nonzero()
posval = posval[0]
DeltaS_ano_plt = totanual.DeltaS[posval]
P_ano_plt = totanual.P[posval]

plt.scatter(P_ano_plt, DeltaS_ano_plt, c='black', marker='+', linewidth=0.8)
plt.ylabel('S-S$_{-ano}$ (mm/ano)')
plt.xlabel('P (mm/ano)')

plt.savefig(pngfigplot, dpi=300, bbox_inches='tight')

plt.show()
