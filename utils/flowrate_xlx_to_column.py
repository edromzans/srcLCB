import numpy as np
import sys
#import pdb; pdb.set_trace()

dirin='/dados/ProcessoOtimizacaoModelos/dadosJaraguari/agua/'
filein='PCJ.csv'

dirout='/dados/ProcessoOtimizacaoModelos/dadosJaraguari/agua/'
fileout='aguadados.txt'

nlines = sum(1 for line in open(dirin+filein))

#datas = np.chararray((12,936), itemsize=19, order='F')
#datas[:] = ' '
#datas = [' ' for x in range(nlines-1)]

datatempo = ' ' 

prec = -999999
vazao = -999999.
escb = -999999.

# prec = np.ndarray(shape=(nlines-1), dtype=int, order='F')
# prec[:] = -999999

# vazao = np.ndarray(shape=((nlines-1)), dtype=float, order='F')
# vazao[:] = -999999.

# escb = np.ndarray(shape=((nlines-1)), dtype=float, order='F')
# escb[:] = -999999.

#sys.exit()

flowrate=open(dirin+filein,'r')
header = flowrate.readline().split(';')

agd=open(dirout+fileout,'w')

kount = 0
for line in flowrate:
    flds = line.split(';')
    
    datatempo = flds[0]
    
    try:
        prec = int(flds[1])
    except ValueError:
        prec = -999999
        print('sem dado de precipitacao')
        
    try:
        vazao = float(flds[2])
    except ValueError:
        vazao = -999999.
        print('sem dado de vazao')
        
    try:
        escb = float(flds[3])
    except ValueError:
        escb = -999999.
        print('sem dado de escoamento basico')

    agd.write(datatempo[0:4]+' '+datatempo[5:7]+' '+datatempo[8:10]+
             ' '+datatempo[11:13]+' '+datatempo[14:16]+' '+datatempo[17:19]
             +'{:8d}'.format(prec)
             +'{:11.2f}'.format(vazao)
             +'{:11.2f}'.format(escb)+'\n')

#    dados[:,kount] = float(flds[1:4])
#    print(flds[1:4])
#    print(prec[kount],vazao[kount],escb[kount])
#    print(float(flds[1]),float(flds[2]))
#    print( np.where(flds[1:4] != ''))
#    break
#    breakpoint()

    kount += 1
flowrate.close()
agd.close()







