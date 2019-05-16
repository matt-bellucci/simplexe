import numpy as np
from probleme import Probleme_standard, Probleme_canonique

"""
Ce module permet d'acceder a des problemes a resoudre et connaitre leur solution
"""
def get_primal():
	A = np.array([[2,3,1,1,0,0],[4,1,2,0,1,0],[3,4,2,0,0,1]])
	b = np.array([5,11,8])
	c = np.array([-5,-4,-3,0,0,0])
	pb = Probleme_standard(A,b,c)
	sol = np.array([2.,0.,1.,0.,1.,0.])
	return (pb,sol)
def exemple_primal():
	A = np.array([[1,1,1,0],[2,1,0,1]])
	b = np.array([40,60])
	c = np.array([-4,-3,0,0])
	pb = Probleme_standard(A,b,c)
	sol = np.array([20.,20.,0.,0.])
	return (pb,sol)

def get_dual():
	A = np.array([[-1,-1,0,1,0],[-2,3,-5,0,1]])
	b = np.array([-4,-10])
	c = np.array([1,2,3,0,0])
	pb = Probleme_standard(A,b,c)
	sol = np.array([5.,0.,0.,1.,0.])
	return (pb,sol)

def get_aux():
	A = np.array([[-1,-1,1,0,0],[1,-1,0,1,0],[0,1,0,0,1]])
	b = np.array([-4,-1,3])
	c = np.array([1,-2,0,0,0])
	pb = Probleme_standard(A,b,c)
	sol = np.array([1.,3.,0.,1.,0.])
	return (pb,sol)

def enter_problem():
	canon = input('Probleme canonique? (o/n): ') == 'o'
	nb_contraintes =  int(input('Nombre de contraintes : '))
	nb_variables = int(input('Nombre de variables : '))
	if canon:
		sep = '<='
	else:
		sep = '='
	A = np.zeros((nb_contraintes,nb_variables))
	c = np.zeros(nb_variables)
	b = np.zeros(nb_contraintes)
	fin = False
	while not fin:
		print('Saisie du cout')
		output = ''
		for i in range(nb_variables):
			c[i] = float(input('Coeff de la variable {0} = '.format(i+1)))
			output += '{0}x{1}'.format(c[i],i+1)
			if i != nb_variables-1:
				output += ' + '
		print('La saisie donne : ')
		print('z = '+output)
		suite = input('Voulez-vous recommencer la saisie? (o/n)')
		fin = suite != 'o'

	print('Saisie des contraintes')
	for i in range(nb_contraintes):
		print('Contrainte {0}'.format(i+1))
		j = 0
		valide = False
		while not valide:
			output = ''
			for j in range(nb_variables):
				A[i,j] = float(input('Coeff de la variable {0} = '.format(j+1)))
				output += '{0}x{1}'.format(A[i,j],j+1)
				if j != nb_variables-1:
					output += ' + '
			b[i] = float(input('Valeur de la contrainte = '))
			output = output + ' ' + sep + ' ' + str(b[i])
			print('Contrainte {0} : {1}'.format(i+1,output))
			valide = input('Recommencer? (o/n) ') == 'n'
	if canon:
		pb = Probleme_canonique(A,b,c)
		pb.affiche()
		print('Conversion en probleme standard')
		pb = pb.canon2stand()
	else:
		pb = Probleme_standard(A,b,c)
	sol_connue = input('La solution est-elle connue? (o/n)') == 'o'
	sol = np.zeros(nb_variables)
	if sol_connue:
		valide = False
		while not valide:
			for i in range(nb_variables):
				sol[i] = input('Sol variable {0} = '.format(i+1))
			print("Solution = {0}".format(sol))
			valide = input("Recommencer saisie? (o/n) ") == 'n'

	return (pb,sol)



