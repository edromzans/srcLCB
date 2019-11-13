import shutil
import tempfile

dirdata1 = '/home/evandro/SiB2run/'
data1 = dirdata1 + 'data1'

param_gradm = 99.9
param_vmax = 999.9
'''
Cria arquivo temporario
'''
with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
    with open(data1) as src_file:
        kline = 1
        for line in src_file:

            # gradm
            if kline == 15:
                # print(line, kline, '<-----------')
                effcon, gradm, binter, respcp, atheta, btheta = line.split()
                tmp_file.write('   '+'{:<8}'.format(effcon)
                               + '{:<8.3f}'.format(param_gradm)
                               + '{:<8}'.format(binter)
                               + '{:<8}'.format(respcp)
                               + '{:<8}'.format(atheta)
                               + '{:<8}'.format(btheta)
                               + '\n')
               
                # tmp_file.write('ops teste \n')
                # tmp_file.write(line)

            # vmax
            # elif kline == 58:
            #     vmax = line.split()

            else:
                tmp_file.write(line)

            kline += 1

'''
Reescreve o data1 a partir do temporario preservando todos os atributos
'''
shutil.copystat(data1, tmp_file.name)
shutil.move(tmp_file.name, data1)
