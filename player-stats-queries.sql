-- INSERT INTEGERO Bath_vs_Harlequins
-- VALUES ('Finn', 'Russell');

-- DELETE FROM games

-- # Table schemas
-- CREATE TABLE games (
--             game_id INTEGER,
--             game_name TEXT,
--             home_id INTEGER,
--             away_id INTEGER,
--             PRIMARY KEY (game_id),
--             FOREIGN KEY (home_id) REFERENCES teams(team_id),
--             FOREIGN KEY (away_id) REFERENCES teams(team_id)
--             );

-- CREATE TABLE teams (
--             team_id INTEGER PRIMARY KEY AUTOINCREMENT,
--             team_name TEXT
--         );

-- CREATE TABLE players (
--             player_id INTEGER PRIMARY KEY AUTOINCREMENT,
--             player_name TEXT,
--             position TEXT,
--             team_id INTEGER,
--             FOREIGN KEY (team_id) REFERENCES teams(team_id)
--             );

-- CREATE TABLE stats (
--                 player_id,
--                 game_id,
--                 penalties INTEGER,
--                 conversions INTEGER,
--                 carries INTEGER,
--                 kicks INTEGER,
--                 passes INTEGER,
--                 metres_carried INTEGER,
--                 line_breaks INTEGER,
--                 offloads INTEGER,
--                 defenders_beaten INTEGER,
--                 try_assists INTEGER,
--                 tries INTEGER,
--                 turnovers_lost INTEGER,
--                 carries_per_minute FLOAT,
--                 tackles_made INTEGER,
--                 tackles_missed INTEGER,
--                 tackles_completed INTEGER,
--                 dominant_tackles INTEGER,
--                 turnovers_won INTEGER,
--                 ruck_turnovers INTEGER,
--                 lineouts_won INTEGER,
--                 tackles_per_minute FLOAT,
--                 red_cards INTEGER,
--                 yellow_cards INTEGER
--                 penalties_conceded INTEGER,
--                 FOREIGN KEY (player_id) REFERENCES players(player_id),
--                 FOREIGN KEY (game_id) REFERENCES games(game_id)             
--                 );

-- INSERT INTEGERO teams (team_id, team_name)
-- VALUES(?, ?)

-- SELECT player_id FROM players WHERE player_name LIKE '%Carreras' AND team_id IN 
--         (SELECT team_id FROM teams WHERE team_name = 'gloucester') 
--         AND player_id IN (SELECT player_id FROM players 
--         WHERE position = 'Centre' or position = 'Scrum Half' 
--         or position = 'Full Back' 
--         or position = 'Fly Half'
--         or position = 'Inside Centre'
--         or position = 'Outside Centre');

-- DELETE FROM games;
-- DELETE FROM stats;
-- SELECT * FROM players WHERE player_name LIKE '%Louis Schreuder%';
-- SELECT carries, player_name FROM stats, players WHERE players.player_id = stats.player_id;
-- SELECT player_name, team_name FROM players, teams WHERE players.team_id = teams.team_id

SELECT * FROM stats JOIN players WHERE stats.player_id = players.player_id;
-- UPDATE stats SET carries = 9 WHERE game_id = 939009 AND player_id = 140;