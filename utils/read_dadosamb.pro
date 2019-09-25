pro read_dadosamb, arqv, datatempo, rad, tmax, tmin, tmed
  
  nlines =  file_lines(arqv) - 1L ; desconta o header
  
  datatempo =  dblarr(nlines)
  rad = fltarr(nlines)
  tmax = fltarr(nlines)
  tmin = fltarr(nlines)
  tmed = fltarr(nlines)

  header = ' '
  
  close, 5
  openr, 5, arqv
  readf, 5, header
  for n = 0L, (nlines-1L) do begin
    readf, 5, ano, mes, dia, hh, mm, ss, rd, tmx, tmn, tm
    ;help,   ano, mes, dia, hh, mm, ss, rd, tmx, tmn, tm
    datatempo[n] = julday(long(mes), long(dia), long(ano), long(hh), long(mm), long(ss)) 
    rad[n] = float(rd)
    tmax[n] = float(tmx)
    tmin[n] = float(tmn)
    tmed[n] = float(tm)
  endfor
  close, 5
  ;help,  datatempo, rad, tmax, tmin, tmed
end


