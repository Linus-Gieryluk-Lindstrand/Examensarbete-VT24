# Imorted modules
from flask import Flask, render_template, request
import actions
import threading
import datetime
import time
import psutil

coffee_app = Flask(__name__)

# Global variables
current_temperature = 0
prior_temperature = 0
coffee_counter = 0
coffee_machine_on = False
start_time = 0

mem_counter = 0
total_mem_usage = 0

def print_self_process_info():
    global mem_counter # int
    global total_mem_usage # float

    # Get the current process ID
    pid = psutil.Process().pid

    # Get memory usage
    memory_info = psutil.Process(pid).memory_info()
    mem_usage = memory_info.rss / (1024 * 1024)  # Convert to MB
    total_mem_usage += mem_usage
    mem_counter += 1

    print(f"PID: {pid}, Memory Usage: {mem_usage} MB")
    print(f"Average Memory Usage: {total_mem_usage / mem_counter} MB")

"""
Routes for website.
"""
@coffee_app.route("/")
def home():
    return render_template("index.html")

@coffee_app.route("/get_temperature")
def get_current_temperature():
    global current_temperature
    return {"temperature": current_temperature}

"""
Route for temperature handling
"""
@coffee_app.route("/update_temperature", methods=["POST"])
def process_temperature_update():
    global current_temperature # float
    global prior_temperature # float
    global coffee_machine_on # bool
    global coffee_counter # int
    global start_time # float

    # Receive temperature and convert into a float.
    data = request.json
    current_temperature = float(data["temperature"])
    print("Received temperature:", current_temperature)

    print_self_process_info()

    # Starts timer -> coffee machine is on.
    if current_temperature >= 40 and coffee_machine_on == False:
        start_time = actions.start_timer()
        coffee_machine_on = True
        coffee_counter += 1
        print("Time started")

    # Ends timer -> the coffee has cooled down.
    if current_temperature < 40 and coffee_machine_on == True:
        end_time = actions.end_timer(start_time)
        print("Timer ended")

    # Triggered if: user forgot coffee -> sends pushover notification.
    if prior_temperature >= 40 and current_temperature < 40 and end_time >= 50:
        actions.coffee_pushover_notifier()
        start_time = 0
        coffee_machine_on = False
    # Triggered if: user remembered coffee.
    elif prior_temperature >= 40 and current_temperature < 40 and end_time <= 50:
        start_time = 0
        coffee_machine_on = False
    else:
        print(f"Prior temperature: {prior_temperature}, New temperature: {current_temperature}")

    prior_temperature = current_temperature
    response = "Temperature received successfully"
    return response

# Sends a weekly coffee usage alert notification Sunday at 8:00 PM and resets the coffee counter.
def coffee_weekly_alert():
    global coffee_counter
    while True:
        now = datetime.datetime.now()
        if now.weekday() == 6 and now.hour == 20 and now.minute == 0:
            actions.coffee_mail_notifier(f"You've made coffee {coffee_counter} times this week!")
            print("Email sent.")
            coffee_counter = 0
            time.sleep(60)
        else:
            time.sleep(10)

# Starts the Flask server.
if __name__ == "__main__":
    mail_thread = threading.Thread(target=coffee_weekly_alert)
    mail_thread.start()
    coffee_app.run(host="0.0.0.0")
