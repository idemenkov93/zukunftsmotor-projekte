import requests

def hole_externe_ip():
    try:
        antwort = requests.get("https://api.ipify.org?format=json")
        daten = antwort.json()
        return daten["ip"]
    except requests.exceptions.RequestException:
        return None

def hole_standort(ip):
    try:
        antwort = requests.get(f"http://ip-api.com/json/{ip}")
        daten = antwort.json()
        return daten
    except requests.exceptions.RequestException:
        return None
