# LunchSquad - Team Lunch Organizer

Eine Streamlit-Anwendung zum Organisieren von Team-Mittagsbestellungen, mit Unterstützung für mehrere Restaurants (YamYam, Döner, Edeka) und anpassbaren Bestellungen.

## Features

- Bestellungen für verschiedene Restaurants verwalten
- Individuelle Bestelloptionen je nach Restaurant
- Persistente Speicherung der Bestellungen (auch nach App-Neustart)
- Export der Bestellungen in verschiedenen Formaten (JSON, CSV, TXT, PNG)
- Import von Bestellungen aus JSON-Dateien
- Übersichtliche Darstellung aller Bestellungen

## Restaurants

### YamYam
- Asiatische Gerichte mit Nummern-Auswahl

### Döner
- Döner, Dürüm, Dönerbox und mehr
- Auswahl verschiedener Läden (Döner Bruder, King Kebabo's, Aldi Döner)
- Individualisierung mit Soßen, Extras und Schärfegrad

### Edeka
- Belegtes Brötchen, Salat, Bäcker-Produkte

## Cloud-Persistenz

Die Anwendung verwendet einen Cloud-Speichermechanismus, um sicherzustellen, dass Bestellungen auch nach einem Neustart der Anwendung verfügbar bleiben, wenn sie auf Streamlit Community Cloud gehostet wird.

## Technische Details

- Implementiert in Python mit Streamlit
- Hierarchischer Persistenz-Ansatz:
  1. Cloud-Speicher (primär für Streamlit Cloud)
  2. Session State (für Kompatibilität)
  3. Dateibasierte Speicherung (für lokale Entwicklung)
- Modulare Struktur mit getrennten Dateien für Modelle, Konfiguration und Hilfsfunktionen

## Starten der Anwendung

```bash
streamlit run app.py
```

## Projektstruktur

- `app.py`: Hauptanwendung mit UI-Code
- `models.py`: Datenmodelle und Persistenz-Logik
- `config.py`: Konfigurationswerte und Optionen
- `utils.py`: Hilfsfunktionen für Formatierung und Validierung
- `cloud_storage.py`: Cloud-Persistenz-Mechanismus für Streamlit Cloud
- `.streamlit/config.toml`: Streamlit-Serverkonfiguration