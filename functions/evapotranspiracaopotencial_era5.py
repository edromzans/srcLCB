'''
Calcula a ETP a partir dos dados das reanalises do
ECMWF ERA5 Land
'''
import numpy as np


def penmanmontaith(t2m, u10, v10, d2m, sp, ssr, str):

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    d2m = d2m - 273.15  # [C]

    str = (str/10.**6)  # [MJ m**-2 d**-1]
    ssr = (ssr/10.**6)  # [MJ m**-2 d**-1]

    sp = sp/10.**3      # [kPa]
    # rs = 0.23           # Albedo - 0.23 grass reference

    # cte psicrometrica
    # psi = 0.063  # [kPa C**-1]
    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]
    psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]

    ea = 0.611*np.exp((17.27*d2m)/(d2m+237.3))  # [kPa]

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    u2 = np.sqrt(u10**2+v10**2)  # [m s**-1]

    tm1 = t2m
    tm0 = np.roll(t2m, 1)
    G = 0.14*(tm1-tm0)

    # Saldo de radiacao de onda curta (Rns):
    #
    # Considerado a radiacao direta e difusa para a superficie (S_sup_down)
    # e o albedo
    #
    # Rns = (1. - rs) * ssrd
    #
    # Usando o saldo de onda curta na superficie (S_sup_down - S_sup_up)
    # do ERA5 Land
    Rns = ssr

    # Saldo de radiacao de onda longa (Rnl):
    # Aqui não entra o que a Terra absorve da
    # emissão de onda longa da atmosfera (L_sup_down)
    Rnl = (str)*(-1)
    #
    # Saldo de onda longa do ERA5 Land
    # Rnl_totalERA5Land = strd - str

    Rn = (Rns - Rnl)

    # ETP Penman-Montaith
    etp_penmanmontaith = (
        (0.408*delta*(Rn-G) + psi*(900./(t2m+273.))*u2*(es-ea)) /
        (delta + psi*(1.+0.34*u2)))  # [mm d**-1]

    return etp_penmanmontaith


def blaneycriddle(k_coef, p_coef, t2m):

    # Conversoes
    t2m = t2m - 273.15  # [C]

    etp_blaneycriddle = k_coef*p_coef*(0.46*t2m + 8.13)

    return etp_blaneycriddle


def hargreavessamani(tisr, tmax, tmin, t2m):

    a = 0.0023  # parametro

    # Conversoes
    t2m = t2m - 273.15  # [C]

    tisr_mmday = tisr / (
        (2500.8-2.37*t2m +
         0.0016*(t2m**2) -
         0.00006*(t2m**3.))*10.**3)  # [mm d**-1]

    etp_hargreavessamani = a*tisr_mmday*np.sqrt(tmax-tmin)*(t2m + 17.8)

    return etp_hargreavessamani


def makkink(t2m, sp, ssrd):

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    ssrd = ssrd*(1./(4184*10.**4))  # [cal cm**-2 d**-1]
    sp = sp/10.**3      # [kPa]

    # cte psicrometrica
    # psi = 0.063  # [kPa C**-1]
    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]

    psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]
    psi = psi*10.  # [mb C**-1]

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]
    delta = delta*10.  # [mb C**-1]

    calorlatvap = calorlatvap*(10.**6)*(1./(4184.*10.**3))  # [cal g**-1]

    etp_makkink = 0.61*(delta/(delta+psi))*(ssrd/calorlatvap) - 0.12

    return etp_makkink


def priestleytaylor(ssr, str, t2m, sp):

    # Conversoes & cte
    alpha = 1.26
    # alpha = 12.6
    t2m = t2m - 273.15  # [C]
    # str = str/(4.1868*(10.**(4)))  # [cal cm**-2 d**-1]
    # ssr = ssr/(4.1868*(10.**(4)))  # [cal cm**-2 d**-1]
    str = str/10.**6
    ssr = ssr/10.**6

    sp = sp/(10.**3)      # [kPa]

    # cte psicrometrica
    # psi = 0.063  # [kPa C**-1]
    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]

    psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]
    # psi = psi*10.  # [mb C**-1]
    print('psicrometrica@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(psi)
    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]
    # delta = delta*10.  # [mb C**-1]

    print('delta-----------------')
    print(delta)
    # calorlatvap = calorlatvap*(1./(4.1868*(10.**(-3))))  # [cal g**-1]

    print('calorlatvap&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(calorlatvap)
    # Saldo de radiacao de onda curta (Rns):
    #
    # Considerado a radiacao direta e difusa para a superficie (S_sup_down)
    # e o albedo
    #
    # Rns = (1. - rs) * ssrd
    #
    # Usando o saldo de onda curta na superficie (S_sup_down - S_sup_up)
    # do ERA5 Land
    Rns = ssr

    # Saldo de radiacao de onda longa (Rnl):
    # Aqui não entra o que a Terra absorve da
    # emissão de onda longa da atmosfera (L_sup_down)
    Rnl = (str)*(-1)
    #
    # Saldo de onda longa do ERA5 Land
    # Rnl_totalERA5Land = strd - str

    Rn = (Rns - Rnl)
    print('Rn%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(Rn)
    etp_priestleytaylor = alpha*(delta/(delta+psi))*(Rn/calorlatvap)

    return etp_priestleytaylor


def rohwer(t2m, d2m, u10, v10):

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    d2m = d2m - 273.15  # [C]

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es = es/0.1333  # [mmHg]

    ea = 0.611*np.exp((17.27*d2m)/(d2m+237.3))  # [kPa]
    ea = ea/0.1333  # [mmHg]

    u2 = np.sqrt(u10**2+v10**2)

    etp_rohwer = 0.44*(1. + 0.27*u2)*(es - ea)

    return etp_rohwer


def penman(t2m, d2m, u10, v10):

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    d2m = d2m - 273.15  # [C]

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es = es/0.1333  # [mmHg]

    ea = 0.611*np.exp((17.27*d2m)/(d2m+237.3))  # [kPa]
    ea = ea/0.1333  # [mmHg]

    u2 = np.sqrt(u10**2+v10**2)  # [m s**-1]
    u2 = u2*(86400./1609.34)  # [milhas d**-1]

    etp_penman = 0.35*(1. + (0.98/(100.*u2)))*(es - ea)

    return etp_penman
