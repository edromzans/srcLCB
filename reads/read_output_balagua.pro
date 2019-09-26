pro read_output_balagua,  arqv,  datatempo, m2, Dm, p2, r2, etp, d2, s2, f2
  
  nlines =  file_lines(arqv) ;- 1L ; desconta o header
  
  datatempo =  dblarr(nlines)
  m2 = fltarr(nlines)
  Dm = fltarr(nlines)
  p2 = fltarr(nlines)
  r2 = fltarr(nlines)
  etp = fltarr(nlines)
  d2 = fltarr(nlines)
  s2 = fltarr(nlines)
  f2 = fltarr(nlines)
  
  vazao =  fltarr(nlines)
  escb =  fltarr(nlines)
  header = ' '
  
  close, 1
  openr, 1, arqv
  ;readf, 1, header
  for n = 0L, nlines-1L do begin
    
    readf, 1, ano, mes, dia, hh, mm, ss, m2r, Dmr, p2r, r2r, etpr, d2r, s2r, f2r
    datatempo[n] = julday(mes, dia, ano, hh, mm, ss) 
    
    m2[n]= m2r
    Dm[n]= Dmr
    p2[n]= p2r
    r2[n] = r2r
    etp[n] = etpr
    d2[n]= d2r
    s2[n]= s2r
    f2[n]= f2r

  endfor
  close, 1

end
