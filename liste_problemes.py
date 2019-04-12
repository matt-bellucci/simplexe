import numpy as np
from probleme import Probleme_standard
def get_primal():
	A = np.array([[2,3,1,1,0,0],[4,1,2,0,1,0],[3,4,2,0,0,1]])
	b = np.array([5,11,8])
	c = np.array([-5,-4,-3,0,0,0])
	pb = Probleme_standard(A,b,c)
	sol = np.array([2,0,1,0,1,0])
	return (pb,sol)

def get_dual():
	A = np.array([[-1,-1,0,1,0],[-2,3,-5,0,1]])
	b = np.array([-4,-10])
	c = np.array([1,2,3,0,0])
	pb = Probleme_standard(A,b,c)
	sol = np.array([5,0,0,1,0])
	return (pb,sol)

def get_aux():
	A = np.array([[-1,-1,1,0,0],[1,-1,0,1,0],[0,1,0,0,1]])
	b = np.array([-4,-1,3])
	c = np.array([1,-2,0,0,0])
	pb = Probleme_standard(A,b,c)
	sol = np.array([1,3,0,1,0])
	return (pb,sol)