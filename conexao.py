import mysql.connector

def get_connection():
    
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="996240874",
        database="my_game_verse"
    )

