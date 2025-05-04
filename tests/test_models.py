import pytest
from app.models import init_db, insert_bowel_movement, get_bowel_movements
import sqlite3

# Fixture to set up and tear down the database for testing
@pytest.fixture
def setup_database():
    # Initialize the database
    init_db()
    yield
    # Clean up the database after tests
    connection = sqlite3.connect('gut_tracker.db')
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS bowel_movements')
    connection.commit()
    connection.close()

def test_init_db(setup_database):
    connection = sqlite3.connect('gut_tracker.db')
    cursor = connection.cursor()

    # Check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='bowel_movements'")
    table = cursor.fetchone()

    assert table is not None, "Table 'bowel_movements' should exist"

    connection.close()

def test_insert_bowel_movement(setup_database):
    data = {
        'consistency': 3,
        'color': 'brown',
        'blood_presence': 'no',
        'pain': 'none',
        'straining': 'none',
        'symptoms': ['bloating', 'gas']
    }

    # Insert a bowel movement record
    insert_bowel_movement(data)

    connection = sqlite3.connect('gut_tracker.db')
    cursor = connection.cursor()

    # Verify the record was inserted
    cursor.execute('SELECT * FROM bowel_movements')
    records = cursor.fetchall()

    assert len(records) == 1, "There should be one record in the table"
    assert records[0][2] == data['consistency'], "Consistency should match"
    assert records[0][3] == data['color'], "Color should match"
    assert records[0][4] == data['blood_presence'], "Blood presence should match"
    assert records[0][5] == data['pain'], "Pain should match"
    assert records[0][6] == data['straining'], "Straining should match"
    assert records[0][7] == ','.join(data['symptoms']), "Symptoms should match"

    connection.close()

def test_get_bowel_movements(setup_database):
    # Insert test data
    test_data = {
        'consistency': 4,
        'color': 'Brown',
        'blood_presence': 'None',
        'pain': 'None',
        'straining': 'None',
        'symptoms': ['Bloating', 'Cramping']
    }
    insert_bowel_movement(test_data)

    # Fetch data using the function
    results = get_bowel_movements()

    # Assert that the inserted data is present in the results
    assert len(results) > 0
    assert any(row['consistency'] == test_data['consistency'] and row['color'] == test_data['color'] for row in results)

