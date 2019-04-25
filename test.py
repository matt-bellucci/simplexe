import liste_problemes
import simplexe

print("Choix test simplexe:")
print("1. Probleme primal-realisable")
print("2. Probleme dual-realisable")
print("3. Probleme auxiliaire")
print("4. Saisir un probleme")
choix = '0'
while int(choix) not in range(1,5):
	choix = input("Choix : ")
	if choix == '1':
		pb,sol = liste_problemes.get_primal()
	elif choix == '2':
		pb,sol = liste_problemes.get_dual()
	elif choix == '3':
		pb,sol = liste_problemes.get_aux()
	elif choix == '4':
		pb,sol = liste_problemes.enter_problem()
	else:
		choix = input("Choix : ")

pb.affiche()
print("Lancement du simplexe")
sol_simplexe,tab = simplexe.resoudre(pb)
print("Solution simplexe = {0}".format(sol_simplexe))
print("Bonne solution = {0}".format(sol))

