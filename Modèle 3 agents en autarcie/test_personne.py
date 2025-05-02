from personne import Paysan, Fermier, Patissier


def test_creation_paysan():
    paysan = Paysan(besoin=5, brs=500, pl=10, prix_blé=2, production_max=20)
    assert paysan.besoin == 5
    assert paysan.brs == 500
    assert paysan.pl == 10
    assert paysan.prix_vente_blé == 2
    assert paysan.production_max == 20
    assert paysan.stock == 0


def test_creation_fermier():
    fermier = Fermier(besoin=5, brs=500, pl=12, prix_oeuf=5, production_max=10)
    assert fermier.besoin == 5
    assert fermier.brs == 500
    assert fermier.pl == 12
    assert fermier.prix_vente_oeuf == 5
    assert fermier.production_max == 10
    assert fermier.stock == 0


def test_creation_patissier():
    patissier = Patissier(besoin=5, pl=[15, 5], brs=500)
    assert patissier.besoin == [10, 5]  # 2 * besoin pour le blé, besoin pour les oeufs
    assert patissier.brs == 500
    assert patissier.pl == [15, 5]
    assert patissier.stock == 0
    assert patissier.stock_blé == 0
    assert patissier.stock_oeuf == 0
    assert patissier.prix_vente_gateau == 25  # 2 * pl[1] + pl[0]


def test_production_patissier():
    patissier = Patissier(besoin=5, pl=[15, 5], brs=500)
    patissier.stock_blé = 4
    patissier.stock_oeuf = 2
    patissier.production()
    assert patissier.stock == 2
    assert patissier.stock_blé == 0
    assert patissier.stock_oeuf == 0


def test_vente_au_marche():
    paysan = Paysan(besoin=5, brs=500, pl=10, prix_blé=2, production_max=20)
    paysan.stock = 10
    marche = {"ble": {"stock": 0, "vendeurs": []}}
    paysan.vendre_au_marche(marche)
    assert paysan.stock == 0
    assert marche["ble"]["stock"] == 10
    assert len(marche["ble"]["vendeurs"]) == 1
    assert marche["ble"]["vendeurs"][0][1] == 2  # prix de vente
    assert marche["ble"]["vendeurs"][0][2] == 10  # quantité


def test_achat_gateau():
    patissier = Patissier(besoin=5, pl=[15, 5], brs=500)
    paysan = Paysan(besoin=5, brs=100, pl=30, prix_blé=2, production_max=20)
    patissier.stock = 2
    patissier.prix_vente_gateau = 25

    paysan.acheter_gateau(patissier)
    assert paysan.stock_achat == 1
    assert paysan.brs == 75  # 100 - 25
    assert patissier.brs == 525  # 500 + 25
    assert patissier.stock == 1


def test_consommation():
    paysan = Paysan(besoin=3, brs=500, pl=10, prix_blé=2, production_max=20)
    paysan.stock_achat = 2
    paysan.consommer()
    assert paysan.besoin == 1
    assert paysan.stock_achat == 0


def test_effectuer_transactions_patissier():
    patissier = Patissier(besoin=5, pl=[15, 5], brs=100)
    fermier = Fermier(besoin=5, brs=500, pl=12, prix_oeuf=10, production_max=10)
    marche = {"oeuf": {"stock": 0, "vendeurs": [(fermier, 10, 5)]},
              "ble": {"stock": 0, "vendeurs": []}}
    
    patissier.effectuer_transactions(marche)
    assert patissier.stock_oeuf > 0
    assert patissier.brs < 100  # vérifie que de l'argent a été dépensé


def test_change_prix_vente():
    patissier = Patissier(besoin=5, pl=[15, 5], brs=500)
    prix_initial = patissier.prix_vente_gateau
    patissier.brs += 100  # simule un gain
    patissier.change_prix_vente()
    assert patissier.prix_vente_gateau > prix_initial