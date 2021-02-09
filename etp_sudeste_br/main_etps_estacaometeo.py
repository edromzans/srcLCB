import evapotranspiracaopotencial_estacaometeo as etp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

arq_dadosmeteo = '/home/evandro/lcbiag/ProcessoOtimizacaoModelos/'\
    'calibracaoBalagua/dados/TAMUXavier/subset/estacaometeoserie.csv'

df_dadosmeteo = pd.read_csv(arq_dadosmeteo, parse_dates=True, index_col=[0])

df_dadosmeteo_mensal = df_dadosmeteo.resample('MS').agg(np.mean)

t2m_max = df_dadosmeteo_mensal.Tmax
t2m_min = df_dadosmeteo_mensal.Tmin
t2m = (t2m_max - t2m_min) / 2.
u2 = df_dadosmeteo_mensal.u2
rh = df_dadosmeteo_mensal.RH
rn = df_dadosmeteo_mensal.Rs
tp = df_dadosmeteo_mensal.precipitacao

lat = -22.7
dayofyear = df_dadosmeteo_mensal.index.dayofyear.values
daysinmonth = df_dadosmeteo_mensal.index.daysinmonth.values


etp_fao56reference = etp.fao56reference(t2m, t2m_max, t2m_min, u2, rh, rn)

etp_asceewripenmanmonteith = etp.asceewripenmanmonteith(t2m, t2m_max, t2m_min,
                                                        u2, rh, rn)

etp_penmanmonteith = etp.penmanmonteith(t2m, t2m_max, t2m_min, u2, rh, rn, 95.)

etp_hargreavessamani = etp.hargreavessamani(lat, dayofyear, t2m,
                                            t2m_max, t2m_min)

etp_mhargreaves = etp.mhargreaves(lat, dayofyear, daysinmonth,
                                  t2m, t2m_max, t2m_min, tp)

etp_priestleytaylor = etp.priestleytaylor(t2m, rn)
