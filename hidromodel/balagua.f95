program balagua
  implicit none
  real:: m1, m2, p2, r2, d2
  real:: etp, a1
  integer:: ano, mes, dia, hora, min, seg
  real:: rad, tmax, tmin, tmed
  integer:: ios=0
  
  !Modelo de balanco de agua - Vandewiele (1992)
  !equacao basica
  !
  !m2 = m1 + p2 - r2 - d2
  !
  !indice 1 e 2 indica posicao no tempo (mes), anterior e posterior
  !m1 e m2 : conteudo de agua no solo
  !p2: precipitacao
  !r2: evapotranspiracao real
  !d2: vazao

  !Calculo da evapotrans potencial (etp)
  open(3, file='dadosamb.txt', status='old')
  read(3, *, iostat=ios) ! read head
  print *, ios
  do while (ios == 0)
     read(3, *, iostat=ios) ano, mes, dia, hora, min, seg, rad, tmax, tmin, tmed
     etp = 0.0023*rad*(tmax-tmin)**0.5*(tmed+17.8)
     print *, etp
  end do
  close(3)
  !m2 = m1 + p2 - r2 - d2
  !r2 = etp*(1-a1**((p2+max(m2,0))/etp))
end program balagua
