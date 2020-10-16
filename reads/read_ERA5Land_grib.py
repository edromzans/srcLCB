import cfgrib
dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA-5_Land/'

# DatasetBuildError: multiple values for unique key, try re-open the file with one of:
#     filter_by_keys={'stepType': 'avgid'}
#     filter_by_keys={'stepType': 'avgua'}
#     filter_by_keys={'stepType': 'avgas'}
#     filter_by_keys={'stepType': 'avgad'}

# ds = cfgrib.open_dataset(dirdata+'ERA5-Land_Monthly_avg_reanalysis.grib',
#                          backend_kwargs=dict(
#                              filter_by_keys={'stepType': 'avgad'}))


# ds = cfgrib.open_datasets(dirdata+'ERA5-Land_Monthly_avg_reanalysis.grib')

# ds = cfgrib.open_file(dirdata+'ERA5-Land_Monthly_avg_reanalysis.grib')

ds = cfgrib.open_dataset(dirdata+'adaptor.mars.internal-1602791368.9543579-18763-23-6299d5da-8c11-4b7b-b334-a3c8320d7967.grib')

print(ds.time)
