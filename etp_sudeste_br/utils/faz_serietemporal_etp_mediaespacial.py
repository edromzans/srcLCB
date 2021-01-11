import xarray as xr

# nc_etp = '../subsets/etp_fao56reference_regular.nc'
nc_etp = '../subsets/etp_thornthwaite_regular.nc'

arquivo_txt = '../subsets/serietemporal_etp_mediaespacial.txt'

# deve ser o codinome da etp no arquivo NetCDF
etpcodname = 'thornthwaite'

ds_etp = xr.open_dataset(nc_etp)

ds_etp[etpcodname].mean(
    {'latitude',
     'longitude'}).to_pandas().to_csv(
        arquivo_txt,
        header=[etpcodname+'(mm*dia**-1)'])

print('Arquivo '+arquivo_txt+' criado.')
