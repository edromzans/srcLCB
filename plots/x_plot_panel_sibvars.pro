@read_out_sibvars
dir = '/dados/SiB'
varfile =  'sib2dt.dat'
file = dir+varfile

read_out_sibvars, file, datetime, vars,  kval

!p.font = 0
device, decomposed = 0 
window, 0, xsize = 2500,  ysize = 1000
!p.multi = [0, 0, 5]
!p.charsize = 3
tvlct, 100, 20, 20, 1

date_label = LABEL_DATE( DATE_FORMAT=['%Y-%N-%D'] )

Tm = fltarr(kval)
em = fltarr(kval)
um = fltarr(kval)
Ki = fltarr(kval)
Prec = fltarr(kval)

Tm[*] = vars[0, *]
em[*] = vars[1, *]
um[*] = vars[2, *]
Ki[*] = vars[3, *]
Prec[*] = vars[32, *]

plot, datetime, Tm, ytitle = 'Tm', xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time' 
plot, datetime, em, ytitle = 'em', xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time'
plot, datetime, um, ytitle = 'um', xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time'
plot, datetime, Ki, ytitle = 'Ki', xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time'
plot, datetime, Prec, ytitle = 'Prec', xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time'

end

