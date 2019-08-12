pro ts_sumday, datetime, sibvar, ts_uniqdays, ts_sibvarsumday

  caldat, datetime, month, day, year
  ts_days = julday(month, day, year, 00)

  ts_uniqdays = ts_days[uniq(ts_days, sort(ts_days))]
  ndays = n_elements(ts_uniqdays)

  ts_sibvarsumday = fltarr(ndays)

  for k = 0, ndays - 1L do begin

    posday = where(datetime ge ts_uniqdays[k] and datetime lt ts_uniqdays[k]+1d)

                                ;print, '----------------------' 
                                ;print, datetime[posday], format = '(c())'
                                ;wait, 2
    
    ts_sibvarsumday[k] = total(sibvar[posday]) 
    
  endfor

end
