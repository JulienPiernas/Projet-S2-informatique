from random import randint, shuffle, seed
import json
x = randint(1, 50000000000000000)
seed(x)
print("Seed = ", x)


class Acheteur:
    def __init__(self, salaire, prix_limite, besoins):
        self.sal = salaire
        self.pl = prix_limite
        self.brs = salaire
        self.besoins = besoins
        self.humeur = "Content"

    def achete(self, prix, vendeur):
        stock = vendeur.get_stock()
        if stock == 0:
            self.humeur = "Pas content : stock vide"
        nb_acheté = 0
        while (
            nb_acheté < self.besoins
            and nb_acheté * prix <= self.brs
            and nb_acheté < stock
        ):
            nb_acheté += 1
        self.brs -= prix * nb_acheté
        if nb_acheté >= self.besoins:
            self.humeur = "Content : besoins satisfaits"
        elif nb_acheté != 0:
            self.humeur = "Moyen : a acheté mais pas assez"
        vendeur.prendre_dans_stock(nb_acheté)

    def achete_oui_non(self, proposition, vendeur):
        if proposition <= self.pl:
            self.achete(proposition, vendeur)
        else:
            self.humeur = "Pas content : prix trop élevé"

    def changer_besoins(self):
        self.besoins += randint(1, 5)
        var = self.humeur
        if 'Pas content' not in var:
            self.besoins -= self.acheté_en_dernier

    def change_prix_limite(self):
        if "Moyen" in self.humeur:
            self.pl *= 1.05
        elif "Pas content" in self.humeur:
            self.pl *= 1.1
        else:
            self.pl *= 0.9
        if self.pl > self.brs:
            self.pl = self.brs


    def avant_tick(self):
        self.brs += self.sal
        self.changer_besoins()
        self.change_prix_limite()


class Vendeur:
    def __init__(self, stock, cout_prod, bourse):
        self.cout_prod = cout_prod
        self.stock = stock
        self.recettes = []
        self.brs_avant_tick = bourse
        self.brs_apres_tick = bourse
        self.prix_courant = cout_prod
        self.prix_archive = []
        self.pourcent_var = 8
        self.sens_variation = 1

    def avant_tick(self):
        nouveaux_produits = randint(20, 500)
        while self.brs_apres_tick < nouveaux_produits * self.cout_prod:
            nouveaux_produits = randint(20, 500)
        self.brs_apres_tick -= nouveaux_produits * self.cout_prod
        self.stock += nouveaux_produits
        self.brs_avant_tick = self.brs_apres_tick

    def get_stock(self):
        return self.stock

    def prendre_dans_stock(self, nb_acheté):
        self.stock -= nb_acheté
        self.brs_apres_tick += nb_acheté * self.prix_courant

    def variation_prix(self):
        self.prix_courant = self.prix_courant * (
            1 + (self.pourcent_var * self.sens_variation) / 100
        )

    def changer_variation(self):
        self.sens_variation = self.sens_variation * -1

    def changer_pourcentage(self):
        if self.pourcent_var > 1.1:
            self.pourcent_var = self.pourcent_var / 2

    def propose_prix(self):
        if (
            len(self.prix_archive) < 3
        ):  # si c'est la première, deuxième ou troisième fois
            self.variation_prix()
            return self.prix_courant
        elif self.recettes[-3] <= self.recettes[-2] <= self.recettes[-1]:
            self.variation_prix()
            return self.prix_courant
        else:
            self.changer_variation()
            self.changer_pourcentage()
            self.variation_prix()
            return self.prix_courant

    def archive(self):
        self.prix_archive.append(self.prix_courant)
        self.recettes.append(self.brs_apres_tick - self.brs_avant_tick)


def simulation_1_vendeur_n_acheteur(vendeur, liste_acheteurs):
    shuffle(liste_acheteurs)
    proposition_prix = vendeur.propose_prix()
    for acheteur in liste_acheteurs:
        acheteur.achete_oui_non(proposition_prix, vendeur)

    vendeur.archive()
    print("Pour le vendeur : ")
    print("Prix courant :", vendeur.prix_courant)
    print("Recette du jour :", vendeur.recettes[-1])
    print("Stock restant :", vendeur.get_stock())
    print("--------------------------------------------------------------------")
    print("pour les acheteurs : ")
    for i in range(len(liste_acheteurs)):
        print("Acheteur n°", i, ": humeur :", liste_acheteurs[i].humeur)
        liste_acheteurs[i].avant_tick()

    vendeur.avant_tick()
    enregistrer_resultats(vendeur, liste_acheteurs, len(vendeur.recettes))
    continuer = input("Continuer ? : (Y/N) : ")
    if continuer == "Y":
        simulation_1_vendeur_n_acheteur(vendeur, liste_acheteurs)


def enregistrer_resultats(vendeur, liste_acheteurs, iteration):
    data = {
        "iteration": iteration,
        "vendeur": {
            "prix_courant": vendeur.prix_courant,
            "recette_du_jour": vendeur.recettes[-1] if vendeur.recettes else 0,
            "stock_restant": vendeur.get_stock()
        },
        "acheteurs": [
            {"id": i, "humeur": acheteur.humeur, "budget_restant": acheteur.brs}
            for i, acheteur in enumerate(liste_acheteurs)
        ]
    }

    with open("resultats.json", "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.write(",\n")
