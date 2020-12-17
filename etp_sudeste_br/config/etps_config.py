# Caminho do arquivo NetCDF referente as ETPs
dataset_etps = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/'\
    'calibracaoBalagua/dados/subsets/dataset_etps.nc'

dir_subsets = './subsets/'

# Selecione um metodo de ETP
# etp_metodo = 'fao56reference'
# etp_metodo = 'asceewri_penmon'
# etp_metodo = 'penmanmonteith'
# etp_metodo = 'hargreavessamani'
# etp_metodo = 'mhargreaves'
# etp_metodo = 'priestleytaylor'
etp_metodo = 'thornthwaite'

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
