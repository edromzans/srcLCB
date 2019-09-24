@read_aguadados

dir = '/home/evandro/src_codes/SiB/hidromodel/'
arqv = 'aguadados_selecao.txt'

read_aguadados, dir+arqv, datatempo, prec, vazao, escb

vazao_ajust = vazao
escb_ajust =  escb

posval = where(vazao gt -999999., pval)
prec_val = prec[posval]
vazao_val = vazao[posval]
escb_val = escb[posval]




;y = A + Bx
result =  linfit(prec_val, vazao_val)
print,  result
a = result[0]
b = result[1]

posk = where(vazao lt -99999., pk)
if pk gt 0 then vazao[posk] = !values.f_nan
if pk gt 0 then begin
  for n = 0L, pk-1L do begin
    vazao_ajust[posk[n]] = a + b*float(prec[posk[n]])    
  endfor
endif


;expr =  'p[0]*exp(p[1]*x)+p[2]' ;'p[0]*x^p[1] + p[2]'

expr = '(p[0]*x)/(p[1]+x)'

p =  [ 54d,  69d ]
;p = [-9097.7449, -0.00093671236, 9085.2569] ;potencia

weights=1d

par = mpfitexpr(expr, vazao_val, escb_val, weights, p)
print,  par

;par = [-9097.7449, -0.00093671236, 9085.2569]
;p =  [ -100005.,  -2000.0326735,  35.867823 ]
;par =  [54., 69.]

posk = where(escb lt -99999., pk)
test = fltarr(pk)
if pk gt 0 then escb[posk]= !values.f_nan
if pk gt 0 then begin
  for n = 0L, pk-1L do begin
    escb_ajust[posk[n]] = (p[0]*vazao_ajust[posk[n]])/(p[1]+vazao_ajust[posk[n]])
                                ;par[0]*vazao_val^par[1] + par[2]
    test[n] = (p[0]*vazao_ajust[posk[n]])/(p[1]+vazao_ajust[posk[n]])
  endfor
endif


tvlct, 255,  0,  0, 2         ; vermelho

window, 0
device, decomposed = 0
plot,  prec,  vazao,  psym = 1,  color = 2
x = findgen(400)
y = a +b*x
oplot, x,  y
oplot, prec,  vazao_ajust,  psym = 5,  symsize = 3

window, 1
plot,  vazao,  escb,  psym = 1
x = findgen(400)
;y = par[0]*x^par[1] + par[2]
y = (p[0]*x)/(p[1]+x)
oplot, x, y

;oplot, vazao_ajust, escb_ajust,  psym = 5,  symsize = 3
oplot, vazao_ajust[posk], test  ,  psym = 5,  symsize = 3,  color = 2


end
