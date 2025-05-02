from personne import Patissier, Paysan, Fermier
from fonction_simulation import simulation
from random import seed, randint

# x = randint(1, 50000000000000000)
# x = 9038446488566274
x = "SOLAL LE BG"
seed(x)

besoin_patissier_départ = 0
prix_achat_oeuf_départ = 15
prix_achat_blé_départ = 5
brs_patissier_départ = 500

prix_achat_gateau_départ = 12

besoin_fermier_départ = 0
brs_fermier_départ = 500
prix_vente_oeuf_départ = 5

prod_oeuf_max = 10

brs_paysan_départ = 500
prix_vente_blé_départ = 2
prod_blé_max = 20

patissier = Patissier(
    besoin_patissier_départ,
    [prix_achat_oeuf_départ, prix_achat_blé_départ],
    brs_patissier_départ,
)



fermier = Fermier(
    besoin_fermier_départ,
    brs_fermier_départ,
    prix_achat_gateau_départ,
    prix_vente_oeuf_départ,
    prod_oeuf_max,
)



paysan = Paysan(
    besoin_fermier_départ,
    brs_fermier_départ,
    prix_achat_gateau_départ,
    prix_vente_blé_départ,
    prod_blé_max,
)


print(simulation(patissier, paysan, fermier))
print("SEED : ", x)
