pro ts_avgmonth, datetime, sibvar, ts_uniqmonths, ts_sibvaravgmonth   

  caldat, datetime, month, day, year
  ts_months = julday(month, 01, year, 00)

  ts_uniqmonths = ts_months[uniq(ts_months, sort(ts_months))]
  nmonths = n_elements(ts_uniqmonths)

  ts_sibvaravgmonth = fltarr(nmonths)

  for k = 0, nmonths - 1L do begin

    if k lt (nmonths - 1L) then begin
      posmonth = where(datetime ge ts_uniqmonths[k] and datetime lt ts_uniqmonths[k+1])
    endif else begin
      posmonth = where(datetime ge ts_uniqmonths[k] and datetime lt !values.f_infinity)
    endelse
    
    ;print, '----------------------' 
    ;print, datetime[posmonth], format = '(c())'
    ;wai, 2
    
    ts_sibvaravgmonth[k] = mean(sibvar[posmonth], /nan) 
    
  endfor
end
