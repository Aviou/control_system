# Verwende das offizielle Python-Image als Basis
FROM python:3.11

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere System-Abhängigkeiten
# Achtung: RUN Befehle für apt-get müssen in einer einzigen Zeile verwendet werden,
# um die Bildgröße klein zu halten und den Docker Cache richtig zu nutzen
RUN apt-get update && apt-get install -y \
    ninja-build \
    && rm -rf /var/lib/apt/lists/*  # Bereinige den apt cache, um Größe zu sparen

# Installiere Python-Abhängigkeiten
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install numpy
# Kopiere den Projektcode in das Arbeitsverzeichnis
COPY . .

# Mache das entrypoint.sh Skript verfügbar und ausführbar
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Setze entrypoint.sh als den zu startenden Befehl
ENTRYPOINT ["entrypoint.sh"]




