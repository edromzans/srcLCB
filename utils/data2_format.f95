program data2_format
  implicit none
  character(len=100):: dir, namefile, frmt
  character(len=500):: line
  character(len=8):: nymd
  real:: swdown, em, tm, um, prec, rnetm
  integer:: ios=0
  
  namefile='data2'

  open(1, file='data2', status='old')
  open(2, file='defaultdata2')
  write(2,'(A8,6A11)') 'datetime', 'Ki(Wm^-2)', 'em(hPa)', 'tm(K)', 'um(ms^-1)', 'prec(mm)', 'Rn(Wm^-2)'
!  write(2,'(A8,6A10)') 'yymmddhh', 'Wm^-2', 'hPa', 'K', 'ms^-1', 'mm', 'Wm^-2'
  
  read(1, *, iostat=ios) ! read head
  
  do while (ios == 0)
     read(1, *, iostat=ios) nymd, swdown, rnetm, em, tm, um, prec !check columns firt 
     write(2,'(A8,6F11.4)') nymd, swdown, em, tm, um, prec, rnetm
  end do

  close(1)
  close(2)
end program data2_format
