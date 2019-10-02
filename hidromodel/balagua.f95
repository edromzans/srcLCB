program balagua
  !Modelo de balanco de agua - Vandewiele (1992)
  !equacao basica
  !
  !m2 = m1 + p2 - r2 - d2
  !
  !indice 1 e 2 indica posicao no tempo (mes), anterior e posterior
  !m1 e m2 : conteudo de agua no solo
  !p2: precipitacao
  !r2: evapotranspiracao real
  !d2: escoamento basico + escoamento lendo (s_t + f_t)
  !q2: vazao observada, sendo; sqrt(q2) = sqrt(d2) + u
  implicit none
  real:: m2, p2, r2, d2
  real:: f2
  real:: m1=500.
  integer(4), parameter:: n_par = 3 !quantidade de parametros
  integer(4), parameter:: m_func = 214 !numero de linhas (wc -l input.txt)
  integer(4), parameter:: ldfjac = m_func !deve ser > n_par 
  !external lmstr1_f
  real(8):: x_a(npar), a2l
  real(8):: fjac(ldfjac,n_par), fjrow(n_par), fvec(m_func), tol, x(n_par) 
  integer(4):: iflag, info
  
  integer(4):: ano, mes, dia, hora, min, seg
  real(8):: etp, escb
  integer(8):: ios=0

  x_a(1) = 0.5
  x_a(2) = 50.
  x_a(3) = 50.
  a2l = 1.

  call lmstr1 ( fcn, m_func, n_par, x_a, fvec, fjac, ldfjac, tol, info )
  
  


  
  !m2 = m1 + p2 - r2 - d2
  !r2 = etp*(1-a1**((p2+max(m2,0))/etp))
  ! !conversao de rad de 10^6(J)(m^-2)(dia^-1) para (mm)(dia^-1)
  ! radmmdia = rad * ( 10.**3. / (2500.8 - 2.37*tmed + 0.0016*(tmed**2.) - 0.00006*(tmed**3.)) )  ! etp = (0.0023*radmmdia*(tmax-tmin)**0.5)*(tmed+17.8)
  ! print '(F10.3)', etp
  
end program balagua

subroutine fnc(m, n, x, fvec, fjrow, iflag)

  open(1, file='output')
  open(3, file='input.txt', status='old')
  read(3, *, iostat=ios) ! read head
  do while (ios == 0)
     read(3, *, iostat=ios) ano, mes, dia, hora, min, seg, etp, p2, q2, escb

     s2 =  !escoamento lento
     n2 = !precipitacao ativa
     f2 = !escoamento rapido

     
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



  
  return
end subroutine fnc
