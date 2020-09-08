# dircopia='/media/evandro/e3203f85-44a0-4132-8800-618b188bc18a/lcbiag'
# dircopia='/media/evandro/4224-7244/lcbiag'
# dircopia='/media/evandro/EDROMZANS/lcbiag'
dircopia='/home/evandro/MEGAsync/lcbiag'
          
mkdir -p $dircopia
mkdir -p $dircopia/src_codes/
mkdir -p $dircopia/chaveiro/

rsync -azvch --progress /dados/SiB $dircopia/ --delete

rsync -azvch --progress /dados/ProcessoOtimizacaoModelos $dircopia/ --delete
#rsync -azvch --progress /dados/CRU_TS $dircopia/ --delete
#rsync -azvch --progress /dados/ERA5-Land $dircopia/ --delete
rsync -azvch --progress /dados/ET0_xavier $dircopia/ --delete


rsync -azvch --progress /home/evandro/documentos $dircopia/ --delete
rsync -azvch --progress /home/evandro/src_codes/{LCB,srcLCB,SiB2model,gitSiB2model,git_SiB2-LCB} $dircopia/src_codes/ --delete 
rsync -azvch --progress /home/evandro/SIBI_controle $dircopia --delete
#rsync -azv --progress /home/evandro/chaveiro/lcb_pswd.kdbx $dircopia/chaveiro/ --delete
rsync -azvch --progress /home/evandro/chaveiro/ $dircopia/chaveiro/ --delete

#copia dos repositorios
svnadmin dump /home/evandro/svnrepos/srcLCB | gzip -9 > $dircopia/srcLCB.dump.gz
svnadmin dump /home/evandro/svnrepos/SiB2model | gzip -9 > $dircopia/SiB2model.dump.gz
