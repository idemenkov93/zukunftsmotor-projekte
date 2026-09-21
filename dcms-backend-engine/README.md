# DCMS Backend Engine

Terminalbasiertes Python-Tool zur Verwaltung einer kleinen Server-Infrastruktur.
Entstanden als 4-Tage-Capstone-Projekt in der Weiterbildung.

## Funktionen

- Server anlegen (generischer Server, Webserver, Datenbankserver — via Vererbung)
- Server löschen, IP-Adresse bearbeiten
- Persistenz der Infrastruktur in `infrastruktur.json` (inkl. automatischem Backup)
- Eigenes Logging mit Rotation (`dcms_audit.log`, ab 50 Zeilen wird archiviert)
- Log-Report (Anzahl INFO/ERROR-Einträge)
- Systemstatus-Check: fragt die eigene öffentliche IP über die öffentliche
  [ipify](https://www.ipify.org/)-API ab und ermittelt darüber grob den
  Standort/Provider über [ip-api.com](https://ip-api.com)

## Architektur

| Datei | Verantwortung |
|---|---|
| `main.py` | Nutzer-Input/Output, Menüsteuerung |
| `server_modell.py` | Klassen `Server`, `Webserver`, `DatenbankServer` (Vererbung) |
| `storage.py` | Laden/Speichern der Infrastruktur als JSON |
| `network.py` | Externe IP- und Standortabfrage |
| `logger.py` | Logging inkl. Rotation |

Bewusste Design-Entscheidungen:

- **DRY-Prinzip**: Logik in Funktionen gekapselt statt Code-Duplikate.
- **Separation of Concerns**: `main.py` kennt nur Input/Output, nicht *wie*
  gespeichert wird — das liegt allein in `storage.py`.
- **Resilienz**: Netzwerkfehler werden mit `try/except` abgefangen, sodass
  das Tool bei fehlendem Internet nicht abstürzt.

## Ausführen

```bash
pip install requests
python main.py
```

`infrastruktur.json` und `dcms_audit.log` werden beim ersten Lauf automatisch
angelegt (sie sind hier bewusst nicht mitversioniert, siehe `.gitignore`).
