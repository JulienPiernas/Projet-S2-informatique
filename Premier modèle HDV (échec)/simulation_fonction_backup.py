from random import shuffle
import hdv
from personne import Paysan, Patissier, Fermier, Personne


def simulation_gateau(liste_personnes: [Personne], hotel: hdv.HDV):
    shuffle(liste_personnes)

    # FAIRE LES ACTIONS DU TICK ET LES DEFINIR
    # Les gens arrivent à l'HDV et font leurs ventes
    # Puis ils font leurs achats
    somme = 0
    for individu in liste_personnes:
        individu.brs = round(individu.brs, 1)
        if type(individu) == Paysan:
            individu.pl = round(individu.pl, 1)
            individu.prix_vente_blé = round(individu.prix_vente_blé, 1)

            acheteur = hdv.Acheteur(individu.pl, individu.brs, individu.besoin, individu.besoin)
            vendeur = hdv.Vendeur(individu.stock, individu.brs, individu.prix_vente_blé, individu.stock)
            ordre_vente = hdv.Ordre_vente(vendeur.prix, vendeur, "Blé", vendeur.stock)
            ordre_achat = hdv.Ordre_achat(acheteur.prix, acheteur, "Gâteau", acheteur.besoin)

            if hotel.recherche_ordre_vente(ordre_achat):
                print(f"{individu} a acheté {ordre_achat}")

            if hotel.recherche_ordre_achat(ordre_vente):
                print(f"{individu} a vendu {ordre_vente}")

            individu.stock = vendeur.stock
            individu.brs = (acheteur.brs + vendeur.brs) / 2
            individu.besoin = acheteur.besoin

            individu.production()
            individu.change_prix_limite()
            individu.change_besoins()
            individu.change_prix_vente()

        elif type(individu) == Fermier:
            individu.pl = round(individu.pl, 1)
            individu.prix_vente_oeuf = round(individu.prix_vente_oeuf, 1)

            acheteur = hdv.Acheteur(individu.pl, individu.brs, individu.besoin, individu.besoin)
            vendeur = hdv.Vendeur(individu.stock, individu.brs, individu.prix_vente_oeuf, individu.stock)
            ordre_vente = hdv.Ordre_vente(vendeur.prix, vendeur, "Oeuf", vendeur.stock)
            ordre_achat = hdv.Ordre_achat(acheteur.prix, acheteur, "Gâteau", acheteur.besoin)

            if hotel.recherche_ordre_vente(ordre_achat):
                print(f"{individu} a acheté {ordre_achat}")

            if hotel.recherche_ordre_achat(ordre_vente):
                print(f"{individu} a vendu {ordre_vente}")

            individu.stock = vendeur.stock
            individu.brs = (acheteur.brs + vendeur.brs) / 2
            individu.besoin = acheteur.besoin

            individu.production()
            individu.change_prix_limite()
            individu.change_besoins()
            individu.change_prix_vente()

        elif type(individu) == Patissier:
            # Arrondir et préparer les valeurs de prix
            individu.pl[0] = round(individu.pl[0], 1)
            individu.pl[1] = round(individu.pl[1], 1)
            individu.prix_vente_gateau = round(individu.prix_vente_gateau, 1)

            # Créer des acheteurs pour les matières premières basés sur le solde actuel du patissier
            acheteur1 = hdv.Acheteur(individu.pl[1], individu.brs, individu.besoin[1], individu.stock_blé)  # Pour le blé
            acheteur2 = hdv.Acheteur(individu.pl[0], individu.brs, individu.besoin[0], individu.stock_oeuf)  # Pour les œufs

            # Créer un vendeur pour la vente de gâteaux à partir des données du patissier
            vendeur = hdv.Vendeur(individu.stock, individu.brs, individu.prix_vente_gateau, individu.stock)

            # Créer les ordres associés
            ordre_achat_1 = hdv.Ordre_achat(individu.pl[1], acheteur1, "Blé", individu.besoin[1])
            ordre_achat_2 = hdv.Ordre_achat(individu.pl[0], acheteur2, "Oeuf", individu.besoin[0])
            ordre_vente = hdv.Ordre_vente(vendeur.prix, vendeur, "Gâteau", vendeur.stock)

            # Traiter les ordres pour les achats de matières premières avec la fonction recherche_ordre_vente 
            if hotel.recherche_ordre_vente(ordre_achat_2):
                print(f"{individu} a acheté {ordre_achat_2}")
            if hotel.recherche_ordre_vente(ordre_achat_1):
                print(f"{individu} a acheté {ordre_achat_1}")

            # Traiter l'ordre de vente du gâteau
            if hotel.recherche_ordre_achat(ordre_vente):
                print(f"{individu} a vendu {ordre_vente}")

            # Mettre à jour les valeurs du patissier d'après les transactions réalisées
            individu.pl[1] = acheteur1.prix
            individu.pl[0] = acheteur2.prix
            individu.besoin[1] = acheteur1.besoin
            individu.besoin[0] = acheteur2.besoin
            individu.stock = vendeur.stock
            individu.stock_blé = acheteur1.stock_achat
            individu.stock_oeuf = acheteur2.stock_achat

            # On met à jour le solde (brs) en combinant les mises à jour des acheteurs et du vendeur.
            # La formule ici prend la moyenne des trois ; à ajuster selon votre logique économique.
            individu.brs = (acheteur1.brs + acheteur2.brs + vendeur.brs) / 3

            # Production (essaye de produire un gâteau si conditions remplies)
            individu.production()

            # Affichage de quelques indicateurs de suivi
            print("individu.stock_blé: ", individu.stock_blé)
            print("individu.stock_oeuf: ", individu.stock_oeuf)
            print("individu.stock_gateau: ", individu.stock)

            # Mise à jour des autres paramètres
            individu.change_prix_limite()
            individu.change_besoins()
            individu.change_prix_vente()

        individu.brs = round(individu.brs, 1)
        somme += individu.brs

        # Maintenant il faut afficher des données significatives de l'évolution du prix de vente de chaque produit (moyenne, prix min, prix max)
        # Il faut également donner d'autres données comme l'argent total dans l'économie ou des informations sur les agents économiques

        print(individu)
    print(somme)

    continuer = input("Continuer ? : (Y/N) : ")
    if continuer == "Y":
        simulation_gateau(liste_personnes, hotel)
