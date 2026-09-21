"""
Einfacher Smoke-Test fuer gui_test.py (ohne echten Flutter-Client).

Idee: main(page) braucht nur ein Objekt mit .add() und .update().
Wir bauen eine simple "Fake-Page", rufen main() damit auf und pruefen,
ob die Event-Handler (echo_klick, zaehler_klick) sich wie erwartet
verhalten - genau wie ein echter Button-Klick es taete.
"""

import flet as ft
from gui_test import main


class FakePage:
    """Minimaler Ersatz fuer ft.Page: sammelt nur, was page.add() bekommt."""

    def __init__(self):
        self.title = None
        self.controls = []
        self.update_calls = 0

    def add(self, *controls):
        self.controls.extend(controls)

    def update(self):
        self.update_calls += 1


def run():
    page = FakePage()
    main(page)

    row = page.controls[1]
    textfield, button = row.controls
    label = page.controls[2]

    textfield.value = "Hallo Flet"
    button.on_click(None)
    assert label.value == "Hallo Flet", f"Echo-App fehlerhaft: {label.value!r}"
    assert page.update_calls >= 1, "page.update() wurde nicht aufgerufen"
    print("OK: Echo-App zeigt den eingegebenen Text im Label an.")

    counter_col = page.controls[5]
    counter_button, counter_label = counter_col.controls
    assert counter_label.value == "Klicks: 0"
    counter_button.on_click(None)
    counter_button.on_click(None)
    assert counter_label.value == "Klicks: 2", f"Zaehler fehlerhaft: {counter_label.value!r}"
    print("OK: Klick-Zaehler erhoeht sich bei jedem Klick um 1.")


if __name__ == "__main__":
    run()
