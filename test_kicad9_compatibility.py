#!/usr/bin/env python3
"""
Test script for KiCad 9 SVG path parsing compatibility.

This script tests the updated SvgPathItem class with various KiCad 9 path formats
to ensure they are parsed correctly without throwing exceptions.
"""

import sys
import os

# Add the current directory to Python path to import pcbdraw modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from pcbdraw.plot import SvgPathItem
    print("✓ Successfully imported SvgPathItem from pcbdraw.plot")
except ImportError as e:
    print(f"✗ Failed to import SvgPathItem: {e}")
    print("Please ensure you're running this script from the PcbDraw directory")
    sys.exit(1)

def test_svg_path_parsing():
    """Test various SVG path formats that KiCad 9 might generate."""
    
    test_cases = [
        # KiCad 9 problematic formats
        ("136.00000", "Single coordinate"),
        ("136.00000 50.00000", "Two coordinates (point)"),
        ("136.00000 50.00000 140.00000 54.00000", "Four coordinates (line)"),
        ("100.5 200.75", "Decimal coordinates"),
        ("0 0", "Origin point"),
        
        # Standard SVG formats (should still work)
        ("M 136 50 L 140 54", "Standard move-line"),
        ("M 100 100", "Simple move"),
        ("M 100 100 L 200 200", "Move and line"),
        ("M 50 50 A 25 25 0 1 0 100 50", "Arc command"),
        
        # Edge cases
        ("M 0 0 L 0 0", "Zero-length line"),
        ("M -100 -50", "Negative coordinates"),
    ]
    
    passed = 0
    failed = 0
    
    print("\n" + "="*70)
    print("Testing SVG Path Parsing with KiCad 9 Compatibility")
    print("="*70)
    
    for path, description in test_cases:
        print(f"\nTest: {description}")
        print(f"Path: '{path}'")
        
        try:
            item = SvgPathItem(path)
            print(f"✓ SUCCESS: start={item.start}, end={item.end}, type='{item.type}'")
            if hasattr(item, 'args') and item.args:
                print(f"           args={item.args}")
            passed += 1
        except Exception as e:
            print(f"✗ FAILED: {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*70)
    
    if failed == 0:
        print("🎉 All tests passed! KiCad 9 SVG path parsing should work correctly.")
        return True
    else:
        print("⚠️  Some tests failed. There may still be issues with certain path formats.")
        return False

if __name__ == "__main__":
    print("KiCad 9 SVG Path Parsing Test Suite")
    print("This script tests the compatibility fixes for SVG path parsing.")
    
    success = test_svg_path_parsing()
    
    if success:
        print("\n✓ The updated SvgPathItem class should resolve the KiCad 9 compatibility issues.")
        print("  You can now update your PcbDraw installation and retry your command.")
    else:
        print("\n✗ There are still issues that need to be addressed.")
        
    sys.exit(0 if success else 1)
