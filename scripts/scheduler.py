import schedule
import time
import os

def run_update_weather():
    os.system('python update_weather.py')

# Schedule the script to run at specific times
schedule.every().day.at("00:00").do(run_update_weather)
schedule.every().day.at("06:00").do(run_update_weather)
schedule.every().day.at("12:00").do(run_update_weather)
schedule.every().day.at("18:00").do(run_update_weather)

while True:
    schedule.run_pending()
    time.sleep(1)