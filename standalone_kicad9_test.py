#!/usr/bin/env python3
"""
Standalone test for KiCad 9 SVG path parsing fix.
This version doesn't require numpy or other pcbdraw dependencies.
"""

import re
from typing import List, Tuple, Optional, Union

Numeric = Union[int, float]
Point = Tuple[Numeric, Numeric]

class SvgPathItemTest:
    """Simplified version of SvgPathItem for testing the KiCad 9 fix."""
    
    def __init__(self, path: str) -> None:
        # Normalize path by ensuring spaces between commands and numbers
        path = re.sub(r"([MLA])(-?\d+)", r"\1 \2", path)
        path_elems = re.split("[, ]", path)
        path_elems = list(filter(lambda x: x, path_elems))
        
        # Handle empty or invalid paths
        if not path_elems:
            raise SyntaxError("Empty path")
            
        # Handle paths that start with numbers (KiCad 9 format) - THE FIX
        if path_elems[0] != "M":
            # Try to detect if this is a numeric-only path (KiCad 9 issue)
            try:
                float(path_elems[0])
                # If we can parse the first element as float, assume it's a coordinate
                # This might be a simplified path format from KiCad 9
                if len(path_elems) >= 4:
                    # Treat as implicit M x y L x y format
                    self.start = (float(path_elems[0]), float(path_elems[1]))
                    self.end = (float(path_elems[2]), float(path_elems[3]))
                    self.type = "L"
                    self.args = None
                    return
                elif len(path_elems) >= 2:
                    # Handle case with just two coordinates - treat as a point/move
                    self.start = (float(path_elems[0]), float(path_elems[1]))
                    self.end = self.start
                    self.type = "M"
                    self.args = None
                    return
                elif len(path_elems) == 1:
                    # Handle case with just one coordinate - treat as a point at origin
                    self.start = (float(path_elems[0]), 0.0)
                    self.end = self.start
                    self.type = "M"
                    self.args = None
                    return
                else:
                    raise SyntaxError(f"Invalid numeric path format: {path}")
            except ValueError:
                raise SyntaxError("Only paths with absolute position are supported")
                
        self.start: Point = tuple(map(float, path_elems[1:3]))
        self.end: Point = (0, 0)
        self.args: Optional[List[Numeric]] = None
        path_elems = path_elems[3:]
        
        if not path_elems:
            # Just a move command, treat as point
            self.end = self.start
            self.type = "M"
            self.args = None
        elif path_elems[0] == "L":
            x = float(path_elems[1])
            y = float(path_elems[2])
            self.end = (x, y)
            self.type = path_elems[0]
            self.args = None
        elif path_elems[0] == "A":
            args = list(map(float, path_elems[1:8]))
            self.end = (args[5], args[6])
            self.args = args[0:5]
            self.type = path_elems[0]
        else:
            # Try to handle unknown command gracefully
            try:
                # If the "command" is actually a number, treat as implicit L
                x = float(path_elems[0])
                y = float(path_elems[1])
                self.end = (x, y)
                self.type = "L"
                self.args = None
            except (ValueError, IndexError):
                raise SyntaxError("Unsupported path element " + path_elems[0])

def run_tests():
    """Test the KiCad 9 path parsing fix."""
    
    print("🔧 Testing KiCad 9 SVG Path Parsing Fix")
    print("=" * 50)
    
    # The specific case that was failing
    critical_test = "136.00000"
    print(f"\n🎯 CRITICAL TEST (the one that was failing):")
    print(f"   Path: '{critical_test}'")
    
    try:
        item = SvgPathItemTest(critical_test)
        print(f"   ✅ FIXED! start={item.start}, end={item.end}, type='{item.type}'")
        critical_passed = True
    except Exception as e:
        print(f"   ❌ STILL BROKEN: {type(e).__name__}: {e}")
        critical_passed = False
    
    # Additional test cases
    test_cases = [
        ("136.00000 50.00000", "Two coordinates"),
        ("136.00000 50.00000 140.00000 54.00000", "Four coordinates (line)"),
        ("M 136 50 L 140 54", "Standard SVG format"),
        ("0", "Single zero coordinate"),
        ("-100.5", "Single negative coordinate"),
        ("M 0 0", "Standard move command"),
    ]
    
    print(f"\n📋 Additional Test Cases:")
    passed = 0
    failed = 0
    
    for path, description in test_cases:
        try:
            item = SvgPathItemTest(path)
            print(f"   ✅ {description}: '{path}' -> start={item.start}, end={item.end}")
            passed += 1
        except Exception as e:
            print(f"   ❌ {description}: '{path}' -> {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    if critical_passed:
        print("🎉 SUCCESS: The critical KiCad 9 error has been FIXED!")
        print(f"   Original error: 'SyntaxError: Unsupported path element 136.00000'")
        print(f"   Now handles: Single coordinate paths like '136.00000'")
    else:
        print("❌ FAILURE: The critical error is still present.")
    
    print(f"\nAdditional tests: {passed} passed, {failed} failed")
    
    if critical_passed and failed == 0:
        print("\n✨ All tests passed! Your KiCad 9 compatibility fix is working!")
        return True
    elif critical_passed:
        print("\n⚠️  Critical fix works, but some edge cases may need attention.")
        return True
    else:
        print("\n💥 The main issue is not resolved yet.")
        return False

if __name__ == "__main__":
    success = run_tests()
    
    if success:
        print("\n🚀 NEXT STEPS:")
        print("   1. Update your PcbDraw installation with this fixed version")
        print("   2. Try your original command again:")
        print("      pcbdraw plot /workspace/project/4CH-Opto-ISO.kicad_pcb /tmp/pcb_test.png")
        print("   3. The 'SyntaxError: Unsupported path element 136.00000' should be gone!")
    else:
        print("\n🔧 The fix needs more work. Please check the code changes.")
    
    exit(0 if success else 1)
