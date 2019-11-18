import pandas as pd
import numpy as np
from lmfit import Minimizer, Parameters, report_fit
import subprocess
from editadata1 import edata1
import shutil
import tempfile
import time

import matplotlib.pyplot as plt

data2 = '/dados/ProcessoOtimizacaoModelos/calibraSiB2/' \
    'data2'

dadosobs = pd.read_table(
        data2, header=0, delim_whitespace=True, names=[
            'datetime', 'Ki', 'em', 'tm', 'um', 'prec', 'Rn', 'Ho', 'LEo'])

LE = dadosobs.LEo
H = dadosobs.Ho


def residualSiB2(params, LE, H):
    # import subprocess

    p_gradm = params['gradm']
    p_vmax = params['vmax']
    
    param_gradm = p_gradm * 1.
    param_vmax = p_vmax * 1.
    
    # dircalibra = '/dados/ProcessoOtimizacaoModelos/calibraSiB2/'
    dircalibra = '/home/evandro/src_codes/SiB/calibracaoSiB2/'
    sib2dt = dircalibra + 'sib2dt.dat'
    data1 = dircalibra + 'data1'

    print('{:<8.3f}'.format(param_gradm), '{:<6.1f}'.format(param_vmax), ' <--')
    # time.sleep(5)
    edata1(dircalibra, param_gradm, param_vmax)


    # with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
    #     with open(data1) as src_file:
    #         kline = 1
    #         for line in src_file:
                
    #             # gradm
    #             if kline == 15:  # numero da linha
    #                 # print(line, kline, '<-----------')
    #                 effcon, gradm, binter, respcp, atheta, btheta = line.split()
    #                 tmp_file.write('   '+'{:<8}'.format(effcon)
    #                                + '{:<8.3f}'.format(param_gradm)
    #                                + '{:<8}'.format(binter)
    #                                + '{:<8}'.format(respcp)
    #                                + '{:<8}'.format(atheta)
    #                                + '{:<8}'.format(btheta)
    #                                + '\n')
    #             # vmax
    #             elif kline == 58:  # numero da linha
    #                 vmax = line.split()
    #                 tmp_file.write(' ' + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '{:<6.1f}'.format(param_vmax)
    #                                + '\n')
    #             else:
    #                 tmp_file.write(line)

    #             kline += 1

    # '''
    # Reescreve o data1 a partir do temporario preservando todos os atributos
    # '''
    # shutil.copystat(data1, tmp_file.name)
    # shutil.move(tmp_file.name, data1)

    '''
    Roda o SiB2
    '''
    subprocess.call('/dados/ProcessoOtimizacaoModelos/calibraSiB2/SiB2runF95')

    dadoscalc = pd.read_table(
        sib2dt, header='infer', delim_whitespace=True)

    LE_c = dadoscalc.LE_C
    H_c = dadoscalc.H_C


    modeloerro = abs(LE_c - LE)
    # modeloerro = LE_c/(LE_c+H_c) - LE/(LE+H)  # *ABS(LE_O(I))
    # fvec(1:m) =(((LE(1:m))/(LE(1:m)+H(1:m))) - ((LE_O(1:m))/(LE_O(1:m)+H_O(1:m))))*ABS(LE_O(I))

    return modeloerro


params = Parameters()
params.add('gradm', min=4., max=20., brute_step=2.)
params.add('vmax', min=50, max=150, brute_step=20.)

otimiza = Minimizer(residualSiB2, params, fcn_args=(LE, H))

out = otimiza.brute(workers=1)
report_fit(out)
