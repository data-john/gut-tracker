import pytest
from datetime import datetime
from app.utils import calculate_frequency, calculate_average_consistency, calculate_pain_trends

def test_calculate_frequency():
    logs = [
        {'date_time': '2025-04-28 08:00:00'},
        {'date_time': '2025-04-29 09:00:00'},
        {'date_time': '2025-05-01 10:00:00'},
        {'date_time': '2025-05-01 11:00:00'},
        {'date_time': '2025-05-05 11:00:00'},
    ]
    result = calculate_frequency(logs)
    assert result == {
        datetime(2025, 4, 28).date(): 4,  # Week starting 28 April
        datetime(2025, 5, 5).date(): 1,  # Week starting 5 May
    }

def test_calculate_average_consistency():
    logs = [
        {'consistency': '3'},
        {'consistency': '4'},
        {'consistency': '5'},
    ]
    result = calculate_average_consistency(logs)
    assert result == 4.0

def test_calculate_pain_trends():
    logs = [
        {'pain': 'Mild Pain while passing'},
        {'pain': 'Sharp pain while passing'},
        {'pain': 'Mild Pain while passing'},
    ]
    result = calculate_pain_trends(logs)
    assert result == {
        'Mild Pain while passing': 2,
        'Sharp pain while passing': 1,
    }