import pandas as pd
import numpy as np

dirdados = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/dadosJaraguari/Leonardo/'

aguadados_csv = 'aguadados.csv'
dadosamb_csv = 'dadosamb.csv'

dirinputbalagua = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/inputs/jaraguari_obs_ecmwf/'
arqvinput = 'input.txt'

aguadados = pd.read_csv(dirdados+aguadados_csv, parse_dates=['date'])
aguadados.rename(columns={' Prec': 'prec',
                          ' PET': 'pet',
                          ' AET': 'aet',
                          ' Rsim': 'rsim',
                          ' Robs': 'robs'}, inplace=True)
aguadados.index = aguadados['date']

dadosamb = pd.read_csv(dirdados+dadosamb_csv, parse_dates=['date'])
dadosamb.rename(columns={' Tmax_K': 'tmax_K',
                         ' Tmin_K': 'tmin_K',
                         ' Tmed_K': 'tmed_K',
                         ' Rad_MJ_m2dia': 'MJ_m2_dia'}, inplace=True)
dadosamb.index = dadosamb['date']

rad = dadosamb['MJ_m2_dia']
tmax = dadosamb['tmax_K'] - 273.15  # K to C
tmin = dadosamb['tmin_K'] - 273.15
tmed = dadosamb['tmed_K'] - 273.15

# radmmdia2 = rad*(10.**6./(28.9*86400.))
radmmdia = rad*(10.**3. /
                (2500.8-2.36*tmed+0.0016*(tmed**2.)-0.00006*(tmed**3.)))

# etp2 = (0.0023*radmmdia2*(tmax-tmin)**0.5)*(tmed+17.8)
etp = (0.0023*radmmdia*(tmax-tmin)**0.5)*(tmed+17.8)

dadosamb['etp'] = etp
# dadosamb['etp2'] = etp2

etp_mm_mes = dadosamb.etp.resample('M').sum()  # soma mensal

xtime = np.arange('1995-01-01', '2017-12-01', dtype='datetime64[M]')

pdts = pd.DatetimeIndex(xtime)

input = open(dirinputbalagua+arqvinput, 'w')

for tk in range(len(xtime)):
    # print(xtime[tp].astype('datetime64[Y]').astype(int) + 1970)
    # print(xtime[tp].astype('datetime64[M]').astype(int) % 12 + 1)

    posetp = np.where((etp_mm_mes.index.year == pdts.year[tk]) &
                      (etp_mm_mes.index.month == pdts.month[tk]))
    posetp = posetp[0]

    posagua = np.where((aguadados.index.year == pdts.year[tk]) &
                       (aguadados.index.month == pdts.month[tk]))
    posagua = posagua[0]

    strdatatempo = pdts[tk].strftime('%Y %m %d %H %M %S')

    # if (posetp.size < 1) or (posagua.size < 1):
    #     print('Falta dados: '+srtdatatempo)
    #     break

    input_etp = etp_mm_mes[posetp]
    input_prec = aguadados['prec'][posagua]
    input_vazao = aguadados['robs'][posagua]

    input.write(strdatatempo
                + etp_mm_mes[posetp].to_string(
                    header=False, index=False,
                    float_format='{:11.2f}'.format)
                + aguadados['prec'][posagua].to_string(
                    header=False, index=False,
                    float_format='{:11.2f}'.format)
                + aguadados['robs'][posagua].to_string(
                    header=False, index=False,
                    float_format='{:11.2f}'.format)
                + '\n')

    # print(etp_mm_mes.index[posetp], etp_mm_mes[posetp])
    # print(pdts.year[tk])
    # print(tk,' <------------------')
    # break
input.close()
