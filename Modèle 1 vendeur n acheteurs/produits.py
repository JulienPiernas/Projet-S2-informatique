# idées de classes pour les produits

class Produits:
    def __init__(self, nom: str, prix_base: float, quantite: int):
        self.nom = nom
        self.prix_base = prix_base
        self.quantite = quantite  # Stock total disponible, pour une personne aussi bien que dans l'HDV

    def ajouter_stock(self, quantite):
        if quantite <0:
            raise ValueError("Il faut ajouter un nombre positif de produits!")
        self.quantite += quantite

    def retirer_stock(self, quantite):
        if quantite > self.quantite:
            raise ValueError("Stock insuffisant !")
        if quantite < 0:
            raise ValueError("Il faut retirer un nombre positif de produits!")
        self.quantite -= quantite

    def __str__(self):
        return f"{self.nom} - {self.prix_base}€ ({self.quantite} en stock)"


class Oeufs(Produits):
    def __init__(self, quantite=100, prix=1.0):
        super().__init__("Oeufs", prix, quantite)


class Ble(Produits):
    def __init__(self, quantite=100, prix=1.0):
        super().__init__("Blé", prix, quantite)


"""
neuf = Oeufs()
print(neuf)
"""
