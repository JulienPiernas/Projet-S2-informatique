from random import shuffle
import hdv
from personne import Paysan, Patissier, Fermier, Personne

def simulation_gateau(liste_personnes : [Personne], hotel : hdv.HDV):
    shuffle(liste_personnes)

    # FAIRE LES ACTIONS DU TICK ET LES DEFINIR
    # Les gens arrivent à l'HDV et font leurs ventes
    # Puis ils font leurs achats

    for individu in liste_personnes:
        if type(individu) == Paysan:
            client = hdv.Acheteur(individu.pl, individu.brs, individu.besoins)
            vendeur = hdv.Vendeur(individu.stock_vente, individu.brs, individu.prix_vente_blé, individu.stock_vente)
            ordre_vente = hdv.Ordre_vente(vendeur.prix, vendeur, "Blé", individu.stock_vente)
            ordre_achat = hdv.Ordre_achat(client.prix, client, "Gâteau", client.quantité)
            hotel.recherche_ordre_vente(ordre_achat)
            hotel.recherche_ordre_achat(ordre_vente)

        elif type(individu) == Fermier:
            client = hdv.Acheteur(individu.pl, individu.brs, individu.besoins)
            vendeur = hdv.Vendeur(individu.stock_vente, individu.brs, individu.prix_vente_oeuf, individu.stock_vente)
            ordre_vente = hdv.Ordre_vente(vendeur.prix, vendeur, "Oeuf", individu.stock_vente)
            ordre_achat = hdv.Ordre_achat(client.prix, client, "Gâteau", client.quantité)
            hotel.recherche_ordre_vente(ordre_achat)
            hotel.recherche_ordre_achat(ordre_vente)

        elif type(individu) == Patissier:
            client1 = hdv.Acheteur(individu.pl[0], individu.brs, individu.besoins)
            client2 = hdv.Acheteur(individu.pl[1], individu.brs, individu.besoins * 2)
            vendeur = hdv.Vendeur(individu.stock_vente, individu.brs, individu.prix_vente_gateau, individu.stock_vente)
            ordre_vente = hdv.Ordre_vente(individu.prix_vente_gateau, vendeur, "Gâteau", individu.stock_vente)
            ordre_achat_2 = hdv.Ordre_achat(client2.prix, client2, "Blé", client2.quantité)
            ordre_achat_1 = hdv.Ordre_achat(client1.prix, client1, "Oeuf", client1.quantité)
            hotel.recherche_ordre_vente(ordre_achat_2)
            hotel.recherche_ordre_vente(ordre_achat_1)
            hotel.recherche_ordre_achat(ordre_vente)

    # NE PAS OUBLIER DE RECHANGER LES ATTRIBUTS DES AGENTS ECONOMIQUE
    # Maintenant il faut afficher des données significatives de l'évolution du prix de vente de chaque produit (moyenne, prix min, prix max)
    # Il faut également donner d'autres données comme l'argent total dans l'économie ou des informations sur les agents économiques

        print(individu)


    continuer = input("Continuer ? : (Y/N) : ")
    if continuer == "Y":
        simulation_gateau(liste_personnes, hotel)