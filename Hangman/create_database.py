import sqlite3
from urllib.request import urlopen

conn = sqlite3.connect('hangman_db.sqlite')
cur = conn.cursor()

cur.executescript('''
CREATE TABLE IF NOT EXISTS Words (Word TEXT);
CREATE TABLE IF NOT EXISTS Leaderboard (Username TEXT, Streak INTEGER);
''')

word_lst = urlopen('http://www.mieliestronk.com/corncob_lowercase.txt').read().decode().split()

cur.execute('SELECT Word FROM Words')
row = cur.fetchone()
if row is None:
    for count,word in enumerate(word_lst):
        cur.execute('INSERT INTO Words (Word) VALUES (?)',(word,))
        if count % 15 == 0:
            conn.commit()
conn.commit()
conn.close()