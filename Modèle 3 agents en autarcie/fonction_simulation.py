from random import randint

from personne import Paysan, Fermier, Patissier

import matplotlib.pyplot as plt


def simulation(
    patissier, paysan, fermier, max_jours=365, seuil_variation=0.01, fenetre_stabilite=5
):
    historique_prix = []
    historique_prix_gateau = []
    historique_prix_ble = []
    historique_prix_oeuf = []
    jours_liste = []
    jours = 0

    # ⚠️ Marché SANS stock initial, mais avec liste de vendeurs
    marche = {
        "ble": {"stock": 0, "vendeurs": []},
        "oeuf": {"stock": 0, "vendeurs": []},
        "gateau": {"stock": 0},
    }

    while jours < max_jours:
        jours += 1
        print(f"\n=== JOUR {jours} ===")

        for agent in [patissier, paysan, fermier]:
            agent.brs_avant_tick = agent.brs

        patissier.change_besoins()
        paysan.change_besoins()
        fermier.change_besoins()
        
        paysan.production()
        fermier.production()

        paysan.vendre_au_marche(marche)
        fermier.vendre_au_marche(marche)

        patissier.effectuer_transactions(marche)
        patissier.production()

        while patissier.stock > 0 and (
            fermier.besoin > 0 or (paysan.besoin > 0 or patissier.besoin_gateaux > 0)
        ):
            stock_depart = patissier.stock
            paysan.acheter_gateau(patissier)
            fermier.acheter_gateau(patissier)
            patissier.consommer()
            if patissier.stock == stock_depart:
                break

        fermier.consommer()
        paysan.consommer()

        patissier.change_prix_limite()
        paysan.change_prix_limite()
        fermier.change_prix_limite()

        patissier.change_prix_vente()
        paysan.change_prix_vente()
        fermier.change_prix_vente()

        historique_prix_gateau.append(patissier.prix_vente_gateau)
        historique_prix_ble.append(paysan.prix_vente_blé)
        historique_prix_oeuf.append(fermier.prix_vente_oeuf)
        jours_liste.append(jours)
        historique_prix.append(patissier.prix_vente_gateau)
        print(
            f"Prix du gâteau : {patissier.prix_vente_gateau:.2f}",
            "   Prix du blé : ",
            paysan.prix_vente_blé,
            "   Prix de l'oeuf : ",
            fermier.prix_vente_oeuf,
        )
        print(
            f"Besoin du pâtissier : {patissier.besoin_gateaux}, Besoin du paysan : {paysan.besoin}, Besoin du fermier : {fermier.besoin}"
        )
        print(
            f"Pâtissier : {patissier.brs:.2f}, Paysan : {paysan.brs:.2f}, Fermier : {fermier.brs:.2f}"
        )
        print(f"Prix limites : {patissier.pl}, {paysan.pl}, {fermier.pl}")

        if len(historique_prix) >= fenetre_stabilite:
            recent = historique_prix[-fenetre_stabilite:]
            max_prix = max(recent)
            min_prix = min(recent)
            if abs(max_prix - min_prix) / max_prix < seuil_variation:
                print(
                    f"\n📊 Prix d'équilibre atteint après {jours} jours : {round(patissier.prix_vente_gateau, 2)} kamas"
                )
                plt.figure(figsize=(10, 6))
                plt.plot(
                    jours_liste,
                    historique_prix_gateau,
                    label="Prix gâteau",
                    color="green",
                )
                plt.plot(
                    jours_liste, historique_prix_ble, label="Prix blé", color="red"
                )
                plt.plot(
                    jours_liste, historique_prix_oeuf, label="Prix oeuf", color="blue"
                )

                plt.xlabel("Jours")
                plt.ylabel("Prix (kamas)")
                plt.title("Évolution des prix au cours du temps")
                plt.legend()
                plt.grid(True)
                plt.show()
                return round(patissier.prix_vente_gateau, 2), jours

    print(f"\n⚠️ Pas de prix d'équilibre trouvé en {max_jours} jours.")
    plt.figure(figsize=(10, 6))
    plt.plot(jours_liste, historique_prix_gateau, label="Prix gâteau", color="brown")
    plt.plot(jours_liste, historique_prix_ble, label="Prix blé", color="yellow")
    plt.plot(jours_liste, historique_prix_oeuf, label="Prix oeuf", color="white")

    plt.xlabel("Jours")
    plt.ylabel("Prix (kamas)")
    plt.title("Évolution des prix au cours du temps")
    plt.legend()
    plt.grid(True)
    plt.show()
    return round(patissier.prix_vente_gateau, 2), jours
