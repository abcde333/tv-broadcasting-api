# fill_data.py
import requests
import random
from datetime import date, timedelta
import time
from tqdm import tqdm  # progress bar, install via pip install tqdm

URL = "http://127.0.0.1:8000"
TIMEOUT = 0.1  # pause between requests to avoid server overload

def safe_post(endpoint, payload):
    """
    Send a POST request safely.
    Handles exceptions and prints errors without stopping the script.
    """
    try:
        response = requests.post(f"{URL}/{endpoint}", json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error at {endpoint}: {e}")

#  Satellites
print("Adding Satellites...")
for i in tqdm(range(50), desc="Satellites"):
    payload = {
        "name": f"Satellite {i}",
        "country": f"Country {i}",
        "service_life": random.randint(5, 25),
        "orbit_radius": round(random.uniform(2000, 40000), 2)
    }
    safe_post("satellites", payload)
    time.sleep(TIMEOUT)

# TV Channels 
print("Adding TV Channels...")
for i in tqdm(range(200), desc="TV Channels"):
    payload = {
        "name": f"TVChannel {i}",
        "broadcast_language": random.choice(["EN", "RU", "ES", "FR"]),
        "country": f"Country {random.randint(0, 49)}",
        "company": f"Company {i}",
        "specifics": "General",
        "metadata_json": {
            "rating": random.randint(1, 5),
            "genre": random.choice(["News","Sports","Music","Series"])
        }
    }
    safe_post("tv-channels", payload)
    time.sleep(TIMEOUT)

# Broadcasts 
print("Adding Broadcasts...")
for i in tqdm(range(1000), desc="Broadcasts"):
    payload = {
        "satellite_id": random.randint(1, 50),
        "tv_channel_id": random.randint(1, 200),
        "frequency": round(random.uniform(1000, 12000), 2),
        "coverage_from": random.randint(1, 100),
        "coverage_to": random.randint(101, 500)
    }
    safe_post("broadcasts", payload)
    time.sleep(TIMEOUT)

print("All data loaded successfully!")
