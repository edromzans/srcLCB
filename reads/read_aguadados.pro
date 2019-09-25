pro read_aguadados,  arqv,  datatempo, prec, vazao,  escb
  
  nlines =  file_lines(arqv) - 1L ; desconta o header
  
  datatempo =  dblarr(nlines)
  prec = intarr(nlines)
  vazao =  fltarr(nlines)
  escb =  fltarr(nlines)
  header = ' '
  
  close, 1
  openr, 1, arqv
  readf, 1, header
  for n = 0L, nlines-1L do begin
    
    readf, 1, ano, mes, dia, hh, mm, ss, pc, vz, eb
;    print,  ano, mes, dia, hh, mm, ss, pc, vz, eb
    datatempo[n] = julday(mes, dia, ano) 
    prec[n] = pc
    vazao[n] = vz
    escb[n] = eb

  endfor
  close, 1
;  help, datatempo, prec, vazao,  escb
end
