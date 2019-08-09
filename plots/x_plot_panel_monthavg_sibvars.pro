@read_out_sibvars
dir = '/dados/SiB/'
varfile =  'sib2dt.dat'
file = dir+varfile

read_out_sibvars, file, datetime, vars, kval

;default
t0 = min(datetime)
t1 = max(datetime)
;set your own date
t0 = julday(01, 01, 2005, 00) ; julday(MM, DD, YYYY, HH)
t1 = julday(01, 01, 2006, 00)

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

Tm_avg = smooth(Tm, swth, /edge_truncate)
em_avg = smooth(em, swth, /edge_truncate)
um_avg = smooth(um, swth, /edge_truncate)
Ki_avg = smooth(Ki, swth, /edge_truncate)
Prec_avg = smooth(Prec, swth, /edge_truncate)

W1_C_avg = smooth(W1_C, swth, /edge_truncate)
W2_C_avg = smooth(W2_C, swth, /edge_truncate)
W3_C_avg = smooth(W3_C, swth, /edge_truncate)
W4_C_avg = smooth(W4_C, swth, /edge_truncate)
W5_C_avg = smooth(W5_C, swth, /edge_truncate)
W6_C_avg = smooth(W6_C, swth, /edge_truncate)
W7_C_avg= smooth(W7_C, swth, /edge_truncate)
W8_C_avg = smooth(W8_C, swth, /edge_truncate)
W9_C_avg = smooth(W9_C, swth, /edge_truncate)
W10_C_avg = smooth(W10_C, swth, /edge_truncate)

Rn_C_avg = smooth(Rn_C, swth, /edge_truncate)
H_C_avg = smooth(H_C, swth, /edge_truncate)
LE_C_avg = smooth(LE_C, swth, /edge_truncate)
G_C_avg = smooth(G_C, swth, /edge_truncate)

Evpt_avg = smooth(Evpt, swth, /edge_truncate)
Trans_avg = smooth(Trans, swth, /edge_truncate)
Esoil_avg = smooth(Esoil, swth, /edge_truncate)
Einterc_avg = smooth(Einterc, swth, /edge_truncate)

Rss_avg = smooth(Rss, swth, /edge_truncate)
Rs_avg = smooth(Rs, swth, /edge_truncate)
Runoff_avg = smooth(Runoff, swth, /edge_truncate)

Rsc_C_avg = smooth(Rsc_C, swth, /edge_truncate)
An_C_avg = smooth(An_C, swth, /edge_truncate)
PPB_avg = smooth(PPB, swth, /edge_truncate)

!p.font = 0
device, decomposed = 0 
window, 0, xsize = 2500,  ysize = 1000
!p.multi = [0, 2, 5]
!p.charsize = 3
;tvlct, 100, 20, 20, 100 ;red
loadct, 13, ncolors = 11
tvlct, 255, 255, 255, 255

date_label = LABEL_DATE( DATE_FORMAT=['%Y-%N-%D'] )

plot, datetime, Tm_avg, ytitle = 'Tm', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
plot, datetime, em_avg, ytitle = 'em', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
plot, datetime, um_avg, ytitle = 'um', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time',  xrange = [t0, t1]
plot, datetime, Ki_avg, ytitle = 'Ki', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]
plot, datetime, Prec_avg, ytitle = 'Prec', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1]

plot, datetime, W1_C_avg, ytitle = 'W(1-10)_C', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [0.3, 1.], /nodata
oplot, datetime, W1_C_avg, color = 1
oplot, datetime, W2_C_avg, color = 2
oplot, datetime, W3_C_avg, color = 3
oplot, datetime, W4_C_avg, color = 4
oplot, datetime, W5_C_avg, color = 5
oplot, datetime, W6_C_avg, color = 6
oplot, datetime, W7_C_avg, color = 7
oplot, datetime, W8_C_avg, color = 8
oplot, datetime, W9_C_avg, color = 9
oplot, datetime, W10_C_avg, color = 10

plot, datetime, Rn_C_avg, ytitle = 'Rn_C H_C LE_C G_C', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [-50., 200.], /nodata
oplot, datetime, Rn_C_avg, color = 1
oplot, datetime, H_C_avg, color = 2
oplot, datetime, LE_C_avg, color = 3
oplot, datetime, G_C_avg, color = 4

plot, datetime, Evpt_avg, ytitle = 'Evpt Trans Esoil Einterc', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [0., 10.], /nodata
oplot, datetime, Evpt, color = 1
oplot, datetime, Trans, color = 2
oplot, datetime, Esoil, color = 3
oplot, datetime, Einterc, color = 4

plot, datetime, Rss_avg, ytitle = 'Rss Rs Runoff ', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [-0.5, 5.], /nodata
oplot, datetime, Rss_avg, color = 1
oplot, datetime, Rs_avg, color = 2
oplot, datetime, Runoff_avg, color = 3

plot, datetime, Rsc_C_avg, ytitle = 'Rsc_C An_C PPB', xstyle = 1, ystyle = 1, $
      xtickformat = 'LABEL_DATE', xtickunits = 'Time', xrange = [t0, t1], yrange = [0, 25.], /nodata
oplot, datetime, Rsc_C_avg, color = 1
oplot, datetime, An_C_avg, color = 2
oplot, datetime, PPB_avg, color = 3
end
