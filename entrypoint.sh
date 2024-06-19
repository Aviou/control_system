#!/bin/bash

# Starte den Django Entwicklungs-Server
python manage.py runserver 0.0.0.0:8000 &

# Füge hier weitere Befehle hinzu, zum Beispiel:
python manage.py startbot &

# Halte den Container am Leben, indem ein Prozess im Vordergrund bleibt
# Hinweis: Dies könnte auch ein Dienst wie Gunicorn für Django sein.
tail -f /dev/null
