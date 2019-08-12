@read_out_sibvars
dir = '/dados/SiB/'
varfile =  'sib2dt.dat'
file = dir+varfile

read_out_sibvars, file, datetime, vars, kval

Tm = fltarr(kval)
Tm[*] = vars[0, *]

caldat, datetime, month, day, year
ts_days = julday(month, day, year, 00)

ts_uniqdays = ts_days[uniq(ts_days, sort(ts_days))]
ndays = n_elements(ts_uniqdays)

ts_varavgday = fltarr(ndays)

for k = 0, ndays - 1L do begin

  posday = where(datetime ge ts_uniqdays[k] and datetime lt ts_uniqdays[k]+1d)

  ;print, '----------------------' 
  ;print, datetime[posday], format = '(c())'
  ;wait, 2
  
  ts_varavgday[k] = mean(Tm[posday], /nan) 
  
endfor

plot, ts_varavgday
end
