import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
from sib2pymod import sib2
import pickle
import time

# data2 = '/dados/ProcessoOtimizacaoModelos/SiB2/input/radiative/' \
#     'data2'

# dadosobs = pd.read_table('data2', header=0, delim_whitespace=True, names=[
#             'datetime', 'Ki', 'em', 'tm', 'um', 'prec', 'Rn'])

# dadosobs = pd.read_table('data3.csv', delim_whitespace=True)
dadosobs = pd.read_csv('data3.csv')

h_o = np.asarray(dadosobs.H)
le_o = np.asarray(dadosobs.LE)

# print(dadosobs)
# time.sleep(30)

# verifica dados validos
posval = np.asarray((h_o > -9999.)
                    & (le_o > -9999.)).nonzero()
posval = posval[0]
h_o = h_o[posval]
le_o = le_o[posval]

nlinha = len(dadosobs)
# print(nlinha, ' <--------- nlinha')


def residualSiB2(params, h_o, le_o, posval, nlinha):

    gradm_param = params['gradm']
    gmudmu_param = params['gmudmu']
    greeness_param = params['greeness']
    vmax_param = params['vmax']

    print(params)

    '''
    Roda o SiB2
    '''
    [h_c, le_c] = sib2(gradm_param, gmudmu_param,
                       greeness_param, vmax_param,
                       nlinha)

    h_c = h_c[posval]
    le_c = le_c[posval]

    # print(len(Rn_O), len(Rn_C))
    # time.sleep(5)
    # print(params)

    modeloerro = (le_c/(h_c+le_c)) - (le_o/(h_o+le_o))

    # remove os 30 primeiros valores calculados
    # modeloerro = modeloerro[30:]
    print(modeloerro)
    return modeloerro


gradm_min = 15.
gradm_max = 17.
gradm_ngrid = 3.
gradm_step = (gradm_max - gradm_min) / gradm_ngrid

gmudmu_min = 0.9
gmudmu_max = 1.1
gmudmu_ngrid = 3.
gmudmu_step = (gmudmu_max - gmudmu_min) / gmudmu_ngrid

greeness_min = 0.5
greeness_max = 0.99
greeness_ngrid = 3.
greeness_step = (greeness_max - greeness_min) / greeness_ngrid

vmax_min = 90.
vmax_max = 110.
vmax_ngrid = 3.
vmax_step = (vmax_max - vmax_min) / vmax_ngrid

params = Parameters()
params.add('gradm',    min=gradm_min   , max=gradm_max   , brute_step=gradm_step   ) 
params.add('gmudmu',   min=gmudmu_min  , max=gmudmu_max  , brute_step=gmudmu_step  )  
params.add('greeness', min=greeness_min, max=greeness_max, brute_step=greeness_step) 
params.add('vmax',     min=vmax_min    , max=vmax_max    , brute_step=vmax_step    )

otimiza = Minimizer(residualSiB2, params,
                    fcn_args=(h_o, le_o, posval, nlinha))

# out_leastsq = otimiza.leastsq()
out_leastsq = otimiza.minimize(method='leastsq')  # Levenberg-Marquardt

out_brute = otimiza.brute(workers=3)

# report_fit(out_brute.params)
# report_fit(out_brute)

dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/SiB2/resultados/'
pickle.dump(out_brute,
            open(dirMR+'sib2_carbonoagua_bruteMinimizerResult.pkl', 'wb'))


print('###################################################')
print('Modulo: Carbono e agua')
print('---Parametros---')
params.pretty_print()
print('---Otimizacao---')
report_fit(out_brute)


# report_fit(out_leastsq.params)
# report_fit(out_leastsq)
