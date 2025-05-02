from random import seed
from code_modèle_compliqué import (
    Patissier,
    Agriculteur,
    Paysan,
    simulation_compliquée,
)

x = 'MPCI'
seed(x)

patissier1 = Patissier("patissier1", 10000, 3)
patissier2 = Patissier("patissier2", 10000, 4)
agriculteur1 = Agriculteur("agriculteur1", 20, 500, 2, 5)
agriculteur2 = Agriculteur("agriculteur2", 20, 500, 3, 6)
paysan1 = Paysan("paysan1", 20, 500, 3, 5)
paysan2 = Paysan("paysan2", 20, 500, 4, 6)
patissier3 = Patissier("patissier3", 1000, 2)
patissier4 = Patissier("patissier4", 1000, 3)
agriculteur3 = Agriculteur("agriculteur3", 20, 500, 2, 2)
agriculteur4 = Agriculteur("agriculteur4", 20, 500, 3, 1)
paysan3 = Paysan("paysan3", 20, 500, 3, 2)
paysan4 = Paysan("paysan4", 20, 500, 4, 1)

petit_monde = [patissier1, patissier2, patissier3, patissier4, agriculteur1, agriculteur2, agriculteur3, agriculteur4, paysan1, paysan2, paysan3, paysan4]


simulation_compliquée(100, petit_monde)
