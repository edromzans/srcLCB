import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

dadosobs = pd.read_table(
    'TempoExSprings.txt', delim_whitespace=True)

t = np.float64(dadosobs['t'])
npos = np.float64(dadosobs['Npos'])


t = t / 3600.


def fit_func(npos, a, b):
    return a*npos + b


params = curve_fit(fit_func, npos, t)

[a, b] = params[0]

print('a = ', a)
print('b = ', b)
print('horas = a*npos + b')
print('npos = (horas - b)/a')

estimatempo = a*npos + b

plt.scatter(npos, t)
plt.plot(npos, estimatempo)
plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 6))
plt.xlabel('possibilidades')
plt.ylabel('tempo (h)')
plt.show()
