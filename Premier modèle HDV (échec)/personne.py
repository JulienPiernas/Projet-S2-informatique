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
            self.pl *= (1 + self.besoin / 100)

    def avant_tick(self):
        self.changer_besoins()



class Paysan(Personne):

    def __init__(self, besoin, brs, pl, prix_blé, production_max, stock=0):
        super().__init__(besoin, brs, pl)
        self.stock = stock
        self.prix_vente_blé = prix_blé
        self.production_max = production_max

    def production(self):
        self.stock += randint(0, self.production_max)

    def __str__(self):
        return f'Cet individu est un Paysan et il possède {self.brs} kamas, besoin de {self.besoin}. Il vend son blé à {self.prix_vente_blé}'

    def vendre_au_marche(self, marche):
        marche["ble"]["stock"] += self.stock
        marche["ble"]["revenu"] -= self.stock * self.prix_vente_blé
        self.brs += self.stock * self.prix_vente_blé
        self.stock = 0

    def change_prix_vente(self):
        if self.brs_avant_tick < self.brs:
            self.prix_vente_blé *= 1 + (randint(1, 20) / 100)
        elif self.brs_avant_tick > self.brs:
            self.prix_vente_blé *= 1 - (randint(1, 20) / 100)


class Fermier(Personne):

    def __init__(self, besoin, brs, pl, prix_oeuf, production_max, stock=0):
        super().__init__(besoin, brs, pl)
        self.stock = stock
        self.prix_vente_oeuf = prix_oeuf
        self.production_max = production_max

    def production(self):
        self.stock += randint(0, self.production_max)

    def __str__(self):
        return f'Cet individu est un Fermier et il possède {self.brs} kamas, besoin de {self.besoin}. Il vend ses oeufs à {self.prix_vente_oeuf}'

    def vendre_au_marche(self, marche):
        marche["oeuf"]["stock"] += self.stock
        marche["oeuf"]["revenu"] -= self.stock * self.prix_vente_oeuf
        self.brs += self.stock * self.prix_vente_oeuf
        self.stock = 0

    def change_prix_vente(self):
        if self.brs_avant_tick < self.brs:
            self.prix_vente_oeuf *= 1 + (randint(1, 20) / 100)
        elif self.brs_avant_tick > self.brs:
            self.prix_vente_oeuf *= 1 - (randint(1, 20) / 100)


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


    def production(self):
        while (self.stock_blé >= 2) and (self.stock_oeuf >= 1):
            self.stock_blé -= 2
            self.stock_oeuf -= 1
            self.stock += 1
            print("\n COOK \n")

    def change_prix_limite(self):
        différence_stoechio = 2 * self.stock_oeuf - self.stock_blé
        self.pl[0] = self.pl[0] - différence_stoechio * 0.05  # 0 = oeuf
        self.pl[1] = self.pl[1] + différence_stoechio * 0.05  # 1 = blé
        if self.besoin[0] > 9:
            self.pl[0] *= 1.05
        elif self.besoin[0] <= 2:
            self.pl[0] *= 0.95
        if self.besoin[1] > 9:
            self.pl[1] *= 1.05
        elif self.besoin[1] <= 2:
            self.pl[1] *= 0.95

    def change_besoins(self):
        self.besoin[0] += randint(1, 10)
        self.besoin[1] += randint(1, 20)

    def __str__(self):
        return f'Cet individu est un Patissier et il possède {self.brs} kamas, besoin de {self.besoin}, il achete du blé à {self.pl[1]} et il achete des oeufs à {self.pl[0]}'

    def change_prix_vente(self):
        if self.brs_avant_tick < self.brs:
            self.prix_vente_gateau *= 1 + (randint(1, 20) / 100)
        elif self.brs_avant_tick > self.brs:
            self.prix_vente_gateau *= 1 - (randint(1, 20) / 100)
