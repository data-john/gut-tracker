import sqlite3
import logging

# Initialize the database connection
def init_db():
    connection = sqlite3.connect('gut_tracker.db')
    cursor = connection.cursor()

    # Create a table for bowel movements
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bowel_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            consistency INTEGER NOT NULL,
            color TEXT NOT NULL,
            blood_presence TEXT NOT NULL,
            pain TEXT NOT NULL,
            straining TEXT NOT NULL,
            symptoms TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

def insert_bowel_movement(data):
    connection = sqlite3.connect('gut_tracker.db')
    cursor = connection.cursor()

    # Insert data into the bowel_movements table
    cursor.execute('''
        INSERT INTO bowel_movements (consistency, color, blood_presence, pain, straining, symptoms)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data['consistency'], data['color'], data['blood_presence'], data['pain'], data['straining'], ','.join(data['symptoms'])))

    connection.commit()
    connection.close()

def get_bowel_movements():
    connection = sqlite3.connect('gut_tracker.db')
    cursor = connection.cursor()

    # Retrieve all bowel movements
    cursor.execute('SELECT * FROM bowel_movements')
    rows = cursor.fetchall()

    connection.close()

    logging.warning(f"Fetched bowel movements: {rows}")
    return rows

# Call the function to initialize the database
init_db()