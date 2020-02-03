@read_out_sibvars
@ts_avgmonth
@ts_summonth

;devel--------------------

;dirdefault = '/home/evandro/src_codes/gitSiB2model/SiB2python/'
;dirdefault = '/home/evandro/SiB2run/'

;dirdefault = '/home/evandro/SIBI_controle/SiBparaEvandro/SiB2/Eucalipto/'
;dirdefault = '/home/evandro/SIBI_controle/SiBparaEvandro/SiB2/Cana_27Nov09/'

;dirdefault = '/dados/ProcessoOtimizacaoModelos/SiB2/momentum/semDT/'
;dirdefault = '/home/evandro/SiB2run/modvars/'
dirdefault = '/home/evandro/src_codes/LCB/srcsib2model/SiB2_DBHM_derive_trans/F95/'
;dirdefault = '/home/evandro/src_codes/LCB/srcsib2model/SiB2_DBHM_derive_trans/F95/semDT/'


;-------------------------

;dir = '/dados/SiB/sites/Pastagem_SP_15Out09/run/'
;dir = '/dados/SiB/sites/Pastagem_Rondonia/run/'
;dir = '/dados/SiB/sites/Floresta_Rondonia/run/'
dir = '/dados/SiB/sites/FlorestaAtlantica-novo/run/'
;dir = '/dados/SiB/sites/FlorestaAtlantica/run/'
;dir = '/dados/SiB/sites/Fazenda-K77/run/'
;dir = '/dados/SiB/sites/Eucalipto/run/'
;dir = '/dados/SiB/sites/Cana_27Nov09/run/'
;dir = '/dados/SiB/sites/Cerrado_27Nov09/run/'
;dir = '/dados/SiB/controle/run/'

;dir =  '/home/evandro/src_codes/gitSiB2model/SiB2pymod/'
;dir = '/home/evandro/lcbiag/SiB/sites/FlorestaAtlantica-novo/run/'
;dir =  '/dados/ProcessoOtimizacaoModelos/SiB2/momentum/comDT/'
dir =  '/home/evandro/src_codes/LCB/srcsib2model/SiB2_DBHM_derive_trans/F95/comDT/'
 
varfile =  'sib2dt.dat'

filedefault = dirdefault+varfile
print, filedefault
read_out_sibvars, filedefault, datetimedefault, varsdefault, varnamesdefault, kvaldefault

file = dir+varfile
print, file
read_out_sibvars, file, datetime, vars, varnames, kval

!p.font = 0
!p.charsize = 3
date_label = LABEL_DATE( DATE_FORMAT=['%Y%N'] )

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
SiBvardefault = fltarr(kval)

xws = 1800
yws = 900
!p.multi = [0, 3, 3]
window, 0, xsize = xws,  ysize = yws, title = 'Variaveis SiB'
device, decomposed = 0
loadct, 13, ncolors = 11
tvlct, 255, 255, 255, 255

;SiBvars
for k = 5L, nvars - 1L do begin
;for k = 15L, 17L do begin

  SiBvar[*] = vars[k, *]
  SiBvardefault[*] = varsdefault[k, *]
  titlevar =  varnames[k]

  plot, SiBvar, SiBvardefault, title = titlevar, xtitle = 'original', ytitle = 'default', $
        xstyle = 1, ystyle = 1,  psym = 3

  plot, datetime, SiBvar - SiBvardefault, ytitle = 'desvio', xstyle = 1, ystyle = 1, $
        xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1] ;,  yrange = [-10, 10]

  plot, datetime, SiBvar , ytitle = titlevar, xstyle = 1, ystyle = 1, $
        xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1] ;,  yrange = [-10, 10]
  oplot, datetime, SiBvardefault,  color = 10


  ts_avgday, datetime, SiBvardefault, ts_uniqdaysdefault, SiBvardefault_dayavg
  ts_avgday, datetime, SiBvar, ts_uniqdays, SiBvar_dayavg

  plot, SiBvar_dayavg, SiBvardefault_dayavg, title = titlevar, xtitle = 'original', ytitle = 'default', $
        xstyle = 1, ystyle = 1,  psym = 3

  plot, ts_uniqdays, SiBvar_dayavg - SiBvardefault_dayavg, ytitle = 'desvio', xstyle = 1, ystyle = 1, $
        xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1] ;,  yrange = [-10, 10]

  plot, ts_uniqdays, SiBvar_dayavg , ytitle = titlevar, xstyle = 1, ystyle = 1, $
        xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1] ;,  yrange = [-10, 10]
  oplot, ts_uniqdays, SiBvardefault_dayavg, color = 10


  ts_avgmonth, datetime, SiBvardefault, ts_uniqmonthsdefault, SiBvardefault_monthavg
  ts_avgmonth, datetime, SiBvar, ts_uniqmonths, SiBvar_monthavg

  plot, SiBvar_monthavg, SiBvardefault_monthavg, title = titlevar, xtitle = 'original', ytitle = 'default', $
        xstyle = 1, ystyle = 1,  psym = 3

  plot, ts_uniqmonths, SiBvar_monthavg - SiBvardefault_monthavg, ytitle = 'desvio', xstyle = 1, ystyle = 1, $
        xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1] ;,  yrange = [-10, 10]

  plot, ts_uniqmonths, SiBvar_monthavg , ytitle = titlevar, xstyle = 1, ystyle = 1, $
        xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1] ;,  yrange = [-10, 10]
  oplot, ts_uniqmonths, SiBvardefault_monthavg, color = 10

  print, '-----------> ', titlevar,  k

  ;Write_png, string(k, format = '(I02)')+'SiB2varC.png',tvrd(true=1)
  
  rp = ' '
  read,rp,prompt='Press ENTER to continue...'
  if rp eq 'q' then stop 
 
endfor

end
