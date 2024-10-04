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

# Fonction pour obtenir l'ID d'un client par son nom et prénom
def obtenir_client_id(nom, prenom):
    cursor.execute('''
    SELECT Client_ID FROM Client
    WHERE Nom = ? AND Prenom = ?
    ''', (nom, prenom))
    result = cursor.fetchone()  # Récupérer le premier résultat
    return result[0] if result else None  # Retourner l'ID ou None si le client n'existe pas

# Fonction pour récupérer les commandes d'un client spécifique par son ID
def extraire_commandes_client_id(client_id):
    cursor.execute('''
    SELECT Commande_ID, Date_Commande, Montant_Commande
    FROM Commande
    WHERE Client_ID = ?
    ''', (client_id,))
    commandes = cursor.fetchall()  # Récupérer toutes les commandes du client
    return commandes

#récupérer les commandes du client 
nom_client = 'Martin'
prenom_client = 'Claire'
client_id = obtenir_client_id(nom_client, prenom_client)

if client_id:
    commandes_client = extraire_commandes_client_id(client_id)
    print(f"Commandes du client {nom_client} {prenom_client} (ID {client_id}) :")
    for commande in commandes_client:
        print(f"Commande ID: {commande[0]}, Date: {commande[1]}, Montant: {commande[2]} €")
else:
    print(f"Aucun client trouvé avec le nom {nom_client} et le prénom {prenom_client}.")

    # Fonction pour obtenir le montant total des commandes d'un client par son ID
def obtenir_montant_total_commandes(client_id):
    cursor.execute('''
    SELECT SUM(Montant_Commande) FROM Commande
    WHERE Client_ID = ?
    ''', (client_id,))
    total = cursor.fetchone()[0]  # Récupérer le total
    return total if total is not None else 0  # Retourner le total ou 0 si aucune commande

# ID du client dont on veut le montant total des commandes
client_id = 61
montant_total = obtenir_montant_total_commandes(client_id)

print(f"Montant total des commandes pour le client avec ID n° {client_id} : {montant_total} €")

# Fonction pour obtenir les clients ayant passé des commandes de plus de 100 euros
def obtenir_clients_commandes_plus_de_100():
    cursor.execute('''
    SELECT DISTINCT c.Client_ID, c.Nom, c.Prenom
    FROM Client c
    JOIN Commande cmd ON c.Client_ID = cmd.Client_ID
    WHERE cmd.Montant_Commande > 100
    ''')
    return cursor.fetchall()  # Récupérer tous les résultats

# Appel de la fonction et affichage des résultats
clients = obtenir_clients_commandes_plus_de_100()

print("Clients ayant passé des commandes de plus de 100 euros :")
for client in clients:
    print(f"ID: {client[0]}, Nom: {client[1]}, Prénom: {client[2]}")

# Fonction pour obtenir les clients ayant passé des commandes après le 01/01/2023
def obtenir_clients_commandes_apres_date(date):
    cursor.execute('''
    SELECT DISTINCT c.Client_ID, c.Nom, c.Prenom
    FROM Client c
    JOIN Commande cmd ON c.Client_ID = cmd.Client_ID
    WHERE cmd.Date_Commande > ?
    ''', (date,))
    return cursor.fetchall()  # Récupérer tous les résultats

# Définir la date à partir de laquelle on veut filtrer
date_limite = '2023-01-01'

# Appel de la fonction et affichage des résultats
clients = obtenir_clients_commandes_apres_date(date_limite)

print("Clients ayant passé des commandes après le 01/01/2023 :")
for client in clients:
    print(f"ID: {client[0]}, Nom: {client[1]}, Prénom: {client[2]}")

# Fermer la connexion à la base de données
conn.close()