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

# Importation des données à partir du fichier client.csv
try:
    with open('client.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        clients_data = [(row['Nom'], row['Prénom'], row['Email'], row['Téléphone'], row['Date_Naissance'], row['Adresse'], row['Consentement_Marketing']) for row in reader]

    # Insertion des données dans la table Client (ignorer les doublons)
    cursor.executemany('''
    INSERT OR IGNORE INTO Client (Nom, Prenom, Email, Telephone, Date_Naissance, Adresse, Consentement_Marketing)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', clients_data)

    # Valider les changements pour la table Client
    conn.commit()
    print("Données des clients importées avec succès.")

    # Importation des données à partir du fichier commande.csv
    with open('commande.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        commandes_data = [(row['Commande_ID'], row['Date_Commande'], row['Montant_Commande'], row['Client_ID']) for row in reader]

    # Insertion des données dans la table Commande (remplacer les doublons)
    cursor.executemany('''
    INSERT OR REPLACE INTO Commande (Commande_ID, Date_Commande, Montant_Commande, Client_ID)
    VALUES (?, ?, ?, ?)
    ''', commandes_data)

    # Valider les changements pour la table Commande
    conn.commit()
    print("Données des commandes importées avec succès.")

    # Récupérer les clients ayant consenti à recevoir des communications marketing
    cursor.execute('''
    SELECT * FROM Client
    WHERE Consentement_Marketing = 1;  -- 1 pour "True"
    ''')

    # Récupérer les résultats
    clients_marketing = cursor.fetchall()

    # Afficher les clients
    if clients_marketing:
        print("Clients ayant consenti à recevoir des communications marketing :")
        for client in clients_marketing:
            print(f"ID : {client[0]}, Nom : {client[1]}, Prénom : {client[2]}, Email : {client[3]}, Téléphone : {client[4]}")
    else:
        print("Aucun client n'a consenti à recevoir des communications marketing.")

    # Demander l'ID du client spécifique
    client_id = 61  # Remplacez par l'ID du client dont vous voulez voir les commandes

    # Récupérer les commandes du client spécifique
    cursor.execute('''
    SELECT * FROM Commande
    WHERE Client_ID = ?;
    ''', (client_id,))

    # Récupérer les résultats
    commandes_client = cursor.fetchall()

    # Afficher les commandes
    if commandes_client:
        print(f"Commandes du client avec ID {client_id} :")
        for commande in commandes_client:
            print(f"Commande ID : {commande[0]}, Date : {commande[1]}, Montant : {commande[2]}")
    else:
        print(f"Aucune commande trouvée pour le client avec ID {client_id}.")

    # Calculer le montant total des commandes du client avec ID n° 61
    cursor.execute('''
    SELECT SUM(Montant_Commande) FROM Commande
    WHERE Client_ID = ?;
    ''', (client_id,))

    total_montant = cursor.fetchone()[0]

    if total_montant is not None:
        print(f"Le montant total des commandes du client avec ID {client_id} est : {total_montant:.2f} euros.")
    else:
        print(f"Aucune commande trouvée pour le client avec ID {client_id}, donc le montant total est 0 euros.")

    # Récupérer les clients ayant passé des commandes de plus de 100 euros
    cursor.execute('''
    SELECT DISTINCT c.Client_ID, c.Nom, c.Prenom
    FROM Client c
    JOIN Commande co ON c.Client_ID = co.Client_ID
    WHERE co.Montant_Commande > 100;
    ''')

    # Récupérer les résultats
    clients_100euros = cursor.fetchall()

    # Afficher les clients
    if clients_100euros:
        print("Clients ayant passé des commandes de plus de 100 euros :")
        for client in clients_100euros:
            print(f"ID : {client[0]}, Nom : {client[1]}, Prénom : {client[2]}")
    else:
        print("Aucun client n'a passé de commandes de plus de 100 euros.")

    # Récupérer les clients ayant passé des commandes après le 01/01/2023
    cursor.execute('''
    SELECT DISTINCT c.Client_ID, c.Nom, c.Prenom
    FROM Client c
    JOIN Commande co ON c.Client_ID = co.Client_ID
    WHERE co.Date_Commande > '2023-01-01';
    ''')

    # Récupérer les résultats
    clients_apres_2023 = cursor.fetchall()

    # Afficher les clients
    if clients_apres_2023:
        print("Clients ayant passé des commandes après le 01/01/2023 :")
        for client in clients_apres_2023:
            print(f"ID : {client[0]}, Nom : {client[1]}, Prénom : {client[2]}")
    else:
        print("Aucun client n'a passé de commandes après le 01/01/2023.")

except sqlite3.IntegrityError as e:
    print(f"Erreur d'intégrité : {e}")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
finally:
    # Fermer la connexion à la base de données
    conn.close()
