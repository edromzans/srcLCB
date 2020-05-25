import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# dirsib2 = '/dados/ProcessoOtimizacaoModelos/SiB2/' \
#     'calibracaoFlorAtlantica/1_rodadaInicial_semcalibracao/'

# dadosobs = pd.read_table(dirsib2+'data3.csv', delim_whitespace=True)
dadosobs = pd.read_csv('data3.csv')  # , delim_whitespace=True)
# Timestamp	Ki	em	tm	um	prec	Rn	H
# LE	NEE	H_f	LE_f	NEE_f	Ustar
# SWC1	SWC2	SWC3	SWC4	SWC5	SWC6	SWC7

# dadoscal = pd.read_table(dirsib2+'sib2dt.dat', delim_whitespace=True)
dadoscal = pd.read_table('sib2dt.dat', delim_whitespace=True)

#    NYMD        Tm        em        um        Ki      Rn_m       alb
# Ldwn      Lupw      Rn_C       H_C      LE_C       G_C       J_C
# Fc_C     Rsc_C      An_C      u*_C        Td      W1_C      W2_C
# W3_C     gcond      Evpt     Trans     Esoil   Einterc      Prec
# Rss        Rs    Runoff   PARidir   PARidif albPARdir albPARdif

xtime = np.asarray(dadosobs.index)

rn_o = np.asarray(dadosobs['Rn'])
ustar_o = np.asarray(dadosobs['Ustar'])
www1_o = np.asarray(dadosobs['VW1'])
h_o = np.asarray(dadosobs['H'])
le_o = np.asarray(dadosobs['LE'])
swc_o = np.asarray(dadosobs['SWC'])

rn_c = np.asarray(dadoscal['Rn_C'])
ustar_c = np.asarray(dadoscal['u*_C'])
www1_c = np.asarray(dadoscal['W1_C'])
h_c = np.asarray(dadoscal['H_C'])
le_c = np.asarray(dadoscal['LE_C'])
swc_c = (np.asarray(dadoscal['W2_C'])+np.asarray(dadoscal['W3_C'])+np.asarray(dadoscal['W4_C'])+np.asarray(dadoscal['W5_C'])+np.asarray(dadoscal['W6_C'])) / 5.

dic_o = {'rn': rn_o, 'ustar': ustar_o, 'www1': www1_o, 'h': h_o, 'le': le_o, 'swc': swc_o}
df_obs = pd.DataFrame(data=dic_o, index=xtime)
df_obs = df_obs.replace(-99999., np.nan)

dic_c = {'rn': rn_c, 'ustar': ustar_c, 'www1': www1_c, 'h': h_c, 'le': le_c, 'swc': swc_c}
df_cal = pd.DataFrame(data=dic_c, index=xtime)

line1x1 = [-1000., 10000.]

nvars = len(df_obs.columns)

fig, ax = plt.subplots(nrows=3, ncols=2)

k = 0
for row in ax:
    for col in row:
        if k < nvars:

            col.plot(line1x1, line1x1, linewidth=0.5, color='black')

            col.scatter(df_obs[df_obs.columns[k]],
                        df_cal[df_cal.columns[k]], marker='+', linewidth=0.8)
            col.set_xlabel(str(df_obs.columns[k])+'_o')
            col.set_ylabel(str(df_cal.columns[k])+'_c')

            col.set_xlim(np.nanmin(df_obs[df_obs.columns[k]]) -.05 ,
                         np.nanmax(df_obs[df_obs.columns[k]])+.5)
            col.set_ylim(np.nanmin(df_obs[df_obs.columns[k]]) -.05,
                         np.nanmax(df_obs[df_obs.columns[k]])+.5)

            print('--------'+str(df_obs.columns[k])+'--------')
            df = pd.DataFrame(data={'obs': df_obs[df_obs.columns[k]],
                                    'cal': df_cal[df_cal.columns[k]]})
            print(df.corr())

        k += 1
plt.tight_layout()

plt.savefig('SemCalibracao.png', dpi=300, bbox_inches='tight')

plt.show()

# x = range(10)
# y = range(10)
# fig, ax = plt.subplots(nrows=2, ncols=2)
# for row in ax:
#     for col in row:
#         col.plot(x, y)
