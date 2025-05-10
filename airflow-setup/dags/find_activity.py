from airflow.decorators import dag, task
from airflow.models import Variable
from datetime import datetime
import requests

API = "https://bored-api.appbrewery.com/random"

@dag(
    start_date = datetime(2025, 5, 10),
    schedule = "@daily",
    tags = ["activity"],
    catchup = False
)

def find_activity():
    @task
    def get_activity():
        r = requests.get(API, timeout = 10)
        return r.json()
    
    @task
    def write_activity_to_file(response):
        filepath = Variable.get("activity_file")
        with open(filepath, "a") as f:
            f.write(f"Today you will: {response['activity']}\n")

        return filepath
    
    @task
    def read_activity_from_file(filepath):
        with open(filepath, "r") as f:
            print (f.read())

    response = get_activity()
    filepath = write_activity_to_file(response)
    read_activity_from_file(filepath)

# Run activity
find_activity()




