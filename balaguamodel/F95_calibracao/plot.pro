;dir = '/home/evandro/srcodes/fortran/hidromodel/calibracao_a23/'
dir = '/home/evandro/src_codes/SiB/hidromodel/calibracao_a23/'
file = 'output.txt'

arq =  dir+file
nlines = file_lines(arq)

s_a2 = fltarr(nlines)
s_a3 = fltarr(nlines)

s_erro = fltarr(nlines)
s_erro2 = fltarr(nlines)

a2 = 0.
a3 = 0.
erro = 0.
erro2 = 0.

close, 1
openr, 1, dir+file

for k = 0L, nlines-1L do begin


  ;x_a(1), x_a(2), sum(errosimples), sum(errosimples**2.),  sum(fvec**2)
  
  readf, 1,  a2, a3, erro, erro2 

  ;print,  a2, a3, erro, erro2

  s_a2[k] = a2
  s_a3[k] = a3

  s_erro[k] = erro
  s_erro2[k] = erro2


endfor
close, 1

!p.multi =  [0, 2, 1]
!p.charsize = 1.5

plot, s_a2, s_erro2, xstyle = 1,  ystyle = 1,  title = 'a2'
plot, s_a3, s_erro2, xstyle = 1,  ystyle = 1, title = 'a3'

end
