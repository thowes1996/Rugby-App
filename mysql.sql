-- INSERT INTO Bath_vs_Harlequins
-- VALUES ('Finn', 'Russell');

-- DELETE FROM games

-- # Table schemas
CREATE TABLE games (
            game_id INTEGER,
            game_name TEXT,
            home_id INTEGER,
            away_id INTEGER,
            PRIMARY KEY (game_id),
            FOREIGN KEY (home_id) REFERENCES teams(team_id),
            FOREIGN KEY (away_id) REFERENCES teams(team_id)
            );

CREATE TABLE teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT
        );

CREATE TABLE players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            position TEXT,
            team_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
            );

-- INSERT INTO teams (team_id, team_name)
-- VALUES(?, ?)

-- SELECT * FROM games, players WHERE players.team_id = home_id or players.team_id = away_id;

-- SELECT player_name, team_name FROM players, teams WHERE players.team_id = teams.team_id




