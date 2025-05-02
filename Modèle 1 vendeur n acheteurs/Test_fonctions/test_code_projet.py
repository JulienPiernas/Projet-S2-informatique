import sys
import os
from random import seed

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from code_projet import Acheteur, Vendeur

# Configuration des tests
seed("TEST")  # Pour avoir des résultats reproductibles

def test_acheteur():
    # Test initialisation
    acheteur = Acheteur(1000, 5, 10)
    assert acheteur.sal == 1000
    assert acheteur.pl == 5
    assert acheteur.brs == 1000
    assert acheteur.besoins == 10
    assert acheteur.humeur == "Content"
    assert acheteur.acheté_en_dernier == 0

    # Test achete
    vendeur = Vendeur(100, 2, 5000)
    acheteur.achete(2, vendeur)
    assert acheteur.brs == 980  # 1000 - (2 * 10)
    assert acheteur.humeur == "Content : besoins satisfaits"
    assert vendeur.get_stock() == 90

    # Test achete_oui_non
    acheteur = Acheteur(1000, 5, 10)
    vendeur = Vendeur(100, 2, 5000)
    acheteur.achete_oui_non(6, vendeur)  # Prix > prix limite
    assert acheteur.humeur == "Pas content : prix trop élevé"

    # Test avant_tick
    ancien_brs = acheteur.brs
    acheteur.avant_tick()
    assert acheteur.brs == ancien_brs + acheteur.sal

def test_vendeur():
    # Test initialisation
    vendeur = Vendeur(1000, 2, 5000)
    assert vendeur.stock == 1000
    assert vendeur.cout_prod == 2
    assert vendeur.brs_avant_tick == 5000
    assert vendeur.prix_courant == 2
    assert len(vendeur.prix_archive) == 0
    assert len(vendeur.recettes) == 0

    # Test get_stock
    assert vendeur.get_stock() == 1000

    # Test prendre_dans_stock
    vendeur.prendre_dans_stock(100)
    assert vendeur.get_stock() == 900
    assert vendeur.brs_apres_tick == 5200  # 5000 + (100 * 2)

    # Test variation_prix
    ancien_prix = vendeur.prix_courant
    vendeur.variation_prix()
    assert vendeur.prix_courant != ancien_prix

    # Test propose_prix
    prix = vendeur.propose_prix()
    assert isinstance(prix, float)
    assert prix > 0

    # Test archive
    vendeur.archive()
    assert len(vendeur.prix_archive) == 1
    assert len(vendeur.recettes) == 1
