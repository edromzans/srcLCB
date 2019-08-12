@read_out_sibvars
@ts_avgmonth
@ts_summonth

;dir = '/dados/SiB/sites/Pastagem_SP_15Out09/run/'
;dir = '/dados/SiB/sites/Pastagem_Rondonia/run/'
;dir = '/dados/SiB/sites/Floresta_Rondonia/run/'
;dir = '/dados/SiB/sites/FlorestaAtlantica-novo/run/'
;dir = '/dados/SiB/sites/FlorestaAtlantica/run/'
;dir = '/dados/SiB/sites/Fazenda-K77/run/'
;dir = '/dados/SiB/sites/Eucalipto/run/'
;dir = '/dados/SiB/sites/Cana_27Nov09/run/'
;dir = '/dados/SiB/sites/Cerrado_27Nov09/run/'
dir = '/dados/SiB/controle/run/'
varfile =  'sib2dt.dat'
file = dir+varfile
print, file
read_out_sibvars, file, datetime, vars, kval

stop

;default
t0 = min(datetime)
t1 = max(datetime)
;set your own date
;t0 = julday(01, 01, 2005, 00) ; julday(MM, DD, YYYY, HH)
;t1 = julday(01, 01, 2006, 00)

Tm = fltarr(kval)
em = fltarr(kval)
um = fltarr(kval)
Ki = fltarr(kval)
Prec = fltarr(kval)

W1_C = fltarr(kval)
W2_C = fltarr(kval)
W3_C = fltarr(kval)
W4_C = fltarr(kval)
W5_C = fltarr(kval)
W6_C = fltarr(kval)
W7_C = fltarr(kval)
W8_C = fltarr(kval)
W9_C = fltarr(kval)
W10_C = fltarr(kval)

Rn_C = fltarr(kval)
H_C = fltarr(kval)
LE_C = fltarr(kval)
G_C = fltarr(kval)

Evpt = fltarr(kval)
Trans = fltarr(kval)
Esoil = fltarr(kval)
Einterc = fltarr(kval)

Rss = fltarr(kval)
Rs = fltarr(kval)
Runoff = fltarr(kval)

Rsc_C = fltarr(kval)
An_C = fltarr(kval)
PPB = fltarr(kval)

;fill variables in accordance with its positions given by
;read_out_sibivar procedure
Tm[*] = vars[0, *]
em[*] = vars[1, *]
um[*] = vars[2, *]
Ki[*] = vars[3, *]
Prec[*] = vars[32, *]

W1_C[*] = vars[17, *]
W2_C[*] = vars[18, *]
W3_C[*] = vars[19, *]
W4_C[*] = vars[20, *]
W5_C[*] = vars[21, *]
W6_C[*] = vars[22, *]
W7_C[*] = vars[23, *]
W8_C[*] = vars[24, *]
W9_C[*] = vars[25, *]
W10_C[*] = vars[26, *]

Rn_C[*] = vars[7, *]
H_C[*] = vars[8, *]
LE_C[*] = vars[9, *]
G_C[*] = vars[10, *]

Evpt[*] = vars[28, *]
Trans[*] = vars[29, *] 
Esoil[*] = vars[30, *] 
Einterc[*] = vars[31, *]  

Rss[*] = vars[33, *]
Rs[*] = vars[34, *]
Runoff[*] = vars[35, *]

Rsc_C[*] = vars[13, *]
An_C[*] = vars[14, *]
PPB[*] = vars[42, *]

;averages
swth = 720 ; smooth with (24 day) (720 month) 

Tm_sth = smooth(Tm, swth, /edge_truncate)
ts_avgmonth, datetime, Tm, ts_uniqmonths, Tm_avg
em_sth = smooth(em, swth, /edge_truncate)
ts_avgmonth, datetime, em, ts_uniqmonths, em_avg
um_sth = smooth(um, swth, /edge_truncate)
ts_avgmonth, datetime, um, ts_uniqmonths, um_avg
Ki_sth = smooth(Ki, swth, /edge_truncate)
Prec_sth = smooth(Prec, swth, /edge_truncate)
ts_summonth, datetime, Prec, ts_uniqmonths, Prec_sum


W1_C_sth = smooth(W1_C, swth, /edge_truncate)
W2_C_sth = smooth(W2_C, swth, /edge_truncate)
W3_C_sth = smooth(W3_C, swth, /edge_truncate)
W4_C_sth = smooth(W4_C, swth, /edge_truncate)
W5_C_sth = smooth(W5_C, swth, /edge_truncate)
W6_C_sth = smooth(W6_C, swth, /edge_truncate)
W7_C_sth= smooth(W7_C, swth, /edge_truncate)
W8_C_sth = smooth(W8_C, swth, /edge_truncate)
W9_C_sth = smooth(W9_C, swth, /edge_truncate)
W10_C_sth = smooth(W10_C, swth, /edge_truncate)

Rn_C_sth = smooth(Rn_C, swth, /edge_truncate)
H_C_sth = smooth(H_C, swth, /edge_truncate)
LE_C_sth = smooth(LE_C, swth, /edge_truncate)
G_C_sth = smooth(G_C, swth, /edge_truncate)

Evpt_sth = smooth(Evpt, swth, /edge_truncate)
Trans_sth = smooth(Trans, swth, /edge_truncate)
Esoil_sth = smooth(Esoil, swth, /edge_truncate)
Einterc_sth = smooth(Einterc, swth, /edge_truncate)

Rss_sth = smooth(Rss, swth, /edge_truncate)
Rs_sth = smooth(Rs, swth, /edge_truncate)
Runoff_sth = smooth(Runoff, swth, /edge_truncate)

Rsc_C_sth = smooth(Rsc_C, swth, /edge_truncate)
An_C_sth = smooth(An_C, swth, /edge_truncate)
PPB_sth = smooth(PPB, swth, /edge_truncate)

!p.font = 0
device, decomposed = 0 
window, 0, xsize = 2500,  ysize = 1000
!p.multi = [0, 2, 5]
!p.charsize = 3
;tvlct, 100, 20, 20, 100 ;red
loadct, 13, ncolors = 11
tvlct, 255, 255, 255, 255

date_label = LABEL_DATE( DATE_FORMAT=['%Y-%N-%D'] )

plot, datetime, Tm_sth, ytitle = 'Tm', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
oplot, ts_uniqmonths, Tm_avg, linestyle = 1;, color = 10
plot, datetime, em_sth, ytitle = 'em', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
oplot, ts_uniqmonths, em_avg, linestyle = 1
plot, datetime, um_sth, ytitle = 'um', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time',  xrange = [t0, t1]
oplot, ts_uniqmonths, um_avg, linestyle = 1
plot, datetime, Ki_sth, ytitle = 'Ki', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
plot, datetime, Prec_sth, ytitle = 'Prec', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1];,  yrange = [0, 400.]
oplot, ts_uniqmonths, Prec_sum, linestyle = 1,  color = 10

plot, datetime, W1_C_sth, ytitle = 'W(1-10)_C', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [0.3, 1.], /nodata
oplot, datetime, W1_C_sth, color = 1
oplot, datetime, W2_C_sth, color = 2
oplot, datetime, W3_C_sth, color = 3
oplot, datetime, W4_C_sth, color = 4
oplot, datetime, W5_C_sth, color = 5
oplot, datetime, W6_C_sth, color = 6
oplot, datetime, W7_C_sth, color = 7
oplot, datetime, W8_C_sth, color = 8
oplot, datetime, W9_C_sth, color = 9
oplot, datetime, W10_C_sth, color = 10

plot, datetime, Rn_C_sth, ytitle = 'Rn_C H_C LE_C G_C', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [-50., 200.], /nodata
oplot, datetime, Rn_C_sth, color = 1
oplot, datetime, H_C_sth, color = 2
oplot, datetime, LE_C_sth, color = 3
oplot, datetime, G_C_sth, color = 4

plot, datetime, Evpt_sth, ytitle = 'Evpt Trans Esoil Einterc', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [0., 10.], /nodata
oplot, datetime, Evpt, color = 1
oplot, datetime, Trans, color = 2
oplot, datetime, Esoil, color = 3
oplot, datetime, Einterc, color = 4

plot, datetime, Rss_sth, ytitle = 'Rss Rs Runoff ', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [-0.5, 5.], /nodata
oplot, datetime, Rss_sth, color = 1
oplot, datetime, Rs_sth, color = 2
oplot, datetime, Runoff_sth, color = 3

plot, datetime, Rsc_C_sth, ytitle = 'Rsc_C An_C PPB', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [0, 25.], /nodata
oplot, datetime, Rsc_C_sth, color = 1
oplot, datetime, An_C_sth, color = 2
oplot, datetime, PPB_sth, color = 3

;Write_png, 'SibPanelDevel.png',tvrd(true=1)
end
