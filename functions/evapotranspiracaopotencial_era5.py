'''
Calcula a ETP a partir dos dados das reanalises do
ECMWF ERA5 Land
'''
import numpy as np


def fao56reference(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                   ssr, str, slhf, sshf):
    # ([K], [K], [K], [m s**-1], [m s**-1], [K], [Pa],
    # [J m**-2], [J m**-2], [J m**-2], [J m**-2])

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    d2m = d2m - 273.15  # [C]

    str = (str/10.**6)  # [MJ m**-2 d**-1]
    ssr = (ssr/10.**6)  # [MJ m**-2 d**-1]
    # strd = (strd/10.**6)  # [MJ m**-2 d**-1]

    slhf = slhf/10.**6
    sshf = sshf/10.**6

    sp = sp/10.**3      # [kPa]
    # rs = 0.23           # Albedo - 0.23 grass reference

    # cte psicrometrica
    # psi = 0.063  # [kPa C**-1]
    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]
    psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es_tmax = 0.611*np.exp((17.27*t2m_max)/(t2m_max+237.3))  # [kPa]
    es_tmin = 0.611*np.exp((17.27*t2m_min)/(t2m_min+237.3))  # [kPa]

    es_daily = (es_tmax + es_tmin)/2.

    ea = 0.611*np.exp((17.27*d2m)/(d2m+237.3))  # [kPa]

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    u2 = np.sqrt(u10**2+v10**2)  # [m s**-1]
    u2 = u2*0.66  # 10m para 2m

    # tm1 = t2m
    # tm0 = np.roll(t2m, 1)
    # G = 0.14*(tm1-tm0)

    # Saldo de radiacao de onda curta (Rns):
    #
    # Considerado a radiacao direta e difusa para a superficie (S_sup_down)
    # e o albedo
    #

    # Rns = (1. - rs) * ssrd
    #
    # Usando o saldo de onda curta na superficie (S_sup_down - S_sup_up)
    # do ERA5 Land
    # Rns = ssr
    #

    # Saldo de radiacao de onda longa (L_sup_down - L_sup_up):
    # Rnl = (str)*(-1)
    #
    # Componente da Terra para a atmosfera
    # L_sup_up = strd - str
    #

    # Rn = (Rns - Rnl)
    Rn = ssr + str

    G = Rn + slhf + sshf

    # ETP FAO-56 Reference Crop Evapotranspiration
    etp_fao56reference = (
        (0.408*delta*(Rn-G) + psi*(900./(t2m+273.))*u2*(es_daily-ea)) /
        (delta + psi*(1.+0.34*u2)))  # [mm d**-1]

    return etp_fao56reference


def asceewripenmanmonteith(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                           ssr, str, slhf, sshf):
    # ([K], [K], [K], [m s**-1], [m s**-1], [K], [Pa],
    # [J m**-2], [J m**-2], [J m**-2], [J m**-2])

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    d2m = d2m - 273.15  # [C]

    str = (str/10.**6)  # [MJ m**-2 d**-1]
    ssr = (ssr/10.**6)  # [MJ m**-2 d**-1]
    # strd = (strd/10.**6)  # [MJ m**-2 d**-1]

    slhf = slhf/10.**6
    sshf = sshf/10.**6

    sp = sp/10.**3      # [kPa]
    # rs = 0.23           # Albedo - 0.23 grass reference

    # cte psicrometrica
    # psi = 0.063  # [kPa C**-1]
    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]
    psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es_tmax = 0.611*np.exp((17.27*t2m_max)/(t2m_max+237.3))  # [kPa]
    es_tmin = 0.611*np.exp((17.27*t2m_min)/(t2m_min+237.3))  # [kPa]

    es_daily = (es_tmax + es_tmin)/2.

    ea = 0.611*np.exp((17.27*d2m)/(d2m+237.3))  # [kPa]

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    u2 = np.sqrt(u10**2+v10**2)  # [m s**-1]
    u2 = u2*0.66  # 10m para 2m

    Rn = ssr + str

    G = Rn + slhf + sshf

    # ASCE-EWRI Standardized Penman-Monteith Equation
    etp_asceewripenmanmonteith = (
        (0.408*delta*(Rn-G) + psi*(1600./(t2m+273.))*u2*(es_daily-ea)) /
        (delta + psi*(1.+0.38*u2)))  # [mm d**-1]

    return etp_asceewripenmanmonteith


def penmanmonteith(t2m, t2m_max, t2m_min, u10, v10, d2m, sp,
                   ssr, str, slhf, sshf):
    # ([K], [K], [K], [m s**-1], [m s**-1], [K], [Pa],
    # [J m**-2], [J m**-2], [J m**-2], [J m**-2])

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    d2m = d2m - 273.15  # [C]

    str = (str/10.**6)  # [MJ m**-2 d**-1]
    ssr = (ssr/10.**6)  # [MJ m**-2 d**-1]
    # strd = (strd/10.**6)  # [MJ m**-2 d**-1]

    slhf = slhf/10.**6
    sshf = sshf/10.**6

    sp = sp/10.**3      # [kPa]

    # cte psicrometrica
    # psi = 0.063  # [kPa C**-1]
    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]
    psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]

    rgas = 0.287  # [kJ kg**-1 K**-1]
    epsilon = 0.622

    # Calculos

    tv = 1.01*(t2m + 273)

    ea = 0.6108*np.exp((17.27*d2m)/(d2m+237.3))  # [kPa]
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es_tmax = 0.611*np.exp((17.27*t2m_max)/(t2m_max+237.3))  # [kPa]
    es_tmin = 0.611*np.exp((17.27*t2m_min)/(t2m_min+237.3))  # [kPa]

    es_daily = (es_tmax + es_tmin)/2.

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    u2 = np.sqrt(u10**2+v10**2)  # [m s**-1]
    u2 = u2*0.66  # 10m para 2m

    rhoa = sp/(rgas*tv)  # [kg m**-3]
    ca = (psi*epsilon*calorlatvap)/sp  # [MJ kg**-1 C**-1]
    ra = 208./u2
    rs = 70.

    Rn = ssr + str

    G = Rn + slhf + sshf

    # ETP Penman-Monteith

    etp_penmanmonteith = (1/calorlatvap)*(
        (delta*(Rn-G)+rhoa*ca*((es_daily-ea)/ra)) /
        (delta + psi*(1.+(ra/rs))))  # [mm d**-1]

    return etp_penmanmonteith


def hargreavessamani(tisr, t2m, t2m_max, t2m_min):
    # ([J m**-2], [K], [K], [K])

    # Conversoes
    t2m = t2m - 273.15  # [C]
    t2m_max = t2m_max - 273.15  # [C]
    t2m_min = t2m_min - 273.15  # [C]

    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]
    chs = 0.00185*(t2m_max-t2m_min)**2-0.0433*(t2m_max-t2m_min)+0.4023

    etp_hargreavessamani = (0.0135*chs*(tisr/calorlatvap) *
                            (np.sqrt(t2m_max-t2m_min))*(t2m + 17.8))

    return etp_hargreavessamani


def mhargreaves(tisr, t2m, t2m_max, t2m_min, tp_monthly):
    # ([J m**-2], [K], [K], [K], [mm month**-1])

    # Conversoes
    t2m = t2m - 273.15  # [C]
    t2m_max = t2m_max - 273.15  # [C]
    t2m_min = t2m_min - 273.15  # [C]

    tisr_mmday = tisr / (
        (2500.8-2.37*t2m +
         0.0016*(t2m**2) -
         0.00006*(t2m**3.))*10.**3)  # [mm d**-1]

    etp_mhargreaves = (0.0013*tisr_mmday*(t2m + 17.) *
                       ((t2m_max-t2m_min)-0.0123*tp_monthly)**0.76)

    return etp_mhargreaves


def priestleytaylor(ssr, str, slhf, sshf, t2m, sp):
    # ([J m**-2], [J m**-2], [J m**-2], [J m**-2], [K], [Pa])

    # Conversoes & cte
    alpha = 1.26
    t2m = t2m - 273.15  # [C]
    str = str/10.**6    # [MJ m**-2 d**-1]
    ssr = ssr/10.**6    # [MJ m**-2 d**-1]
    sp = sp/(10.**3)    # [kPa]

    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]

    # cte psicrometrica
    # psi = 0.063  # [kPa C**-1]
    psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]

    # Calculos
    es = 0.6108*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    Rn = ssr + str

    G = Rn + slhf + sshf

    etp_priestleytaylor = alpha*((delta/(delta+psi))*(Rn/calorlatvap)
                                         - (G/calorlatvap))

    return etp_priestleytaylor


def thornthwaite(t2m, Ith, ath, hrday, ndaymonth):
    # Ith =
    # ath =
    etp_thornthwaite = 16*(hrday/24)*(ndaymonth/30)*((10*t2m)/Ith)**ath

    return etp_thornthwaite
