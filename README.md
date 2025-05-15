# LeagueBracketTool Documentation

LeagueBracketTool is a web application designed for managing tournaments, including team and player management, match generation, and tournament progression. It provides both a public view for spectators and an admin interface for tournament organizers.

## Dependencies

The application requires the following Python package:

- **Flask**: A lightweight WSGI web application framework.

All dependencies are included in the provided Python environment.

## Installation Procedure

Follow these steps to set up and run the LeagueBracketTool application on GNU/Linux:

1. **Clone or Download the Project**: Ensure you have the project files in a local directory.

2. **Navigate to the Project Directory**: Open a terminal and change to the project directory:

   ```bash
   cd /path/to/LeagueBracketTool
   ```

3. **Set Execution Permissions for the Launch Script**: If the `launch.sh` script is not executable, run:

   ```bash
   chmod +x launch.sh
   ```

4. **Run the Application**: Execute the launch script to start the Flask development server:

   ```bash
   ./launch.sh
   ```

   This script activates the pre-configured Python environment with all dependencies installed and starts the server.

5. **Access the Application**: Open a web browser and navigate to:

   ```plaintext
   http://127.0.0.1:5000/
   ```

   This URL displays the main menu, where you can enter a tournament ID. The menu includes two buttons:

   - **Accéder au Tournoi**: Access the public view of the tournament.
   - **Connexion Admin**: Access the admin interface (requires a password).

## Configuration

- **No Additional Configuration Required**: The project includes a pre-configured Python environment with all dependencies installed. A sample database is also pre-created and populated with data for immediate use.

- **Database Path**: The application stores SQLite databases in the `databases/` directory, with each tournament having its own database file (e.g., `databases/LOL026.db`).

- **Sample Tournament Access**: A sample tournament is provided for testing:

  - **Tournament ID**: `LOL026`
  - **Admin Password**: `TUExkwJW`
  - **Access Instructions**:
    - **Public Interface**: Enter `LOL026` on the main page and click **Accéder au Tournoi**.
    - **Admin Interface**: Enter `LOL026` on the main page, click **Connexion Admin**, and use the password `TUExkwJW`.

## Database Initialization

The application uses SQLite databases to store tournament data. A pre-existing database (`LOL026.db`) is included with sample data for immediate use. To access it:

- **Public Interface**:
  - On the main page (`http://127.0.0.1:5000/`), enter the tournament ID `LOL026` and click **Accéder au Tournoi**.
- **Admin Interface**:
  - On the main page, enter the tournament ID `LOL026`, click **Connexion Admin**, and enter the password `TUExkwJW`.

To create a new tournament database:

1. From the main page, click **Créer un Nouveau Tournoi** (URL: `http://127.0.0.1:5000/create`).
2. Enter a tournament name and submit the form.
3. The application will automatically generate a unique tournament ID (e.g., `LOL123`) and a password, create a new SQLite database in the `databases/` directory, and redirect you to the admin interface.

The database schema includes the following tables:

- `tournois`: Stores tournament details (ID, name, password).
- `equipe`: Stores team details (team number, name).
- `joueur`: Stores player details (player ID, pseudonym, team number).
- `matchs`: Stores match details (match ID, blue team, red team, status, winner, phase).

## Web URLs

- **Main Page**: `http://127.0.0.1:5000/`

  - Displays a form to enter a tournament ID with buttons to access the public view or admin login.

- **Public Interface**: `http://127.0.0.1:5000/view/<idTournois>`

  - Example: `http://127.0.0.1:5000/view/LOL026`
  - Displays tournament details, including teams, players, and match statuses, accessible to all users without authentication.

- **Admin Interface**: `http://127.0.0.1:5000/admin/<idTournois>`

  - Example: `http://127.0.0.1:5000/admin/LOL026`
  - Requires authentication with the tournament password. Provides tools to manage teams, players, matches, and tournament progression.

- **Create Tournament**: `http://127.0.0.1:5000/create`

  - Allows users to create a new tournament by specifying a name, generating a new database and credentials.

## Usage Instructions

1. **Accessing the Sample Tournament**:

   - On the main page, enter `LOL026` as the tournament ID.
   - For public access, click **Accéder au Tournoi** to view teams, players, and matches.
   - For admin access, click **Connexion Admin**, then enter the password `TUExkwJW` to manage the tournament.

2. **Admin Features**:

   - **Matches**: Generate and manage matches, start/stop matches, and set winners.
   - **Teams**: Create, delete, or rename teams.
   - **Players**: Add, remove, rename, or transfer players between teams.
   - **Search**: Search for teams or players by name.
   - **Account**: View tournament ID and password, and log out.

3. **Public Features**:

   - View lists of teams and players.
   - View match statuses (not started, in progress, or finished) and winners.
   - A golden notification appears when the tournament concludes, announcing the winning team.

4. **Creating a New Tournament**:

   - From the main page, click **Créer un Nouveau Tournoi**.
   - Enter a tournament name and submit.
   - Note the generated tournament ID and password for future access.

## Notes

- The application runs in debug mode by default (`app.run(debug=True)`), which is suitable for development but should be disabled in production.
- Ensure the `databases/` directory has write permissions for creating new tournament databases.
- The sample tournament (`LOL026`) is pre-populated with teams and players for demonstration purposes.
- The application includes a pre-configured Python environment with Flask installed, eliminating the need for manual dependency installation.

For further assistance, refer to the source code or contact the project maintainers.
