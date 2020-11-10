'''
Calcula a ETP a partir dos dados das reanalises do
ECMWF ERA5
'''
import numpy as np


def penmanmontaith(t2m, u10, v10, d2m, sp, ssr, str, slhf, sshf):
    # ([K], [m s**-1], [m s**-1], [K], [Pa], [J m**-2], [J m**-2], [J m**-2],
    # [J m**-2])

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
    # G = 0.

    # ETP Penman-Montaith
    etp_penmanmontaith = (
        (0.408*delta*(Rn-G) + psi*(900./(t2m+273.))*u2*(es-ea)) /
        (delta + psi*(1.+0.34*u2)))  # [mm d**-1]

    return etp_penmanmontaith


def hargreavessamani(tisr, tmax, tmin, t2m):
    # ([J m**-2], [C], [C], [K])

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
    # ([K], [Pa], [J m**-2])

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    ssrd = ssrd/10.**6  # [MJ m**-2 d**-1]
    sp = sp/10.**3      # [kPa]

    calorlatvap = 2.501 - (2.361*10.**(-3))*t2m  # [MJ kg**-1]

    # cte psicrometrica
    # psi = 0.063  # [kPa C**-1]
    psi = 0.00163*(sp/calorlatvap)  # [kPa C**-1]

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    etp_makkink = 0.61*(delta/(delta+psi))*(ssrd/calorlatvap) - 0.12

    return etp_makkink


def priestleytaylor(ssr, str, t2m, sp):
    # ([J m**-2], [J m**-2], [K], [Pa])

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
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]

    delta = (4098*es)/((t2m+237.3)**2)  # [kPa C**-1]

    Rn = ssr + str

    etp_priestleytaylor = alpha*(delta/(delta+psi))*(Rn/calorlatvap)

    return etp_priestleytaylor


def penman(t2m, d2m, u10, v10):
    # ([K], [K], [m s**-1], [m s**-1])

    # Conversoes & cte
    t2m = t2m - 273.15  # [C]
    d2m = d2m - 273.15  # [C]

    # Calculos
    es = 0.611*np.exp((17.27*t2m)/(t2m+237.3))  # [kPa]
    es = es/0.1333224  # [mmHg]

    ea = 0.611*np.exp((17.27*d2m)/(d2m+237.3))  # [kPa]
    ea = ea/0.1333224  # [mmHg]

    u2 = np.sqrt(u10**2+v10**2)  # [m s**-1]
    # u2 = u2*(86400./1609.34)  # [milhas d**-1]
    u2 = u2*(3600./1609.34)  # [mph]
    u2 = u2*0.66  # 10m para 2m

    etp_penman = 0.35*(1. + 9.8*(10.**(-3))*u2)*(es - ea)

    return etp_penman
