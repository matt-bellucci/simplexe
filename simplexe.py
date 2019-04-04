import numpy as np
from probleme import *


def simplexe(pb,base):

	A = pb.A
	b = pb.b
	d = pb.c
	#while (any(i<0 for i in d)):
	col = np.argmin(d)
	[sort,entre] = pivot(A,b,d)
	print(base[sort])
	print(entre)
	print(base)

def pivot(A,b,d,critere="naturel"):
	if critere=="naturel":
		return pivot_nat(A,b,d)
	elif critere=="bland":
		return privot_bland(A,b,d)
	else:
		print("Critere {0} n'existe pas, application critere naturel".format(critere))
		return pivot(A,b,d)
	argmin = 0
	mini = b[0]/vec[0]
	for i in range(vec.size):
		if vec[i]<0:
			continue
		else:
			t = b[i]/vec[i]
			if t<mini:
				mini = t
				argmin = i
	return argmin

def pivot_nat(A,b,d):
	entrante = np.argmin(d) # plus petit j ou d est le plus petit
	sortante = 0
	vec = A[:,entrante]
	mini = b[0]/vec[0]
	for i in range(b.size):
		if vec[i]<0:
			continue
		else:
			t = b[i]/vec[i]
			if t<mini:
				mini = t
				sortante = i
	return [sortante,entrante]

#def pivot_bland(vec,b):
