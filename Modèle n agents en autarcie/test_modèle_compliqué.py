from code_modèle_compliqué import Patissier, Paysan, Agriculteur, HDV
from pytest import approx

patissier1 = Patissier("patissier1", 1000, 3)
patissier2 = Patissier("patissier2", 1000, 4)
agriculteur1 = Agriculteur("agriculteur1", 20, 500, 2, 5)
agriculteur2 = Agriculteur("agriculteur2", 20, 500, 3, 6)
paysan1 = Paysan("paysan1", 20, 500, 3, 5)
paysan2 = Paysan("paysan2", 20, 500, 4, 6)

petit_monde = [patissier1, patissier2, agriculteur1, agriculteur2, paysan1, paysan2]

hdv = HDV(petit_monde)

"""
Début de Journée

"""


def test_début_journée_pay_agr1():
    agriculteur1.début_de_journée()
    assert agriculteur1.besoin_gateau == 2
    assert agriculteur1.n_stress == 0
    assert agriculteur1.moy_gateau == 1
    assert agriculteur1.prix_acheté == []
    assert agriculteur1.stock == 25


def test_début_journée_pay_agr2():
    paysan1.prix_acheté = [6, 11, 4]
    paysan1.besoin_gateau = 17
    paysan1.début_de_journée()
    assert paysan1.besoin_gateau == 20
    assert paysan1.n_stress == 17
    assert paysan1.moy_gateau == approx(7)
    assert paysan1.prix_acheté == []
    assert paysan1.stock == 25


def test_début_journée_pat1():
    patissier1.début_de_journée()
    assert patissier1.besoin_gateau == 3
    assert patissier1.n_stress == 0
    assert patissier1.moy_blé == 1
    assert patissier1.moy_oeuf == 1
    assert patissier1.prix_blé_acheté == []
    assert patissier1.prix_oeuf_acheté == []


def test_début_journée_pat2():
    patissier1.prix_blé_acheté = [6, 11, 4]
    patissier1.prix_oeuf_acheté = [4, 6]
    patissier1.besoin_gateau = 17
    patissier1.début_de_journée()
    assert patissier1.besoin_gateau == 20
    assert patissier1.n_stress == 17
    assert patissier1.moy_blé == approx(7)
    assert patissier1.moy_oeuf == approx(5)
    assert patissier1.prix_blé_acheté == []
    assert patissier1.prix_oeuf_acheté == []


"""
Produire (Patissier)

"""


def test_produire_pat():
    patissier2.besoin_gateau = 2
    patissier2.stock_blé = 5
    patissier2.stock_oeuf = 9
    patissier2.produire()
    assert patissier2.besoin_gateau == 0
    assert patissier2.stock == 2
    assert patissier2.stock_blé == 1
    assert patissier2.stock_oeuf == 1


"""
Propose prix

"""


def test_propose_prix_agr_pay1():
    prop = agriculteur1.propose_prix()
    assert prop.prix == approx(0.08)
    assert prop.vendeur == agriculteur1


def test_propose_prix_agr_pay2():
    prop = paysan1.propose_prix()
    assert prop.vendeur == paysan1
    assert prop.prix == approx(10.36)


def test_propose_prix_pat1():
    patissier1.stock = 10
    prop = patissier1.propose_prix()
    assert prop.vendeur == patissier1
    assert prop.prix == approx(32.3)


"""
HDV

"""


def test_création_hdv():
    assert len(hdv.liste_agriculteur) == 2
    assert len(hdv.liste_patissier) == 2
    assert len(hdv.liste_paysan) == 2


def test_déposer_ordre_achat_se_passe_bien():
    patissier1.moy_blé = 3
    patissier1.moy_oeuf = 2
    patissier1.n_stress = 0
    patissier1.stock = 10

    patissier2.moy_blé = 4
    patissier2.moy_oeuf = 3
    patissier2.n_stress = 2
    patissier2.stock = 9

    agriculteur1.bourse = 10000
    agriculteur1.besoin_gateau = 5

    agriculteur1.achète(hdv)

    assert patissier1.stock == 5
    assert patissier2.stock == 9
    assert agriculteur1.besoin_gateau == 0


def test_déposer_ordre_achat_pas_d_argent():
    patissier1.moy_blé = 3
    patissier1.moy_oeuf = 2
    patissier1.n_stress = 0
    patissier1.stock = 10

    patissier2.moy_blé = 4
    patissier2.moy_oeuf = 3
    patissier2.n_stress = 2
    patissier2.stock = 9

    agriculteur1.bourse = 5
    agriculteur1.besoin_gateau = 5

    agriculteur1.achète(hdv)

    assert patissier1.stock == 7
    assert patissier2.stock == 9
    assert agriculteur1.besoin_gateau == 2


def test_déposer_ordre_achat_plus_de_stock():
    patissier1.moy_blé = 3
    patissier1.moy_oeuf = 2
    patissier1.n_stress = 0
    patissier1.stock = 3

    patissier2.moy_blé = 4
    patissier2.moy_oeuf = 3
    patissier2.n_stress = 2
    patissier2.stock = 0

    agriculteur1.bourse = 10000
    agriculteur1.besoin_gateau = 5

    agriculteur1.achète(hdv)

    assert patissier1.stock == 0
    assert patissier2.stock == 0
    assert agriculteur1.besoin_gateau == 2
