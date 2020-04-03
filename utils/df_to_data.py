import pandas as pd
# import numpy as np

dirinput = '/dados/ProcessoOtimizacaoModelos/SiB2/input/FlorAtlantica/'

# datacsv = 'data2_sib2_svg_2014_full_data.csv'
datacsv = 'SVG_2014_horario.csv'

data2df = pd.read_csv(dirinput+datacsv, sep=',')

# data2df.to_csv(dirinput+'data2.csv',
data2df.to_csv(dirinput+'data3.csv',
               sep='\t', index=False, header=True,
               float_format='%11.4f')
