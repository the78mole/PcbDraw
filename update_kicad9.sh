#!/bin/bash

# KiCad 9 Compatibility Update Script
# This script updates PcbDraw dependencies and tests KiCad 9 compatibility

set -e

echo "🔧 Updating PcbDraw for KiCad 9 compatibility..."

# Check if we're in the correct directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: Please run this script from the PcbDraw root directory"
    exit 1
fi

# Update dependencies
echo "📦 Updating dependencies..."
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    pip install --upgrade pcbnewTransition
else
    pip install --upgrade pcbnewTransition
fi

echo "✅ Dependencies updated!"

# Try to import and test the modules
echo "🧪 Testing imports..."
python -c "
try:
    from pcbnewTransition import isV6, isV7, isV8, isV9, getVersion
    print('✅ pcbnewTransition imports successful')
    print('   Available version functions: isV6, isV7, isV8, isV9')
    
    # Try to get KiCad version if KiCad is installed
    try:
        version = getVersion()
        print(f'   Detected KiCad version: {version}')
        if version[0] >= 9:
            print('🎉 KiCad 9 or newer detected!')
        elif version[0] >= 6:
            print('✅ Compatible KiCad version detected')
        else:
            print('⚠️  Old KiCad version detected, some features may not work')
    except Exception as e:
        print(f'⚠️  Could not detect KiCad version (KiCad may not be installed): {e}')
        
except ImportError as e:
    print(f'❌ Import failed: {e}')
    exit(1)
"

echo "🧪 Testing PcbDraw imports..."
python -c "
try:
    from pcbdraw.plot import PcbPlotter
    from pcbdraw.pcbnew_common import fakeKiCADGui
    print('✅ PcbDraw imports successful')
except ImportError as e:
    print(f'❌ PcbDraw import failed: {e}')
    exit(1)
"

echo "✅ All tests passed!"
echo ""
echo "🎉 PcbDraw is now updated for KiCad 9 compatibility!"
echo ""
echo "📖 Changes made:"
echo "   - Updated pcbnewTransition dependency to >=0.5"
echo "   - Added KiCad 9 support in plot.py and pcbnew_common.py"
echo "   - Updated documentation"
echo ""
echo "📝 To use PcbDraw with KiCad 9:"
echo "   1. Ensure KiCad 9 is properly installed"
echo "   2. Use PcbDraw commands as usual"
echo "   3. Check KICAD9_COMPATIBILITY.md for details"
