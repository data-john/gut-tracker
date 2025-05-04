from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import logging
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from datetime import datetime, timedelta
from calendar import monthrange
from app.models import get_bowel_movements, insert_bowel_movement
from app.utils import calculate_frequency, calculate_average_consistency, calculate_pain_trends
import matplotlib.pyplot as plt


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
        self.manager.current = 'calendar'  # Navigate to the calendar view

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
        home_button = Button(text='Home', size_hint=(1, 0.1))
        home_button.bind(on_press=self.go_home)
        layout.add_widget(home_button)

        self.add_widget(layout)

    def populate_calendar(self):
        # Get the current date
        # today = datetime(2025, 5, 3)  # Fixed date for consistency
        today = datetime.today()  # Fixed date for consistency
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
            logging.warning(f"Logs for {day}: {logs}")

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

    def get_logs_by_date(self, date:datetime):
        # Placeholder function to simulate fetching logs for a specific date
        # Replace this with an actual database query
        logs = get_bowel_movements()
        date_logs = []
        for log in logs:
            log_date = datetime.strptime(log["date_time"], '%Y-%m-%d %H:%M:%S')
            if log_date.date() == date.date():
                # return [{'consistency': log[2], 'blood_presence': log[3], 'pain': log[4]}]
                date_logs.append(log)
        return date_logs

    def view_entry(self, instance):
        # Display a popup with log details for the selected day
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.scrollview import ScrollView

        # Parse the date from the button text
        selected_date = datetime.strptime(instance.text, '%d %b')
        selected_date = selected_date.replace(year=datetime.today().year)  # Add the current year

        # Fetch logs for the selected date
        logs = self.get_logs_by_date(selected_date)

        # Create a layout for the popup content
        content_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        if logs:
            for log in logs:
                log_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=100)

                # Extract time from the log's date_time
                log_time = datetime.strptime(log['date_time'], '%Y-%m-%d %H:%M:%S').strftime('%H:%M')

                # Add time on the left
                log_row.add_widget(Label(text=log_time, size_hint_x=0.2, halign='left', valign='middle'))

                # Add details on the right
                log_details = f"Consistency: {log['consistency']}\nBlood Presence: {log['blood_presence']}\nPain: {log['pain']}\nStraining: {log['straining']}\nSymptoms: {log['symptoms']}"
                log_row.add_widget(Label(text=log_details, size_hint_x=0.8, halign='left', valign='middle'))

                content_layout.add_widget(log_row)
        else:
            content_layout.add_widget(Label(text="No logs for this day.", size_hint_y=None, height=40))

        # Add a scroll view to handle multiple logs
        scroll_view = ScrollView()
        scroll_view.add_widget(content_layout)

        # Create and open the popup
        popup = Popup(title=f"Logs for {instance.text}",
                      content=scroll_view,
                      size_hint=(0.8, 0.8))
        popup.open()

    def go_home(self, _):
        print("Going to the home screen")
        self.manager.current = 'home'
    
    def on_enter(self):
        # Clear the existing calendar grid to avoid duplication
        self.calendar_grid.clear_widgets()

        # Add day headers again
        for day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
            self.calendar_grid.add_widget(Label(text=day, bold=True, size_hint_y=None, height=40))

        # Repopulate the calendar with updated data
        self.populate_calendar()
        
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Button to go to Calendar View
        calendar_button = Button(text='View Calendar', size_hint=(1, 0.2))
        calendar_button.bind(on_press=self.go_to_calendar)
        layout.add_widget(calendar_button)

        # Button to go to Add Log
        add_log_button = Button(text='Add Log', size_hint=(1, 0.2))
        add_log_button.bind(on_press=self.go_to_add_log)
        layout.add_widget(add_log_button)

        # Button to go to Analytics (not implemented yet)
        analytics_button = Button(text='View Analytics', size_hint=(1, 0.2))
        analytics_button.bind(on_press=self.go_to_analytics)
        layout.add_widget(analytics_button)

        self.add_widget(layout)

    def go_to_calendar(self, _):
        self.manager.current = 'calendar'

    def go_to_add_log(self, _):
        self.manager.current = 'log'
    
    def go_to_analytics(self, _):
        self.manager.current = 'analytics'


class AnalyticsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Title
        layout.add_widget(Label(text='Analytics', font_size=24, size_hint=(1, 0.1)))

        # Scrollable view for analytics
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.analytics_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        self.analytics_content.bind(minimum_height=self.analytics_content.setter('height'))
        scroll_view.add_widget(self.analytics_content)
        layout.add_widget(scroll_view)

        # Back Button
        back_button = Button(text='Back', size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_home)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_enter(self):
        # Clear previous analytics content
        self.analytics_content.clear_widgets()

        # Fetch logs from the database
        logs = get_bowel_movements()

        # Calculate metrics
        frequency = calculate_frequency(logs)
        average_consistency = calculate_average_consistency(logs)
        pain_trends = calculate_pain_trends(logs)

        # Display metrics
        self.analytics_content.add_widget(Label(text=f'Frequency (Bowel Movements per Week): {frequency}', size_hint_y=None, height=40))
        self.analytics_content.add_widget(Label(text=f'Average Consistency: {average_consistency:.2f}', size_hint_y=None, height=40))
        self.analytics_content.add_widget(Label(text=f'Pain Trends: {pain_trends}', size_hint_y=None, height=40))

        # Add a graph for consistency trends
        self.add_consistency_graph(logs)

    def add_consistency_graph(self, logs):
        try:
            # Prepare data for the graph
            dates = [datetime.strptime(log['date_time'], '%Y-%m-%d %H:%M:%S') for log in logs]
            consistencies = [int(log['consistency']) for log in logs]

            # Sort data by date
            sorted_data = sorted(zip(dates, consistencies), key=lambda x: x[0])
            dates, consistencies = zip(*sorted_data)

            # Create a matplotlib figure
            fig, ax = plt.subplots()
            ax.plot(dates, consistencies, marker='o', linestyle='-', color='b')
            ax.set_title('Consistency Trends')
            ax.set_xlabel('Date')
            ax.set_ylabel('Consistency (1-7)')
            ax.grid(True)

            logging.warning("[DEBUG] Matplotlib figure created successfully.")

            # Add the graph to the Kivy layout with explicit size hints
            graph_widget = FigureCanvasKivyAgg(fig)
            graph_widget.size_hint = (1, None)
            graph_widget.height = 400  # Set a fixed height for better visibility
            self.analytics_content.add_widget(graph_widget)
            logging.warning("[DEBUG] Graph widget added to the layout successfully.")
        except Exception as e:
            logging.error(f"[ERROR] Failed to add consistency graph: {e}")

    def go_home(self, _):
        self.manager.current = 'home'