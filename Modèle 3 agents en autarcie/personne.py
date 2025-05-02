from random import randint


class Personne:
    def __init__(self, besoin, brs, pl):
        self.brs = brs
        self.brs_avant_tick = brs
        self.besoin = besoin
        self.pl = pl
        self.stock_achat = 0

    def change_besoins(self):
        if self.besoin > 6:
            self.besoin += randint(1, 2)
        else:
            self.besoin += randint(1, 3)

    def change_prix_limite(self):
        if self.pl > self.brs:
            self.pl = self.brs
        if self.besoin > 0:
            self.pl *= 1 + self.besoin / 100


class Paysan(Personne):
    def __init__(self, besoin, brs, pl, prix_blé, production_max, stock=0):
        super().__init__(besoin, brs, pl)
        self.stock = stock
        self.prix_vente_blé = prix_blé
        self.production_max = production_max

    def production(self):
        self.stock += randint(0, int(self.production_max))

    def vendre_au_marche(self, marche):
        marche["ble"]["stock"] += self.stock
        marche["ble"]["vendeurs"].append((self, self.prix_vente_blé, self.stock))
        self.stock = 0

    def acheter_gateau(self, patissier):
        if (
            patissier.stock > 0
            and patissier.prix_vente_gateau <= self.pl
            and self.brs >= patissier.prix_vente_gateau
        ):
            self.stock_achat += 1
            self.brs -= patissier.prix_vente_gateau
            patissier.brs += patissier.prix_vente_gateau
            patissier.stock -= 1

    def change_besoins(self):
        self.besoin += randint(1, 3)

    def change_prix_vente(self):
        if self.brs_avant_tick < self.brs:
            self.prix_vente_blé *= 1 + (randint(5, 20) / 100)
        elif self.brs_avant_tick > self.brs:
            self.prix_vente_blé *= 1 - (randint(5, 20) / 100)

    def __str__(self):
        return f"Paysan avec {self.brs} kamas, vend blé à {self.prix_vente_blé}"

    def consommer(self):
        while self.stock_achat > 0 and self.besoin > 0:
            self.besoin -= 1
            self.stock_achat -= 1


class Fermier(Personne):
    def __init__(self, besoin, brs, pl, prix_oeuf, production_max, stock=0):
        super().__init__(besoin, brs, pl)
        self.stock = stock
        self.prix_vente_oeuf = prix_oeuf
        self.production_max = production_max

    def production(self):
        self.stock += randint(0, self.production_max)

    def vendre_au_marche(self, marche):
        marche["oeuf"]["stock"] += self.stock
        marche["oeuf"]["vendeurs"].append((self, self.prix_vente_oeuf, self.stock))
        self.stock = 0

    def acheter_gateau(self, patissier):
        if (
            patissier.stock > 0
            and patissier.prix_vente_gateau <= self.pl
            and self.brs >= patissier.prix_vente_gateau
        ):
            self.stock_achat += 1
            self.brs -= patissier.prix_vente_gateau
            patissier.brs += patissier.prix_vente_gateau
            patissier.stock -= 1

    def change_besoins(self):
        self.besoin += randint(1, 2)

    def change_prix_vente(self):
        if self.brs_avant_tick < self.brs:
            self.prix_vente_oeuf *= 1 + (randint(5, 20) / 100)
        elif self.brs_avant_tick > self.brs:
            self.prix_vente_oeuf *= 1 - (randint(5, 20) / 100)

    def __str__(self):
        return f"Fermier avec {self.brs} kamas, vend œufs à {self.prix_vente_oeuf}"

    def consommer(self):
        while self.stock_achat > 0 and self.besoin > 0:
            self.besoin -= 1
            self.stock_achat -= 1


class Patissier(Personne):

    def __init__(
        self,
        besoin,
        pl,
        brs,
        stock_blé=0,
        stock_oeuf=0,
        stock=0,
    ):
        super().__init__(besoin, brs, pl)
        self.stock_oeuf = stock_oeuf
        self.stock_blé = stock_blé
        self.stock = stock
        self.pl = pl
        self.besoin = [2 * besoin, besoin]
        self.prix_vente_gateau = 2 * pl[1] + pl[0]
        self.besoin_gateaux = 0
        self.acheter_oeuf_first = True

    def production(self):
        """Produit des gâteaux si les ressources sont suffisantes et s'il reste de l'argent pour produire plus."""
        while self.stock_blé >= 2 and self.stock_oeuf >= 1 and self.brs > 0:
            self.stock_blé -= 2
            self.stock_oeuf -= 1
            self.stock += 1  # Ajoute un gâteau au stock
            print(
                f"Le pâtissier a produit un gâteau. Nouveau stock : {self.stock} gâteaux."
            )

    def change_prix_limite(self):
        # Le pâtissier a deux prix limites : un pour le blé et un pour les œufs
        for i in range(2):
            if self.pl[i] > self.brs:
                self.pl[i] = self.brs

            # Augmentation des prix limites en fonction des besoins
            if self.besoin[i] > 10:  # Besoins critiques en ingrédients
                self.pl[i] *= 1.2
            elif self.besoin[i] > 5:  # Besoins élevés
                self.pl[i] *= 1.1
            elif self.besoin[i] <= 2:  # Peu de besoins
                self.pl[i] *= 0.95

    def change_besoins_achat(self):
        self.besoin[0] += 1
        self.besoin[1] += 2

    def change_besoins(self):
        self.besoin_gateaux += 1

    def __str__(self):
        return f"Cet individu est un Patissier et il possède {self.brs} kamas, besoin de {self.besoin}, il achete du blé à {self.pl[1]} et il achete des oeufs à {self.pl[0]}"

    def change_prix_vente(self):
        """Ajuste le prix de vente du gâteau en fonction des gains ou pertes"""
        print(f"\n-- État avant modification --")
        print(f"Richesse initiale : {self.brs_avant_tick}")
        print(f"Prix de vente initial : {self.prix_vente_gateau}")

        # Si le pâtissier a gagné de l'argent
        if self.brs > self.brs_avant_tick:
            variation = randint(5, 10) / 100
            self.prix_vente_gateau *= 1 + variation
            print(
                f"Le pâtissier a gagné de l'argent. Augmentation du prix de {round(variation*100, 2)}%. Nouveau prix : {round(self.prix_vente_gateau, 2)} kamas."
            )

        # Si le pâtissier a perdu de l'argent
        elif self.brs < self.brs_avant_tick:
            variation = randint(5, 10) / 100
            self.prix_vente_gateau *= 1 - variation
            print(
                f"Le pâtissier a perdu de l'argent. Diminution du prix de {round(variation*100, 2)}%. Nouveau prix : {round(self.prix_vente_gateau, 2)} kamas."
            )

        # Si aucune transaction, baisse pour attirer plus de clients
        elif self.stock > 0:
            self.prix_vente_gateau *= 0.95  # Réduction de 5%
            print(
                f"Le pâtissier n'a pas vendu de gâteaux. Baisse du prix à {round(self.prix_vente_gateau, 2)} kamas pour attirer plus de clients."
            )


        print(f"\n-- État après modification --")
        print(f"Prix final : {round(self.prix_vente_gateau, 2)}")

    def consommer(self):
        if self.stock > 0 and self.besoin_gateaux > 0:
            self.besoin_gateaux -= 1
            self.stock -= 1

    def effectuer_transactions(self, marche):
        ingredients = [("oeuf", 0), ("ble", 1)] if self.acheter_oeuf_first else [("ble", 1), ("oeuf", 0)]
        self.acheter_oeuf_first = not self.acheter_oeuf_first  # Inverse pour la prochaine fois

        for ingredient, pl_index in ingredients:
            nouveaux_vendeurs = []
            for vendeur, prix, quantite in marche[ingredient]["vendeurs"]:
                if prix <= self.pl[pl_index] and self.brs >= prix:
                    achete = min(quantite, int(self.brs // prix))
                    vendeur.brs += achete * prix
                    self.brs -= achete * prix
                    if ingredient == "oeuf":
                        self.stock_oeuf += achete
                    else:
                        self.stock_blé += achete
                    quantite -= achete
                if quantite > 0:
                    nouveaux_vendeurs.append((vendeur, prix, quantite))
            marche[ingredient]["vendeurs"] = nouveaux_vendeurs
