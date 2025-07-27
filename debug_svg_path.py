#!/usr/bin/env python3
"""Debug script to test SVG path parsing with KiCad 9 format."""

import re
from typing import List, Tuple, Optional, Union

Numeric = Union[int, float]
Point = Tuple[Numeric, Numeric]

class SvgPathItem:
    def __init__(self, path: str) -> None:
        print(f"DEBUG: Parsing path: '{path}'")
        
        # Normalize path by ensuring spaces between commands and numbers
        path = re.sub(r"([MLA])(-?\d+)", r"\1 \2", path)
        path_elems = re.split("[, ]", path)
        path_elems = list(filter(lambda x: x, path_elems))
        
        print(f"DEBUG: Path elements: {path_elems}")
        
        # Handle empty or invalid paths
        if not path_elems:
            raise SyntaxError("Empty path")
            
        # Handle paths that start with numbers (KiCad 9 format)
        if path_elems[0] != "M":
            print(f"DEBUG: Path doesn't start with M, first element: '{path_elems[0]}'")
            # Try to detect if this is a numeric-only path (KiCad 9 issue)
            try:
                float(path_elems[0])
                print(f"DEBUG: First element is numeric: {float(path_elems[0])}")
                # If we can parse the first element as float, assume it's a coordinate
                # This might be a simplified path format from KiCad 9
                if len(path_elems) >= 4:
                    # Treat as implicit M x y L x y format
                    self.start = (float(path_elems[0]), float(path_elems[1]))
                    self.end = (float(path_elems[2]), float(path_elems[3]))
                    self.type = "L"
                    self.args = None
                    print(f"DEBUG: Created line from {self.start} to {self.end}")
                    return
                elif len(path_elems) >= 2:
                    # Handle case with just two coordinates - treat as a point/move
                    self.start = (float(path_elems[0]), float(path_elems[1]))
                    self.end = self.start
                    self.type = "M"
                    self.args = None
                    print(f"DEBUG: Created point at {self.start}")
                    return
                elif len(path_elems) == 1:
                    # Handle case with just one coordinate - treat as a point at origin
                    self.start = (float(path_elems[0]), 0.0)
                    self.end = self.start
                    self.type = "M"
                    self.args = None
                    print(f"DEBUG: Created single-coordinate point at {self.start}")
                    return
                else:
                    raise SyntaxError(f"Invalid numeric path format: {path}")
            except ValueError as e:
                print(f"DEBUG: ValueError when parsing as numeric: {e}")
                raise SyntaxError("Only paths with absolute position are supported")
                
        print(f"DEBUG: Standard path processing")
        self.start: Point = tuple(map(float, path_elems[1:3])) # type: ignore
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

# Test the problematic case
if __name__ == "__main__":
    test_paths = [
        "136.00000",  # The problematic case from the error
        "136.00000 50.00000",  # Two coordinates
        "136.00000 50.00000 140.00000 54.00000",  # Four coordinates
        "M 136 50 L 140 54",  # Standard format
    ]
    
    for test_path in test_paths:
        print(f"\n=== Testing path: '{test_path}' ===")
        try:
            item = SvgPathItem(test_path)
            print(f"SUCCESS: start={item.start}, end={item.end}, type={item.type}")
        except Exception as e:
            print(f"ERROR: {e}")
