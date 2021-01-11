import numpy as np


def extratrad(lat, dayofyear):

    # lat = -22.90
    # dayofyear = 200
    gsc = 0.0820  # [MJ m-2 min-1]

    latrad = np.radians(lat)

    dr = 1+0.033*np.cos(((2*np.pi)/365)*dayofyear)

    soldec = 0.409*np.sin(((2*np.pi)/365)*dayofyear-1.39)

    ws = np.arccos(-np.tan(latrad)*np.tan(soldec))

    ra = ((24*60)/np.pi)*gsc*dr*(ws*np.sin(latrad)*np.sin(soldec) +
                                 np.cos(latrad)*np.cos(soldec)*np.sin(ws))

    return ra  # [MJ m**-2 day**-1]
