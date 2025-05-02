import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from ordres_HDV import Acheteur, Vendeur, Ordre_achat, Ordre_vente, HDV

def test_transaction_reussie1():
    hdv = HDV()
    vendeur = Vendeur(stock=10, bourse=100, prix_min=5)
    acheteur = Acheteur(prix_max=6, bourse=200, produit_voulu=10)
    ordre_vente = Ordre_vente(produit_dispo=10, prix_min=5, vendeur=vendeur)
    ordre_achat = Ordre_achat(produit_voulu=10, prix_max=6, acheteur=acheteur)
    
    hdv.ordres_vente.append(ordre_vente)
    resultat = hdv.recherche_ordre_vente(ordre_achat)
    
    assert resultat is True
    assert vendeur.stock == 0               # 10 - 10 
    assert vendeur.brs_apres_tick == 150    # 100 + (10 * 5) 
    assert acheteur.bourse == 150           # 200 - (10 * 5)
    assert len(hdv.ordres_vente) == 0       # ordre vente retiré



