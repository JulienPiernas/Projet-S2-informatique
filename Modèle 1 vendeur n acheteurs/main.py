from code_projet import Vendeur, Acheteur, simulation_1_vendeur_n_acheteur
from random import randint

vendeur = Vendeur(1000, 2, 5000)

liste_acheteurs = []
for i in range(20):
    liste_acheteurs.append(Acheteur(randint(1000, 5000), randint(2, 10), randint(5, 50)))

simulation_1_vendeur_n_acheteur(vendeur, liste_acheteurs)
