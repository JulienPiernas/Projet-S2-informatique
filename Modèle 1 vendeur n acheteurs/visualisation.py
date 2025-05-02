import json
import matplotlib.pyplot as plt

# Lecture du fichier JSON

def load_data():
    iterations = []
    prix = []

    with open('resultats.json', 'r') as file:
        content = '[' + file.read().rstrip(',\n') + ']'
        data = json.loads(content)

        # Trouver où commence la dernière simulation
        last_sim_start = 0
        for i, entry in enumerate(data):
            if entry["iteration"] == 1 and i > 0:
                last_sim_start = i

        # Ne prendre que les données de la dernière simulation
        for entry in data[last_sim_start:]:
            if "vendeur" in entry and "prix_courant" in entry["vendeur"]:
                iterations.append(entry["iteration"])
                prix.append(entry["vendeur"]["prix_courant"])

    return iterations, prix


def plot_price_evolution():
    iterations, prix = load_data()

    plt.figure(figsize=(10, 6))
    plt.plot(iterations, prix, 'b-', marker='o')
    plt.title('Évolution du prix de vente au fil des itérations')
    plt.xlabel('Itération')
    plt.ylabel('Prix courant')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    plot_price_evolution()
