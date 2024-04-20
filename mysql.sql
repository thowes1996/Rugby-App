INSERT INTO Bath_vs_Harlequins
VALUES ('Finn', 'Russell');

DELETE FROM games

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
            team_id INTEGER,
            team_name TEXT,
            PRIMARY KEY (team_id)
        );

CREATE TABLE players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            position TEXT,
            team_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
            );

INSERT INTO teams (team_id, team_name)
VALUES(?, ?)


.schema




