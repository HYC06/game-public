import sqlite3
import pygame

def character_finder(username):
    conn = sqlite3.connect('Account database.db')
    c = conn.cursor()

    char = c.execute(f"""
            SELECT Character
            FROM Game
            WHERE Username = '{username}'
            """)
    character_type = str(c.fetchone())[2:3]
    return character_type

def get_rounds(username):
    conn = sqlite3.connect('Account database.db')
    c = conn.cursor()

    #fetches and returns a single digit from the rounds field 
    #specified with the username
    round = c.execute(f"""
            SELECT Rounds
            FROM Game
            WHERE Username = '{username}'
            """)
    rounds = c.fetchone()[0]
    return rounds

def set_rounds(username, round):
    conn = sqlite3.connect('Account database.db')
    c = conn.cursor()

    #updates the rounds field specified with the username
    round = c.execute(f"""
            UPDATE Game
            SET Rounds = '{round}' 
            WHERE Username = '{username}'
            """)
    
    conn.commit()

def set_point(username,new_score):
    conn = sqlite3.connect('Account database.db')
    c = conn.cursor()

    score = c.execute(f"""
            SELECT Score
            FROM Game
            WHERE Username = '{username}'
            """)
    score = c.fetchone()[0]

    #updates high score if their new score beats their record
    if new_score > score:
        c.execute(f"""
            UPDATE Game
            SET Score = '{new_score}' 
            WHERE Username = '{username}'
            """)
        
    #saves changes
    conn.commit()

def get_points(username):
    conn = sqlite3.connect('Account database.db')
    c = conn.cursor()

    #fetches and returns score specified with the username
    point = c.execute(f"""
            SELECT Score
            FROM Game
            WHERE Username = '{username}'
            """)
    points = c.fetchone()[0]
    return points

if __name__ == "__main__":
    character_finder()
    get_rounds()
    set_rounds()
    set_point()
    get_points()
