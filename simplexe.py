import numpy as np
from probleme import *


def simplexe(pb,base):

	A = pb.A
	b = pb.b
	c = pb.c
	#while (any(i<0 for i in c)):
	col = np.argmin(c)
	lin = pivot(A[:,col],b)
	base[lin] = col
	print(col)
	print(lin)
	print(base)

def pivot(vec,b):
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
