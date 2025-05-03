import sqlite3

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
            symptoms TEXT NOT NULL
        )
    ''')

    connection.commit()
    connection.close()

# Call the function to initialize the database
init_db()