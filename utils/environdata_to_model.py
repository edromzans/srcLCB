import sys
#Converte em colunas txt os dados de vazao em planilhas
#Deve salvar os dados como csv, com delimitador de colunas ';'
#O idioma da planilha deve ser en_us, eliminando ',' como
#delimitador decimal

dirin1='/dados/ProcessoOtimizacaoModelos/dadosJaraguari/ambientais/'
filein1='rad.csv'

dirin2='/dados/ProcessoOtimizacaoModelos/dadosJaraguari/ambientais/'
filein2='temp.csv'

dirout='/dados/ProcessoOtimizacaoModelos/dadosJaraguari/ambientais/'
fileout='dadosamb.txt'

nlines1 = sum(1 for line in open(dirin1+filein1))
nlines2 = sum(1 for line in open(dirin2+filein2))

datatemporad = ' '
datatempotem = ' '
rad = -999999
tmax = -999999.
tmin = -999999.
tmed = -999999.

radf=open(dirin1+filein1,'r')
hderrad = radf.readline().split(',')

temf=open(dirin2+filein2,'r')
hdertem = temf.readline().split(',')

dsamb=open(dirout+fileout,'w')
dsamb.write('{:^19}'.format('datatempo')+' '
           +'{:11}'.format('rad')
           +'{:11}'.format('tmax')
           +'{:11}'.format('tmin')
           +'{:11}'.format('tmed')
            +'\n')

for k in range(0, nlines1-1):
    flds_rad = radf.readline().split(',')
    flds_tem = temf.readline().split(',')
     
    datatemporad = flds_rad[0]
    datatempotem = flds_tem[0]

    if datatemporad != datatempotem:
        print('tempo nao coincide')
        print(datatemporad, datatempotem)
        break
    
    try:
        rad = float(flds_rad[1])
    except ValueError:
        rad = -999999.
        print(datatemporad[0:4]+' '+datatemporad[5:7]+' '+datatemporad[8:10]+' '
             +datatemporad[11:13]+' '+datatemporad[14:16]+' '+datatemporad[17:19]
             +' sem dado de radiacao')

    try:
        tmax = float(flds_tem[1])
    except ValueError:
        tmax = -999999.
        print(datatempotem[0:4]+' '+datatempotem[5:7]+' '+datatempotem[8:10]+' '
             +datatempotem[11:13]+' '+datatempotem[14:16]+' '+datatempotem[17:19]
             +' sem dado de temperatura')

    try:
        tmin = float(flds_tem[2])
    except ValueError:
        tmin = -999999.
        print(datatempotem[0:4]+' '+datatempotem[5:7]+' '+datatempotem[8:10]+' '
             +datatempotem[11:13]+' '+datatempotem[14:16]+' '+datatempotem[17:19]
             +' sem dado de temperatura')

    if tmax > -999999. and tmin > -999999.:
        tmed = (tmax + tmin)/2.
    else:
        tmed = -999999.
    
    dsamb.write(datatemporad[0:4]+' '+datatemporad[5:7]+' '+datatemporad[8:10]+' '
             +datatemporad[11:13]+'00 00 00'
             +'{:11.2f}'.format(rad)
             +'{:11.2f}'.format(tmax)
             +'{:11.2f}'.format(tmin)
             +'{:11.2f}'.format(tmed)+'\n')

radf.close()
temf.close()
dsamb.close()
