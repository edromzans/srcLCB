'''
Calcula a ETP a partir dos dados das reanalises do
ECMWF ERA5 Land
'''
import numpy as np


def fao56reference(t2m, t2m_max, t2m_min, u2, rh, rn):

    # Conversoes & cte

    # cte psicrometrica
    psi = 0.063  # [kPa C**-1] ver  Annex 2, Table 2.2, Allen (1998)

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es_tmax = 0.611*np.exp((17.27*t2m_max)/(t2m_max+237.3))  # [kPa]
    es_tmin = 0.611*np.exp((17.27*t2m_min)/(t2m_min+237.3))  # [kPa]
    es_daily = (es_tmax + es_tmin)/2.

    ea = (rh/100.)*es_daily

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    Rn = rn

    G = 0.

    # ETP FAO-56 Reference Crop Evapotranspiration
    etp_fao56reference = (
        (0.408*delta*(Rn-G) + psi*(900./(t2m+273.))*u2*(es_daily-ea)) /
        (delta + psi*(1.+0.34*u2)))  # [mm d**-1]

    return etp_fao56reference


def asceewripenmanmonteith(t2m, t2m_max, t2m_min, u2, rh, rn):

    # Conversoes & cte

    # cte psicrometrica
    psi = 0.063  # [kPa C**-1] ver  Annex 2, Table 2.2, Allen (1998)

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es_tmax = 0.611*np.exp((17.27*t2m_max)/(t2m_max+237.3))  # [kPa]
    es_tmin = 0.611*np.exp((17.27*t2m_min)/(t2m_min+237.3))  # [kPa]
    es_daily = (es_tmax + es_tmin)/2.

    ea = (rh/100.)*es_daily

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    Rn = rn

    G = 0.

    # ASCE-EWRI Standardized Penman-Monteith Equation
    etp_asceewripenmanmonteith = (
        (0.408*delta*(Rn-G) + psi*(1600./(t2m+273.))*u2*(es_daily-ea)) /
        (delta + psi*(1.+0.38*u2)))  # [mm d**-1]

    return etp_asceewripenmanmonteith


def penmanmonteith(t2m, t2m_max, t2m_min, u2, rh, rn, sp):

    # Conversoes & cte
    # sp = sp/(10.**3)  # [kPa]

    # cte psicrometrica
    psi = 0.063  # [kPa C**-1] ver  Annex 2, Table 2.2, Allen (1998)
    calorlatvap = 2.45  # [MJ kg**-1]

    rgas = 0.287  # [kJ kg**-1 K**-1]
    epsilon = 0.622

    # Calculos
    tv = 1.01*(t2m + 273)

    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es_tmax = 0.611*np.exp((17.27*t2m_max)/(t2m_max+237.3))  # [kPa]
    es_tmin = 0.611*np.exp((17.27*t2m_min)/(t2m_min+237.3))  # [kPa]

    es_daily = (es_tmax + es_tmin)/2.

    ea = (rh/100.)*es_daily

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    rhoa = sp/(rgas*tv)  # [kg m**-3]
    ca = (psi*epsilon*calorlatvap)/sp  # [MJ kg**-1 C**-1] Calor especifico ar
    ra = 208./u2
    rs = 70.

    Rn = rn

    G = 0

    # ETP Penman-Monteith

    etp_penmanmonteith = (1/calorlatvap)*(
        (delta*(Rn-G)+rhoa*ca*((es_daily-ea)/ra)) /
        (delta + psi*(1.+(ra/rs))))  # [mm d**-1]

    return etp_penmanmonteith


def hargreavessamani(lat, dayofyear, t2m, t2m_max, t2m_min):
    # ([J m**-2], [K], [K], [K])

    # Conversoes
    calorlatvap = 2.45  # [MJ kg**-1]
    chs = (0.00185*(t2m_max-t2m_min)**2)-0.0433*(t2m_max-t2m_min)+0.4023

    # Calculando Ra -------------------------------------
    gsc = 0.0820  # [MJ m-2 min-1]

    latrad = np.radians(lat)

    dr = 1+0.033*np.cos(((2*np.pi)/365)*dayofyear)

    soldec = 0.409*np.sin(((2*np.pi)/365)*dayofyear-1.39)

    ws = np.arccos(-np.tan(latrad)*np.tan(soldec))

    ra = ((24*60)/np.pi)*gsc*dr*(ws*np.sin(latrad)*np.sin(soldec) +
                                 np.cos(latrad)*np.cos(soldec)*np.sin(ws))
    #---------------------------------------------------

    # Hargreaves and Samani, 1985
    etp_hargreavessamani = (0.0135*chs*(ra/calorlatvap)
                            * (np.sqrt(t2m_max-t2m_min))*(t2m + 17.8))
    # [mm d**-1]

    return etp_hargreavessamani


def mhargreaves(lat, dayofyear, daysinmonth, t2m, t2m_max, t2m_min, tp):

    # Conversoes
    # tp = tp*10**3  # [mm d**-1]
    # ndiasmes = t2m.time.dt.daysinmonth.values
    # tp = tp*ndiasmes[:, np.newaxis, np.newaxis]  # [mm month**-1]
    tp = tp*daysinmonth  # [mm month**-1]

    # Calculando Ra -------------------------------------
    gsc = 0.0820  # [MJ m-2 min-1]

    latrad = np.radians(lat)

    dr = 1+0.033*np.cos(((2*np.pi)/365)*dayofyear)

    soldec = 0.409*np.sin(((2*np.pi)/365)*dayofyear-1.39)

    ws = np.arccos(-np.tan(latrad)*np.tan(soldec))

    ra = ((24*60)/np.pi)*gsc*dr*(ws*np.sin(latrad)*np.sin(soldec) +
                                 np.cos(latrad)*np.cos(soldec)*np.sin(ws))
    #---------------------------------------------------

    # ra_mmday = (ra*(10**6)) / (
    #     (2500.8-2.37*t2m +
    #      0.0016*(t2m**2) -
    #      0.00006*(t2m**3.))*10.**3)  # [mm d**-1]
    ra_mmday = ra*0.408  # aproximacao FAO

    # Modified Hargreaves
    etp_mhargreaves = (0.0013*ra_mmday*(t2m + 17.) *
                       (((t2m_max-t2m_min)-0.0123*tp)**0.76))
    # [mm d**-1]
    return etp_mhargreaves


def priestleytaylor(t2m, rn):

    # Conversoes & cte
    alpha = 1.26
    calorlatvap = 2.45  # [MJ kg**-1]
    # cte psicrometrica
    psi = 0.063  # [kPa C**-1]
    
    # Calculos
    es = 0.6108*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    Rn = rn

    G = 0.

    # Priestley and Taylor, (1972)
    etp_priestleytaylor = alpha*((delta/(delta+psi))*(Rn/calorlatvap)
                                 - (G/calorlatvap))
    # [mm d**-1]
    return etp_priestleytaylor


def thornthwaite(t2m, Ith, ath, daylh):

    etp_thornthwaite = (16 * (daylh/24)
                        * (1/30)
                        * ((10*t2m)/Ith)**ath)  # [mm d**-1]

    return etp_thornthwaite
