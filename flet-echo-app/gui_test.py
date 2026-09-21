"""
gui_test.py
Uebung: Einstieg in grafische Oberflaechen mit Flet
Datum: 21.09.2026

Teil 1: Leeres Grundgeruest (abgetippt nach Vorlage aus der Praesentation)
Teil 2: Echo-App mit Event Handling (Textfeld + Button + Label)
Bonus:  Klick-Zaehler (zweites Beispiel fuer Event Handling)

Wichtig zur Flet-Version:
"pip install flet" installiert seit Kurzem standardmaessig Flet 1.0.
Dort wurde ft.ElevatedButton in ft.Button umbenannt und der Text kommt
nicht mehr ueber text=, sondern ueber content=. Die Kursfolien sind
noch fuer die alte, klassische API geschrieben (ft.ElevatedButton,
text=). Deshalb hier: pip install flet==0.28.3
Damit laeuft der Code aus den Folien 1:1, ohne Anpassungen.
"""

import flet as ft


def main(page: ft.Page):
    page.title = "DCMS Dashboard - GUI Uebung"

    # ---------------------------------------------------------------
    # Teil 2: Echo-App
    # Ein Textfeld, ein Button und ein Label.
    # Klick auf den Button -> Text aus dem Feld wird im Label angezeigt.
    # ---------------------------------------------------------------
    eingabe = ft.TextField(label="Text eingeben")
    ausgabe_label = ft.Text(value="", size=18, color=ft.Colors.BLUE)

    def echo_klick(e):
        # Event-Handler: das Parameter 'e' ist das Event-Objekt.
        # Wert aus dem Textfeld auslesen und ins Label schreiben.
        ausgabe_label.value = eingabe.value
        page.update()  # Goldene Regel: ohne update() sieht man die Aenderung nicht!

    echo_button = ft.ElevatedButton(text="Anzeigen", on_click=echo_klick)

    # ---------------------------------------------------------------
    # Bonus: Klick-Zaehler
    # Zeigt, wie man sich einen Zustand (Zaehlerstand) zwischen
    # mehreren Events merkt.
    # ---------------------------------------------------------------
    zaehlerstand = 0
    zaehler_label = ft.Text(value="Klicks: 0", size=16)

    def zaehler_klick(e):
        nonlocal zaehlerstand
        zaehlerstand += 1
        zaehler_label.value = f"Klicks: {zaehlerstand}"
        page.update()

    zaehler_button = ft.ElevatedButton(text="Klick mich", on_click=zaehler_klick)

    # ---------------------------------------------------------------
    # Layout: alles der Page hinzufuegen
    # ---------------------------------------------------------------
    page.add(
        ft.Text("Echo-App", size=22, weight=ft.FontWeight.BOLD),
        ft.Row(controls=[eingabe, echo_button]),
        ausgabe_label,
        ft.Divider(),
        ft.Text("Klick-Zaehler (Bonus)", size=22, weight=ft.FontWeight.BOLD),
        ft.Column(controls=[zaehler_button, zaehler_label]),
    )


if __name__ == "__main__":
    ft.app(target=main)
