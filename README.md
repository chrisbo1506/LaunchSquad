# LunchSquad - Team Lunch Organizer (Streamlit Version)

Eine Streamlit-Webanwendung zur Organisation von Team-Mittagsbestellungen mit erweiterter Datenpersistenz und Cloud-kompatibler Funktionalität.

## Beschreibung

LunchSquad ist eine benutzerfreundliche Anwendung, die es Teams ermöglicht, Mittagsbestellungen bei verschiedenen Restaurants zu koordinieren. Die Anwendung unterstützt mehrere Restaurants (YamYam, Döner, Edeka) mit anpassbaren Bestelloptionen und bietet eine übersichtliche Verwaltung aller Bestellungen.

## Funktionen

- Interaktive Restaurantauswahl mit spezifischen Bestellformularen
- Speichern und Laden von Bestellungen mit robuster Datenpersistenz
- Export von Bestellungen in verschiedenen Formaten (CSV, JSON, TXT, Bild)
- Import von Bestellungen aus JSON-Dateien
- Responsive Benutzeroberfläche mit Streamlit

## Installation und Ausführung

### Lokale Ausführung

1. Repository klonen:
```
git clone https://github.com/deinbenutzername/launchsquad.git
cd launchsquad
```

2. Abhängigkeiten installieren:
```
pip install -r requirements.txt
```

3. Anwendung starten:
```
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Erstelle einen Account auf [Streamlit Sharing](https://streamlit.io/sharing)
2. Verbinde dein GitHub-Repository mit Streamlit Sharing
3. Wähle `app.py` als Hauptdatei und starte die Anwendung

## Konfiguration

Die Anwendung ist für die Verwendung in der Streamlit Cloud optimiert. Die wichtigsten Konfigurationsdateien sind:

- `.streamlit/config.toml` - Streamlit Server-Konfiguration
- `pyproject.toml` - Python-Abhängigkeiten

## Datenpersistenz

Die Anwendung verwendet einen hybriden Ansatz zur Datenpersistenz:

1. Lokale JSON-Datei (`lunch_orders.json`) für persistente Speicherung
2. Streamlit Session State für vorübergehende Datenspeicherung während der Sitzung

Dieser Ansatz stellt sicher, dass Daten auch in der Streamlit Cloud-Umgebung erhalten bleiben.

## Fehlerbehebung

Wenn die Anwendung in der Streamlit Cloud nicht startet:

1. Überprüfe die `.streamlit/config.toml` auf korrekte Server-Einstellungen
2. Stelle sicher, dass `pyproject.toml` alle notwendigen Abhängigkeiten enthält
3. Überprüfe die Logs in der Streamlit Cloud-Benutzeroberfläche

## Lizenz

[MIT Lizenz](LICENSE)