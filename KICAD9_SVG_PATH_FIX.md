# KiCad 9 SVG Path Handling Fix

This patch addresses the SVG path parsing issue in KiCad 9 where paths may start with numeric values instead of standard SVG commands.

## Problem

KiCad 9 generates SVG paths that don't follow the standard SVG path syntax that PcbDraw expects. Instead of:
```
M 136.00000 50.00000 L 140.00000 54.00000
```

KiCad 9 might generate:
```
136.00000 50.00000 140.00000 54.00000
```

## Solution

The fix includes:

1. **Enhanced SvgPathItem parsing**: Detects numeric-only paths and handles them gracefully
2. **Fallback mechanism**: If parsing fails, extracts coordinates and creates simple line paths
3. **Better error handling**: Provides debugging information while continuing processing

## Files Modified

- `pcbdraw/plot.py`: Updated `SvgPathItem.__init__()` and `get_board_polygon()`

## Testing

To test the fix with a KiCad 9 project:

```bash
# Enable debug output to see any path parsing warnings
pcbdraw plot your_board.kicad_pcb output.svg --silent=false
```

The tool will now show warnings for problematic paths but continue processing instead of crashing.

## Technical Details

The fix handles these cases:
1. Standard SVG paths (M x y L x y) - unchanged
2. Numeric-only paths (x y x y) - converted to implicit line commands
3. Invalid/malformed paths - skipped with warning, fallback attempted
4. Empty paths - handled gracefully

This maintains backward compatibility while adding KiCad 9 support.
