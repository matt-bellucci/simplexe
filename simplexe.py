import copy
import numpy as np
from probleme import Probleme_standard
from tableau import Tableau, is_positive
import liste_problemes


def conversion_pb(pb):
	# Construction du tableau a partir des donnees du probleme
	A = pb.A
	b = pb.b.reshape(pb.b.size,1) # on met le vecteur en b en colonne
	c = pb.c
	c = np.append(c,0) # ajout du 0 dans derniere ligne derniere colonne du tableau
	tab_matrix = np.vstack((np.hstack((A,b)),c))
	tab = Tableau(tab_matrix)
	return tab

def is_primal(pb):
	return is_positive(pb.b)

def simplexe(tab,base,primal,ite_max=10):

	# Demarrage iterations
	bases = [copy.copy(base)]
	ite = 0
	print(base)
	if primal:
		cond = tab.is_positive(tab.nb_lines-1)
	else:
		cond = tab.is_positive(tab.nb_cols-1,axis=1)

	while ite<ite_max and not cond:
		print(tab)
		print("==========Ite {0}=============".format(ite+1))
		# chercher pivot
		line,col = pivot(tab,primal=primal)
		# actualiser base
		base[line] = col

		bases.append(copy.copy(base))

		actualisation_tableau(tab,line,col)
		if primal:
			cond = tab.is_positive(tab.nb_lines-1)
		else:
			cond = tab.is_positive(tab.nb_cols-1,axis=1)
		ite += 1
	print(tab)
	if ite >= ite_max:
		print("Pas de convergence")
	sol = affiche_solution(tab,base)
	return (sol,base)

def pivot(tab,critere="naturel",primal=True):

	if primal:
		c = np.array(tab.get_line(tab.nb_lines-1)[:-1])
	else:
		c = np.array(tab.get_column(tab.nb_cols-1)[:-1])

	if critere == "bland": # si primal, i est la colonne, sinon ligne
		i = pivot_bland(c)
	else:
		i = pivot_naturel(c)

	b = tab.get_column(tab.nb_cols-1)
	a_i = tab.get_column(i)

	div = b/a_i # division de b par a_i
	pos_ind = [i for i in range(len(div)) if div[i]>0] # recuperation des indices ou la division est strict positive
	if primal:
		ind = np.argmin(div[pos_ind]) # recuperation de l'indice du min pour les elements strict positifs de div
	else:
		ind = np.argmax(div[pos_ind])
	j = pos_ind[ind] # recuperation de la ligne du tableau correspondant a ce min des elements >0
	if primal:
		return (j,i)
	else:
		return (i,j)

def pivot_naturel(c):

	return np.argmin(c)

def pivot_bland(c):

	return np.where(c<0)[0][0]
	
def actualisation_tableau(tab,line,col):
		a_ij = tab.get_element(line,col)
		tab.mult_line(line,1/a_ij)
		# colonne du pivot a 0
		a_ij = tab.get_element(line,col)
		for k in range(tab.nb_lines):
			if k == line:
				continue
			else:
				a_ik = tab.get_element(k,col)
				coef = -a_ik/a_ij
				tab.add_lines(k,line,coef=coef)	
def resoudre(pb):
	base = [pb.c.size-1-k for k in range(pb.b.size)]
	base.sort()
	# print("base = {0}".format(base))

	primal = is_primal(pb)
	print("primal = {0}".format(primal))
	if not primal and not is_positive(pb.c):
		print("Pas de base primale ou duale-realisable")
		tab,base = probleme_auxiliaire(pb,base)
		primal = True
	else:
		tab = conversion_pb(pb)
	x = simplexe(tab,base,primal)
	return x

def affiche_solution(tab,base):
	sol = np.zeros(tab.nb_cols-1)
	for i in range(len(base)):
		sol[base[i]] = tab.get_element(i,tab.nb_cols-1)
	print("La solution est : {0}, avec z = {1} et:".format(sol[range(len(base))],-tab.get_element(tab.nb_lines-1,tab.nb_cols-1)))
	for i in range(len(sol)):
		print("x{0} = {1}".format(i,sol[i]))
	return sol


def probleme_auxiliaire(pb,base):

	A = pb.A
	b = pb.b
	c = pb.c
	# on modifie le probleme pour avoir b positif
	for i in range(len(b)):
		if b[i]<0:
			b[i] *= -1
			A[i] *= -1
		# on ajoute de nouvelles var d'ecart
		n_vars = np.zeros(len(b)) 
		n_vars[i] = 1
	A_aux = np.hstack((A,np.eye(len(b))))
	b_aux = b.reshape(b.size,1)
	tab = np.hstack((A_aux,b_aux))
	c_aux = np.hstack((-np.sum(A,axis=0),np.zeros(len(b)),-np.sum(b)))
	tab = Tableau(np.vstack((tab,c_aux)))
	base = [pb.c.size-1-k for k in range(pb.b.size)]
	base.sort()
	sol_aux, base_aux = simplexe(tab,base,True)
	print(sol_aux)
	print(base_aux)

	z = -np.dot(sol_aux[:-len(b)],pb.c)
	print(z)
	# on supprime les colonnes des nouvelles variables d'ecart
	new_tab = np.delete(tab.tab,range(len(c)-1,len(c)+len(b)-1),1) 
	new_tab[-1,-1] = z
	not_inbase = [k for k in range(len(new_tab[0])) if k not in base_aux]
	for i in range(new_tab.shape[1]-1):
		if i in base_aux:
			new_tab[new_tab.shape[0]-1,i] = 0
		else:
			# produit scalaire entre les coeffs des colonnes non en base du tableau par les coeffs
			# de la fonction cout correspondant a chaque indice de base 
			new_tab[new_tab.shape[0]-1,i] = -np.dot(new_tab[:-1,i], c[base_aux]) 
	print(new_tab)
	tab_aux = Tableau(new_tab)

	return (tab_aux,base_aux)


def main():


	pb = liste_problemes.get_aux()
	pb.affiche()
	sol_s = resoudre(pb)
	# print(sol-sol_s)

if __name__ == "__main__":
	main()