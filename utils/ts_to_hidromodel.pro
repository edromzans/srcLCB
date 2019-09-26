@read_aguadados
@read_dadosamb
dir = '/home/evandro/src_codes/SiB/hidromodel/'
arqv = 'aguadados_selecao.txt'
arqvdsamb = 'dadosamb_selecao.txt'
arqvinput = 'input.txt'

read_aguadados, dir+arqv, datatempo_aguadados, prec, vazao, escb

vazao_ajust = vazao
escb_ajust =  escb

posval = where(vazao gt -999999., pval)
prec_val = prec[posval]
vazao_val = vazao[posval]
escb_val = escb[posval]

expr = 'p[0]*x^p[1] + p[2]' ;ajuste de potencia
p =  [ 0.01d,  1.5d, +9d]

parvz = mpfitexpr(expr, prec_val, vazao_val, weights, p)
print,  parvz

posk = where(vazao lt -99999., pk)
if pk gt 0 then vazao[posk] = !values.f_nan
if pk gt 0 then begin
  vzcomp = fltarr(pk)
  dxvzcomp = fltarr(pk)
  for n = 0L, pk-1L do begin

    vazao_ajust[posk[n]] =  parvz[0]*(float(prec[posk[n]]))^parvz[1]+parvz[2]

    vzcomp[n] = parvz[0]*(float(prec[posk[n]]))^parvz[1]+parvz[2]
    dxvzcomp[n] = prec[posk[n]]
    
  endfor
endif

;expr =  'p[0]*exp(p[1]*x)+p[2]' ;exponencial
expr = '(p[0]*x)/(p[1]+x)' ;hiperbole

p =  [ 54d,  69d ]
;p = [-9097.7449, -0.00093671236, 9085.2569] ;potencia
weights=1d

pareb = mpfitexpr(expr, vazao_val, escb_val, weights, p)
print,  pareb

;pareb = [-9097.7449, -0.00093671236, 9085.2569]
;p =  [ -100005.,  -2000.0326735,  35.867823 ]
;pareb =  [54., 69.]

posk = where(escb lt -99999., pk)
if pk gt 0 then escb[posk]= !values.f_nan
if pk gt 0 then begin
  ebcomp = fltarr(pk)
  dxebcomp = fltarr(pk)
  for n = 0L, pk-1L do begin

    escb_ajust[posk[n]] = (p[0]*vazao_ajust[posk[n]])/(p[1]+vazao_ajust[posk[n]])
    ebcomp[n] = (p[0]*vazao_ajust[posk[n]])/(p[1]+vazao_ajust[posk[n]])
    dxebcomp[n] = vazao_ajust[posk[n]]

  endfor
endif

tvlct, 255,  0,  0, 2         ; vermelho

window, 0
device, decomposed = 0
plot,  prec,  vazao_ajust,  psym = 1
x = findgen(400)
y = parvz[0]*x^parvz[1]+parvz[2]
oplot, x,  y
oplot, dxvzcomp, vzcomp,  psym = 6,  symsize = 3,  color = 2

window, 1
plot,  vazao_ajust, escb_ajust,  psym = 1
x = findgen(400)
;y = pareb[0]*x^pareb[1] + pareb[2]
y = (pareb[0]*x)/(pareb[1]+x)
oplot, x, y
oplot, dxebcomp, ebcomp  ,  psym = 6,  symsize = 3,  color = 2

;; window, 2
;; posor = sort(vazao_ajust)
;; plot, vazao_ajust[posor], escb_ajust[posor]
;; window, 3
;; posor = sort(prec)
;; plot, prec[posor], vazao_ajust[posor]


caldat, datatempo_aguadados, mes, dia,  ano
ts_mes = julday(mes, 01, ano, 00, 00, 00)
ntempoagua = n_elements(datatempo_aguadados)

mytimes =  timegen(start = ts_mes[0], final = ts_mes[ntempoagua-1L],  units = 'Months')

nmymes =  n_elements(mytimes)

rad_avgmes = fltarr(nmymes)
tmax_avgmes = fltarr(nmymes)
tmin_avgmes = fltarr(nmymes)
tmed_avgmes = fltarr(nmymes)
etp_avgmes = fltarr(nmymes)

print, dir+arqvdsamb
read_dadosamb, dir+arqvdsamb, datatempo_dsamb, rad, tmax, tmin, tmed

;input hidromodel balagua
close, 1
openw, 1, dir+arqvinput

for n = 0L, nmymes-1L do begin

  if n lt (nmymes-1L) then begin
    posmes = where(datatempo_dsamb ge mytimes[n] and datatempo_dsamb lt mytimes[n+1], pmes)
    posmesagua = where(datatempo_aguadados ge mytimes[n] and datatempo_aguadados lt mytimes[n+1], pmesag)
  endif else begin
    posmes = where(datatempo_dsamb ge mytimes[n] and datatempo_dsamb lt !values.f_infinity, pmes)
    posmesagua = where(datatempo_aguadados ge mytimes[n] and datatempo_aguadados lt !values.f_infinity, pmesag)
  endelse

  radmes = rad[posmes]
  tmedmes = tmed[posmes]
  tmaxmes = tmax[posmes]
  tminmes = tmin[posmes]
  
  radmmdia1 = radmes*( 10.^3./(2500.8-2.37*tmedmes+0.0016*(tmedmes^2.)-0.00006*(tmedmes^3.)) )
  radmmdia2 = radmes * (10.^6. / (28.9*86400.) )
  ;print,  mean(radmmdia1), mean(radmmdia2),  format = '(2F20.5)'

  ;; plot, radmmdia1
  ;; oplot, radmmdia2,  color = 2
  ;; rp = ' '
  ;; read,rp,prompt='Press ENTER to continue...'
  ;; if rp eq 'q' then stop

  radmmdia = radmmdia2
  
  etp = (0.0023*radmmdia*(tmaxmes-tminmes)^0.5)*(tmedmes+17.8)

  ;medias mensais
  rad_avgmes[n] = mean(radmes, /nan)
  tmax_avgmes[n] = mean(tmaxmes, /nan)
  tmin_avgmes[n] = mean(tminmes, /nan)
  tmed_avgmes[n] = mean(tmedmes, /nan)
  etp_avgmes[n] = mean(etp, /nan) * float(pmes) ; de [mm/dia] para [mm]

  ;print,  n,  pmes,  pmesag,  posmesagua
  ;if pmes lt 0 or pmesag lt 0 then stop
  if pmesag gt 1 then stop
  
  printf,1, mytimes[n], etp_avgmes[n], prec[posmesagua[0]], vazao_ajust[posmesagua[0]], escb_ajust[posmesagua[0]], format = '(c(CYI4," ",CMOI02," ",CDI02," ",CHI02," ",CMI02," ",CSI02),4F11.2)'
    
endfor
close, 1
end
