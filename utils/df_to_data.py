import pandas as pd
# import numpy as np

# dirinput = '/dados/ProcessoOtimizacaoModelos/SiB2/input/FlorAtlantica/'
dirinput = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/SiB2/' \
    'input/FlorAtlantica/2014-2016/'

# datacsv = 'data2_sib2_svg_2014_full_data.csv'
# datacsv = 'SVG_2014_horario.csv'
datacsv = 'Data_SiB2_hourly_2014_2016_v5.csv'

datadf = pd.read_csv(dirinput+datacsv, sep=',')

data2dic = {'datetime': datadf.datetime,
            'Ki': datadf.Ki,
            'em': datadf.em,
            'tm': datadf.tm,
            'um': datadf.um,
            'prec': datadf.prec,
            'Rn': datadf.Rn}

data2df = pd.DataFrame(data=data2dic)

data2df.to_csv(dirinput+'data2',
               sep='\t', index=False, header=True,
               float_format='%11.4f')

# # data2df.to_csv(dirinput+'data2.csv',
# data2df.to_csv(dirinput+'data3.csv',
#                sep='\t', index=False, header=True,
#                float_format='%11.4f')
