from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import sqlite3, random
from scripts.utils import generate_idTournoi, generate_password, get_database_path
from scripts.databases import create_database, insert_dataTournoi, list_team, list_players, create_team_db, delete_team_db, edit_team_name_db, add_player_db, remove_player_db, edit_player_name_db, change_team_db
from scripts.databases import set_match_winner, update_match_status, get_active_teams, create_match, generate_tournament_matches, get_team_win_stats

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Nécessaire pour les messages flash et sessions

def get_tournament_name(idTournois):
    """Récupère le nom du tournoi à partir de l'idTournois."""
    db_path = get_database_path(idTournois)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT nomTournois FROM tournois WHERE idTournois = ?", (idTournois,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "Tournoi inconnu"
    except sqlite3.Error:
        return "Tournoi inconnu"

def get_tournament_credentials(idTournois):
    """Récupère l'idTournois et le password à partir de la table tournois."""
    db_path = get_database_path(idTournois)
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT idTournois, password FROM tournois WHERE idTournois = ?", (idTournois,))
        result = cursor.fetchone()
        conn.close()
        return {'idTournois': result[0], 'password': result[1]} if result else {'idTournois': idTournois, 'password': 'Inconnu'}
    except sqlite3.Error:
        return {'idTournois': idTournois, 'password': 'Inconnu'}

def load_admin_data(idTournois):
    """Charge les données des équipes, joueurs, matchs et statistiques pour la page admin."""
    db_path = get_database_path(idTournois)
    teams = []
    players = []
    matches_by_tour = {}
    team_stats = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT numEquipe, nomEquipe FROM equipe")
        teams = cursor.fetchall()
        cursor.execute("""
            SELECT joueur.idJoueur, joueur.pseudo, joueur.numEquipe, equipe.nomEquipe
            FROM joueur
            LEFT JOIN equipe ON joueur.numEquipe = equipe.numEquipe
        """)
        players = cursor.fetchall()
        # Récupérer les matchs par tour
        cursor.execute("SELECT DISTINCT phase FROM matchs ORDER BY phase")
        tours = [row[0] for row in cursor.fetchall()]
        for tour in tours:
            cursor.execute("""
                SELECT idMatch, numEquipeBleu, numEquipeRouge, statut, numEquipeGagnante, phase,
                       e1.nomEquipe AS nomEquipeBleu, e2.nomEquipe AS nomEquipeRouge
                FROM matchs
                LEFT JOIN equipe e1 ON matchs.numEquipeBleu = e1.numEquipe
                LEFT JOIN equipe e2 ON matchs.numEquipeRouge = e2.numEquipe
                WHERE phase = ?
            """, (tour,))
            matches_by_tour[tour] = cursor.fetchall()
        conn.close()
        # Récupérer les statistiques des victoires par équipe
        team_stats = get_team_win_stats(idTournois)
    except sqlite3.Error as e:
        flash(f"Erreur lors de la récupération des données : {e}", "error")
    return teams, players, matches_by_tour, team_stats

def reset_admin_session():
    """Réinitialise la session admin."""
    session.pop('admin_authenticated', None)
    session.pop('idTournois', None)

# Route pour la page d'accueil
@app.route('/', methods=['GET', 'POST'])
def index():
    # Réinitialiser la session admin
    reset_admin_session()
    
    if request.method == 'POST':
        idTournois = request.form.get('idTournois')
        db_path = get_database_path(idTournois)
        if not os.path.exists(db_path):
            flash("Identifiant de tournoi invalide.", "error")
            return render_template('index.html')
        
        # Vérifier quelle action a été soumise
        if 'view_tournament' in request.form:
            return redirect(url_for('view', idTournois=idTournois))
        elif 'admin_login' in request.form:
            return redirect(url_for('admin', idTournois=idTournois))
    
    return render_template('index.html')

# Route pour créer un tournoi
@app.route('/create', methods=['GET', 'POST'])
def create_tournament():
    # Réinitialiser la session admin
    reset_admin_session()
    
    if request.method == 'POST':
        nomTournois = request.form.get('nomTournois')
        if not nomTournois:
            flash("Le nom du tournoi est requis.", "error")
            return render_template('create.html')
        
        idTournois = generate_idTournoi()
        password = generate_password()
        
        # Créer la base de données et insérer les données
        create_database(idTournois)
        insert_dataTournoi(idTournois, nomTournois, password)
        
        # Authentifier automatiquement l'utilisateur
        session['admin_authenticated'] = True
        session['idTournois'] = idTournois
        
        # Charger les données pour la page admin
        teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
        credentials = get_tournament_credentials(idTournois)
        
        flash(f"Tournoi {nomTournois} créé avec succès ! ID: {idTournois}, Mot de passe: {password}. Prenez note du mot de passe", "success")
        return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, 
                             teams=teams, players=players, matches_by_tour=matches_by_tour, 
                             credentials=credentials, team_stats=team_stats, default_tab='account')
    
    return render_template('create.html')

# Route pour la page publique
@app.route('/view/<idTournois>')
def view(idTournois):
    # Réinitialiser la session admin
    reset_admin_session()
    
    db_path = get_database_path(idTournois)
    if not os.path.exists(db_path):
        flash("Tournoi introuvable.", "error")
        return redirect(url_for('index'))
    
    nomTournois = get_tournament_name(idTournois)
    teams, players, matches_by_tour, _ = load_admin_data(idTournois)
    
    return render_template('view.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour)

# Route pour la page d'administration
@app.route('/admin/<idTournois>', methods=['GET', 'POST'])
def admin(idTournois):
    db_path = get_database_path(idTournois)
    if not os.path.exists(db_path):
        flash("Tournoi introuvable.", "error")
        return redirect(url_for('index'))
    
    nomTournois = get_tournament_name(idTournois)
    
    if request.method == 'POST':
        password = request.form.get('password')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM tournois WHERE idTournois = ?", (idTournois,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == password:
            session['admin_authenticated'] = True
            session['idTournois'] = idTournois
            teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
            credentials = get_tournament_credentials(idTournois)
            return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='matches')
        else:
            flash("Mot de passe incorrect.", "error")
            return render_template('admin_login.html', idTournois=idTournois, nomTournois=nomTournois)
    
    if session.get('admin_authenticated') and session.get('idTournois') == idTournois:
        teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
        credentials = get_tournament_credentials(idTournois)
        return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='matches')
    
    return render_template('admin_login.html', idTournois=idTournois, nomTournois=nomTournois)

# Routes pour les actions d'administration
@app.route('/admin/<idTournois>/create_team', methods=['POST'])
def create_team(idTournois):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    nomTournois = get_tournament_name(idTournois)
    nomEquipe = request.form.get('nomEquipe')
    joueurs = [request.form.get(f'joueur{i}') for i in range(1, 6)]
    
    if not nomEquipe or not all(joueurs):
        flash("Tous les champs sont requis.", "error")
    else:
        try:
            conn = sqlite3.connect(get_database_path(idTournois))
            cursor = conn.cursor()
            cursor.execute("INSERT INTO equipe (nomEquipe) VALUES (?)", (nomEquipe,))
            numEquipe = cursor.lastrowid
            for pseudo in joueurs:
                cursor.execute("INSERT INTO joueur (pseudo, numEquipe) VALUES (?, ?)", (pseudo, numEquipe))
            conn.commit()
            conn.close()
            flash(f"Équipe {nomEquipe} créée avec succès.", "success")
        except sqlite3.Error as e:
            flash(f"Erreur lors de la création : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='teams')

@app.route('/admin/<idTournois>/delete_team', methods=['POST'])
def delete_team(idTournois):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    nomTournois = get_tournament_name(idTournois)
    numEquipe = request.form.get('numEquipe')
    try:
        delete_team_db(idTournois, numEquipe)
        flash("Équipe supprimée avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de la suppression : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='teams')

@app.route('/admin/<idTournois>/edit_team_name', methods=['POST'])
def edit_team_name(idTournois):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    nomTournois = get_tournament_name(idTournois)
    numEquipe = request.form.get('numEquipe')
    newNomEquipe = request.form.get('newNomEquipe')
    try:
        conn = sqlite3.connect(get_database_path(idTournois))
        cursor = conn.cursor()
        cursor.execute("UPDATE equipe SET nomEquipe = ? WHERE numEquipe = ?", (newNomEquipe, numEquipe))
        conn.commit()
        conn.close()
        flash("Nom de l'équipe mis à jour.", "success")
    except sqlite3.Error as e:
        flash(f"Erreur lors de la modification : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='teams')

@app.route('/admin/<idTournois>/add_player', methods=['POST'])
def add_player(idTournois):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    nomTournois = get_tournament_name(idTournois)
    pseudo = request.form.get('pseudo')
    numEquipe = request.form.get('numEquipe')
    try:
        add_player_db(idTournois, pseudo, numEquipe)
        flash(f"Joueur {pseudo} ajouté avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de l'ajout : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='players')

@app.route('/admin/<idTournois>/remove_player', methods=['POST'])
def remove_player(idTournois):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    nomTournois = get_tournament_name(idTournois)
    numJoueur = request.form.get('numJoueur')
    try:
        remove_player_db(idTournois, numJoueur)
        flash("Joueur supprimé avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de la suppression : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='players')

@app.route('/admin/<idTournois>/edit_player_name', methods=['POST'])
def edit_player_name(idTournois):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    nomTournois = get_tournament_name(idTournois)
    numJoueur = request.form.get('numJoueur')
    newPseudo = request.form.get('newPseudo')
    try:
        conn = sqlite3.connect(get_database_path(idTournois))
        cursor = conn.cursor()
        cursor.execute("UPDATE joueur SET pseudo = ? WHERE idJoueur = ?", (newPseudo, numJoueur))
        conn.commit()
        conn.close()
        flash("Pseudo du joueur mis à jour.", "success")
    except sqlite3.Error as e:
        flash(f"Erreur lors de la modification : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='players')

@app.route('/admin/<idTournois>/change_team', methods=['POST'])
def change_team(idTournois):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    nomTournois = get_tournament_name(idTournois)
    numJoueur = request.form.get('numJoueur')
    newNumEquipe = request.form.get('newNumEquipe')
    try:
        change_team_db(idTournois, numJoueur, newNumEquipe)
        flash("Joueur transféré avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors du changement d'équipe : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='players')

@app.route('/launch_matches/<idTournois>', methods=['POST'])
def launch_matches(idTournois):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    try:
        tour = generate_tournament_matches(idTournois)
        flash(f"Matchs du Tour {tour} générés avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de la génération des matchs : {e}", "error")
        teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
        nomTournois = get_tournament_name(idTournois)
        credentials = get_tournament_credentials(idTournois)
        return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='matches')
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    nomTournois = get_tournament_name(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='matches')

@app.route('/admin/<idTournois>/start_match/<int:idMatch>', methods=['POST'])
def start_match(idTournois, idMatch):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    try:
        update_match_status(idTournois, idMatch, "en cours")
        flash(f"Match {idMatch} démarré.", "success")
    except Exception as e:
        flash(f"Erreur lors du démarrage du match : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    nomTournois = get_tournament_name(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='matches')

@app.route('/admin/<idTournois>/stop_match/<int:idMatch>', methods=['POST'])
def stop_match(idTournois, idMatch):
    if not session.get('admin_authenticated') or session.get('idTournois') != idTournois:
        flash("Veuillez vous connecter à l'administration.", "error")
        return redirect(url_for('admin', idTournois=idTournois))
    
    numEquipeGagnante = request.form.get('numEquipeGagnante')
    try:
        set_match_winner(idTournois, idMatch, numEquipeGagnante)
        flash(f"Match {idMatch} terminé. Équipe {numEquipeGagnante} gagnante.", "success")
        
        # Vérifier si tous les matchs du tour sont terminés
        db_path = get_database_path(idTournois)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT phase FROM matchs WHERE idMatch = ?", (idMatch,))
        current_tour = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM matchs WHERE phase = ? AND statut != ?", (current_tour, "terminé"))
        unfinished_matches = cursor.fetchone()[0]
        conn.close()
        
        if unfinished_matches == 0:
            # Générer le tour suivant
            active_teams = get_active_teams(idTournois)
            winners = []
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT numEquipeGagnante FROM matchs WHERE phase = ?", (current_tour,))
            winners = [row[0] for row in cursor.fetchall() if row[0]]
            conn.close()
            
            if len(winners) == 1:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT nomEquipe FROM equipe WHERE numEquipe = ?", (winners[0],))
                winner_name = cursor.fetchone()[0]
                conn.close()
                flash(f"L'équipe {winner_name} a gagné le tournoi !", "success")
            elif len(winners) >= 2:
                random.shuffle(winners)
                next_tour = int(current_tour.split()[1]) + 1
                for i in range(0, len(winners) - 1, 2):
                    create_match(idTournois, winners[i], winners[i + 1], next_tour)
                flash(f"Matchs du Tour {next_tour} générés.", "success")
                
    except Exception as e:
        flash(f"Erreur lors de l'arrêt du match : {e}", "error")
    
    teams, players, matches_by_tour, team_stats = load_admin_data(idTournois)
    nomTournois = get_tournament_name(idTournois)
    credentials = get_tournament_credentials(idTournois)
    return render_template('admin.html', idTournois=idTournois, nomTournois=nomTournois, teams=teams, players=players, matches_by_tour=matches_by_tour, credentials=credentials, team_stats=team_stats, default_tab='matches')

if __name__ == '__main__':
    app.run(debug=True)