program balagua
  implicit none
  real:: m2, p2, r2, d2
  real:: m1=500., a1=0.5
  integer:: ano, mes, dia, hora, min, seg
  real:: etp, escb
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

  open(3, file='input.txt', status='old')
  read(3, *, iostat=ios) ! read head
  print *, ios
  do while (ios == 0)
     read(3, *, iostat=ios) ano, mes, dia, hora, min, seg, etp, p2, d2, escb
     
     r2 = amin1(etp*(1.-a1**((p2+max(m2,0.))/etp)), (p2+max(m2,0.)) )

     !print *, amin1(20.,5.)

     m2 = m1 + p2 - r2 - d2

     print '(I5,I03,2F11.1)', ano, mes,  m2, (m2-m1)
     
     m1 = m2
  end do
  close(3)
  !m2 = m1 + p2 - r2 - d2
  !r2 = etp*(1-a1**((p2+max(m2,0))/etp))


  ! !conversao de rad de 10^6(J)(m^-2)(dia^-1) para (mm)(dia^-1)
  ! radmmdia = rad * ( 10.**3. / (2500.8 - 2.37*tmed + 0.0016*(tmed**2.) - 0.00006*(tmed**3.)) ) 
  ! etp = (0.0023*radmmdia*(tmax-tmin)**0.5)*(tmed+17.8)
  ! print '(F10.3)', etp
  
end program balagua
