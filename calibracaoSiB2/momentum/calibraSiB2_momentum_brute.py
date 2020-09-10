import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from sib2pymod import sib2
import time
import pickle

# data2 = '/home/evandro/src_codes/LCB/srcLCB/calibracaoSiB2/momentum/' \
#     'data2'

data2 = 'data2'
zlt_aero_ts = 'zlt_aero_ts.dat'

# dadosobs = pd.read_table(
#     data2, header=0, delim_whitespace=True, names=[
#         'datetime', 'Ki', 'em', 'tm', 'um', 'prec',
#         'Rn', 'ustar', 'Ho', 'LEo'])
# ustar_o_serie = np.asarray(dadosobs.ustar)

# dadosobs = pd.read_table('data3.csv', delim_whitespace=True)
dadosobs = pd.read_csv('data3.csv')
ustar_o_serie = np.asarray(dadosobs.Ustar)

# print(dadosobs)
# time.sleep(30)

df_zlt_aero = pd.read_table(zlt_aero_ts, sep='\s+')
zlt_serie = np.asarray(df_zlt_aero.zlt)

# verifica dados validos
# posval = np.asarray(ustar_o > -9999.).nonzero()
# posval = posval[0]
# ustar_o = ustar_o[posval]

nlinha = len(dadosobs)


# 'ha, z0d, dd, g2, g3, cc1, cc2, corb1, corb2'
f_params_calibrado = open('params_calibrado_brute.dat', 'w')
f_params_calibrado.write(
            '{:>11} {:>11} {:>11} {:>11} {:>11} {:>11} {:>11} {:>11} {:>11} {:>11}\n'.format(
                'zlt',
                'ha',
                'z0d',
                'dd',
                'g2',
                'g3',
                'cc1',
                'cc2',
                'corb1',
                'corb2'))


def residualSiB2(params, ustar_o, posval, nlinha):

    ha_param = params['ha']
    z0d_param = params['z0d']
    dd_param = params['dd']
    g2_param = params['g2']
    g3_param = params['g3']
    cc1_param = params['cc1']
    cc2_param = params['cc2']
    corb1_param = params['corb1']
    corb2_param = params['corb2']

    '''
    Roda o SiB2
    '''

    [ustar_c, zlt_ts] = sib2(ha_param, z0d_param, dd_param, g2_param,
                             g3_param, cc1_param, cc2_param, corb1_param,
                             corb2_param,
                             nlinha)

    ustar_c = ustar_c[posval]
    zlt_ts = zlt_ts[posval]

    print('----ustar_c-----')
    print(ustar_c)

    print('----ustar_o-----')
    print(ustar_o)

    print('----zlt_SiB2-----')
    print(zlt_ts)

    # print(len(ustar_o), len(ustar_c))
    # time.sleep(35)
    print(params)
    # print(ustar_o)
    # print(ustar_c)
    print('----modeloerro----')
    modeloerro = ustar_o - ustar_c
    print(modeloerro)
    return modeloerro


# gk = df_zlt_aero.groupby('zlt')
# print(gk.first())
# gk2 = df_zlt_aero.groupby(['zlt','ha','z0d','dd','g2','g3','cc1','cc2','corb1','corb2'])
# print(gk2.first())

df_zlt_g = df_zlt_aero.groupby('zlt').mean()

# print(df_zlt_g)
# time.sleep(10)

nzlt = len(df_zlt_g)

zlt_g_serie = np.asarray(df_zlt_g.index)

ha_serie = np.asarray(df_zlt_g.ha)
z0d_serie = np.asarray(df_zlt_g.z0d)
dd_serie = np.asarray(df_zlt_g.dd)
g2_serie = np.asarray(df_zlt_g.g2)
g3_serie = np.asarray(df_zlt_g.g3)
cc2_serie = np.asarray(df_zlt_g.cc2)
cc1_serie = np.asarray(df_zlt_g.cc1)
corb1_serie = np.asarray(df_zlt_g.corb1)
corb2_serie = np.asarray(df_zlt_g.corb2)

# Determine o range dos parametros

perc = 30.

ha_min = np.min(ha_serie) - np.min(ha_serie)*(perc/100.)
ha_max = np.max(ha_serie) + np.max(ha_serie)*(perc/100.)
ha_ngrid = 3.
ha_step = (ha_max - ha_min) / ha_ngrid

z0d_min = np.min(z0d_serie) - np.min(z0d_serie)*(perc/100.)
z0d_max = np.max(z0d_serie) + np.max(z0d_serie)*(perc/100.)
z0d_ngrid = 3.
z0d_step = (z0d_max - z0d_min) / z0d_ngrid

dd_min = np.min(dd_serie) - np.min(dd_serie)*(perc/100.)
dd_max = np.max(dd_serie) + np.max(dd_serie)*(perc/100.)
dd_ngrid = 3.
dd_step = (dd_max - dd_min) / dd_ngrid

g2_min = np.min(g2_serie) - np.min(g2_serie)*(perc/100.)
g2_max = np.max(g2_serie) + np.max(g2_serie)*(perc/100.)
g2_ngrid = 3.
g2_step = (g2_max - g2_min) / g2_ngrid

g3_min = np.min(g3_serie) - np.min(g3_serie)*(perc/100.)
g3_max = np.max(g3_serie) + np.max(g3_serie)*(perc/100.)
g3_ngrid = 3.
g3_step = (g3_max - g3_min) / g3_ngrid

cc1_min = np.min(cc1_serie) - np.min(cc1_serie)*(perc/100.)
cc1_max = np.max(cc1_serie) + np.max(cc1_serie)*(perc/100.)
cc1_ngrid = 3.
cc1_step = (cc1_max - cc1_min) / cc1_ngrid

cc2_min = np.min(cc2_serie) - np.min(cc2_serie)*(perc/100.)
cc2_max = np.max(cc2_serie) + np.max(cc2_serie)*(perc/100.)
cc2_ngrid = 3.
cc2_step = (cc2_max - cc2_min) / cc2_ngrid

corb1_min = np.min(corb1_serie) - np.min(corb1_serie)*(perc/100.)
corb1_max = np.max(corb1_serie) + np.max(corb1_serie)*(perc/100.)
corb1_ngrid = 3.
corb1_step = (corb1_max - corb1_min) / corb1_ngrid

corb2_min = np.min(corb2_serie) - np.min(corb2_serie)*(perc/100.)
corb2_max = np.max(corb2_serie) + np.max(corb2_serie)*(perc/100.)
corb2_ngrid = 3.
corb2_step = (corb2_max - corb2_min) / corb2_ngrid


for k in range(0, nzlt):
    print(k, '   <---------k')
    # time.sleep(1)

    hav = ha_serie[k]
    zltv = zlt_g_serie[k]
    z0dv = z0d_serie[k]
    ddv = dd_serie[k]
    g2v = g2_serie[k]
    g3v = g3_serie[k]
    cc1v = cc1_serie[k]
    cc2v = cc2_serie[k]
    corb1v = corb1_serie[k]
    corb2v = corb2_serie[k]

    print('----zlt_Selecionado-----')
    print(zltv)

    params = Parameters()
    params.add('ha',    min=ha_min,    max=ha_max   , brute_step=ha_step   )
    params.add('z0d',   min=z0d_min,   max=z0d_max  , brute_step=z0d_step  )
    params.add('dd',    min=dd_min,    max=dd_max   , brute_step=dd_step   )
    params.add('g2',    min=g2_min,    max=g2_max   , brute_step=g2_step   )
    params.add('g3',    min=g3_min,    max=g3_max   , brute_step=g3_step   )
    params.add('cc1',   min=cc1_min,   max=cc1_max  , brute_step=cc1_step  )
    params.add('cc2',   min=cc2_min,   max=cc2_max  , brute_step=cc2_step  )
    params.add('corb1', min=corb1_min, max=corb1_max, brute_step=corb1_step)
    params.add('corb2', min=corb2_min, max=corb2_max, brute_step=corb2_step)
    
    # seleciona zlt

    # posval = np.asarray(zlt_serie == zltv).nonzero()
    # posval = np.asarray(ustar_o > -9999.).nonzero()

    posval = np.asarray((zlt_serie == zltv)
                        & (ustar_o_serie > -9999.)).nonzero()
    posval = posval[0]

    # print('-----Selecao zlt------')
    # print(zltv, ' <<<<--------')
    # print(zlt_serie[posval])
    # print('----------------------')
    # break

    if len(posval) <= 0:
        print('------falta dados para calibracao------')
        # break
        f_params_calibrado.write(
            '{:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f}\n'.format(
                zltv,
                hav,
                z0dv,
                ddv,
                g2v,
                g3v,
                cc1v,
                cc2v,
                corb1v,
                corb2v))
    else:
        ustar_o = ustar_o_serie[posval]

        # print(ustar_o)
        # print(zlt_serie[posval])

        otimiza = Minimizer(residualSiB2, params,
                            fcn_args=(ustar_o, posval, nlinha))

        out_brute = otimiza.brute(workers=3)

        # report_fit(out_brute.params)
        # report_fit(out_brute)

        dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/SiB2/resultados/'
        pickle.dump(out_brute,
                    open(dirMR+'sib2_momentum_bruteMinimizerResult.pkl', 'wb'))

        print('###################################################')
        print('Modulo: Momentum')
        print('---Parametros---')
        params.pretty_print()
        print('---Otimizacao---')
        report_fit(out_brute)

        haw = float(out_brute.params['ha'])
        z0dw = float(out_brute.params['z0d'])
        ddw = float(out_brute.params['dd'])
        g2w = float(out_brute.params['g2'])
        g3w = float(out_brute.params['g3'])
        cc1w = float(out_brute.params['cc1'])
        cc2w = float(out_brute.params['cc2'])
        corb1w = float(out_brute.params['corb1'])
        corb2w = float(out_brute.params['corb2'])

        f_params_calibrado.write(
            '{:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f} {:11.3f}\n'.format(
                zltv,
                haw,
                z0dw,
                ddw,
                g2w,
                g3w,
                cc1w,
                cc2w,
                corb1w,
                corb2w))

        # if k == 3:
        #     f_params_calibrado.close()
        #     break
f_params_calibrado.close()
