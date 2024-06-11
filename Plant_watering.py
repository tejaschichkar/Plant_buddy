import datetime
import pickle

class PlantReminder:
    def __init__(self):
        self.plants = {}
        self.load_reminders()

    def add_plant(self, plant_name, watering_schedule):
        self.plants[plant_name] = {'schedule': watering_schedule, 'last_watered': None}

    def check_watering_time(self):
        current_time = datetime.datetime.now().time()
        reminders = []

        for plant, data in self.plants.items():
            schedule = data['schedule']
            last_watered = data['last_watered']

            if current_time >= schedule and (last_watered is None or last_watered < datetime.datetime.now().date()):
                reminders.append(f"Don't forget to water {plant} now!")
                data['last_watered'] = datetime.datetime.now().date()

        return reminders

    def add_new_plant(self):
        plant_name = input("Enter the plant name: ")
        
        if plant_name == "exit":
            return
        else:
            watering_time = input("Enter the watering time (HH:MM format): ")

        try:
            watering_schedule = datetime.datetime.strptime(watering_time, "%H:%M").time()
            self.add_plant(plant_name, watering_schedule)
            print(f"{plant_name} added successfully!")
            self.save_reminders()
        except ValueError:
            print("Invalid time format. Please use HH:MM.")

    def show_and_edit_reminders(self):
        for plant, data in self.plants.items():
            print(f"Plant: {plant}, Watering Time: {data['schedule']}, Last Watered: {data['last_watered']}")

        plant_to_edit = input("Enter the plant name to edit its watering time (or 'exit' to exit): ")

        if plant_to_edit.lower() == 'exit':
            return

        if plant_to_edit in self.plants:
            new_watering_time = input(f"Enter the new watering time for {plant_to_edit} (HH:MM format): ")
            try:
                new_schedule = datetime.datetime.strptime(new_watering_time, "%H:%M").time()
                self.plants[plant_to_edit]['schedule'] = new_schedule
                print(f"Watering time for {plant_to_edit} updated successfully!")
                self.save_reminders()
            except ValueError:
                print("Invalid time format. Please use HH:MM.")
        else:
            print(f"{plant_to_edit} not found in the reminders.")

    def update_watering_status(self):
        for plant in self.plants:
            user_input = input(f"Did you water {plant} today? (yes/no): ").lower()
            if user_input == 'yes':
                self.plants[plant]['last_watered'] = datetime.datetime.now().date()
                self.save_reminders()

    def save_reminders(self):
        with open('plant_reminders.pkl', 'wb') as file:
            pickle.dump(self.plants, file)

    def load_reminders(self):
        try:
            with open('plant_reminders.pkl', 'rb') as file:
                self.plants = pickle.load(file)
        except FileNotFoundError:
            pass

# Example usage:
reminder = PlantReminder()

# Adding plants and their watering schedules
reminder.add_plant("Rose", datetime.time(8, 0))  # Water at 8:00 AM
reminder.add_plant("Fern", datetime.time(12, 30))  # Water at 12:30 PM
reminder.add_plant("Cactus", datetime.time(18, 0))  # Water at 6:00 PM

# User input for adding more plant reminders
reminder.add_new_plant()

# User input for showing or editing existing reminders
reminder.show_and_edit_reminders()

# User input for updating watering status
reminder.update_watering_status()

# Checking for watering time and displaying reminders
reminders = reminder.check_watering_time()
for reminder_text in reminders:
    print(reminder_text)