class Acheteur:
    def __init__(self, prix_max, brs, quantité_voulue, besoin, stock_achat=0):
        self.prix = prix_max
        self.besoin = besoin
        self.brs = brs
        self.quantité = quantité_voulue
        self.stock_achat = stock_achat

    def __str__(self):
        return f'{type(self)}'


class Vendeur:
    def __init__(self, stock, brs, prix_min, quantité_vente):
        self.stock = stock
        self.prix = prix_min
        self.brs_avant_tick = brs
        self.brs = brs
        self.quantité = quantité_vente

    def __str__(self):
        return f'{type(self)}'


class Ordre_achat:
    def __init__(self, prix_max, acheteur: Acheteur, produit_voulu, quantité_voulue):
        self.prix = prix_max
        self.acheteur = acheteur
        self.quantité = quantité_voulue
        self.produit_voulu = produit_voulu

    def __str__(self):
        return f"Ordre d'achat de {self.quantité} {self.produit_voulu} pour {self.prix}"


class Ordre_vente:
    def __init__(self, prix_min, vendeur: Vendeur, produit_vendu, quantité_dispo):
        self.prix = prix_min
        self.vendeur = vendeur
        self.quantité = quantité_dispo
        self.produit_vendu = produit_vendu

    def __str__(self):
        return f"Ordre de vente de {self.quantité} {self.produit_vendu} pour {self.prix}"


class HDV:
    def __init__(self, liste_produits):
        self.dico_hdv = {}
        for e in liste_produits:
            self.dico_hdv[e] = [[], []]

        # On associe à chaque produit une liste de 2 listes qui sont la liste des ordres de ventes t[0] et la liste des ordres d'achat t[1]

    def transaction_ordre_achat(
        self, vendeur: Vendeur, acheteur: Acheteur, ordre_achat: Ordre_achat, ordre_vente: Ordre_vente
    ):  # acheteur paye prix min
        vendeur.stock -= ordre_vente.quantité
        acheteur.stock_achat += ordre_vente.quantité
        vendeur.brs += ordre_vente.quantité * ordre_achat.prix
        acheteur.brs -= ordre_vente.quantité * ordre_achat.prix
        acheteur.besoin -= ordre_vente.quantité

    def transaction_ordre_vente(
        self, vendeur: Vendeur, acheteur: Acheteur, ordre_vente: Ordre_vente, ordre_achat: Ordre_achat
    ):  # vendeur fait payer prix max
        vendeur.stock -= ordre_vente.quantité
        acheteur.stock_achat += ordre_vente.quantité
        vendeur.brs += ordre_vente.quantité * ordre_achat.prix
        acheteur.brs -= ordre_vente.quantité * ordre_achat.prix
        acheteur.besoin -= ordre_vente.quantité

    def recherche_ordre_vente(self, ordre_achat: Ordre_achat):
        if ordre_achat.quantité <= 0:
            return False
        for ordre in self.dico_hdv[ordre_achat.produit_voulu][0]:
            if ordre.quantité >= ordre_achat.quantité and ordre.prix <= ordre_achat.prix:
                self.dico_hdv[ordre_achat.produit_voulu][0].remove(ordre)
                self.transaction_ordre_vente(
                    ordre.vendeur, ordre_achat.acheteur, ordre_achat, ordre
                )
                print(f"TRANSACTION DE {ordre}. VENDEUR : {ordre.vendeur}, ACHETEUR : {ordre_achat.acheteur}")
                return True
        if ordre_achat.acheteur.brs > ordre_achat.prix * 0.02:
            ordre_achat.acheteur.brs -= ordre_achat.prix * 0.02
            self.dico_hdv[ordre_achat.produit_voulu][1].append(ordre_achat)
        return False

    def recherche_ordre_achat(self, ordre_vente: Ordre_vente):
        if ordre_vente.quantité <= 0:
            return False
        for ordre in self.dico_hdv[ordre_vente.produit_vendu][1]:
            if (
                (ordre.quantité <= ordre_vente.quantité)
                and (ordre.prix >= ordre_vente.prix)
            ):
                self.dico_hdv[ordre_vente.produit_vendu][1].remove(ordre)
                self.transaction_ordre_achat(
                    ordre_vente.vendeur, ordre.acheteur, ordre_vente, ordre
                )
                print(f"TRANSACTION DE {ordre_vente}. VENDEUR : {ordre_vente.vendeur}, ACHETEUR : {ordre.acheteur}")
                return True
        if ordre_vente.vendeur.brs > ordre_vente.prix * 0.02:
            ordre_vente.vendeur.stock -= ordre_vente.quantité
            ordre_vente.vendeur.brs -= ordre_vente.prix * 0.02
            self.dico_hdv[ordre_vente.produit_vendu][0].append(ordre_vente)
        return False

    def __str__(self):
        return f"L'hotêl de vente a pour ordres {self.dico_hdv}"
