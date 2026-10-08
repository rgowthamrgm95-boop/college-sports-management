from flask import Flask, render_template, request
import psycopg
import os

app = Flask(__name__, template_folder=".")


def create_database():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            player_name TEXT NOT NULL,
            register_number TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            sport TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sports (
            id SERIAL PRIMARY KEY,
            sport_name TEXT NOT NULL,
            coach_name TEXT NOT NULL,
            players_count INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            team_name TEXT NOT NULL,
            sport_name TEXT NOT NULL,
            captain_name TEXT NOT NULL,
            players_count INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            sport_name TEXT NOT NULL,
            team1 TEXT NOT NULL,
            team2 TEXT NOT NULL,
            match_date TEXT NOT NULL,
            venue TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM players")
    player_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sports")
    sport_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM teams")
    team_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM matches")
    match_count = cursor.fetchone()[0]

    print(player_count, sport_count, team_count, match_count)

    conn.close()

    return render_template(
    "index.html",
    player_count=player_count,
    sport_count=sport_count,
    team_count=team_count,
    match_count=match_count
)


@app.route("/players")
def players():
    return render_template("players.html")


@app.route("/register", methods=["POST"])
def register():
    player_name = request.form["player_name"]
    register_number = request.form["register_number"]
    department = request.form["department"]
    year = request.form["year"]
    sport = request.form["sport"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO players
        (player_name, register_number, department, year, sport)
        VALUES (?, ?, ?, ?, ?)
    """, (player_name, register_number, department, year, sport))

    conn.commit()
    conn.close()

    return "Player Registered Successfully!"


@app.route("/player-list")
def player_list():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()

    conn.close()

    return render_template("player_list.html", players=players)

@app.route("/delete-player/<int:player_id>")
def delete_player(player_id):
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))
    conn.commit()

    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()

    conn.close()

    return render_template("player_list.html", players=players)

@app.route("/edit-player/<int:id>")
def edit_player(id):
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players WHERE id = ?", (id,))
    player = cursor.fetchone()

    conn.close()

    return render_template("edit_player.html", player=player)

@app.route("/update-player/<int:id>", methods=["POST"])
def update_player(id):
    player_name = request.form["player_name"]
    register_number = request.form["register_number"]
    department = request.form["department"]
    year = request.form["year"]
    sport = request.form["sport"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE players
        SET player_name = ?,
            register_number = ?,
            department = ?,
            year = ?,
            sport = ?
        WHERE id = ?
    """, (player_name, register_number, department, year, sport, id))

    conn.commit()
    conn.close()

    return "Player Updated Successfully! <br><br><a href='/player-list'>Back to Player List</a>"


@app.route("/sports")
def sports():
    return render_template("sports.html")


@app.route("/add-sport", methods=["POST"])
def add_sport():
    sport_name = request.form["sport_name"]
    coach_name = request.form["coach_name"]
    players_count = request.form["players_count"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sports
        (sport_name, coach_name, players_count)
        VALUES (?, ?, ?)
    """, (sport_name, coach_name, players_count))

    conn.commit()
    conn.close()

    return "Sport Added Successfully!"


@app.route("/sports-list")
def sports_list():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sports")
    sports = cursor.fetchall()

    conn.close()

    return render_template("sports_list.html", sports=sports)

@app.route("/edit-sport/<int:id>")
def edit_sport(id):
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sports WHERE id = ?", (id,))
    sport = cursor.fetchone()

    conn.close()

    return render_template("edit_sport.html", sport=sport)

@app.route("/update-sport/<int:id>", methods=["POST"])
def update_sport(id):
    sport_name = request.form["sport_name"]
    coach_name = request.form["coach_name"]
    players_count = request.form["players_count"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE sports
        SET sport_name = ?,
            coach_name = ?,
            players_count = ?
        WHERE id = ?
    """, (sport_name, coach_name, players_count, id))

    conn.commit()
    conn.close()

    return "Sport Updated Successfully! <br><br><a href='/sports-list'>Back to Sports List</a>"

@app.route("/delete-sport/<int:id>")
def delete_sport(id):
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sports WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return "Sport Deleted Successfully! <br><br><a href='/sports-list'>Back to Sports List</a>"


@app.route("/teams")
def teams():
    return render_template("teams.html")


@app.route("/add-team", methods=["POST"])
def add_team():
    team_name = request.form["team_name"]
    sport_name = request.form["sport_name"]
    captain_name = request.form["captain_name"]
    players_count = request.form["players_count"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teams
        (team_name, sport_name, captain_name, players_count)
        VALUES (?, ?, ?, ?)
    """, (team_name, sport_name, captain_name, players_count))

    conn.commit()
    conn.close()

    return "Team Added Successfully!"


@app.route("/teams-list")
def teams_list():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()

    conn.close()

    return render_template("teams_list.html", teams=teams)

@app.route("/edit-team/<int:id>")
def edit_team(id):
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM teams WHERE id = ?", (id,))
    team = cursor.fetchone()

    conn.close()

    return render_template("edit_team.html", team=team)

@app.route("/update-team/<int:id>", methods=["POST"])
def update_team(id):
    team_name = request.form["team_name"]
    sport_name = request.form["sport_name"]
    captain_name = request.form["captain_name"]
    players_count = request.form["players_count"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE teams
        SET team_name = ?,
            sport_name = ?,
            captain_name = ?,
            players_count = ?
        WHERE id = ?
    """, (team_name, sport_name, captain_name, players_count, id))

    conn.commit()
    conn.close()

    return "Team Updated Successfully! <br><br><a href='/teams-list'>Back to Teams List</a>"
    

@app.route("/delete-team/<int:id>")
def delete_team(id):
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("DELETE FROM teams WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return "Team Deleted Successfully! <br><br><a href='/teams-list'>Back to Teams List</a>"

@app.route("/matches")
def matches():
    return render_template("matches.html")


@app.route("/matches-list")
def matches_list():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM matches")
    matches = cursor.fetchall()

    conn.close()

    return render_template("matches_list.html", matches=matches)

@app.route("/add-match", methods=["POST"])
def add_match():
    sport_name = request.form["sport_name"]
    team1 = request.form["team1"]
    team2 = request.form["team2"]
    match_date = request.form["match_date"]
    venue = request.form["venue"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO matches
        (sport_name, team1, team2, match_date, venue)
        VALUES (?, ?, ?, ?, ?)
    """, (sport_name, team1, team2, match_date, venue))

    conn.commit()
    conn.close()

    return "Match Added Successfully!"

@app.route("/edit-match/<int:id>")
def edit_match(id):
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM matches WHERE id = ?", (id,))
    match = cursor.fetchone()

    conn.close()

    return render_template("edit_match.html", match=match)

@app.route("/update-match/<int:id>", methods=["POST"])
def update_match(id):
    sport_name = request.form["sport_name"]
    team1 = request.form["team1"]
    team2 = request.form["team2"]
    match_date = request.form["match_date"]
    venue = request.form["venue"]

    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE matches
        SET sport_name = ?,
            team1 = ?,
            team2 = ?,
            match_date = ?,
            venue = ?
        WHERE id = ?
    """, (sport_name, team1, team2, match_date, venue, id))

    conn.commit()
    conn.close()

    return "Match Updated Successfully! <br><br><a href='/matches-list'>Back to Matches List</a>"

@app.route("/delete-match/<int:id>")
def delete_match(id):
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("DELETE FROM matches WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return "Match Deleted Successfully! <br><br><a href='/matches-list'>Back to Matches List</a>"
    

create_database()

if __name__ == "__main__":
    app.run(debug=True)
