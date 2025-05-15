import sqlite3
import os
import random
from scripts.utils import get_database_path

def create_database(idTournois):
    db_path = get_database_path(idTournois)
    
    # Créer la base de données si elle n'existe pas
    if not os.path.exists(f"databases/{idTournois}.db"):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Créer la table `tournois`
        cursor.execute('''
        CREATE TABLE tournois (
            idTournois TEXT PRIMARY KEY,
            nomTournois TEXT NOT NULL,
            password TEXT NOT NULL
        )
        ''')

        # Créer la table `equipe`
        cursor.execute('''
        CREATE TABLE equipe (
            numEquipe INTEGER PRIMARY KEY,
            nomEquipe TEXT NOT NULL
        )
        ''')

        # Créer la table `joueur`
        cursor.execute('''
        CREATE TABLE joueur (
            idJoueur INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL,
            numEquipe INTEGER,
            FOREIGN KEY(numEquipe) REFERENCES equipe(numEquipe)
        )
        ''')

        # Créer la table `matchs`
        cursor.execute('''
        CREATE TABLE matchs (
            idMatch INTEGER PRIMARY KEY AUTOINCREMENT,
            numEquipeBleu INTEGER,
            numEquipeRouge INTEGER,
            numEquipeGagnante INTEGER,
            statut TEXT,
            dateHeure TEXT,
            phase TEXT,
            FOREIGN KEY(numEquipeBleu) REFERENCES equipe(numEquipe),
            FOREIGN KEY(numEquipeRouge) REFERENCES equipe(numEquipe),
            FOREIGN KEY(numEquipeGagnante) REFERENCES equipe(numEquipe)
        )
        ''')

        # Committer les changements
        conn.commit()
        
        # Fermer la connexion
        conn.close()
    else:
        raise Exception(f"La base de données pour le tournoi avec l'identifiant {idTournois} existe déjà.")

import csv
import sqlite3
import os
from scripts.utils import get_database_path

def import_to_database(idTournois):
    db_path = get_database_path(idTournois)

    if not os.path.exists(db_path):
        raise Exception(f"La base de données avec l'identifiant {idTournois} n'existe pas.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Importer tournois.csv
        path_tournois = os.path.join("import", "tournois.csv")
        if os.path.exists(path_tournois):
            with open(path_tournois, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute('''
                        INSERT OR IGNORE INTO tournois (idTournois, nomTournois, password)
                        VALUES (?, ?, ?)
                    ''', (row["idTournois"], row["nomTournois"], row["password"]))
        else:
            raise Exception("Fichier 'tournois.csv' introuvable.")

        # Importer equipe.csv
        path_equipe = os.path.join("import", "equipe.csv")
        if os.path.exists(path_equipe):
            with open(path_equipe, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute('''
                        INSERT OR IGNORE INTO equipe (numEquipe, nomEquipe)
                        VALUES (?, ?)
                    ''', (row["numEquipe"], row["nomEquipe"]))
        else:
            raise Exception("Fichier 'equipe.csv' introuvable.")

        # Importer joueur.csv
        path_joueur = os.path.join("import", "joueur.csv")
        if os.path.exists(path_joueur):
            with open(path_joueur, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute('''
                        INSERT OR IGNORE INTO joueur (idJoueur, pseudo, numEquipe)
                        VALUES (?, ?, ?)
                    ''', (row["idJoueur"], row["pseudo"], row["numEquipe"]))
        else:
            raise Exception("Fichier 'joueur.csv' introuvable.")

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def insert_dataTournoi(idTournois, nomTournois, password):
    db_path = get_database_path(idTournois)
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insérer les informations du tournoi dans la table `tournois`
        try:
            cursor.execute('''
            INSERT INTO tournois (idTournois, nomTournois, password)
            VALUES (?, ?, ?)
            ''', (idTournois, nomTournois, password))

            # Committer les changements
            conn.commit()

        except sqlite3.Error as e:
            conn.rollback()
            raise e

        # Fermer la connexion
        conn.close()
    else:
        raise Exception(f"La base de données pour le tournoi avec l'identifiant {idTournois} n'existe pas.")

def list_team(idTournois):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT numEquipe, nomEquipe FROM equipe")
        equipes = cursor.fetchall()
        return equipes
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()

def list_players(idTournois):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT joueur.idJoueur, joueur.pseudo, joueur.numEquipe, equipe.nomEquipe
            FROM joueur
            LEFT JOIN equipe ON joueur.numEquipe = equipe.numEquipe
            ORDER BY joueur.idJoueur ASC
        """)
        joueurs = cursor.fetchall()
        return joueurs
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()

def fetch_from_db(db_path, table, column):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT {column} FROM {table} LIMIT 1;")
        result = cursor.fetchone()

        conn.close()

        return result[0] if result else ""

    except sqlite3.Error as e:
        raise e
    
def create_team_db(idTournois, nomEquipe):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if not nomEquipe:
        raise Exception("Le nom d'équipe n'est pas valide")
    
    try:
        cursor.execute("INSERT INTO equipe (nomEquipe) VALUES (?)", (nomEquipe,))
        numEquipe = cursor.lastrowid

        conn.commit()
        return numEquipe

    except sqlite3.Error as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def delete_team_db(idTournois, numEquipe):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if not numEquipe.isdigit():
            raise Exception("Numéro d'équipe invalide.")

        # Vérifie si l'équipe existe
        cursor.execute("SELECT nomEquipe FROM equipe WHERE numEquipe = ?", (numEquipe,))
        row = cursor.fetchone()

        if not row:
            raise Exception(f"Aucune équipe trouvée avec le numéro {numEquipe}.")

        # Supprimer les joueurs d'abord
        cursor.execute("DELETE FROM joueur WHERE numEquipe = ?", (numEquipe,))
        # Puis supprimer l'équipe
        cursor.execute("DELETE FROM equipe WHERE numEquipe = ?", (numEquipe,))

        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def edit_team_name_db(idTournois, numEquipe):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if not numEquipe.isdigit():
            raise Exception("Numéro d'équipe invalide.")

        # Vérifie si l'équipe existe
        cursor.execute("SELECT nomEquipe FROM equipe WHERE numEquipe = ?", (numEquipe,))
        row = cursor.fetchone()

        if not row:
            raise Exception(f"Aucune équipe trouvée avec le numéro {numEquipe}.")

        newNameEquipe = input("Nouveau nom de l'équipe : ").strip()

        if not newNameEquipe:
            raise Exception("Le nom ne peut pas être vide.")

        cursor.execute("UPDATE equipe SET nomEquipe = ? WHERE numEquipe = ?", (newNameEquipe, numEquipe))
        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def add_player_db(idTournois, pseudo, numEquipe):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if not pseudo:
            raise Exception("Le nom ne peut pas être vide")
    
        if not numEquipe:
            raise Exception("Le numéro d'équipe ne peut pas être vide")

        # Vérifier si l'équipe existe
        cursor.execute("SELECT nomEquipe FROM equipe WHERE numEquipe = ?", (numEquipe,))
        row = cursor.fetchone()
        if not row:
            raise Exception(f"Aucune équipe trouvée avec le numéro {numEquipe}.")

        # Ajouter le joueur à l'équipe spécifiée
        cursor.execute("INSERT INTO joueur (pseudo, numEquipe) VALUES (?, ?)", (pseudo, numEquipe))
        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def remove_player_db(idTournois, numJoueur):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if not numJoueur.isdigit():
            raise Exception("Numéro de joueur invalide.")

        # Vérifie si le joueur existe
        cursor.execute("""
            SELECT joueur.pseudo, joueur.numEquipe, equipe.nomEquipe
            FROM joueur
            LEFT JOIN equipe ON joueur.numEquipe = equipe.numEquipe
            WHERE joueur.idJoueur = ?""", (numJoueur,))
        row = cursor.fetchone()

        if not row:
            raise Exception(f"Aucun joueur trouvé avec le numéro {numJoueur}.")

        # Supprime le joueur
        cursor.execute("DELETE FROM joueur WHERE idJoueur = ?", (numJoueur,))
        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def edit_player_name_db(idTournois, numJoueur):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if not numJoueur.isdigit():
            raise Exception("Le numéro de joueur est invalide.")

        # Vérifie si le joueur existe
        cursor.execute("SELECT pseudo FROM joueur WHERE idJoueur = ?", (numJoueur,))
        row = cursor.fetchone()

        if not row:
            raise Exception(f"Aucun joueur trouvé avec le numéro {numJoueur}.")

        new_pseudo = input("Nouveau pseudo : ").strip()

        if not new_pseudo:
            raise Exception("Le pseudo ne peut pas être vide.")

        cursor.execute(
            "UPDATE joueur SET pseudo = ? WHERE idJoueur = ?",
            (new_pseudo, numJoueur)
        )
        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def change_team_db(idTournois, numJoueur, newNumEquipe):
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        if not numJoueur.isdigit() or not newNumEquipe.isdigit():
            raise Exception("ID joueur ou numéro d'équipe invalide.")

        # Vérifie que le joueur existe
        cursor.execute("SELECT pseudo, numEquipe FROM joueur WHERE idJoueur = ?", (numJoueur,))
        joueur = cursor.fetchone()
        if not joueur:
            raise Exception(f"Aucun joueur trouvé avec le numéro {numJoueur}.")

        # Vérifie que la nouvelle équipe existe
        cursor.execute("SELECT nomEquipe FROM equipe WHERE numEquipe = ?", (newNumEquipe,))
        equipe = cursor.fetchone()
        if not equipe:
            raise Exception(f"Aucune équipe trouvée avec le numéro {newNumEquipe}.")

        # Mise à jour de l’équipe du joueur
        cursor.execute(
            "UPDATE joueur SET numEquipe = ? WHERE idJoueur = ?",
            (newNumEquipe, numJoueur)
        )
        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        raise e

    finally:
        conn.close()

def get_active_teams(idTournois):
    """Récupère la liste des numEquipe encore actives dans le tournoi."""
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT numEquipe FROM equipe")
        teams = [row[0] for row in cursor.fetchall()]
        return teams
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()

def create_match(idTournois, numEquipeBleu, numEquipeRouge, tour):
    """Crée un match dans la table matchs avec le statut 'non commencé'."""
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO matchs (numEquipeBleu, numEquipeRouge, statut, phase)
            VALUES (?, ?, ?, ?)
        """, (numEquipeBleu, numEquipeRouge, "non commencé", f"Tour {tour}"))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_match_status(idTournois, idMatch, statut):
    """Met à jour le statut d'un match ('non commencé', 'en cours', 'terminé')."""
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE matchs SET statut = ? WHERE idMatch = ?", (statut, idMatch))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def set_match_winner(idTournois, idMatch, numEquipeGagnante):
    """Met à jour le match avec l'équipe gagnante et le statut 'terminé'."""
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE matchs
            SET statut = ?, numEquipeGagnante = ?
            WHERE idMatch = ?
        """, ("terminé", numEquipeGagnante, idMatch))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_matches_by_tour(idTournois, tour):
    """Récupère tous les matchs d'un tour donné."""
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT idMatch, numEquipeBleu, numEquipeRouge, statut, numEquipeGagnante, phase,
                   e1.nomEquipe AS nomEquipeBleu, e2.nomEquipe AS nomEquipeRouge
            FROM matchs
            LEFT JOIN equipe e1 ON matchs.numEquipeBleu = e1.numEquipe
            LEFT JOIN equipe e2 ON matchs.numEquipeRouge = e2.numEquipe
            WHERE phase = ?
        """, (f"Tour {tour}",))
        matches = cursor.fetchall()
        return matches
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()

def generate_tournament_matches(idTournois):
    """Génère les matchs pour un tournoi par élimination directe."""
    active_teams = get_active_teams(idTournois)
    if len(active_teams) < 2:
        raise Exception("Pas assez d'équipes pour générer des matchs.")

    # Mélanger les équipes pour un appariement aléatoire
    random.shuffle(active_teams)
    tour = 1

    # Créer les matchs du premier tour
    matches = []
    for i in range(0, len(active_teams) - 1, 2):
        match_id = create_match(idTournois, active_teams[i], active_teams[i + 1], tour)
        matches.append(match_id)
        print(f"Match créé : idMatch={match_id}, EquipeBleu={active_teams[i]}, EquipeRouge={active_teams[i + 1]}, Tour={tour}")  # Débogage
    
    return tour

def get_team_win_stats(idTournois):
    """Récupère le nombre de victoires par équipe dans le tournoi."""
    db_path = get_database_path(idTournois)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT equipe.numEquipe, equipe.nomEquipe, COUNT(matchs.numEquipeGagnante) as victoires
            FROM equipe
            LEFT JOIN matchs ON equipe.numEquipe = matchs.numEquipeGagnante
            GROUP BY equipe.numEquipe, equipe.nomEquipe
            ORDER BY victoires DESC, equipe.numEquipe ASC
        """)
        stats = cursor.fetchall()
        return stats
    except sqlite3.Error as e:
        raise e
    finally:
        conn.close()