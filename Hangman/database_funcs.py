import sqlite3
from colorama import Fore, Style

conn = sqlite3.connect('hangman_db.sqlite')
cur = conn.cursor()

def add_word(user_input):
    word = user_input.lower()
    cur.execute('SELECT Word FROM Words WHERE Word = ?',(word,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Words VALUES (?)',(word,))
        conn.commit()
        print("'"+user_input+"'",'Added to Database')
    else:
        print('ERROR: Word Already in Database')

def add_leaderboard(user_name,user_streak):
    cur.execute('SELECT Username FROM Leaderboard WHERE Username = ?',(user_name,))
    row = cur.fetchone()
    if row is None:
        cur.execute('INSERT INTO Leaderboard (Username,Streak) VALUES (?,?)',(user_name,user_streak))
    else:
        cur.execute('UPDATE Leaderboard SET Streak = ? WHERE Username = ?',(user_streak,user_name))
    conn.commit()

def top_five_leaderboard():
    sqlstr = cur.execute('SELECT Username,Streak FROM Leaderboard ORDER BY Streak DESC LIMIT 5')
    for username,streak in sqlstr:
        print(Fore.RED+Style.BRIGHT+username,Fore.RED+Style.BRIGHT+str(streak)+'\n')

def rand_word():
    cur.execute('SELECT * FROM Words ORDER BY RANDOM() LIMIT 1')
    return(cur.fetchone()[0])

def top_five_min():
    cur.execute('SELECT MIN(Streak) FROM (SELECT Streak FROM Leaderboard ORDER BY Streak DESC LIMIT 5)')
    row = cur.fetchone()
    if row is None:
        return(0)
    else:
        return(row[0])
