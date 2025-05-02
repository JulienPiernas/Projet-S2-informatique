from personne import Patissier, Fermier, Paysan
from hdv import HDV
from simulation_fonction_backup import simulation_gateau

liste_personne = []
nb_patissier = 1
nb_fermier = 15
nb_paysan = 30
for i in range(nb_patissier):
    liste_personne.append(Patissier(1, [10, 5], 100))

for i in range(nb_fermier):
    liste_personne.append(Fermier(1, 100, 30, 2))

for i in range(nb_paysan):
    liste_personne.append(Paysan(1, 100, 30, 1))

HOTEL_DE_VENTE = HDV(["Blé", "Oeuf", "Gâteau"])

simulation_gateau(liste_personne, HOTEL_DE_VENTE)
