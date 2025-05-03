from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from app.models import insert_bowel_movement
import logging
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from datetime import datetime, timedelta
from calendar import monthrange
from app.models import get_bowel_movements

class LogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Consistency
        layout.add_widget(Label(text='Consistency (1-7):'))
        self.consistency_spinner = Spinner(
            text='Select',
            values=('1', '2', '3', '4', '5', '6', '7')
        )
        layout.add_widget(self.consistency_spinner)

        # Color
        layout.add_widget(Label(text='Color:'))
        self.color_spinner = Spinner(
            text='Select',
            values=('Brown', 'Green', 'Yellow', 'Black')
        )
        layout.add_widget(self.color_spinner)

        # Blood Presence
        layout.add_widget(Label(text='Blood Presence:'))
        self.blood_spinner = Spinner(
            text='Select',
            values=('None', 'Little', 'Lots')
        )
        layout.add_widget(self.blood_spinner)

        # Pain
        layout.add_widget(Label(text='Pain:'))
        self.pain_spinner = Spinner(
            text='Select',
            values=(
                'None', 'Itching', 'Mild Pain while passing',
                'Mild Pain while passing and afterwards',
                'Constant throbbing pain', 'Sharp pain while passing',
                'Sharp pain while passing and afterwards'
            )
        )
        layout.add_widget(self.pain_spinner)

        # Straining
        layout.add_widget(Label(text='Straining:'))
        self.strain_spinner = Spinner(
            text='Select',
            values=('None', 'Little', 'Lots')
        )
        layout.add_widget(self.strain_spinner)

        # Symptoms
        layout.add_widget(Label(text='Symptoms (check all that apply):'))
        self.symptoms = {}
        for symptom in ['Bloating', 'Cramping', 'Headache', 'Pus present', 'Nausea', 'Dizziness']:
            symptom_layout = BoxLayout(orientation='horizontal')
            symptom_checkbox = CheckBox()
            self.symptoms[symptom] = symptom_checkbox
            symptom_layout.add_widget(symptom_checkbox)
            symptom_layout.add_widget(Label(text=symptom))
            layout.add_widget(symptom_layout)

        # Submit Button
        submit_button = Button(text='Submit', size_hint=(1, 0.2))
        submit_button.bind(on_press=self.submit_form)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def submit_form(self, _):
        # Collect data from the form
        data = {
            'consistency': self.consistency_spinner.text,
            'color': self.color_spinner.text,
            'blood_presence': self.blood_spinner.text,
            'pain': self.pain_spinner.text,
            'straining': self.strain_spinner.text,
            'symptoms': [symptom for symptom, checkbox in self.symptoms.items() if checkbox.active]
        }

        # Validate required fields
        if data['consistency'] == 'Select':
            self.show_error_message("Please select a consistency value.")
            return
        if data['color'] == 'Select':
            self.show_error_message("Please select a color.")
            return
        if data['blood_presence'] == 'Select':
            self.show_error_message("Please select a blood presence value.")
            return
        if data['pain'] == 'Select':
            self.show_error_message("Please select a pain level.")
            return
        if data['straining'] == 'Select':
            self.show_error_message("Please select a straining value.")
            return

        # Save the data to the database
        # logging.warning(f"Submitting form with data: {data}")
        try:
            insert_bowel_movement(data)
            print("Form submitted with data:", data)
        except Exception as e:
            self.show_error_message(f"An error occurred: {str(e)}")

    def show_error_message(self, message):
        # Display an error message to the user
        from kivy.uix.popup import Popup
        popup = Popup(title='Error',
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

class CalendarView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        layout.add_widget(Label(text='Log History Calendar', font_size=24, size_hint=(1, 0.1)))

        # Calendar Grid
        self.calendar_grid = GridLayout(cols=7, spacing=5, size_hint_y=None)
        self.calendar_grid.bind(minimum_height=self.calendar_grid.setter('height'))

        # Add day headers with proper height
        for day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
            self.calendar_grid.add_widget(Label(text=day, bold=True, size_hint_y=None, height=40))

        # Populate calendar with days
        self.populate_calendar()

        # Scrollable view for the calendar
        scroll_view = ScrollView(size_hint=(1, 0.8))
        scroll_view.add_widget(self.calendar_grid)
        layout.add_widget(scroll_view)

        # Back Button
        back_button = Button(text='Back', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def populate_calendar(self):
        # Get the current date
        today = datetime(2025, 5, 3)  # Fixed date for consistency
        start_date = today - timedelta(days=30)  # Show the last 30 days

        # Calculate the starting day of the week for alignment
        first_day_of_week = start_date.weekday()  # 0 = Monday, 6 = Sunday
        offset = (first_day_of_week + 1) % 7  # Adjust to start with Sunday

        # Add empty labels for alignment
        for _ in range(offset):
            self.calendar_grid.add_widget(Label(text="", size_hint_y=None, height=40))

        # Add day buttons
        for i in range(31):
            day = start_date + timedelta(days=i)
            # Fetch logs for the day (placeholder function, replace with actual database query)
            logs = self.get_logs_by_date(day)

            # Determine button color based on logs
            if logs:
                consistency_values = [log['consistency'] for log in logs if 'consistency' in log]
                blood_presence = any(log['blood_presence'] != 'None' for log in logs)
                pain_high = any(log['pain'] in ['Constant throbbing pain', 'Sharp pain while passing', 'Sharp pain while passing and afterwards'] for log in logs)

                if blood_presence or pain_high:
                    button_color = (1, 0, 0, 1)  # Red
                elif any(3 <= int(consistency) <= 4 for consistency in consistency_values):
                    button_color = (0, 1, 0, 1)  # Green
                else:
                    button_color = (1, 1, 1, 1)  # Default white
            else:
                button_color = (1, 1, 1, 1)  # Default white

            day_button = Button(text=day.strftime('%d %b'), size_hint_y=None, height=40, background_color=button_color)
            day_button.bind(on_press=self.view_entry)
            self.calendar_grid.add_widget(day_button)

    def get_logs_by_date(self, date):
        # Placeholder function to simulate fetching logs for a specific date
        # Replace this with an actual database query
        logs = get_bowel_movements()
        for log in logs:
            log_date = datetime.strptime(log[1], '%Y-%m-%d %H:%M:%S')
            if log_date.date() == date.date():
                # return [{'consistency': log[2], 'blood_presence': log[3], 'pain': log[4]}]
                return log
        return []

    def view_entry(self, instance):
        # Placeholder for viewing log entries for a specific day
        print(f"Viewing entries for {instance.text}")

    def go_back(self, _):
        # Placeholder for navigating back to the previous screen
        print("Going back to the previous screen")