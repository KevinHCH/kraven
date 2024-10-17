import os
import json
import requests
from datetime import datetime

# Define time range
START_HOUR = 9
END_HOUR = 21

# Function to check if the current time is between 09:00 and 21:00 CET
def is_time_to_run():
    current_hour = datetime.now().hour
    return START_HOUR <= current_hour < END_HOUR


def run_spider(target_url, topic_name):
    endpoint = "http://localhost:6800/schedule.json"
    payload = {
        'project': 'default',
        'spider': 'upwork',
        'target_url': target_url,
        'topic_name': topic_name
    }
    response = requests.post(endpoint, data=payload)
    if response.status_code == 200:
        print(f"Scheduled spider for {topic_name} ({target_url})")
    else:
        print(f"Failed to schedule spider for {topic_name} ({target_url}): {response.status_code}")

def main():
    urls_file = "/data/urls.json"
    
    if is_time_to_run():
        # Read and process URLs from urls.json
        if os.path.exists(urls_file):
            with open(urls_file, 'r') as file:
                urls = json.load(file)
                for url_data in urls:
                    name = url_data.get("name")
                    url = url_data.get("url")
                    if name and url:
                        run_spider(url, name)
        else:
            print(f"File {urls_file} not found.")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Not running spider - outside of scheduled hours")

if __name__ == "__main__":
    main()
