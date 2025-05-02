class Acheteur:
    def __init__(self, prix_max, bourse, produit_voulu):
        self.prix = prix_max
        self.bourse = bourse
        self.besoins = produit_voulu


class Vendeur:
    def __init__(self, stock, bourse, prix_min):
        self.stock = stock
        self.prix = prix_min
        self.brs_avant_tick = bourse
        self.brs_apres_tick = bourse


class Ordre_achat:
    def __init__(self, produit_voulu, prix_max, acheteur):
        self.produit = produit_voulu
        self.prix = prix_max
        self.acheteur = acheteur


class Ordre_vente:
    def __init__(self, produit_dispo, prix_min, vendeur):
        self.produit = produit_dispo
        self.prix = prix_min
        self.vendeur = vendeur


class HDV:
    def __init__(self):
        self.ordres_achat = []
        self.ordres_vente = []

    def transaction_ordre_achat(
        self, vendeur, acheteur, ordre_achat, ordre_vente
    ):  # acheteur paye prix min
        vendeur.stock -= ordre_vente.produit
        vendeur.brs_apres_tick += ordre_vente.produit * ordre_achat.prix
        acheteur.bourse -= ordre_vente.produit * ordre_achat.prix

    def transaction_ordre_vente(
        self, vendeur, acheteur, ordre_vente, ordre_achat
    ):  # vendeur fait payer prix max
        vendeur.stock -= ordre_vente.produit
        vendeur.brs_apres_tick += ordre_vente.produit * ordre_achat.prix
        acheteur.bourse -= ordre_vente.produit * ordre_achat.prix

    def recherche_ordre_vente(self, ordre_achat):
        for ordre in self.ordres_vente:
            if (
                ordre.produit == ordre_achat.produit
                and ordre.prix <= ordre_achat.prix
            ):
                self.ordres_vente.remove(ordre)
                self.transaction_ordre_vente(
                    ordre.vendeur, ordre_achat.acheteur, ordre_achat, ordre
                )
                return True
        self.ordres_achat.append(ordre_achat)
        return False

    def recherche_ordre_achat(self, ordre_vente):
        for ordre in self.ordres_vente:
            if (
                ordre.produit_voulu == ordre_vente.produit_dispo
                and ordre.prix_max >= ordre_vente.prix_min
            ):
                self.ordres_achat.remove(ordre)
                self.transaction_ordre_achat(
                    ordre_vente.vendeur, ordre.acheteur, ordre_vente, ordre
                )
                return True
        self.ordres_vente.append(ordre_vente)
        return False
