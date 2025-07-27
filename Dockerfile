# Dockerfile für PcbDraw mit KiCad 9 Unterstützung
FROM ubuntu:22.04

# System-Abhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    xvfb \
    libwxgtk3.0-gtk3-dev \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis erstellen
WORKDIR /app

# PcbDraw Code kopieren
COPY . /app/pcbdraw/

# Python Umgebung einrichten
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Umgebungsvariablen für headless Betrieb
ENV DISPLAY=:99
ENV PCBDRAW_HEADLESS=1

# PcbDraw installieren
RUN cd /app/pcbdraw && pip install -e .

# Xvfb für GUI-Anwendungen im Hintergrund starten
RUN echo '#!/bin/bash\nXvfb :99 -screen 0 1024x768x24 &\nexec "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["pcbdraw", "--help"]
