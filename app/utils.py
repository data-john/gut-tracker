from collections import defaultdict, Counter
from datetime import datetime, timedelta

def calculate_frequency(logs):
    """
    Calculate the number of bowel movements per week.
    :param logs: List of log dictionaries with 'date_time' field.
    :return: Dictionary with week start dates as keys and counts as values.
    """

    frequency = defaultdict(int)
    for log in logs:
        log_date = datetime.strptime(log['date_time'], '%Y-%m-%d %H:%M:%S')
        week_start = log_date - timedelta(days=log_date.weekday())
        frequency[week_start.date()] += 1

    return dict(frequency)

def calculate_average_consistency(logs):
    """
    Calculate the mean Bristol score over a period.
    :param logs: List of log dictionaries with 'consistency' field.
    :return: Float representing the average consistency.
    """
    consistencies = [int(log['consistency']) for log in logs if log['consistency'].isdigit()]
    if not consistencies:
        return 0
    return sum(consistencies) / len(consistencies)

def calculate_pain_trends(logs):
    """
    Calculate the average pain level over time.
    :param logs: List of log dictionaries with 'pain' field.
    :return: Dictionary with pain levels as keys and their frequencies as values.
    """

    pain_levels = [log['pain'] for log in logs if log['pain']]
    return dict(Counter(pain_levels))