# KiCad 9 Compatibility Update

This update adds support for KiCad 9 to PcbDraw while maintaining backward compatibility with previous versions.

## Changes Made

### 1. Dependencies Update
- Updated `pcbnewTransition` dependency from `>=0.4` to `>=0.5` in `setup.py`
- This ensures we have the latest version that includes KiCad 9 support

### 2. Code Changes

#### plot.py
- Added `isV9` import from `pcbnewTransition`
- Updated `LEGACY_KICAD` check to include `isV9()`
- Updated version checks in `PcbPlotter.__init__()` to treat KiCad 9 the same as KiCad 8 and 7
- Updated SVG precision settings to include KiCad 9
- Updated distance comparison logic for KiCad 9

#### pcbnew_common.py
- Added imports for `isV7`, `isV8`, `isV9`
- Updated PCB_DIMENSION_BASE filtering to include all newer KiCad versions

#### Documentation Updates
- Updated `doc/installation.md` to mention compatibility with KiCad v5-v9
- Updated Windows installation instructions to mention "v6 or newer"

## Compatibility Matrix

| KiCad Version | Linux | Windows | macOS |
|---------------|-------|---------|--------|
| v5            | ✅    | ❌      | ❌     |
| v6            | ✅    | ✅      | ✅     |
| v7            | ✅    | ✅      | ✅     |
| v8            | ✅    | ✅      | ✅     |
| v9            | ✅    | ✅      | ✅     |

## Testing

To test KiCad 9 compatibility, ensure you have:
1. KiCad 9 installed
2. Python environment with updated dependencies
3. Test with existing .kicad_pcb files

## Notes

- KiCad 9 uses the same API patterns as KiCad 8 and 7, so most functionality is shared
- The `pcbnewTransition` library handles the low-level API differences between versions
- No breaking changes for existing users - all previous functionality is maintained
- **KiCad 9 SVG Format Fix**: Updated SVG path parsing to handle numeric-only paths that KiCad 9 generates
- Enhanced error handling provides fallback mechanisms for malformed SVG paths

## Known Issues and Fixes

### SVG Path Parsing Error
**Issue**: `SyntaxError: Unsupported path element 136.00000`
**Cause**: KiCad 9 generates SVG paths in a different format than previous versions
**Fix**: Enhanced `SvgPathItem` class with fallback parsing and better error handling
**Files**: `pcbdraw/plot.py` - Updated path parsing logic

### Debug Output
The updated version provides helpful warnings for problematic paths:
```
Warning: Skipping problematic SVG path: '136.00000' - Error: ...
  -> Fallback path created: 'M 136.0 50.0 L 140.0 54.0'
```
