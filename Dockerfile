# Dockerfile für PcbDraw mit KiCad 9 Unterstützung
FROM ubuntu:22.04

# System-Abhängigkeiten installieren
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis erstellen
WORKDIR /app

# PcbDraw Code kopieren
COPY . /app/pcbdraw/

# Python Umgebung einrichten
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# PcbDraw installieren
RUN cd /app/pcbdraw && pip install -e .

# Entry point
CMD ["pcbdraw", "--help"]
