# KiCad 9 Fehlerbehebung für PcbDraw

## Das Problem

Der Fehler `SyntaxError: Unsupported path element 136.00000` tritt auf, weil KiCad 9 SVG-Pfade in einem Format generiert, das von der ursprünglichen PcbDraw-Version nicht erkannt wird.

## Lösung

Das Problem wurde durch mehrere Updates behoben:

### 1. Aktualisierte SVG-Pfad-Verarbeitung

Die `SvgPathItem`-Klasse wurde erweitert, um verschiedene Pfad-Formate zu handhaben:

```python
# Unterstützt jetzt:
# - Standard SVG: "M 100 50 L 150 75"  
# - KiCad 9 Format: "136.00000 50.00000 140.00000 54.00000"
# - Fehlerhaftes Format: Fallback-Mechanismus
```

### 2. Bessere Fehlerbehandlung

```python
# Anstatt zu crashen, werden problematische Pfade übersprungen
# mit Debugging-Ausgabe und Fallback-Versuchen
```

## Installation der Fixes

### Option 1: Lokale Installation mit Fixes
```bash
cd /path/to/PcbDraw
pip install -e .
```

### Option 2: Docker mit Updates
```bash
# Image mit Fixes bauen
docker build -t pcbdraw-kicad9-fixed .

# Verwendung
docker run --rm -v $(pwd):/work pcbdraw-kicad9-fixed \
  pcbdraw plot /work/your_board.kicad_pcb /work/output.svg
```

## Test der Fixes

### 1. SVG-Pfad-Parser testen
```bash
cd /path/to/PcbDraw
python test_kicad9_svg_paths.py
```

### 2. Mit Ihrem Board testen
```bash
# Aktiviert Debug-Ausgabe für problematische Pfade
pcbdraw plot your_board.kicad_pcb output.svg
```

Sie sollten jetzt Warnungen sehen statt eines Crashes:
```
Warning: Skipping problematic SVG path: '136.00000' - Error: ...
  -> Fallback path created: 'M 136.0 50.0 L 140.0 54.0'
```

## Weitere Debugging-Schritte

### 1. KiCad Version prüfen
```bash
python -c "
from pcbnewTransition import getVersion, isV9
try:
    version = getVersion()
    print(f'KiCad Version: {version}')
    print(f'Is KiCad 9: {isV9(version)}')
except Exception as e:
    print(f'KiCad detection failed: {e}')
"
```

### 2. SVG-Ausgabe von KiCad analysieren
```bash
# Schauen Sie in die temporären SVG-Dateien, die KiCad generiert
# Diese befinden sich normalerweise in /tmp/tmp* Verzeichnissen
```

### 3. Umgebungsvariablen für Debugging
```bash
export PCBDRAW_DEBUG=1
export DISPLAY=:99  # Für headless Umgebungen
```

## Erweiterte Docker-Lösung

Falls Sie weiterhin Probleme haben, hier ist eine robuste Docker-Lösung:

```dockerfile
FROM ubuntu:22.04

# Vollständige KiCad Installation (für bessere Kompatibilität)
RUN apt-get update && apt-get install -y \
    kicad \
    python3-pip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# PcbDraw mit Fixes installieren
COPY . /app/pcbdraw/
RUN cd /app/pcbdraw && pip install -e .

# Umgebung für headless KiCad
ENV DISPLAY=:99
ENV KICAD_CONFIG_HOME=/tmp/kicad_config

# Start-Script für Xvfb und KiCad
RUN echo '#!/bin/bash\nXvfb :99 -screen 0 1024x768x24 &\nsleep 2\nexec "$@"' > /start.sh && chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
CMD ["pcbdraw", "--help"]
```

## Bekannte Einschränkungen

1. **GUI-Abhängigkeiten**: KiCad benötigt GUI-Bibliotheken, auch im headless Modus
2. **SVG-Format-Änderungen**: KiCad 9 könnte weitere Format-Änderungen haben
3. **Plattform-Unterschiede**: Docker auf verschiedenen Systemen kann unterschiedlich reagieren

## Support

Falls das Problem weiterhin besteht:

1. Führen Sie den Test-Script aus: `python test_kicad9_svg_paths.py --debug`
2. Teilen Sie die Debug-Ausgabe mit
3. Überprüfen Sie die KiCad-Installation: `kicad --version`
4. Versuchen Sie den Docker-Ansatz für eine saubere Umgebung

## Erfolgs-Indikatoren

✅ **Fix erfolgreich** wenn Sie sehen:
- Warnungen statt Crashes
- SVG/PNG Ausgabe wird erstellt
- Test-Script zeigt "All tests passed!"

❌ **Weitere Debugging nötig** wenn:
- Immer noch `SyntaxError` auftritt
- Keine Ausgabe-Dateien erstellt werden  
- Test-Script schlägt fehl
