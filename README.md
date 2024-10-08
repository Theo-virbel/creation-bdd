# Création d'une base de données

Dans ce brief, vous allez créer une base de données à partir de fichiers CSV. 
Pour ce faire, vous devrez d'abord vous renseigner sur ce qu'est un MCD (Modèle Conceptuel de Données) et un MPD (Modèle Physique de Données), puis les réaliser. 
Ensuite, vous développerez des requêtes SQL pour extraire des données pertinentes. 
L'objectif est de maîtriser la conception et l'implémentation d'une base de données, ainsi que de savoir exécuter des requêtes SQL pour extraire les informations nécessaires.

# Contexte du projet

Vous travaillez pour une entreprise qui collecte des données clients dans le cadre d'une campagne marketing.

Deux tables vous sont fournies : une table **client **et une table commande.

Votre mission consiste à concevoir une base de données et à y intégrer ces tables.

Une fois la base de données créée, vous devrez extraire les informations suivantes :

Les clients ayant consenti à recevoir des communications marketing.
Les commandes d'un client spécifique.
Le montant total des commandes du client avec ID n° 61 .

Les clients ayant passé des commandes de plus de 100 euros.

Les clients ayant passé des commandes après le 01/01/2023.

# Modalités pédagogiques

Analyse des jeux de données.
Élaboration d'un modèle conceptuel des données (MCD) :


Se renseigner sur ce qu'est un MCD et utiliser un outil comme Drawdb.app pour le créer.
Transformation du MCD en un modèle physique des données (MPD):
S'aider du cahier des charges en ressources.
Création et implémentation de la base de données :
Implémenter la base sur un SGBD (SQLite, MySQL, PostgreSQL, etc.) et créer les tables.
Programmation de l'import des données :
Écrire un script Python pour importer les données dans la base de données en respectant les contraintes définies dans le MPD.
Extraction les données demandées par requête SQL.

