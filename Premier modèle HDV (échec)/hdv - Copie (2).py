class Acheteur:
    def __init__(self, prix_max, bourse, quantité_voulue):
        self.prix = prix_max
        self.bourse = bourse
        self.quantité = quantité_voulue


class Vendeur:
    def __init__(self, stock, bourse, prix_min, quantité_vente):
        self.stock = stock
        self.prix = prix_min
        self.brs_avant_tick = bourse
        self.brs_apres_tick = bourse
        self.quantité = quantité_vente


class Ordre_achat:
    def __init__(self, prix_max, acheteur, produit_voulu, quantité_voulue):
        self.prix = prix_max
        self.acheteur = acheteur
        self.quantité = quantité_voulue
        self.produit_voulu = produit_voulu


class Ordre_vente:
    def __init__(self, prix_min, vendeur, produit_vendu, quantité_dispo):
        self.prix = prix_min
        self.vendeur = vendeur
        self.quantité = quantité_dispo
        self.produit_vendu = produit_vendu


class HDV:
    def __init__(self, liste_produits):
        self.produits = liste_produits
        self.dico_hdv = {}
        for e in liste_produits :
            self.dico_hdv[e] = ([], [])

        # On associe à chaque produit un tuple de 2 listes qui sont la liste des ordres de ventes t[0]et la liste des ordres d'achat t[1]


    def transaction_ordre_achat(
        self, vendeur, acheteur, ordre_achat, ordre_vente
    ):  # acheteur paye prix min
        vendeur.stock -= ordre_vente.quantité
        vendeur.brs_apres_tick += ordre_vente.quantité * ordre_achat.prix
        acheteur.bourse -= ordre_vente.quantité * ordre_achat.prix


    def transaction_ordre_vente(
        self, vendeur, acheteur, ordre_vente, ordre_achat
    ):  # vendeur fait payer prix max
        vendeur.stock -= ordre_vente.quantité
        vendeur.brs_apres_tick += ordre_vente.quantité * ordre_achat.prix
        acheteur.bourse -= ordre_vente.quantité * ordre_achat.prix


    def recherche_ordre_vente(self, ordre_achat):
        for ordre in self.ordres_dico_hdv[ordre_achat.produit_voulu][0]:
            if ordre.quantité == ordre_achat.quantité and ordre.prix <= ordre_achat.prix:
                self.ordres_dico_hdv[ordre_achat.produit_voulu][0].remove(ordre)
                self.transaction_ordre_vente(
                    ordre.vendeur, ordre_achat.acheteur, ordre_achat, ordre
                )
                return True
        if ordre_achat.acheteur.bourse > ordre_achat.prix * 0.02:
            ordre_achat.acheteur.bourse -= ordre_achat.prix * 0.02
            self.ordres_dico_hdv[ordre_achat.produit_voulu][1](ordre_achat)
        return False


    def recherche_ordre_achat(self, ordre_vente):
        for ordre in self.ordres_dico_hdv[ordre_vente.produit_vendu][1]:
            if (
                ordre.quantité == ordre_vente.quantité
                and ordre.prix >= ordre_vente.prix
            ):
                self.ordres_dico_hdv[ordre_vente.produit_vendu][1](ordre)
                self.transaction_ordre_achat(
                    ordre_vente.vendeur, ordre.acheteur, ordre_vente, ordre
                )
                return True
        if ordre_vente.vendeur.bourse > ordre_vente.prix * 0.02:
            ordre_vente.vendeur.bourse -= ordre_vente.prix * 0.02
            self.ordres_dico_hdv[ordre_vente.produit_vendu][0](ordre_vente)
        return False
