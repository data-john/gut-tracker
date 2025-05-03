import pytest
from kivy.uix.screenmanager import ScreenManager
from app.views import LogScreen

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