# Anleitung: PcbDraw mit KiCad 9 in anderen Projekten nutzen

## Szenario 1: Anderes Python-Projekt auf demselben System

### Methode A: Direkte lokale Installation
```bash
# In Ihrem anderen Projekt-Verzeichnis
cd /path/to/your/other/project

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# oder: venv\Scripts\activate  # Windows

# PcbDraw lokal installieren
pip install -e /home/daniel/GIT/Python/PcbDraw
```

### Methode B: Über requirements.txt
```bash
# requirements.txt in Ihrem Projekt:
echo "-e /home/daniel/GIT/Python/PcbDraw" >> requirements.txt

# Dann installieren:
pip install -r requirements.txt
```

## Szenario 2: Verteilung an andere Entwickler

### Wheel-Package erstellen und teilen
```bash
# Im PcbDraw-Verzeichnis
./build_local_package.sh

# Das erstellte .whl File teilen
# Andere können es dann installieren mit:
# pip install PcbDraw-*.whl
```

### Git-Repository nutzen
```bash
# Wenn Sie das Repository auf GitHub/GitLab gepusht haben
pip install git+https://github.com/the78mole/PcbDraw.git
```

## Szenario 3: CI/CD Pipeline

### GitHub Actions Beispiel
```yaml
name: Test with updated PcbDraw

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install PcbDraw from Git
      run: |
        pip install git+https://github.com/the78mole/PcbDraw.git
    
    - name: Test PcbDraw
      run: |
        pcbdraw --help
```

## Szenario 4: Docker-Container

### Container bauen
```bash
# Im PcbDraw-Verzeichnis
docker build -t pcbdraw-kicad9 .

# Container nutzen
docker run --rm -v $(pwd):/work pcbdraw-kicad9 pcbdraw plot /work/board.kicad_pcb /work/output.svg
```

## Szenario 5: Entwicklungsumgebung teilen

### setup.py für Ihr eigenes Projekt
```python
# setup.py in Ihrem Projekt
from setuptools import setup, find_packages

setup(
    name="mein-projekt",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Andere Dependencies...
    ],
    dependency_links=[
        "git+https://github.com/the78mole/PcbDraw.git#egg=PcbDraw"
    ],
)
```

## Szenario 6: Lokaler Package-Server

### Einfachen HTTP-Server für Packages starten
```bash
# Im dist/ Verzeichnis nach dem Build
python -m http.server 8000

# Andere können dann installieren mit:
# pip install --extra-index-url http://your-server:8000 PcbDraw
```

## Tipps für die Nutzung

### 1. Version-Checking in Ihrem Code
```python
try:
    from pcbdraw import __version__
    from pcbnewTransition import getVersion, isV9
    
    print(f"PcbDraw version: {__version__}")
    kicad_version = getVersion()
    print(f"KiCad version: {kicad_version}")
    
    if isV9(kicad_version):
        print("✅ KiCad 9 detected and supported!")
    
except ImportError as e:
    print(f"❌ PcbDraw import failed: {e}")
```

### 2. Graceful Fallback
```python
try:
    from pcbdraw.plot import PcbPlotter
    PCBDRAW_AVAILABLE = True
except ImportError:
    PCBDRAW_AVAILABLE = False
    print("⚠️ PcbDraw not available, skipping PCB visualization")

if PCBDRAW_AVAILABLE:
    # Nutze PcbDraw Features
    pass
```

### 3. Umgebungsvariablen für Konfiguration
```bash
# Für verschiedene KiCad-Installationen
export KICAD_CONFIG_HOME=/path/to/kicad/config
export PCBDRAW_INKSCAPE=/path/to/inkscape
```

## Fehlerbehebung

### Häufige Probleme und Lösungen

1. **KiCad nicht gefunden**
   ```bash
   # KiCad-Pfad zur PATH hinzufügen
   export PATH="/Applications/KiCad/KiCad.app/Contents/MacOS:$PATH"  # macOS
   export PATH="/usr/bin/kicad:$PATH"  # Linux
   ```

2. **pcbnew Import-Fehler**
   ```bash
   # Prüfen ob KiCad Python-Bindings verfügbar sind
   python -c "import pcbnew; print('KiCad Python bindings OK')"
   ```

3. **Abhängigkeits-Konflikte**
   ```bash
   # Saubere virtuelle Umgebung erstellen
   python -m venv fresh_env
   source fresh_env/bin/activate
   pip install -e /path/to/PcbDraw
   ```
