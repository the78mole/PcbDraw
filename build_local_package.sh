#!/bin/bash

# Script zum Erstellen eines lokalen Wheel-Packages für PcbDraw

echo "🔧 Building local PcbDraw wheel package..."

# Prüfen ob wir im richtigen Verzeichnis sind
if [ ! -f "setup.py" ]; then
    echo "❌ Error: Please run this script from the PcbDraw root directory"
    exit 1
fi

# Build dependencies installieren
echo "📦 Installing build dependencies..."
pip install build wheel

# Package erstellen
echo "🏗️ Building wheel package..."
python -m build

echo "✅ Package built successfully!"
echo ""
echo "📁 Generated files:"
ls -la dist/

echo ""
echo "📖 To install in other projects:"
echo "   pip install dist/PcbDraw-*.whl"
echo ""
echo "📖 To install with dependencies:"
echo "   pip install dist/PcbDraw-*.whl[dev]"
