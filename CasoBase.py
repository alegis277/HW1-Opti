import numpy as np
from scipy.optimize import minimize
import time
import matplotlib.pyplot as plt


# Parametros

P = 22000
r = 2.75/100 #%
M = 16

Lim_pago_inferior = 0
Lim_pago_superior = None
Debe_pagar_deuda = False

alpha = 1
beta = 36

#Matplotlib

plt.rcParams["figure.figsize"] = (11,5)

f, ax1 = plt.subplots(1,2)


#Condiciones iniciales
x0 = np.concatenate( [ np.zeros(M) , np.zeros(M) ] ) #x_k, u_k


#Limites (bounds)
struct0 = [(0,None)]
bounds0 = np.repeat(struct0, len(x0)/2, axis=0)
bounds0 = tuple([tuple(row) for row in bounds0])

struct1 = [(Lim_pago_inferior, Lim_pago_superior)]
bounds1 = np.repeat(struct1, len(x0)/2, axis=0)
bounds1 = tuple([tuple(row) for row in bounds1])

bounds = bounds0 + bounds1


#Funcion objetivo

def fun(x):
	sum_obj = 0
	for i in range(M):
		sum_obj += (alpha * x[i]**2) + (beta * x[i+M]**2)

	return 0.5*sum_obj


#Restricciones de igualdad

cons = []

for k in range(0, M):

	def eq_actual(x, k=k):
		if k==0:
			return -x[k] + (1+r)*P - x[k+M]
		else:
			return -x[k] + (1+r)*x[k-1] - x[k+M]

	cons.append({'type': 'eq', 'fun': eq_actual })

if Debe_pagar_deuda:
	cons.append({'type': 'eq', 'fun': lambda x:  x[M-1] })





cons = tuple(cons)
inicial = time.time()

print("Iniciando optimizacion....")
res = minimize(fun, x0, bounds=bounds, constraints=cons)
final = time.time()
print(res)
print("Optimizacion finalizada - Tiempo de optimizacion:",final-inicial)


ax1[0].scatter(list(range(0,M+1)), np.concatenate(([P],res.x[0:M])), label="$x_k$")
ax1[0].set_xlabel('Tiempo [Meses]')
ax1[0].set_ylabel('$x_k$')
ax1[0].set_xlim(0,M)
ax1[0].set_ylim(0,None)

ax1[0].grid(b=True, which='major', color='#666666', linestyle='-')
ax1[0].minorticks_on()
ax1[0].grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax1[0].set_title('Comportamiento de $x_k$')


ax1[1].scatter(list(range(1,M+1)), res.x[M:(M*2)], label="$u_k$")
ax1[1].set_xlabel('Tiempo [Meses]')
ax1[1].set_ylabel('$u_k$')
ax1[1].set_xlim(0,M)
ax1[1].set_ylim(0,None)

ax1[1].grid(b=True, which='major', color='#666666', linestyle='-')
ax1[1].minorticks_on()
ax1[1].grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
ax1[1].set_title('Comportamiento de $u_k$')


plt.show()