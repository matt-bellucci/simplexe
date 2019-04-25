import numpy as np
from probleme import Probleme_standard
from tableau import Tableau, is_positive
import liste_problemes


def conversion_pb(pb):
	"""
	Construction du tableau du simplexe a partir des donnees du probleme
	
	Parameters
	----------

	pb : Probleme_standard
		Le probleme a convertir inclus dans l'objet Probleme_standard

	Returns
	-------
	Tableau
		le tableau du simplexe
	"""
	A = pb.A
	b = pb.b.reshape(pb.b.size,1) # on met le vecteur en b en colonne
	c = pb.c
	c = np.append(c,0) # ajout du 0 dans derniere ligne derniere colonne du tableau
	tab_matrix = np.vstack((np.hstack((A,b)),c))
	tab = Tableau(tab_matrix)
	return tab

def is_primal(pb):
	"""
	Detecte si la base est primale-realisable
	"""
	return is_positive(pb.b)

def simplexe(tab,base,primal,ite_max=10,print_sol=True):
	"""
	Effectue un simplexe

	Algorithme du simplexe qui detecte si le probleme est primal ou dual-realisable
	Si aucun des deux, va passer par un probleme auxiliaire pour trouver une base primale-realisable
	Sinon, va s'arreter au bout d'un nombre fixe d'iterations

	Parameters
	----------
	tab : Tableau
		Le tableau initiale du simplexe, genere a partir d'un probleme standard
	base : numpy.ndarray
		Liste des indices des variables d'une base realisable
	primal : boolean
		Vrai si la base est primale-realisable
		Faux sinon
	ite_max: int
		Le nombre d'iterations maximum avant d'arreter l'algorithme

	Returns
	-------
	sol : numpy.ndarray
		Liste des valeurs prises par toutes les variables, y compris les variables d'ecart
	base : numpy.ndarray
		Liste des indices des variables en base de la solution trouvee
	"""

	ite = 0
	if primal:
		cond = tab.is_positive(tab.nb_lines-1)
	else:
		cond = tab.is_positive(tab.nb_cols-1,axis=1)

	while ite<ite_max and not cond:
		# print("==========Ite {0}=============".format(ite+1))
		# print(tab)
		# chercher pivot
		line,col = pivot(tab,primal=primal)

		# actualiser base
		base[line] = col
		actualisation_tableau(tab,line,col)

		# si primal, on cherche sur le vecteur d (ligne en bas du tableau)
		# sinon sur le vecteur b (colonne a droite)
		if primal:
			cond = tab.is_positive(tab.nb_lines-1)
		else:
			cond = tab.is_positive(tab.nb_cols-1,axis=1)
		ite += 1
	if ite >= ite_max:
		print("Pas de convergence")
	sol = get_solution(tab,base,print_sol=print_sol)
	return (sol,base)

def pivot(tab,critere="naturel",primal=True):
	"""
	Trouve le pivot pour une nouvelle meilleure base

	Utilise le critere de Bland ou naturel pour d'abord rechercher la colonne (ou ligne si dual),
	puis trouve l'autre coordonnee sur le meme critere, le plus petit rapport entre b et la colonne
	(ou ligne) choisie

	Parameters
	----------
	tab : Tableau
		Le tableau du simplexe
	critere : string 
		Soit "naturel", soit "bland", si aucun des deux, naturel est pris par defaut
	primal : boolean
		vrai si la base est primale realisable
		faux sinon

	Returns
	-------
	i,j : int
		la position du pivot, j est la ligne (colonne) si primal (resp. dual)
		et i la colonne (ligne) si primal (resp. dual)

	"""
	# on selectionne le vecteur ou l'on cherche la colonne ou la ligne
	if primal:
		# si primal, on etudie la derniere ligne
		c = np.array(tab.get_line(tab.nb_lines-1)[:-1])
	else:
		# sinon, si dual, on etudie la derniere colonne
		c = np.array(tab.get_column(tab.nb_cols-1)[:-1])

	# si primal, i est la colonne, sinon ligne
	if critere == "bland": 
		i = pivot_bland(c)
	else:
		i = pivot_naturel(c)
	# on divise la derniere colonne avec la ligne ou colonne trouvee 
	b = tab.get_column(tab.nb_cols-1) # derniere colonne
	a_i = tab.get_column(i) # ligne (colonne) choisie
	# division de chaque element de b par ceux de a_i
	div = b/a_i
	# recuperation des indices ou la division est strict positive
	pos_ind = [i for i in range(len(div)) if div[i]>0] 
	if primal:
		# recuperation de l'indice du min pour les elements strict positifs de div
		ind = np.argmin(div[pos_ind]) 
	else:
		# recuperation de l'indice du max pour les elements strict positifs de div
		# c'est a dire que le pivot sera negatif
		ind = np.argmax(div[pos_ind])
	j = pos_ind[ind] # recuperation de la ligne du tableau correspondant a ce min des elements >0
	if primal:
		return (j,i)
	else:
		return (i,j)

def pivot_naturel(c):
	"""
	retourne la position du plus petit element de c (necessairement negatif)

	"""
	return np.argmin(c)

def pivot_bland(c):
	"""
	retourne la position du premier element negatif
	"""
	return np.where(c<0)[0][0]
	
def actualisation_tableau(tab,line,col):
	"""
	passe le pivot a 1 (en divisant la ligne) puis la colonne du pivot a 0 (addition et multiplication de lignes)
	Le tableau est directement actualise dans la fonction
	Parameters
	----------
	tab : Tableau
		le tableau du simplexe directement modifie
	line,col : int
		la ligne et colonne du pivot

	"""
	# on divise la ligne du pivot par la valeur du pivot
	a_ij = tab.get_element(line,col)
	tab.mult_line(line,1/a_ij)

	# on passe la colonne du pivot a 0
	a_ij = tab.get_element(line,col)
	for k in range(tab.nb_lines):
		if k == line:
			continue
		else:
			# on cherche par quelle valeur multiplie la ligne du pivot pour qu'en l'additionnant
			# avec la ligne i, on obtienne 0 sur la colonne du pivot
			a_ik = tab.get_element(k,col)
			coef = -a_ik/a_ij
			tab.add_lines(k,line,coef=coef)	

def resoudre(pb):
	"""
	Trouve une premiere base realisable puis resoud le probleme avec le simplexe

	Calcule une premiere base realisable, par defaut composee des variables d'ecart,
	puis verifie si cette base est primale ou duale realisable. Si c'est le cas, appelle
	le simplexe directement, sinon appelle la fonction probleme_auxiliaire pour trouver une base
	primale realisable

	Parameters
	-----------
	pb : Probleme_standard
		Le probleme a resoudre, sous forme standard

	Returns
	-------
	sol : numpy.ndarray
		Liste des valeurs prises par toutes les variables, y compris les variables d'ecart
	base : numpy.ndarray
		Liste des indices des variables en base de la solution trouvee
	"""

	# calcul de la base, composee des variables d'ecart
	base = [pb.c.size-1-k for k in range(pb.b.size)]
	base.sort()
	# print("base = {0}".format(base))

	# verification pour savoir si primal realisable, dual realisable ou aucun des deux
	primal = is_primal(pb)
	# print("primal = {0}".format(primal))

	# si aucun des deux, appel de probleme_auxiliaire pour trouver une base primale realisable
	if not primal and not is_positive(pb.c):
		print("Pas de base primale ou duale-realisable")
		tab,base = probleme_auxiliaire(pb)
		primal = True
	else:
		tab = conversion_pb(pb)
	return simplexe(tab,base,primal)

def get_solution(tab,base,print_sol=True):
	"""
	Affiche la solution a partir du tableau et de la base et renvoie la liste
	des valeurs de la solution trouvee a cette etape du simplexe

	Parameters
	----------
	tab : Tableau
		Le tableau du simplexe
	base : numpy.ndarray
		La liste des numeros de variables en base

	Returns
	-------
	sol : numpy.ndarray
		La liste des valeurs dans l'ordre des variables de la solution trouvee par le tableau
	"""

	# initialisation des valeurs a 0
	sol = np.zeros(tab.nb_cols-1)

	# on lit la liste des bases qui est dans le meme ordre que les lignes du tableau du simplexe
	# et on met ces valeurs aux positions correspondantes de la liste solution
	for i in range(len(base)):
		sol[base[i]] = tab.get_element(i,tab.nb_cols-1)
	if print_sol:
		# Affichage des solutions sans variables d'ecart et la valeur de la fonction a minimiser correspondante
		print("La solution est : {0}, avec z = {1} et:".format(sol[range(len(base))],-tab.get_element(tab.nb_lines-1,tab.nb_cols-1)))
		# Affichage des valeurs de toutes les variables
		for i in range(len(sol)):
			print("x{0} = {1}".format(i,sol[i]))
	return sol


def probleme_auxiliaire(pb):
	"""
	Cherche une base primale realisable d'un probleme

	Cherche une base primale realisable en resolvant le probleme auxiliaire au probleme donne.
	Le probleme auxiliaire est caracterise par:
	- passage des contraintes a des valeurs positives
	- ajout d'une variable d'ecart par contrainte pour compenser cette modification
	- minimisation des variables d'ecart ajoutee
	On resoud le simplexe correspondant, puis on modifie le tableau du simplexe obtenu
	pour en deduire une base primale realisable du probleme initial

	Potential bugs
	--------------
	On considere que la base du probleme auxiliaire est primale realisable,
	mais ce n'est peut etre pas le cas, a confirmer theoriquement, sinon il faut
	verifier si primal, dual ou ni l'un ni l'autre et faire un appel recursif au probleme 
	auxiliaire

	Parameters
	----------
	pb : Probleme_standard
		Le probleme initial a resoudre, dont on ne dispose pas de base
		primale ou duale realisable
	
	Returns
	-------
	tab_aux : Tableau
		Le tableau du simplexe pour demarrer l'algorithme du simplexe sur le probleme
		initial, avec une base primale realisable
	base_aux : numpy.ndarray
		Liste des numeros de variables qui sont dans la base primale realisable trouvee

	"""

	A = pb.A
	b = pb.b
	c = pb.c

	# ===== Transformation en probleme auxiliaire =====
	# modification le probleme pour avoir b positif
	for i in range(len(b)):
		if b[i]<0:
			b[i] *= -1
			A[i] *= -1
		
	 
	# ajout de nouvelles var d'ecart pour compenser
	A_aux = np.hstack((A,np.eye(len(b))))
	# passage de b en vecteur colonne
	b_aux = b.reshape(b.size,1)
	# concatenation de A_aux et b_aux pour former le tableau du simplexe, sans la derniere ligne
	tab = np.hstack((A_aux,b_aux))
	# calcul de la derniere ligne, qui est l'oppose de la somme des colonnes du tableau
	# sauf pour les nouvelles variables d'ecart
	# ici, on calcule c_aux de cette maniere : [somme des colonnes de A, 0 pour les nvlles var d'ecart, somme colonne b_aux]
	c_aux = np.hstack((-np.sum(A,axis=0),np.zeros(len(b)),-np.sum(b)))
	# concatenation du tableau et de sa derniere ligne et creation d'une instance de Tableau avec ce tableau
	tab = Tableau(np.vstack((tab,c_aux)))

	# ==== Resolution probleme auxiliare ====

	# calcul d'une premiere base primale realisable pour le probleme auxiliaire
	base = [pb.c.size-1-k for k in range(pb.b.size)]
	base.sort()
	# algo du simplexe pour le probleme, avec une base primale realisable (vor potential bugs dans doc)
	sol_aux, base_aux = simplexe(tab,base,True,print_sol=False)

	z = -np.dot(sol_aux[:-len(b)],pb.c)

	# ==== Retour au probleme initial avec la nouvelle base ====

	# suppression des colonnes des nouvelles variables d'ecart
	new_tab = np.delete(tab.tab,range(len(c)-1,len(c)+len(b)-1),1) 
	

	# Calcul des coeffs de la derniere ligne

	# Valeur en bas a droite du tableau prend la valeur du cout obtenu avec cette base
	new_tab[-1,-1] = z
	# si la variable est en base, la valeur prend 0 sinon
	# produit scalaire entre les coeffs des colonnes non en base du tableau par les coeffs
	# de la fonction cout correspondant a chaque indice de base
	for i in range(new_tab.shape[1]-1):
		if i in base_aux:
			new_tab[new_tab.shape[0]-1,i] = 0
		else:
			new_tab[new_tab.shape[0]-1,i] = -np.dot(new_tab[:-1,i], c[base_aux]) 

	tab_aux = Tableau(new_tab)

	return (tab_aux,base_aux)


def main():


	pb,sol = liste_problemes.get_aux()
	pb.affiche()
	sol_s,base = resoudre(pb)
	print(sol_s-sol)

if __name__ == "__main__":
	main()