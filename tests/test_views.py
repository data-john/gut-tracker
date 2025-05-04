import pytest
from kivy.uix.screenmanager import ScreenManager
from app.views import LogScreen, CalendarView, HomeScreen
from app.models import init_db, insert_bowel_movement
import sqlite3

@pytest.fixture
def log_screen():
    return LogScreen()

def test_initial_state(log_screen):
    # Test initial state of the spinners
    assert log_screen.consistency_spinner.text == 'Select'
    assert log_screen.color_spinner.text == 'Select'
    assert log_screen.blood_spinner.text == 'Select'
    assert log_screen.pain_spinner.text == 'Select'

    # Test initial state of the symptoms checkboxes
    for symptom, checkbox in log_screen.symptoms.items():
        assert not checkbox.active

def test_submit_form_validation(log_screen):
    # Test validation for required fields
    log_screen.submit_form(None)
    # Assuming show_error_message is called, we can't directly test the popup here.
    # Instead, we can mock or check for side effects in a more advanced test setup.

    log_screen.consistency_spinner.text = '1'
    log_screen.color_spinner.text = 'Brown'
    log_screen.blood_spinner.text = 'None'
    log_screen.pain_spinner.text = 'None'

    # Test successful submission
    try:
        log_screen.submit_form(None)
    except Exception as e:
        pytest.fail(f"submit_form raised an exception: {e}")

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

def test_get_logs_by_date(setup_database):
    # Insert test data
    test_data_1 = {
        'consistency': 4,
        'color': 'Brown',
        'blood_presence': 'None',
        'pain': 'None',
        'straining': 'None',
        'symptoms': ['Bloating', 'Cramping']
    }
    test_data_2 = {
        'consistency': 3,
        'color': 'Green',
        'blood_presence': 'Little',
        'pain': 'Mild Pain while passing',
        'straining': 'A little',
        'symptoms': ['Gas']
    }

    insert_bowel_movement(test_data_1)
    insert_bowel_movement(test_data_2)

    # Fetch logs for a specific date
    from datetime import datetime
    specific_date = datetime.now()
    cv = CalendarView()
    results = cv.get_logs_by_date(specific_date)

    # Assert that the logs for the specific date are returned
    assert len(results) > 0, "There should be logs for the specific date"
    assert any(row[2] == test_data_1['consistency'] and row[3] == test_data_1['color'] for row in results), "Test data 1 should be in the results"
    assert any(row[2] == test_data_2['consistency'] and row[3] == test_data_2['color'] for row in results), "Test data 2 should be in the results"