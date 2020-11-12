import cdsapi

dirdata = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/' \
    'calibracaoBalagua/dados/ECMWF_ERA5/'

era5land = 'reanalysis-era5-land-monthly-means.nc'

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-land-monthly-means',
    {
        'product_type': 'monthly_averaged_reanalysis',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
            '2m_temperature', 'forecast_albedo', 'leaf_area_index_high_vegetation',
            'leaf_area_index_low_vegetation', 'potential_evaporation', 'skin_temperature',
            'surface_latent_heat_flux', 'surface_net_solar_radiation', 'surface_net_thermal_radiation',
            'surface_pressure', 'surface_sensible_heat_flux', 'surface_solar_radiation_downwards',
            'surface_thermal_radiation_downwards', 'total_evaporation', 'total_precipitation',
        ],
        'year': [
            '1981', '1982', '1983',
            '1984', '1985', '1986',
            '1987', '1988', '1989',
            '1990', '1991', '1992',
            '1993', '1994', '1995',
            '1996', '1997', '1998',
            '1999', '2000', '2001',
            '2002', '2003', '2004',
            '2005', '2006', '2007',
            '2008', '2009', '2010',
            '2011', '2012', '2013',
            '2014', '2015', '2016',
            '2017', '2018', '2019',
            '2020',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'time': '00:00',
        'area': [
            -13, -56, -27, -38,
        ],
        'format': 'netcdf',
    },
    dirdata+era5land)
