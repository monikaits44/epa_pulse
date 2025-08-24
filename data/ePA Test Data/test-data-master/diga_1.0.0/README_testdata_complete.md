# Testdata complete DiGA 1.0.0

## Zusammensetzung des DiGA_allProfiles_incomplete_1.0.0 Datensatzes

Ausgangsbasis war der validierte MIO42 Beispieldatensatz zu Adipositas (siehe kbv_mock_example2_adipositas), da dieser bereits viele Abschnittselemente enthalten hat.

Zusätzliche Abschnittselemente, welche in den beiden anderen Beispielen (Depression und Migräne) vorhanden waren, wurden ergänzt. Hierbei muss beachtet werden:

- die entsprechenden Entries müssen ergänzt werden
  - Etwaige Referenzen die sich zwischen den Beispielen unterschieden haben müssen vereinheitlicht werden - z.B. Patientenreferenz
  - Etwaige Referenzelemente, welche von neu hinzugefügten Abschnitten referenziert werden, müssen ebenfalls übernommen werden
- Sections bzw. Referenzen in der Composition müssen ergänzt werden
  - wenn Abschnitt noch nicht vorhanden: als neue Section ergänzen (Kodierung mittels SNOMED CT)
  - wenn Abschnitt bereits vorhanden: Ergänzungen der entsprechenden Referenz auf das dazugehörige Entry

Ergänzungen aus den beiden anderen Beispielen wurden mittels Kommentar markiert.

Noch offene Elemente nach Zusammenführung der Beispieldaten sind unter "Noch offene Elemente" zu finden.

Der aktuelle Datensatz enthält jedes FHIR-Profil aus dem DiGA-Datenmodell der MIO42 zumindesten einmal (jedoch nicht in seiner vollständigen Abbildung - optionale Elemente fehlen teilweise noch).
Die Struktur des Datenmodells wurde über Kommentierungen zwecks Übersichtlichkeit im Testdatensatz nachgebildet. 
Stand 31/05/2022 sind noch 2 Profile offen (Herkunftsdaten und periphere arterielle Sauerstoffsättigung - siehe unten). Hier warten wir noch auf ein Statement von Seiten der MIO42!
Fehlende Profile sind mittel ``<!-- Fehlt -->`` gekennzeichnet.

## Aufbau eines Gesamtdatensatzes

- Verpflichtende Angaben
  - Versicherte Person
  - DiGA
  - Metainformationen
  - Herkunftsdaten
  - Betrachtungszeitraum
- Abschnitte
  - Fragebögen
  - Befunde und Ergebnisse
  - Aktivitäten
  - Nahrung
  - Lebensstilfaktoren
  - Probleme
  - Umweltfaktoren
  - Medikation
  - Beurteilungen
  - Ziele
  - Kontakte
  - Termine
  - Patientenberichte
- Referenzelemente
  - Bewertungsskala
  - Arzneimittel
  - Gerät
  - Gerätehersteller

## Noch offene Elemente

- [x] 1. Verpflichtenden Elemente
  - [x] 1.4. Herkunftsdaten (könnte aus den Beispieldaten "Betrachtungszeitraum" übernommen werden)
    - [x]  Frage an MIO42 bzgl Herkunftsdaten
- [x] 2. Abschnittselemente
  - [x] 2.2. Vitalparameter
    - [x] 2.2.1.1 Körperlänge
    - [x] 2.2.1.2. periphere arterielle Sauerstoffsättigung -> 
      - [x] Validiert NICHT (daher derzeit auskommentiert!) - siehe Kommentar in den Testdaten -> Rückmeldung an MIO42? UPDATE: wurde gefixt - valdiert jetzt korrekt!
    - [x] 2.2.1.3. Körpertemperatur
    - [x] 2.2.1.6. Blutdruck
    - [x] 2.2.1.7. Kopfumfang
    - [x] 2.2.1.8. Atemfrequenz
    - [x] 2.2.1.9. Glukosespiegel (könnte aus den Beispieldaten "Betrachtungszeitraum" übernommen werden)
  - [x] 2.11. kontakte
    - [x] 2.11.1. Einrichtung
    - [x] 2.11.3. Behandelnde Person/Einrichtung
    - [x] 2.11.4. Kontaktperson
  - [x] 2.12. Termine
    - [x] 2.12.2. Vergangene Termine

## Noch offene Todos

- [x] Ergänzen der fehlenden Elemente
  - [x] Kommentierung im File (z.B. ``<!-- Manuell ergänzt -->``)
- [ ] Abgleich der FHIR-Profile mit den Daten - alle Elemente mindestens einmal befüllt?
  - [ ] Kommetierung im File (z.B. ``<!-- Manuell erweitert -->``)
- [x] Einarbeiten der Änderungen nach Festlegung DiGA 1.0.0 -> DONE: ICF URIs angepasst
