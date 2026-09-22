import json
import os
from server_modell import DatenbankServer, Server, Webserver
import shutil

def daten_speichern(server_liste):
    if os.path.exists("infrastruktur.json"):
        shutil.copy("infrastruktur.json", "infrastruktur_backup.json")
    liste_als_dicts = []
    for server in server_liste:
        liste_als_dicts.append(server.__dict__)

    with open("infrastruktur.json", "w", encoding="utf-8") as datei:
        json.dump(liste_als_dicts, datei, indent=4)

def daten_laden():
    server_liste = []
    if os.path.exists("infrastruktur.json"):
        with open("infrastruktur.json", "r", encoding="utf-8") as datei:
            gespeicherte_liste = json.load(datei)
        for eintrag in gespeicherte_liste:
            # Anhand der gespeicherten Felder erkennen, welche Unterklasse es war
            # (Webserver hat "domain", DatenbankServer hat "db_typ") - so gehen
            # domain/ssl_aktiv bzw. db_typ/port beim Neuladen nicht mehr verloren.
            if "domain" in eintrag:
                neuer_server = Webserver(
                    eintrag["name"], eintrag["ip"], eintrag["os"],
                    eintrag["domain"], eintrag["ssl_aktiv"],
                )
            elif "db_typ" in eintrag:
                neuer_server = DatenbankServer(
                    eintrag["name"], eintrag["ip"], eintrag["os"],
                    eintrag["db_typ"], eintrag["port"],
                )
            else:
                neuer_server = Server(eintrag["name"], eintrag["ip"], eintrag["os"])
            neuer_server.status = eintrag["status"]
            server_liste.append(neuer_server)
    return server_liste
