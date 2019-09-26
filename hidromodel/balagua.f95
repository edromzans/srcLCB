program balagua
  implicit none
  real:: m2, p2, r2, d2
  real:: f2
  real:: m1=500.
  real:: a1=0.5, a2, a3, a4 ! (a4= 0.5 ou 1. ou 2.)
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

  open(1, file='output')
  open(3, file='input.txt', status='old')
  read(3, *, iostat=ios) ! read head
  do while (ios == 0)
     read(3, *, iostat=ios) ano, mes, dia, hora, min, seg, etp, p2, d2, escb
     
     r2 = amin1(etp*(1.-a1**((p2+max(m1,0.))/etp)), (p2+max(m1,0.)) )

     !print *, amin1(20.,5.)

     !d2 = a2*(max(m1,0.))**a4 + a3*(max(m1,0))*(p2-etp*(1-exp(-p2/etp)))

     m2 = m1 + p2 - r2 - d2

     !d2 = s2 + f2  !(s=escoamento basico - escb; f = escoamento rapido )
     f2 = d2 - escb 
     
     !print '(I4,I3,I3,I3,I3,I3,7F11.1)', ano, mes, dia, hora, min, seg, m2, (m2-m1), p2, r2, d2, escb, f2 
     write(1,'(I4,I3,I3,I3,I3,I3,8F11.1)') ano, mes, dia, hora, min, seg, m2, (m2-m1), p2, r2, etp, d2, escb, f2
     
     m1 = m2
  end do
  close(3)
  close(1)
  
  !m2 = m1 + p2 - r2 - d2
  !r2 = etp*(1-a1**((p2+max(m2,0))/etp))
  ! !conversao de rad de 10^6(J)(m^-2)(dia^-1) para (mm)(dia^-1)
  ! radmmdia = rad * ( 10.**3. / (2500.8 - 2.37*tmed + 0.0016*(tmed**2.) - 0.00006*(tmed**3.)) )  ! etp = (0.0023*radmmdia*(tmax-tmin)**0.5)*(tmed+17.8)
  ! print '(F10.3)', etp
  
end program balagua
