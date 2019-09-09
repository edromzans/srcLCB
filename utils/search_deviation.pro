@read_out_sibvars
@ts_avgmonth
@ts_summonth

;devel--------------------
dirdefault = '/home/evandro/SiB2run/'
;dirdefault = '/home/evandro/SIBI_controle/SiBparaEvandro/SiB2/Eucalipto/'
;dirdefault = '/home/evandro/SIBI_controle/SiBparaEvandro/SiB2/Cana_27Nov09/'
;-------------------------

;dir = '/dados/SiB/sites/Pastagem_SP_15Out09/run/'
dir = '/dados/SiB/sites/Pastagem_Rondonia/run/'
;dir = '/dados/SiB/sites/Floresta_Rondonia/run/'
;dir = '/dados/SiB/sites/FlorestaAtlantica-novo/run/'
;dir = '/dados/SiB/sites/FlorestaAtlantica/run/'
;dir = '/dados/SiB/sites/Fazenda-K77/run/'
;dir = '/dados/SiB/sites/Eucalipto/run/'
;dir = '/dados/SiB/sites/Cana_27Nov09/run/'
;dir = '/dados/SiB/sites/Cerrado_27Nov09/run/'
;dir = '/dados/SiB/controle/run/'

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



k = 12
print,  varnames[k],  ' <---------original'
print,  varnamesdefault[k],  ' <-------default'

SiBvar[*] = vars[k, *]
SiBvardefault[*] = varsdefault[k, *]

deviation =  abs(SiBvardefault - SiBvar)

mindev = min(deviation,  max = maxdev, subscript_max = posmaxdev)

print, deviation[posmaxdev], '  <<<<<<<<<<'
print, datetime[posmaxdev],  ' <---------original',  format = '(c(),A15)'
print, datetimedefault[posmaxdev], ' <-------default', format = '(c(),A15)'

print, SiBvar[posmaxdev],  '<---------original'
print, SiBvardefault[posmaxdev],  ' <-------default'
 


end
