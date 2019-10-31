module varsobs
  implicit none
  integer (kind=4) :: ano
  integer (kind=4) :: mes
  integer (kind=4) :: dia
  integer (kind=4) :: hora
  integer (kind=4) :: min
  integer (kind=4) :: seg
  integer (kind=8), parameter :: nlines=215 !qtd linhas
  real (kind=8) :: p2(nlines)
  real (kind=8) :: q2(nlines)
  real (kind=8) :: etp(nlines)
  real (kind=8) :: escb(nlines)
  integer (kind=8) :: kount
contains
  subroutine readobs()
    open(3, file='input.txt', status='old')
    !sem header !read(3, *) ! read header
    do kount=1, nlines
       read(3, *) ano, mes, dia, hora, min, seg, etp(kount), p2(kount), q2(kount), escb(kount)
       !print *, ano, etp(kount), p2(kount), q2(kount), escb(kount)
    end do
  close(3)
  end subroutine readobs
end module varsobs

