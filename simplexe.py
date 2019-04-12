import copy
import numpy as np
from probleme import Probleme_standard
from tableau import Tableau, is_positive
import liste_problemes

def simplexe(pb,base):

	bases = [copy.copy(base)]
	ite_max = 10

	# Construction du tableau a partir des donnees du probleme

	A = pb.A
	b = pb.b.reshape(pb.b.size,1) # on met le vecteur en b en colonne
	c = pb.c
	c = np.append(c,0) # ajout du 0 dans derniere ligne derniere colonne du tableau
	tab_matrix = np.vstack((np.hstack((A,b)),c)) # concatenation de A, b et c pour former le tab du simplexe
	tab = Tableau(tab_matrix)
	primal = is_positive(tab.get_column(tab.nb_cols-1))
	print("primal = {0}".format(primal))
	if not primal and not is_positive(tab.get_line(tab.nb_lines-1)):

		print("Pas de base primale ou duale-realisable")
		tab,base = probleme_auxiliaire(tab,base)

	# Demarrage iterations

	ite = 0
	while ite<ite_max and not tab.is_positive(tab.nb_lines-1):
		# print("==========Ite {0}=============".format(ite+1))
		# chercher pivot
		line,col = pivot(tab,primal=primal)
		# actualiser base
		base[line] = col
		bases.append(copy.copy(base))

		actualisation_tableau(tab,line,col)

		ite += 1

	if ite >= ite_max:
		print("Pas de convergence")
	sol = affiche_solution(tab,base)
	return sol

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
	amin = np.argmin(div[pos_ind]) # recuperation de l'indice du min pour les elements strict positifs de div
	j = pos_ind[amin] # recuperation de la ligne du tableau correspondant a ce min des elements >0
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
	x = simplexe(pb,base)
	return x

def affiche_solution(tab,base):
	sol = np.zeros(tab.nb_cols-1)
	for i in range(len(base)):
		sol[base[i]] = tab.get_element(i,tab.nb_cols-1)
	print("La solution est : {0}, avec z = {1} et:".format(sol[range(len(base))],-tab.get_element(tab.nb_lines-1,tab.nb_cols-1)))
	for i in range(len(sol)):
		print("x{0} = {1}".format(i,sol[i]))
	return sol


def probleme_auxiliaire(tab,base):





	return (tab,base)


def main():


	pb,sol = liste_problemes.get_primal()
	pb.affiche()
	sol_s = resoudre(pb)
	print(sol-sol_s)

if __name__ == "__main__":
	main()