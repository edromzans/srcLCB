pro read_out_sibvars, file, datetime, vars, kval
;dir = '/dados/SiB/'
;varfile =  'sib2dt.dat'
;file = dir+varfile
  nlines = file_lines(file)

  linehead = ' '
  line$ = ' '

  close, 1
  openr, 1, file
  readf, 1, linehead
  close, 1

  varnames =  strsplit(linehead,  ' ', /extract)

  nx =  n_elements(varnames)
  num_var = indgen(nx) - 1

;identify the position of each variable
  for k = 1, nx-1L do begin
    print, num_var[k], varnames[k],  format = '(I3,A12)'
  endfor

;read all variables
  vars =  fltarr(nx-1L, nlines-1L)
  datetime = dblarr(nlines-1L)

  kval = 0L

  close, 1
  openr, 1, file
  for k = 0, nlines-1L do begin
    if (k le 0) then begin
      readf, 1, linehead
    endif else begin
      readf, 1, line$
      varsline = strsplit(line$, ' ', /extract)
      
      year = fix('20'+strmid(varsline[0], 0, 2)) ;check if 1900 '19' or 2000 '20' year
      month = fix(strmid(varsline[0], 2, 2))
      day = fix(strmid(varsline[0], 4, 2))
      hour = fix(strmid(varsline[0], 6, 2))
      datetime[kval] = julday(month, day, year, hour)

      vars[*, kval] = float(varsline[1:nx-1L]) ;converting vars from string to float

      kval += 1L
    endelse
  endfor
  close, 1
end
