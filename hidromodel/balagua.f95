program main
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
  call calibra()
end program main

subroutine calibra()
  implicit none
  integer (kind=4), parameter:: n_par = 3 !quantidade de parametros
  integer (kind=4), parameter:: m_func = 214 !numero de linhas (wc -l input.txt)
  integer (kind=4), parameter:: ldfjac = m_func !deve ser > n_par 
  real (kind=8) x_a(n_par)
  real (kind=8) a_2
  real (kind=8) fjac(ldfjac,n_par)
  real (kind=8) fjrow(n_par)
  real (kind=8) fvec(m_func)
  real (kind=8) tol
  integer (kind=4) iflag
  integer (kind=4) info
  external jcn

  x_a(1) = 0.5
  x_a(2) = 10.
  x_a(3) = 10.
  
  !call jcn( m_func, n_par, x_a, fvec, fjrow, iflag )
  call lmstr1( jcn, m_func, n_par, x_a, fvec, fjac, ldfjac, tol, info )
  
  write ( *, '(a)' ) ' '
  write ( *, '(a,i6)' ) '  Returned value of INFO = ', info
  print *, '------------>', x_a
end subroutine calibra

subroutine jcn(m_func, n_par, x_a, fvec, fjrow, iflag)
  implicit none
  integer (kind=4) n_par 
  integer (kind=4) m_func
  real (kind=8) x_a(n_par)
  real (kind=8) a_2
  real (kind=8) fjrow(n_par)
  real (kind=8) fvec(m_func)
  integer(kind=4) iflag
  real (kind=8) m1 
  real (kind=8) m2
  real (kind=8) p2
  real (kind=8) r2
  real (kind=8) d2
  real (kind=8) q2
  real (kind=8) etp
  real (kind=8) escb
  real (kind=8) f2
  real (kind=8) s2
  real (kind=8) n2
  integer (kind=4) ano
  integer (kind=4) mes
  integer (kind=4) dia
  integer (kind=4) hora
  integer (kind=4) min
  integer (kind=4) seg
  integer (kind=8) ios
  integer (kind=8) kount
  integer (kind=8) ikount

  m1 = 500.
  a_2 = 1. !parametro a2linha = 1/2, 1 ou 2
  
  ios = 0
  kount = 0
  ikount = 0
  
  if (iflag == 1) then
     print *, 'flag 1'
     open(1, file='output.txt')
     open(3, file='input.txt', status='old')
     read(3, *, iostat=ios) ! read head
     do while (ios == 0)
        read(3, *, iostat=ios) ano, mes, dia, hora, min, seg, etp, p2, q2, escb
        
        r2 = dmin1( etp*(1.-x_a(1)**((p2+max(m1,0.))/etp)), (p2+max(m1,0.)) )
        
        s2 = x_a(2)*(max(m1,0.)**a_2) !escoamento lento
        n2 = p2-etp*(1-exp(-p2/etp)) !precipitacao ativa
        f2 = x_a(3)*max(m1,0.)*n2 !escoamento rapido
        d2 = s2+f2
        
        m2 = m1 + p2 - r2 - d2
        
        fvec(kount) = sqrt(q2) - sqrt(d2)
                
        write(1,'(I4,I3,I3,I3,I3,I3,14F11.1)') ano, mes, dia, hora, min, seg,&
             m2, (m2-m1), p2, r2, etp, d2, s2, escb, f2, fvec(kount), x_a(1),&
             x_a(2), x_a(3), a_2
        
        m1 = m2
        kount = kount + 1
     end do
     close(3)
     close(1)

  end if
     
  ! else! if (2 <= iflag ) then
  !    print *, 'opsssssss', n_par, iflag
  !    iflag = 0
  !    do ikount = 1, n_par
  !       fjrow(ikount) = float(ikount)*x_a(ikount)
  !    end do
  !    print *, fjrow
  ! end if

  return
end subroutine jcn
