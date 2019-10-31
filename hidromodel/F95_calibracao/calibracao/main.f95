subroutine jcn(m_func, n_par, x_a, fvec, fjrow, iflag)
  use varsobs
  implicit none
  integer (kind=8) :: n_par 
  integer (kind=8) :: m_func
  real (kind=8) :: x_a(n_par)
  real (kind=8) :: a_2
  real (kind=8) :: fjrow(n_par)
  real (kind=8) :: fvec(m_func)
  real (kind=8) :: errosimples(m_func)
  integer (kind=4) :: iflag
  real (kind=8) :: m1
  real (kind=8) :: m2
  real (kind=8) :: d2
  real (kind=8) :: r2
  real (kind=8) :: f2
  real (kind=8) :: s2
  real (kind=8) :: n2
  integer (kind=8) :: ikount
    
  call readobs()

  m1 = 500.
  a_2 = 0.5 !parametro a2linha = 1/2, 1 ou 2
  
  ikount = 0
  
  if (iflag == 1) then
     do kount=1, m_func
        r2 = dmin1( etp(kount)*(1.-x_a(1)**((p2(kount)+max(m1,0.))/etp(kount))), (p2(kount)+max(m1,0.)) )
        
        s2 = x_a(2)*(max(m1,0.)**a_2) !escoamento lento
        n2 = p2(kount)-etp(kount)*(1-exp(-p2(kount)/etp(kount))) !precipitacao ativa
        f2 = x_a(3)*max(m1,0.)*n2 !escoamento rapido
        d2 = s2+f2

        !print *,  etp(kount), p2(kount), q2(kount), escb(kount) 
        !print *, 'parametros: ', x_a
        !print *, '----->', q2(kount), d2, abs(q2(kount)-d2)
        
        m2 =  m1 + p2(kount) - r2 - d2
        !fvec(kount) = sqrt(q2(kount)) - sqrt(d2)
        fvec(kount) = q2(kount)-d2
        errosimples(kount) = abs(q2(kount)-d2)
        
        !       write(1,'(I4,I3,I3,I3,I3,I3,14F11.1)') ano, mes, dia, hora, min, seg,&
        !            m2, (m2-m1), p2, r2, etp, d2, s2, escb, f2, fvec(kount), x_a(1),&
        !            x_a(2), x_a(3), a_2
        
        m1 = m2
     end do
     !Avaliando a mudança dos parametros e diminuicao do erro <-------------------------------
     !print *, 'parametros (3), soma(errosimples), soma(vfec): ', x_a, sum(errosimples), sum(fvec**2)
  !end if
  else if (2 <= iflag ) then
     print *, '#################$$$$$$$$$$----------> ', iflag

     
     fjrow(1)
     fjrow(2)
     fjrow(3)


     

     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
     !iflag = 0
     !do ikount = 1, n_par
     !   fjrow(ikount) = float(ikount)*x_a(ikount)
     !end do
     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  end if

  return
end subroutine jcn

subroutine calibra()
  implicit none
  integer (kind=8), parameter:: n_par = 3 !quantidade de parametros
  integer (kind=8), parameter:: m_func = 215 !numero de linhas (wc -l input.txt)
  integer (kind=8), parameter:: ldfjac = m_func !deve ser > n_par 
  real (kind=8) :: x_a(n_par)
  real (kind=8) :: fjac(ldfjac,n_par)
  real (kind=8) :: fjrow(n_par)
  real (kind=8) :: fvec(m_func)
  real (kind=8) :: tol
  integer (kind=4) :: iflag
  integer (kind=4) :: info
  external jcn

  x_a(1) = 0.5
  x_a(2) = 0.5
  x_a(3) = 0.5
  
  tol = 0.00001D+00

  call lmstr1( jcn, m_func, n_par, x_a, fvec, fjac, ldfjac, tol, info )
  
  write ( *, '(a)' ) ' '
  write ( *, '(a,i6)' ) '  Returned value of INFO = ', info
  print *, '------------>', x_a
end subroutine calibra

program main
  implicit none
  call calibra()
end program main
