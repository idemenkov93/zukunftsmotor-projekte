# Flet Echo-App

Erster Einstieg in grafische Oberflächen (GUI) mit dem Python-Framework
[Flet](https://flet.dev) — Umstieg von prozeduralem Terminal-Code auf
Event-Driven Programming.

## Was die App macht

- **Echo-App**: Text in ein Textfeld eingeben, auf "Anzeigen" klicken — der
  Text erscheint in einem Label darunter.
- **Klick-Zähler (Bonus)**: zählt Klicks auf einen zweiten Button hoch.

Beide Beispiele zeigen das gleiche Prinzip: eine Funktion (Event-Handler)
reagiert auf ein Ereignis (`on_click`), verändert einen Control-Wert und
ruft `page.update()` auf, damit die Änderung sichtbar wird.

## Wichtiger Hinweis zur Flet-Version

`pip install flet` installiert aktuell standardmäßig **Flet 1.0**. Dort
wurde `ft.ElevatedButton` in `ft.Button` umbenannt, und der Button-Text
kommt über `content=` statt `text=`. Dieses Projekt nutzt bewusst die
klassische API:

```bash
pip install flet==0.28.3
python gui_test.py
```

## Test

`test_gui_test.py` prüft die Event-Handler-Logik über ein einfaches
Fake-Page-Objekt (Mock), ohne dass ein echtes Fenster geöffnet werden muss:

```bash
python test_gui_test.py
```
