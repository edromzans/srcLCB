@read_out_sibvars
@ts_avgmonth
@ts_summonth

;devel--------------------
dir = '/home/evandro/SiB2run/'  
;-------------------------


;dir = '/dados/SiB/sites/Pastagem_SP_15Out09/run/'
;dir = '/dados/SiB/sites/Pastagem_Rondonia/run/'
;dir = '/dados/SiB/sites/Floresta_Rondonia/run/'
;dir = '/dados/SiB/sites/FlorestaAtlantica-novo/run/'
;dir = '/dados/SiB/sites/FlorestaAtlantica/run/'
;dir = '/dados/SiB/sites/Fazenda-K77/run/'
;dir = '/dados/SiB/sites/Eucalipto/run/'
;dir = '/dados/SiB/sites/Cana_27Nov09/run/'
;dir = '/dados/SiB/sites/Cerrado_27Nov09/run/'
;dir = '/dados/SiB/controle/run/'
varfile =  'sib2dt.dat'
file = dir+varfile
print, file
read_out_sibvars, file, datetime, vars, varnames, kval

;default
t0 = min(datetime)
t1 = max(datetime)
;set your own date
;t0 = julday(01, 01, 2005, 00) ; julday(MM, DD, YYYY, HH)
;t1 = julday(01, 01, 2006, 00)

;get daytime hourly resolution
pos1day = where( datetime ge datetime[0] and datetime lt datetime[0]+1d, daytimeres) 
print, 'hourly resolution in the day = ' , daytimeres

nvars = n_elements(varnames)
SiBvar = fltarr(kval)

!p.font = 0
!p.charsize = 2
date_label = LABEL_DATE( DATE_FORMAT=['%Y%N'] )

xws = 2500
yws = 1000
!p.multi = [0, 5, 9]
window, 0, xsize = xws,  ysize = yws, title = 'Variaveis SiB'
device, decomposed = 0
loadct, 13, ncolors = 11
tvlct, 255, 255, 255, 255

;SiBvars
for k = 0L, nvars - 1L do begin

  SiBvar[*] = vars[k, *]
  titlevar =  varnames[k]
  plot, datetime, SiBvar, ytitle = titlevar, xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
  print, '-----------> ', titlevar
  ;read, u
  
endfor

;; !p.multi = [0, 5, 9]
;; window, 1, xsize = xws,  ysize = yws
;; device, decomposed = 0
;; loadct, 13, ncolors = 11
;; tvlct, 255, 255, 255, 255

;; ;Month smooth SiBvars
;; for k = 0L, nvars - 1L do begin

;;   SiBvar[*] = vars[k, *]
;;   titlevar =  varnames[k]
;;   swth = daytimeres * 30.
;;   SiBvar_sth = smooth(SiBvar, swth, /edge_truncate)
;;   plot, datetime, SiBvar_sth, ytitle = titlevar, xstyle = 1, ystyle = 1, $
;;       xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
;;   print, '-----------> ', titlevar
;;   ;read, u
  
;; endfor

!p.multi = [0, 5, 9]
window, 1, xsize = xws,  ysize = yws, title = 'Media diaria'
device, decomposed = 0
loadct, 13, ncolors = 11
tvlct, 255, 255, 255, 255

;Day average SiBvars
for k = 0L, nvars - 1L do begin

  SiBvar[*] = vars[k, *]
  titlevar =  varnames[k]
    
  ts_avgday, datetime, SiBvar, ts_uniqdays, SiBvar_avg
    
  plot, ts_uniqdays, SiBvar_avg, ytitle = titlevar, xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
  print, '-----------> ', titlevar
  ;read, u
  
endfor

!p.multi = [0, 5, 9]
window, 2, xsize = xws,  ysize = yws,  title = 'Media mensal'
device, decomposed = 0
loadct, 13, ncolors = 11
tvlct, 255, 255, 255, 255

;Month average SiBvars
for k = 0L, nvars - 1L do begin

  SiBvar[*] = vars[k, *]
  titlevar =  varnames[k]
    
  ts_avgmonth, datetime, SiBvar, ts_uniqmonths, SiBvar_avg
    
  plot, ts_uniqmonths, SiBvar_avg, ytitle = titlevar, xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
  print, '-----------> ', titlevar
  ;read, u
  
endfor

end
