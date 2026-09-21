"""
17_taschenrechner.py

Modularer Industrie-Taschenrechner
-----------------------------------
Ein Terminal-Taschenrechner, der die Grundrechenarten (Addition,
Subtraktion, Multiplikation, Division) als eigene Funktionen
bereitstellt und über ein Menü im Hauptprogramm gesteuert wird.

Architektur:
    -> Oben:  Die Rechen-Logik (einzelne Funktionen)
    -> Unten: Das Hauptmenü (while-Schleife & input)

Autor: Ihor Demenkov
"""

# ---------------------------------------------------------
# Konstanten
# ---------------------------------------------------------
VERLAUF = []  # Speichert alle bisher durchgeführten Rechnungen als Strings


# ---------------------------------------------------------
# Phase 1: Die Mathematik-Engine
# ---------------------------------------------------------
def addiere(a: float, b: float) -> float:
    """Addiert zwei Zahlen und gibt das Ergebnis zurück."""
    return a + b


def subtrahiere(a: float, b: float) -> float:
    """Subtrahiert b von a und gibt das Ergebnis zurück."""
    return a - b


def multipliziere(a: float, b: float) -> float:
    """Multipliziert zwei Zahlen und gibt das Ergebnis zurück."""
    return a * b


def dividiere(a: float, b: float) -> float:
    """
    Dividiert a durch b und gibt das Ergebnis zurück.

    Achtung, Fehlerquelle: Division durch 0 ist nicht definiert.
    In diesem Fall wird eine Fehlermeldung ausgegeben und 0.0
    zurückgegeben, damit das Programm nicht abstürzt.
    """
    if b == 0:
        print("Fehler: Division durch 0 ist nicht erlaubt!")
        return 0.0
    else:
        return a / b


# ---------------------------------------------------------
# Phase 2: Das DRY-Prinzip anwenden
# ---------------------------------------------------------
def hole_zahl(text_fuer_nutzer: str) -> float:
    """
    Fragt den Nutzer nach einer Zahl und gibt sie als float zurück.

    So muss float(input(...)) nicht bei jeder Rechenart erneut
    geschrieben werden.
    """
    return float(input(text_fuer_nutzer))


# ---------------------------------------------------------
# Phase 3 & 4: Das Hauptprogramm (Menü, Steuerung, Verlauf)
# ---------------------------------------------------------
while True:
    print("=== MODULARER TASCHENRECHNER ===")
    print("[1] Addieren (+)")
    print("[2] Subtrahieren (-)")
    print("[3] Multiplizieren (*)")
    print("[4] Dividieren (/)")
    print("[5] Beenden")
    print("[6] Verlauf anzeigen")
    print("================================")

    wahl = input("Bitte wähle eine Option (1-6): ")

    if wahl in ("1", "2", "3", "4"):
        zahl1 = hole_zahl("Erste Zahl: ")
        zahl2 = hole_zahl("Zweite Zahl: ")

        if wahl == "1":
            ergebnis = addiere(zahl1, zahl2)
            rechenzeichen = "+"
        elif wahl == "2":
            ergebnis = subtrahiere(zahl1, zahl2)
            rechenzeichen = "-"
        elif wahl == "3":
            ergebnis = multipliziere(zahl1, zahl2)
            rechenzeichen = "*"
        else:  # wahl == "4"
            ergebnis = dividiere(zahl1, zahl2)
            rechenzeichen = "/"

        print(f"Ergebnis: {ergebnis}")

        # Rechnung für den Verlauf zusammenbauen und speichern
        rechnung = f"{zahl1} {rechenzeichen} {zahl2} = {ergebnis}"
        VERLAUF.append(rechnung)

    elif wahl == "5":
        print("Auf Wiedersehen!")
        break

    elif wahl == "6":
        print("--- VERLAUF ---")
        if not VERLAUF:
            print("Noch keine Rechnungen durchgeführt.")
        else:
            for eintrag in VERLAUF:
                print(eintrag)
        print("---------------")

    else:
        print("Ungültige Eingabe. Bitte wähle eine Zahl von 1 bis 6.")
