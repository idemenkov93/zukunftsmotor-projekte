# DCMS Backend Engine - GUI (Flet 1.0)

Grafische Oberflaeche fuer mein Capstone-Projekt [DCMS Backend Engine](../dcms-backend-engine),
gebaut mit [Flet 1.0](https://flet.dev). Statt des Text-Menues im Terminal laesst sich die
Server-Infrastruktur hier ueber ein Fenster verwalten: Server anlegen (generisch, Webserver
oder Datenbankserver), IP bearbeiten, online/offline umschalten, loeschen, den echten
Netzwerkstatus pruefen (externe IP + Standort) und einen Log-Report anzeigen.

Wichtig: Die komplette Businesslogik (`server_modell.py`, `storage.py`, `network.py`,
`logger.py`) ist unveraendert aus dem Original-Projekt uebernommen - die GUI ist nur eine
zusaetzliche Bedienoberflaeche fuer dieselben Module. Einzige Aenderung: ein Bug in
`storage.py` wurde behoben, durch den ein Webserver oder Datenbankserver nach einem
Neustart immer als einfacher Server geladen wurde (Domain/SSL bzw. DB-Typ/Port gingen
verloren). Jetzt erkennt `daten_laden()` den richtigen Typ anhand der gespeicherten Felder.

## Starten

```
pip install "flet[all]" requests
flet run gui_main.py
```

## Dateien

- `gui_main.py` - die Flet-1.0-Oberflaeche (Server-Karten, Dialoge, Event-Handler)
- `main.py` - das urspruengliche Text-Menue (Referenz, unveraendert)
- `server_modell.py`, `storage.py`, `network.py`, `logger.py` - gemeinsame Module fuer
  GUI und Text-Menue
