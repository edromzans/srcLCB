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

# print(dadosobs)
# time.sleep(30)

Rn_O = dadosobs.Rn
# verifica dados validos
posval = np.asarray(Rn_O > -9999.).nonzero()
posval = posval[0]
Rn_O = Rn_O[posval]

nlinha = len(dadosobs)
# print(nlinha, ' <--------- nlinha')


def residualSiB2(params, Rn_O, posval, nlinha):

    tran_1_1 = params['tran_11']
    tran_2_1 = params['tran_21']
    tran_1_2 = params['tran_12']
    tran_2_2 = params['tran_22']
    ref_1_1 = params['ref_11']
    ref_2_1 = params['ref_21']
    ref_1_2 = params['ref_12']
    ref_2_2 = params['ref_22']
    soref_1 = params['soref_1']
    soref_2 = params['soref_2']
    chil_param = params['chil']

    # print(p_trans_viva_nir, p_ref_viva_nir, p_ref_solo_par, p_ref_solo_nir)
    print(params)

    '''
    Roda o SiB2
    '''

    Rn_C = sib2(tran_1_1, tran_2_1, tran_1_2, tran_2_2,
                ref_1_1, ref_2_1, ref_1_2, ref_2_2, soref_1, soref_2,
                chil_param, nlinha)

    Rn_C = Rn_C[posval]

    # print(len(Rn_O), len(Rn_C))
    # time.sleep(5)
    # print(params)

    modeloerro = Rn_O - Rn_C

    # remove os 30 primeiros valores calculados
    # modeloerro = modeloerro[30:]
    # print(modeloerro)
    return modeloerro


tran_11_min = 0.01
tran_11_max = 0.2
tran_11_ngrid = 2.
tran_11_step = (tran_11_max - tran_11_min) / tran_11_ngrid

tran_21_min = 0.01
tran_21_max = 0.6
tran_21_ngrid = 2.
tran_21_step = (tran_21_max - tran_21_min) / tran_21_ngrid

tran_12_min = 0.0001
tran_12_max = 0.5
tran_12_ngrid = 2.
tran_12_step = (tran_12_max - tran_12_min) / tran_12_ngrid

tran_22_min = 0.0001
tran_22_max = 0.5
tran_22_ngrid = 2.
tran_22_step = (tran_22_max - tran_22_min) / tran_22_ngrid

ref_11_min = 0.01
ref_11_max = 0.2
ref_11_ngrid = 2.
ref_11_step = (ref_11_max - ref_11_min) / ref_11_ngrid

ref_21_min = 0.01
ref_21_max = 0.8
ref_21_ngrid = 2.
ref_21_step = (ref_21_max - ref_21_min) / ref_21_ngrid

ref_12_min = 0.01
ref_12_max = 0.4
ref_12_ngrid = 2.
ref_12_step = (ref_12_max - ref_12_min) / ref_12_ngrid

ref_22_min = 0.01
ref_22_max = 0.6
ref_22_ngrid = 2.
ref_22_step = (ref_22_max - ref_22_min) / ref_22_ngrid

soref_1_min = 0.01
soref_1_max = 0.3
soref_1_ngrid = 2.
soref_1_step = (soref_1_max - soref_1_min) / soref_1_ngrid

soref_2_min = 0.01
soref_2_max = 0.4
soref_2_ngrid = 2.
soref_2_step = (soref_2_max - soref_2_min) / soref_2_ngrid

chil_min = 0.05
chil_max = 0.2
chil_ngrid = 2.
chil_step = (chil_max - chil_min) / chil_ngrid

params = Parameters()
params.add('tran_11', max=tran_11_max, min=tran_11_min, brute_step=tran_11_step)
params.add('tran_21', max=tran_21_max, min=tran_21_min, brute_step=tran_21_step)
params.add('tran_12', max=tran_12_max, min=tran_12_min, brute_step=tran_12_step)
params.add('tran_22', max=tran_22_max, min=tran_22_min, brute_step=tran_22_step)
params.add('ref_11',  max=ref_11_max,  min=ref_11_min , brute_step=ref_11_step)
params.add('ref_21',  max=ref_21_max,  min=ref_21_min , brute_step=ref_21_step)
params.add('ref_12',  max=ref_12_max,  min=ref_12_min , brute_step=ref_12_step)
params.add('ref_22',  max=ref_22_max,  min=ref_22_min , brute_step=ref_22_step)
params.add('soref_1', max=soref_1_max, min=soref_1_min, brute_step=soref_1_step)
params.add('soref_2', max=soref_2_max, min=soref_2_min, brute_step=soref_2_step)
params.add('chil',    max=chil_max,    min=chil_min   , brute_step=chil_step)

otimiza = Minimizer(residualSiB2, params,
                    fcn_args=(Rn_O, posval, nlinha))

out_brute = otimiza.brute(workers=3)

# dirMR = '/dados/ProcessoOtimizacaoModelos/SiB2/resultados/'
dirMR = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/SiB2/resultados/'

pickle.dump(out_brute, open(dirMR+'sib2_radiation_bruteMinimizerResult.pkl', 'wb'))

print('###################################################')
print('Modulo: Radiacao')
print('---Parametros---')
params.pretty_print()
print('---Otimizacao---')
report_fit(out_brute)
