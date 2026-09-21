import logger
from server_modell import Server, Webserver, DatenbankServer
import storage
import network

logger.schreibe_log("INFO", "Programm gestartet")

server_liste = storage.daten_laden()

while True:
    print("[1] Server hinzufügen")
    print("[2] Log-Report anzeigen")
    print("[3] Server löschen")
    print("[4] IP bearbeiten")
    print("[5] System-Status prüfen")
    print("[9] Beenden")
    eingabe = input("Deine Wahl: ")
    try:
        wahl = int(eingabe)
    except ValueError:
        logger.schreibe_log("ERROR", "Ungültige Eingabe (keine Zahl)")
        print("Bitte eine Zahl eingeben!")
        continue

    if wahl == 1:
        name = input("Name des neuen Servers: ")
        ip = input("Bitte gib deine IP-Adresse ein: ")
        os = input("Welches Betriebssystem verwenden Sie?: ")
        typ = input("Möchten Sie einen (1) generischen Server, (2) Webserver oder (3) Datenbankserver anlegen? ")

        if typ == "1":
            neuer_server = Server(name, ip, os)
        elif typ == "2":
            domain = input("Domain: ")
            ssl_aktiv = input("SSL aktiv? (ja/nein): ")
            neuer_server = Webserver(name, ip, os, domain, ssl_aktiv)
        elif typ == "3":
            db_typ = input("DB-Typ: ")
            port = input("Port: ")
            neuer_server = DatenbankServer(name, ip, os, db_typ, port)

        server_liste.append(neuer_server)
        logger.schreibe_log("INFO", f"Server {name} hinzugefügt")

    elif wahl == 2:
        error_counter = 0
        info_counter = 0
        with open("dcms_audit.log", "r", encoding="utf-8") as datei:
            for zeile in datei:
                if "[ERROR]" in zeile:
                    error_counter += 1
                elif "[INFO]" in zeile:
                    info_counter += 1
        print(f"Log-Report: {info_counter} INFO, {error_counter} ERROR")

    elif wahl == 3:
        such_name = input("Name des zu löschenden Servers: ")
        gefunden = None
        for server in server_liste:
            if server.name == such_name:
                gefunden = server

        if gefunden is not None:
            server_liste.remove(gefunden)
            logger.schreibe_log("INFO", f"Server {such_name} gelöscht")
            storage.daten_speichern(server_liste)
        else:
            print("Server nicht gefunden!")

    elif wahl == 4:
        such_name = input("Name des Servers, dessen IP geändert werden soll: ")
        gefunden = None
        for server in server_liste:
            if server.name == such_name:
                gefunden = server

        if gefunden is not None:
            neue_ip = input("Neue IP-Adresse: ")
            gefunden.ip = neue_ip
            logger.schreibe_log("INFO", f"IP von Server {such_name} geändert auf {neue_ip}")
            storage.daten_speichern(server_liste)
        else:
            print("Server nicht gefunden!")

    elif wahl == 5:
        ip = network.hole_externe_ip()
        if ip is not None:
            standort = network.hole_standort(ip)
            if standort is not None:
                print(f"System online. Externe IP: {ip}. Standort: {standort['city']}, {standort['country']}. Provider: {standort['isp']}.")
            else:
                print("Standort konnte nicht ermittelt werden.")
        else:
            print("Keine Internetverbindung verfügbar.")

    elif wahl == 9:
        logger.schreibe_log("INFO", "Beendigungsversuch")
        storage.daten_speichern(server_liste)
        print("Programm wird beendet...")
        break

    else:
        logger.schreibe_log("ERROR", f"Unbekannte Menüoption: {wahl}")
        print("Diese Option gibt es nicht!")
