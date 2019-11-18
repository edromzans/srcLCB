def edata1(dirdata1, param_gradm, param_vmax):
    import shutil
    import tempfile

    # dirdata1 = '/home/evandro/SiB2run/'
    data1 = dirdata1 + 'data1'

    # param_gradm = 99.9
    # param_vmax = 99.9
    '''
Cria self.assertRaises(Exception, fun)quivo temporario
    '''
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(data1) as src_file:
            kline = 1
            for line in src_file:
                
                # gradm
                if kline == 15:  # numero da linha
                    # print(line, kline, '<-----------')
                    effcon, gradm, binter, respcp, atheta, btheta = line.split()
                    tmp_file.write('   '+'{:<8}'.format(effcon)
                                   + '{:<8.3f}'.format(param_gradm)
                                   + '{:<8}'.format(binter)
                                   + '{:<8}'.format(respcp)
                                   + '{:<8}'.format(atheta)
                                   + '{:<8}'.format(btheta)
                                   + '\n')
                # vmax
                elif kline == 58:  # numero da linha
                    vmax = line.split()
                    tmp_file.write(' ' + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '{:<6.1f}'.format(param_vmax)
                                   + '\n')
                else:
                    tmp_file.write(line)

                kline += 1

    '''
    Reescreve o data1 a partir do temporario preservando todos os atributos
    '''
    shutil.copystat(data1, tmp_file.name)
    shutil.move(tmp_file.name, data1)
