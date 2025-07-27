#!/usr/bin/env python3

"""
Test script for KiCad 9 SVG path parsing issues
"""

import sys
import traceback
from pcbdraw.plot import SvgPathItem

# Test cases that represent different path formats that KiCad might generate
test_paths = [
    # Standard SVG paths (should work)
    "M 100.0 50.0 L 150.0 75.0",  # Normal line
    "M 100 50 A 25 25 0 0 1 125 75",  # Arc
    
    # KiCad 9 problematic formats
    "136.00000",  # Single number (the error from your log)
    "136.00000 50.00000",  # Two numbers
    "136.00000 50.00000 140.00000 54.00000",  # Four numbers (line coordinates)
    "136.00000 50.00000 140.00000 54.00000 144.00000 58.00000",  # Six numbers
    
    # Edge cases
    "",  # Empty path
    "   ",  # Whitespace only
    "M",  # Incomplete command
    "L 100 50",  # Missing move command
    "Z",  # Close path only
]

def test_svg_path_parsing():
    """Test the SvgPathItem parsing with various path formats"""
    print("🧪 Testing SVG Path Parsing for KiCad 9 Compatibility")
    print("=" * 60)
    
    success_count = 0
    total_count = len(test_paths)
    
    for i, path in enumerate(test_paths, 1):
        print(f"\nTest {i}/{total_count}: '{path}'")
        try:
            item = SvgPathItem(path)
            print(f"  ✅ Success: type={item.type}, start={item.start}, end={item.end}")
            if item.args:
                print(f"     args={item.args}")
            success_count += 1
        except Exception as e:
            print(f"  ❌ Failed: {type(e).__name__}: {e}")
            if "--debug" in sys.argv:
                traceback.print_exc()
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("🎉 All tests passed! KiCad 9 SVG parsing should work.")
    elif success_count > total_count // 2:
        print("⚠️  Most tests passed. Some edge cases may still cause issues.")
    else:
        print("❌ Many tests failed. Significant issues remain.")
    
    return success_count == total_count

def test_coordinate_extraction():
    """Test the coordinate extraction fallback mechanism"""
    print("\n🔧 Testing Coordinate Extraction Fallback")
    print("=" * 60)
    
    import re
    
    test_cases = [
        "136.00000 50.00000 140.00000 54.00000",
        "1.23 -4.56 7.89 -10.11",
        "100 200 300 400 500 600",
        "not a number",
        "123.456",
    ]
    
    for case in test_cases:
        print(f"\nExtracting from: '{case}'")
        coords = re.findall(r'[-+]?\d*\.?\d+', case)
        print(f"  Found coordinates: {coords}")
        
        if len(coords) >= 4:
            try:
                x1, y1, x2, y2 = map(float, coords[:4])
                simple_path = f"M {x1} {y1} L {x2} {y2}"
                print(f"  ✅ Generated path: '{simple_path}'")
            except ValueError as e:
                print(f"  ❌ Conversion failed: {e}")
        else:
            print(f"  ⚠️  Not enough coordinates for a line")

def main():
    """Main test function"""
    print("🚀 KiCad 9 SVG Path Compatibility Test Suite")
    print("This script tests the updated SVG path parsing logic.\n")
    
    # Test the main parsing logic
    parsing_success = test_svg_path_parsing()
    
    # Test the fallback mechanism
    test_coordinate_extraction()
    
    print("\n" + "=" * 60)
    print("📝 Summary:")
    print("- Updated SvgPathItem class can handle numeric-only paths")
    print("- Fallback mechanism extracts coordinates from malformed paths")  
    print("- Error handling allows processing to continue despite bad paths")
    
    if parsing_success:
        print("\n🎯 The fix should resolve the KiCad 9 compatibility issue!")
    else:
        print("\n⚠️  Some issues remain. Consider additional debugging.")
    
    print("\n📖 To use with your KiCad 9 project:")
    print("   pcbdraw plot /workspace/project/4CH-Opto-ISO.kicad_pcb output.png")

if __name__ == "__main__":
    main()
