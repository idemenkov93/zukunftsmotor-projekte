# Modularer Taschenrechner

Ein Terminal-Taschenrechner, der die Grundrechenarten (Addition, Subtraktion,
Multiplikation, Division) als eigene, einzeln testbare Funktionen bereitstellt
und über ein Menü gesteuert wird.

## Features

- Grundrechenarten als separate Funktionen (DRY-Prinzip: Eingabe-Logik über
  eine gemeinsame Hilfsfunktion `hole_zahl()`)
- Schutz vor Division durch 0 (keine Exception, sondern kontrollierte
  Fehlermeldung)
- Rechenverlauf, der während der Laufzeit im Speicher gehalten und auf
  Wunsch angezeigt wird

## Ausführen

```bash
python taschenrechner.py
```
