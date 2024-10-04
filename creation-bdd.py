import sqlite3
import csv

# Créer ou se connecter à une base de données SQLite
conn = sqlite3.connect('creation-bdd.db')

# Créer un curseur
cursor = conn.cursor()

# Création de la table Client
cursor.execute('''
CREATE TABLE IF NOT EXISTS Client (
    Client_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT NOT NULL,
    Prenom TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    Telephone TEXT,
    Date_Naissance DATE,
    Adresse TEXT,
    Consentement_Marketing BOOLEAN NOT NULL
);
''')

# Création de la table Commande
cursor.execute('''
CREATE TABLE IF NOT EXISTS Commande (
    Commande_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Date_Commande DATE NOT NULL,
    Montant_Commande REAL NOT NULL,
    Client_ID INTEGER NOT NULL,
    FOREIGN KEY (Client_ID) REFERENCES Client(Client_ID) ON DELETE CASCADE
);
''')

# Fonction pour insérer les clients dans la table Client
def inserer_clients(client):
    with open(client, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Sauter l'en-tête du fichier CSV
        for row in reader:
            # Vérification qu'il y a bien 7 colonnes et que la ligne n'est pas vide
            if len(row) == 7:
                cursor.execute('''
                INSERT OR IGNORE INTO Client (Nom, Prenom, Email, Telephone, Date_Naissance, Adresse, Consentement_Marketing)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
            else:
                print(f"Ligne incorrecte ou incomplète : {row}")
    conn.commit()

# Fonction pour insérer les commandes dans la table Commande
def inserer_commandes(commande):
    with open(commande, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Sauter l'en-tête du fichier CSV
        for row in reader:
            # Vérification qu'il y a bien 3 colonnes et que la ligne n'est pas vide
            if len(row) == 3:
                cursor.execute('''
                INSERT INTO Commande (Date_Commande, Montant_Commande, Client_ID)
                VALUES (?, ?, ?)
                ''', (row[0], row[1], row[2]))
            else:
                print(f"Ligne incorrecte ou incomplète : {row}")
    conn.commit()

# Appel des fonctions pour insérer les données depuis les fichiers CSV
inserer_clients('client.csv')
inserer_commandes('commande.csv')

# Fonction pour récupérer les clients ayant consenti à recevoir des communications marketing
def extraire_clients_consentement_marketing():
    cursor.execute('''
    SELECT Nom, Prenom, Email, Telephone, Adresse
    FROM Client
    WHERE Consentement_Marketing = 1
    ''')
    clients = cursor.fetchall()  # Récupérer tous les résultats
    return clients

# Appel de la fonction et affichage des résultats
clients_consentement = extraire_clients_consentement_marketing()
print("Clients ayant consenti à recevoir des communications marketing :")
for client in clients_consentement:
    print(f"Nom: {client[0]}, Prénom: {client[1]}, Email: {client[2]}, Téléphone: {client[3]}, Adresse: {client[4]}")

