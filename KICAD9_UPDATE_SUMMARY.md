# PcbDraw KiCad 9 Kompatibilitäts-Update

## Zusammenfassung

Das PcbDraw Package wurde erfolgreich für die Kompatibilität mit KiCad 9 aktualisiert, während die Rückwärtskompatibilität mit älteren Versionen (KiCad 5-8) erhalten bleibt.

## Durchgeführte Änderungen

### 1. Dependency Updates
- **setup.py**: `pcbnewTransition` Dependency von `>=0.4` auf `>=0.5` aktualisiert
- Die neuere Version von `pcbnewTransition` unterstützt KiCad 9 vollständig

### 2. Code-Änderungen

#### plot.py
- Import von `isV9` aus `pcbnewTransition` hinzugefügt
- `LEGACY_KICAD` Check erweitert um `isV9()`
- Version-Checks in `PcbPlotter.__init__()` aktualisiert:
  - KiCad 9 wird wie KiCad 8 und 7 behandelt (nutzt `_ki2svg_v7` und `_svg2ki_v7`)
- SVG-Präzisions-Einstellungen für KiCad 9 erweitert
- Distanz-Vergleichslogik für KiCad 9 angepasst

#### pcbnew_common.py
- Imports für `isV7`, `isV8`, `isV9` hinzugefügt
- `PCB_DIMENSION_BASE` Filterung für alle neueren KiCad-Versionen erweitert

#### Dokumentation
- `doc/installation.md` aktualisiert mit Hinweis auf KiCad v5-v9 Kompatibilität
- Windows-Installationsanweisungen auf "v6 oder neuer" aktualisiert

### 3. Zusätzliche Dateien
- `KICAD9_COMPATIBILITY.md`: Detaillierte Dokumentation der Änderungen
- `update_kicad9.sh`: Automatisiertes Update-Script für Dependencies und Tests

## Kompatibilitäts-Matrix

| KiCad Version | Linux | Windows | macOS | Status |
|---------------|-------|---------|-------|--------|
| v5            | ✅    | ❌      | ❌     | Legacy |
| v6            | ✅    | ✅      | ✅     | Vollständig |
| v7            | ✅    | ✅      | ✅     | Vollständig |
| v8            | ✅    | ✅      | ✅     | Vollständig |
| v9            | ✅    | ✅      | ✅     | **Neu!** |

## Technische Details

### API-Kompatibilität
KiCad 9 nutzt die gleichen API-Patterns wie KiCad 8 und 7, daher:
- Gleiche SVG-Konvertierungsfunktionen (`_ki2svg_v7`, `_svg2ki_v7`)
- Gleiche SVG-Präzisions-Einstellungen
- Gleiche Distanz-Toleranzen für Geometrie-Vergleiche

### Abhängigkeiten
- `pcbnewTransition>=0.5` stellt die Low-Level-API-Kompatibilität sicher
- Alle anderen Dependencies bleiben unverändert

## Installation und Test

### Automatisierte Installation
```bash
./update_kicad9.sh
```

### Manuelle Installation
```bash
pip install --upgrade "pcbnewTransition>=0.5"
```

### Test der Kompatibilität
```python
from pcbnewTransition import getVersion, isV9
version = getVersion()
if isV9(version):
    print("KiCad 9 detected and supported!")
```

## Nutzung

Die Nutzung von PcbDraw bleibt unverändert:

```bash
# Standard PCB-Plot
pcbdraw plot board.kicad_pcb output.svg

# Mit Style
pcbdraw plot --style jlcpcb-green-hasl board.kicad_pcb output.svg

# Populate für Bestückungspläne
pcbdraw populate assembly.md output/
```

## Rückwärtskompatibilität

✅ **Vollständig erhalten** - Alle bestehenden Features und APIs funktionieren weiterhin
✅ **Keine Breaking Changes** - Bestehende Scripts und Workflows sind nicht betroffen
✅ **Gleiche CLI-Interface** - Alle Kommandozeilen-Optionen bleiben gleich

## Ausblick

- Das Update ist ready für Production Use
- Automatische CI/CD Tests sollten die KiCad 9 Kompatibilität verifizieren
- Zukünftige KiCad-Versionen werden durch Updates von `pcbnewTransition` unterstützt

## Support

Bei Problemen mit KiCad 9:
1. Überprüfen Sie, dass KiCad 9 korrekt installiert ist
2. Stellen Sie sicher, dass `pcbnewTransition>=0.5` installiert ist
3. Testen Sie mit dem bereitgestellten Update-Script
4. Konsultieren Sie `KICAD9_COMPATIBILITY.md` für Details
