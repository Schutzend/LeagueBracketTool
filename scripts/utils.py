import os, random, string, platform

def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def generate_idTournoi():    
    while True:
        idTournois = f"LOL{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"

        if not os.path.exists(get_database_path(idTournois)):
            return idTournois

def generate_password():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

def get_database_path(idTournois):
    return f"databases/{idTournois}.db"

import csv
import os

def get_idTournois_from_csv():
    file_path = os.path.join("import", "tournois.csv")
    
    if not os.path.exists(file_path):
        print("Fichier 'import/tournois.csv' introuvable.")
        return None

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                return row.get("idTournois")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
        return None

def get_nomTournois_from_csv():
    file_path = os.path.join("import", "tournois.csv")
    
    if not os.path.exists(file_path):
        print("Fichier 'import/tournois.csv' introuvable.")
        return None

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                return row.get("nomTournois")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
        return None
    
def get_password_from_csv():
    file_path = os.path.join("import", "tournois.csv")
    
    if not os.path.exists(file_path):
        print("Fichier 'import/tournois.csv' introuvable.")
        return None

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                return row.get("password")
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")
        return None