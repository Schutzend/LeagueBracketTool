import time

from scripts.utils import clear
from scripts.databases import list_team, list_players, create_team_db, delete_team_db, edit_team_name_db, add_player_db, remove_player_db, edit_player_name_db, change_team_db

def administration(idTournois, nomTournois, password) :
    clear()
    print(f"== Administration du tournoi {nomTournois} ==")
    print(f"== Identifiant de tournoi : {idTournois} ==")
    print(f"== Mot de passe de gestion : {password} ==")
    print("")
    print("1. Lister les équipes ou les joueurs")
    print("2. Créer une équipe")
    print("3. Supprimer une équipe entière et ses joueurs")
    print("4. Modifier le nom de l'équipe")
    print("5. Ajouter un joueur")
    print("6. Retirer un joueur")
    print("7. Modifier le nom du joueur")
    print("8. Changer un joueur d'une équipe")
    print("")
    print("9. Lancer les matchs (non disponible)")
    print("10. Quitter")

    choix = input("\nChoisissez une option (1-10) : ")

    if choix == '1':
        list_table(idTournois, nomTournois, password)
    elif choix == '2':
        create_team(idTournois, nomTournois, password)
    elif choix == '3':
        delete_team(idTournois, nomTournois, password)
    elif choix == '4':
        edit_team_name(idTournois, nomTournois, password)
    elif choix == '5':
        add_player(idTournois, nomTournois, password)
    elif choix == '6':
        remove_player(idTournois, nomTournois, password)
    elif choix == '7':
        edit_player_name(idTournois, nomTournois, password)
    elif choix == '8':
        change_team(idTournois, nomTournois, password)
    elif choix == '10':
        print("\nMerci d'avoir utilisé LeagueBracketTool. À bientôt !")
        exit()
    else:
        print("Choix invalide, veuillez réessayer.")
        time.sleep(2)
        administration(idTournois, nomTournois, password)

def list_table(idTournois, nomTournois, password):
    clear()
    print("===== Liste des équipes et des joueurs =====")
    print("1. Équipes")
    print("2. Joueurs")
    choix = input("\nQuelle table voulez-vous afficher ? (1-2) : ").strip()

    if choix == "1":
        list_team(idTournois)
        input("\nAppuyez sur Entrée pour continuer...")
        administration(idTournois, nomTournois, password)
    elif choix == "2":
        list_players(idTournois)
        input("\nAppuyez sur Entrée pour continuer...")
        administration(idTournois, nomTournois, password)
    else:
        print("Choix invalide.")
        input("\nAppuyez sur Entrée pour continuer...")
        administration(idTournois, nomTournois, password)

def create_team(idTournois, nomTournois, password):
    clear()
    print("===== Création d'une équipe =====")
    nomEquipe = input("Nom de l'équipe : ")

    create_team_db(idTournois, nomEquipe)

    input("\nAppuyez sur Entrée pour continuer...")
    administration(idTournois, nomTournois, password)

def delete_team(idTournois, nomTournois, password):
    clear()
    print("===== Suppression d'une équipe =====")
    numEquipe = input("Entrez le numéro de l'équipe à supprimer : ")

    delete_team_db(idTournois, numEquipe)

    input("\nAppuyez sur Entrée pour continuer...")
    administration(idTournois, nomTournois, password)

def edit_team_name(idTournois, nomTournois, password):
    clear()
    print("===== Modifier le nom d'une équipe =====")
    
    numEquipe = input("Entrez le numéro de l'équipe à modifier : ")
    edit_team_name_db(idTournois, numEquipe)

    input("\nAppuyez sur Entrée pour continuer...")
    administration(idTournois, nomTournois, password)

def add_player(idTournois, nomTournois, password):
    clear()
    print("===== Ajout d'un joueur =====")

    pseudo = input("Entrez le pseudo du joueur : ")
    numEquipe = input("Entrez le numéro d'équpe à associer : ")

    add_player_db(idTournois, pseudo, numEquipe)

    input("\nAppuyez sur Entrée pour continuer...")
    administration(idTournois, nomTournois, password)

def remove_player(idTournois, nomTournois, password):
    clear()
    print("===== Suppression d'un joueur =====")

    numJoueur = input("Quelle est l'identifiant du joueur : ")
    remove_player_db(idTournois, numJoueur)

    input("\nAppuyez sur Entrée pour continuer...")
    administration(idTournois, nomTournois, password)

def edit_player_name(idTournois, nomTournois, password):
    clear()
    print("===== Modifier le pseudo d'un joueur =====")

    numJoueur = input("Entrez le numéro du joueur à modifier : ")
    edit_player_name_db(idTournois, numJoueur)

    input("\nAppuyez sur Entrée pour continuer...")
    administration(idTournois, nomTournois, password)

def change_team(idTournois, nomTournois, password):
    clear()
    print("===== Changer un joueur d'équipe =====")

    numJoueur = input("Entrez le numéro du joueur : ")
    change_team_db(idTournois, numJoueur)

    input("\nAppuyez sur Entrée pour continuer...")
    administration(idTournois, nomTournois, password)