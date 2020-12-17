# Caminho do arquivo NetCDF referente as ETPs
dataset_reanalise = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/'\
    'calibracaoBalagua/dados/subsets/'\
    'dataset_to_etps_reanalysis-era5-land-monthly-means.nc'

dir_subsets = './subsets/'

# Descricao das variaveis #############################
# u10: "10 metre U wind component" ;
# v10: "10 metre V wind component" ;
# d2m: "2 metre dewpoint temperature" ;
# t2m: "2 metre temperature" ;
# pev: "Potential evaporation" ;
# slhf: "Surface latent heat flux" ;
# ssr: "Surface net solar radiation" ;
# str: "Surface net thermal radiation" ;
# sp: "Surface pressure" ;
# sshf: "Surface sensible heat flux" ;
# ssrd: "Surface solar radiation downwards" ;
# strd: "Surface thermal radiation downwards" ;
# tp: "Total precipitation" ;
# t2m_max: "2 metre maximum temperature" ;
# t2m_min: "2 metre minimum temperature" ;
# ra: "Extraterrestial radiation for daily periods" ;
# Ith: "Thornthwaite I index" ;
# ath: "Thornthwaite a index" ;
# daylh: "Daylight hours (N)" ;
#######################################################
# Selecione uma variavel:
# var = 'u10'
# var = 'v10'
var = 't2m'
# var = 'd2m'
# var = 'pev'
# var = 'slhf'
# var = 'ssr'
# var = 'str'
# var = 'sp'
# var = 'sshf'
# var = 'ssrd'
# var = 'strd'
# var = 'tp'
# var = 't2m_max'
# var = 't2m_min'
# var = 'ra'
# var = 'Ith'
# var = 'ath'
# var = 'daylh'

# Defina o periodo inicial e final
t_inicio = '1981-01-01'
t_final = '2020-08-01'
# Periodo maximo:
# t_inicio = '1981-01-01'
# t_final = '2020-08-01'

# Defina a regiao espacial regular de extração de subconjunto de dados
xlon0 = -55
xlon1 = -43
ylat0 = -25
ylat1 = -18
#
# Regiao maxima:
# xlon0 = -56.
# xlon1 = -38.
# ylat0 = -13.
# ylat1 = -27.
#

# Caminho do shape file para extração de subconjunto de dados
# no interior do poligono geografico.
extrac_shape = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ugrhi/' \
    'chuva_vazao_shape/shape_file/shape_file_limite/pcj_basin.shp'

# Defina o flag espacial: 0 para selecao regular
#                         1 para selecao por shape file
flag_espc = 0
