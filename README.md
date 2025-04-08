# LunchSquad - Team Lunch Organizer

Eine Streamlit Web-Anwendung zur Organisation von Teambestellungen für das Mittagessen.

## Beschreibung

LunchSquad hilft Teams dabei, ihre Mittagsbestellungen zu organisieren. Die Anwendung unterstützt verschiedene Restaurants (YamYam, Döner, Edeka) und ermöglicht jedem Teammitglied, seine individuelle Bestellung anzupassen und zu speichern.

## Funktionen

- **Mehrere Restaurants**: Unterstützung für YamYam, Döner und Edeka
- **Anpassbare Bestellungen**: Verschiedene Optionen je nach Restaurant
- **Bestellungsverwaltung**: Hinzufügen, Entfernen und Anzeigen von Bestellungen
- **Exportfunktionen**: Export von Bestellungen als CSV, JSON, Text oder Bild
- **Persistente Speicherung**: Bestellungen werden automatisch in einer JSON-Datei gespeichert

## Verwendung

1. Wähle ein Restaurant aus der Hauptseite
2. Fülle das Bestellformular aus
3. Klicke auf "Hinzufügen"
4. Verwalte alle Bestellungen im Bestellungsmenü
5. Exportiere die Liste bei Bedarf

## Restaurants und Optionen

### YamYam
- Boxen mit verschiedenen Größen und Basis-Optionen
- Anpassbare Toppings und Extras

### Döner
- Verschiedene Döner-Shops zur Auswahl
- Individuell anpassbare Bestellungen mit Extras

### Edeka
- Verschiedene Produkte wie Salate und Bäcker-Artikel
- Anpassbare Saucen und Salat-Optionen

## Installation für Entwickler

Benötigte Bibliotheken:
```
pip install streamlit pandas pillow
```

Starten der Anwendung im Entwicklungsmodus:
```
streamlit run app.py
```

## Bereitstellung für Nutzer

Die Anwendung kann auf verschiedene Weise für Nutzer bereitgestellt werden:

1. **Streamlit Community Cloud** (empfohlen):
   - Erstelle einen Account auf streamlit.io/cloud
   - Verbinde dein GitHub-Repository
   - Veröffentliche die App für öffentlichen Zugriff

2. **Replit** (aktuell):
   - Teile den Link zu dieser Replit-App
   - Nutzer können direkt im Browser auf die App zugreifen

3. **Andere Hosting-Optionen**:
   - Heroku, Render, DigitalOcean, etc.

## Dateistruktur

- `app.py`: Hauptanwendung und UI-Komponenten
- `models.py`: Datenmodelle und Bestellungsverwaltung
- `utils.py`: Hilfsfunktionen für Formatierung und Export
- `config.py`: Konfigurationseinstellungen
- `lunch_orders.json`: Gespeicherte Bestellungen

## Version

Version 1.0.0

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).
