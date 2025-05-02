from random import shuffle
import matplotlib.pyplot as plt


class Personne:
    def __init__(self, nom, stock, bourse, delta_besoin):
        # Un nom pour différencier une personne d'une autre
        self.nom = nom
        # Le stock de départ et la bourse de départ
        self.stock = stock
        self.bourse = bourse
        # Le besoin de départ est l'incrémentation une fois (delta_besoin)
        self.besoin_gateau = 0
        self.delta_besoin = delta_besoin
        # Au départ le niveau de stress est à 0
        self.n_stress = 0
        # prix précédents + moyenne des prix des produits acheté au tick précedent + nb de gateaux acheté
        self.prix_acheté = []
        self.moy_gateau = 1
        self.gateau_acheté = 0

    def achète(self, hdv):
        # On fait une demande d'achat à l'hdv (valable pour paysan et agriculteur)
        quantité = self.besoin_gateau + self.n_stress
        hdv.deposer_ordre_achat(OrdreAchat("gateau", quantité, self))
        self.besoin_gateau = max(0, self.besoin_gateau - self.gateau_acheté)
        self.gateau_acheté = 0

    def propose_prix(self):
        prix_proposé = (
            self.moy_gateau * (self.besoin_gateau + self.n_stress)
        ) / self.stock
        return PropositionPrix(prix_proposé, self)

    def début_de_journée(self):
        self.gateau_acheté = 0
        # v1
        self.besoin_gateau += self.delta_besoin
        self.n_stress = max(self.besoin_gateau - self.delta_besoin, 0)
        # v2
        # self.n_stress = self.besoin_gateau
        # self.besoin_gateau = self.delta_besoin
        if len(self.prix_acheté) >= 1:
            self.moy_gateau = sum(self.prix_acheté) / len(self.prix_acheté)
            self.prix_acheté = []
        else:
            self.moy_gateau = 1
        self.stock += self.delta_production


"""
Les trois agents

"""


class Patissier(Personne):
    # la recette des patissiers est : 1 oeufs + 2 blé = 1 gateau
    RECETTE = {"oeuf": 1, "blé": 2}
    # La constante de marge
    K_MARGE = 2

    def __init__(self, nom, bourse, delta_besoin, stock=0):
        super().__init__(nom, stock, bourse, delta_besoin)
        # Stock de blé et d'oeuf
        self.stock_blé = 0
        self.stock_oeuf = 0
        # Qu'est ce que je vends ?
        self.produit = "gateau"
        # moyenne des prix du blé et des oeufs du tick précedent
        self.prix_oeuf_acheté = []
        self.prix_blé_acheté = []
        self.moy_oeuf = 1
        self.moy_blé = 1

    def achète(self, hdv, produit):
        # On surcharge achète
        qté = Patissier.RECETTE[produit] * (
            self.besoin_gateau + self.n_stress + Patissier.K_MARGE
        )
        hdv.deposer_ordre_achat(OrdreAchat(produit, qté, self))

    def produire(self):
        # tant qu'on peut produire selon la recette on produit
        while (
            self.stock_oeuf - Patissier.RECETTE["oeuf"] >= 0
            and self.stock_blé - Patissier.RECETTE["blé"] >= 0
        ):
            self.stock_blé -= Patissier.RECETTE["blé"]
            self.stock_oeuf -= Patissier.RECETTE["oeuf"]
            # Si on a plus besoin de gateau, on les rajoutent au stock
            if self.besoin_gateau <= 0:
                self.stock += 1
            else:
                self.besoin_gateau -= 1

    def propose_prix(self):
        # on surcharge propose prix
        prix_proposé = (
            self.moy_oeuf * Patissier.RECETTE["oeuf"]
            + self.moy_blé * Patissier.RECETTE["blé"]
        ) * (self.n_stress + Patissier.K_MARGE)
        prix_proposé /= self.stock
        return PropositionPrix(prix_proposé, self)

    def début_de_journée(self):
        # v1
        self.besoin_gateau += self.delta_besoin
        self.n_stress = max(self.besoin_gateau - self.delta_besoin, 0)
        # V2
        # self.n_stress = self.besoin_gateau
        # self.besoin_gateau = self.delta_besoin
        if len(self.prix_blé_acheté) >= 1:
            self.moy_blé = sum(self.prix_blé_acheté) / len(self.prix_blé_acheté)
            self.prix_blé_acheté = []
        else:
            self.moy_blé = 1
        if len(self.prix_oeuf_acheté) >= 1:
            self.moy_oeuf = sum(self.prix_oeuf_acheté) / len(self.prix_oeuf_acheté)
            self.prix_oeuf_acheté = []
        else:
            self.moy_blé = 1


class Paysan(Personne):
    def __init__(self, nom, stock, bourse, delta_besoin, delta_production):
        super().__init__(nom, stock, bourse, delta_besoin)
        # Qu'est ce que je vends ?
        self.produit = "oeuf"
        # Combien j'en produit par tick ?
        self.delta_production = delta_production


class Agriculteur(Personne):
    def __init__(self, nom, stock, bourse, delta_besoin, delta_production):
        super().__init__(nom, stock, bourse, delta_besoin)
        # Qu'est ce que je vends ?
        self.produit = "blé"
        # Combien j'en produit par tick ?
        self.delta_production = delta_production


"""
Ordre d'achat + proposition de prix + HDV

"""


class OrdreAchat:
    def __init__(self, produit, quantité, acheteur):
        self.produit = produit
        self.quantité = quantité
        self.acheteur = acheteur


class PropositionPrix:
    def __init__(self, prix, vendeur):
        self.prix = prix
        self.vendeur = vendeur


class HDV:
    def __init__(self, liste_agent):
        self.liste_paysan = [agent for agent in liste_agent if agent.produit == "oeuf"]
        self.liste_agriculteur = [
            agent for agent in liste_agent if agent.produit == "blé"
        ]
        self.liste_patissier = [
            agent for agent in liste_agent if agent.produit == "gateau"
        ]

    def deposer_ordre_achat(self, ordre_achat):
        produit = ordre_achat.produit

        # Les vendeurs potentiels en fonction du produit voulu
        if produit == "gateau":
            liste_vendeur = [
                patissier for patissier in self.liste_patissier if patissier.stock > 0
            ]
        elif produit == "blé":
            liste_vendeur = [
                agriculteur
                for agriculteur in self.liste_agriculteur
                if agriculteur.stock > 0
            ]
        else:
            liste_vendeur = [paysan for paysan in self.liste_paysan if paysan.stock > 0]

        liste_proposition = [vendeur.propose_prix() for vendeur in liste_vendeur]
        liste_proposition.sort(key=lambda i: i.prix)  # à voir si ça marche

        qté_restante = ordre_achat.quantité
        i_vendeur = 0
        # Tant que la demande n'est pas satisfaite et qu'il y a encore des vendeurs avec du stock et que l'acheteur a encore de l'argent
        while (
            qté_restante > 0
            and i_vendeur < len(liste_proposition)
            and ordre_achat.acheteur.bourse - liste_proposition[i_vendeur].prix >= 0
        ):
            if produit == "gateau":
                # On fait la transaction de 1 gateau
                # on enlève 1 gateau du stock du vendeur
                liste_proposition[i_vendeur].vendeur.stock -= 1
                # On ajoute le prix du gateau au vendeur
                liste_proposition[i_vendeur].vendeur.bourse += liste_proposition[
                    i_vendeur
                ].prix
                # On prélève le prix à l'acheteur
                ordre_achat.acheteur.bourse -= liste_proposition[i_vendeur].prix
                # On ajoute le gateau aux gateaux achetés
                ordre_achat.acheteur.gateau_acheté += 1
            elif produit == "oeuf":
                # on fait la transaction de 1 oeuf
                # on enlève 1 oeuf du stock du vendeur
                liste_proposition[i_vendeur].vendeur.stock -= 1
                # On ajoute le prix de l'oeuf au vendeur
                liste_proposition[i_vendeur].vendeur.bourse += liste_proposition[
                    i_vendeur
                ].prix
                # On prélève le prix à l'acheteur
                ordre_achat.acheteur.bourse -= liste_proposition[i_vendeur].prix
                # On ajoute l'oeuf au stock d'oeuf
                ordre_achat.acheteur.stock_oeuf += 1
            else:
                # on fait la transaction de 1 blé
                # on enlève 1 blé du stock du vendeur
                liste_proposition[i_vendeur].vendeur.stock -= 1
                # On ajoute le prix du blé au vendeur
                liste_proposition[i_vendeur].vendeur.bourse += liste_proposition[
                    i_vendeur
                ].prix
                # On prélève le prix à l'acheteur
                ordre_achat.acheteur.bourse -= liste_proposition[i_vendeur].prix
                # On ajoute l'oeuf au stock d'oeuf
                ordre_achat.acheteur.stock_blé += 1

            # On vérifie si le vendeur actuel a encore du stock
            if liste_proposition[i_vendeur].vendeur.stock <= 0:
                if produit == "gateau":
                    ordre_achat.acheteur.prix_acheté.append(
                        liste_proposition[i_vendeur].prix
                    )
                    i_vendeur += 1
                elif produit == "oeuf":
                    ordre_achat.acheteur.prix_oeuf_acheté.append(
                        liste_proposition[i_vendeur].prix
                    )
                    i_vendeur += 1
                else:
                    ordre_achat.acheteur.prix_blé_acheté.append(
                        liste_proposition[i_vendeur].prix
                    )
                    i_vendeur += 1

            qté_restante -= 1

        # On oublie pas le prix de l'acheteur courant
        if qté_restante <= 0 and i_vendeur < len(liste_proposition):
            if produit == "gateau":
                ordre_achat.acheteur.prix_acheté.append(
                    liste_proposition[i_vendeur].prix
                )
            elif produit == "oeuf":
                ordre_achat.acheteur.prix_oeuf_acheté.append(
                    liste_proposition[i_vendeur].prix
                )
            else:
                ordre_achat.acheteur.prix_blé_acheté.append(
                    liste_proposition[i_vendeur].prix
                )


"""
La simulation

"""


# def simulation_compliquée(nb_tick, petit_monde):
#     # On crée l'HDV qui acceuillera tout le petit monde
#     hdv = HDV(petit_monde)
#     # On effectue n_tick tick
#     for _ in range(nb_tick):
#         # Au début du tick, tout le monde fait ce qu'il a à faire
#         for personne in petit_monde:
#             personne.début_de_journée()

#         # Les patissier achète d'abord : On les mélange pour simuler l'ordre d'arrivée
#         shuffle(hdv.liste_patissier)
#         for patissier in hdv.liste_patissier:
#             # On achète les oeufs
#             patissier.achète(hdv, "oeuf")
#             # On achète le blé
#             patissier.achète(hdv, "blé")
#             # On produit
#             patissier.produire()

#         # On crée une liste composée de tous les agents qui achètent des gateaux :
#         # Les paysans et les agriculteurs
#         liste_achète_gateau = hdv.liste_agriculteur + hdv.liste_paysan

#         # On mélange et on achète
#         shuffle(liste_achète_gateau)
#         for personne in liste_achète_gateau:
#             personne.achète(hdv)

#     # A la fin, on fait un retour
#     for p in petit_monde:
#         if p.produit == "gateau":
#             print(
#                 "Patissier : Nom : {}, n_stress : {}, bourse : {}, moy_blé : {}, moy_oeuf : {}, stock : {}".format(
#                     p.nom, p.n_stress, p.bourse, p.moy_blé, p.moy_oeuf, p.stock
#                 )
#             )
#         elif p.produit == "oeuf":
#             print(
#                 "Paysan : Nom : {}, n_stress : {}, bourse : {}, prix_moy : {}, stock : {}".format(
#                     p.nom, p.n_stress, p.bourse, p.moy_gateau, p.stock
#                 )
#             )
#         elif p.produit == "blé":
#             print(
#                 "Agriculteur : Nom : {}, n_stress : {}, bourse : {}, prix_moy : {}, stock : {}".format(
#                     p.nom, p.n_stress, p.bourse, p.moy_gateau, p.stock
#                 )
#             )


def simulation_compliquée(nb_tick, petit_monde):
    # On crée l'HDV qui acceuillera tout le petit monde
    hdv = HDV(petit_monde)

    # Initialisation des listes pour stocker les moyennes à chaque tick
    ticks = []
    moy_gateaux = []
    moy_bles = []
    moy_oeufs = []

    # On effectue n_tick tick
    for tick in range(nb_tick):
        # Au début du tick, tout le monde fait ce qu'il a à faire
        for personne in petit_monde:
            personne.début_de_journée()

        # Les patissier achètent d'abord : On les mélange pour simuler l'ordre d'arrivée
        shuffle(hdv.liste_patissier)
        for patissier in hdv.liste_patissier:
            # On achète les oeufs
            patissier.achète(hdv, "oeuf")
            # On achète le blé
            patissier.achète(hdv, "blé")
            # On produit
            patissier.produire()

        # On crée une liste composée de tous les agents qui achètent des gateaux :
        # Les paysans et les agriculteurs
        liste_achète_gateau = hdv.liste_agriculteur + hdv.liste_paysan

        # On mélange et on achète
        shuffle(liste_achète_gateau)
        for personne in liste_achète_gateau:
            personne.achète(hdv)

        # Collecte des données pour le graphe
        ticks.append(tick)
        moy_gateaux.append(
            sum(p.moy_gateau for p in petit_monde if p.produit == "gateau")
            / max(1, len([p for p in petit_monde if p.produit == "gateau"]))
        )
        moy_bles.append(
            sum(p.moy_blé for p in petit_monde if p.produit == "gateau")
            / max(1, len([p for p in petit_monde if p.produit == "gateau"]))
        )
        moy_oeufs.append(
            sum(p.moy_oeuf for p in petit_monde if p.produit == "gateau")
            / max(1, len([p for p in petit_monde if p.produit == "gateau"]))
        )

    # Génération du graphe
    plt.figure(figsize=(10, 6))
    plt.plot(ticks, moy_gateaux, label="Moyenne Gateaux", color="blue")
    plt.plot(ticks, moy_bles, label="Moyenne Blé", color="green")
    plt.plot(ticks, moy_oeufs, label="Moyenne Œufs", color="orange")
    plt.xlabel("Ticks")
    plt.ylabel("Moyennes")
    plt.title("Évolution des moyennes des prix produits au fil des ticks")
    plt.legend()
    plt.grid()
    plt.show()

    # A la fin, on fait un retour
    for p in petit_monde:
        if p.produit == "gateau":
            print(
                "Patissier : Nom : {}, n_stress : {}, bourse : {}, moy_blé : {}, moy_oeuf : {}, stock : {}".format(
                    p.nom, p.n_stress, p.bourse, p.moy_blé, p.moy_oeuf, p.stock
                )
            )
        elif p.produit == "oeuf":
            print(
                "Paysan : Nom : {}, n_stress : {}, bourse : {}, prix_moy : {}, stock : {}".format(
                    p.nom, p.n_stress, p.bourse, p.moy_gateau, p.stock
                )
            )
        elif p.produit == "blé":
            print(
                "Agriculteur : Nom : {}, n_stress : {}, bourse : {}, prix_moy : {}, stock : {}".format(
                    p.nom, p.n_stress, p.bourse, p.moy_gateau, p.stock
                )
            )
