from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox

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

        # Symptoms
        layout.add_widget(Label(text='Symptoms (check all that apply):'))
        self.symptoms = {}
        for symptom in ['Bloating', 'Cramping', 'None']:
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
            'symptoms': [symptom for symptom, checkbox in self.symptoms.items() if checkbox.active]
        }
        print("Form submitted with data:", data)