import datetime
import os

def schreibe_log(level: str, nachricht: str):
    if os.path.exists("dcms_audit.log"):
        with open("dcms_audit.log", "r", encoding="utf-8") as alte_datei:
            zeilen = alte_datei.readlines()
        anzahl_zeilen = len(zeilen)
        if anzahl_zeilen > 50:
            os.replace("dcms_audit.log", "dcms_audit_old.log")


    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_zeile = f"[{time_now}] [{level}] {nachricht}"
    with open("dcms_audit.log", "a", encoding="utf-8") as datei:
        datei.write(log_zeile + "\n")
