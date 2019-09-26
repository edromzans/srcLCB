@read_output_balagua

dir = '/home/evandro/src_codes/SiB/hidromodel/'
arqv = 'output' 
read_output_balagua,  dir+arqv,  datatempo, m2, Dm, p2, r2, etp, d2, s2, f2

!p.multi = [0, 2, 4]
!p.charsize = 3
date_label = LABEL_DATE( DATE_FORMAT=['%Y%N'] )

window, 0,  xsize = 1800, ysize = 1010

plot, datatempo, m2, xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time', title = 'm2'

plot, datatempo, Dm, xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time', title = 'Dm'

plot, datatempo, p2, xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time', title = 'p2'

plot, datatempo, r2, xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time', title = 'r2'

plot, datatempo, etp, xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time', title = 'etp'

plot, datatempo, d2, xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time', title = 'd2'

plot, datatempo, s2, xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time', title = 's2'

plot, datatempo, f2, xstyle = 1, ystyle = 1, xtickformat = 'LABEL_DATE', xtickunits = 'Time', title = 'f2'

end
