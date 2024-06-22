import pandas as pd
import sqlite3

# f = open('C:/Users/tomho/Desktop/Projects/Rugby-App/player-stats.csv', 'w')

# connection = sqlite3.connect('C:/Users/tomho/Desktop/Projects/player-stats.db')
# cursor = connection.cursor()

# cursor.execute('SELECT * FROM stats')

# colnames = [desc[0] for desc in cursor.description]

# while True:
#     df = pd.DataFrame(cursor.fetchall())
#     if len(df) == 0:
#         break
#     else:
#         df.to_csv(f, header=colnames)

# f.close()
# cursor.close()
# connection.close()

df = pd.read_csv('player-stats.csv')
print(df.head())