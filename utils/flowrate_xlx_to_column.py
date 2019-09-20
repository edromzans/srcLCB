#Converte em colunas txt os dados de vazao em planilhas
#Deve salvar os dados como csv, com delimitador de colunas ';'
#O idioma da planilha deve ser en_us, eliminando ',' como
#delimitador decimal

dirin='/dados/ProcessoOtimizacaoModelos/dadosJaraguari/agua/'
filein='PCJ.csv'

dirout='/dados/ProcessoOtimizacaoModelos/dadosJaraguari/agua/'
fileout='aguadados.txt'

nlines = sum(1 for line in open(dirin+filein))

datatempo = ' ' 
prec = -999999
vazao = -999999.
escb = -999999.

#------------------------------------------------------------
#selecione o bloco de dados: datatempo, prec, vazao e esc_bas.
#considere o primeiro bloco como 0, segundo como 1, ...
bloco = 10 #estacao 626000000; lat=-22.88,long=-46.63; RIO ABAIXO (FAZ. CACHOEIRA); Curso do Rio Jaguari
#-------------------------------------------------------------

n = bloco*4

flowrate=open(dirin+filein,'r')
header = flowrate.readline().split(';')

agd=open(dirout+fileout,'w')
agd.write('{:^19}'.format(header[0+n])+' '
          +'{:8}'.format(header[1+n])
          +'{:11}'.format(header[2+n])
          +'{:11}'.format(header[3+n])
          +'\n')

for line in flowrate:
    flds = line.split(';')
    
    datatempo = flds[0+n]
    
    try:
        prec = int(flds[1+n])
    except ValueError:
        prec = -999999
        print(datatempo[0:4]+' '+datatempo[5:7]+' '+datatempo[8:10]+
             ' '+datatempo[11:13]+' '+datatempo[14:16]+' '+datatempo[17:19]
             +' sem dado de precipitacao')
        
    try:
        vazao = float(flds[2+n])
    except ValueError:
        vazao = -999999.
        print(datatempo[0:4]+' '+datatempo[5:7]+' '+datatempo[8:10]+
             ' '+datatempo[11:13]+' '+datatempo[14:16]+' '+datatempo[17:19]
             +' sem dado de vazao')
        
    try:
        escb = float(flds[3+n])
    except ValueError:
        escb = -999999.
        print(datatempo[0:4]+' '+datatempo[5:7]+' '+datatempo[8:10]+
             ' '+datatempo[11:13]+' '+datatempo[14:16]+' '+datatempo[17:19]
             +' sem dado de escoamento basico')

    agd.write(datatempo[0:4]+' '+datatempo[5:7]+' '+datatempo[8:10]+
             ' '+datatempo[11:13]+' '+datatempo[14:16]+' '+datatempo[17:19]
             +'{:8d}'.format(prec)
             +'{:11.2f}'.format(vazao)
             +'{:11.2f}'.format(escb)+'\n')

flowrate.close()
agd.close()
