"""Fix double-encoded UTF-8 (Windows-1252 mojibake) in HTML/text files.

Pattern: file was saved as UTF-8, then read as cp1252, then saved as UTF-8 again.
Fix: reverse the process by encoding chars back to cp1252 bytes, then decode as UTF-8.
"""

import sys
import os

# Build reverse cp1252 map: Unicode char -> byte value
# Handles all 256 byte values including undefined cp1252 positions (0x81,0x8D,0x8F,0x90,0x9D)
reverse_cp1252 = {}
for byte_val in range(256):
    try:
        char = bytes([byte_val]).decode('cp1252')
        reverse_cp1252[char] = byte_val
    except Exception:
        reverse_cp1252[chr(byte_val)] = byte_val


def fix_mojibake(text):
    """Convert double-encoded UTF-8 (via cp1252) back to correct UTF-8."""
    result = bytearray()
    for ch in text:
        cp = ord(ch)
        if cp < 0x80:
            result.append(cp)
        elif ch in reverse_cp1252:
            result.append(reverse_cp1252[ch])
        else:
            # Character not representable in cp1252 - keep as-is
            result.extend(ch.encode('utf-8'))
    return result.decode('utf-8')


def needs_fixing(text):
    """Heuristic: check if text contains common mojibake patterns."""
    patterns = [
        '\u00e2\u20ac',      # â€ (start of many mojibake sequences)
        '\u00c3\u0082\u00c2',  # Ã‚Â (double-encoded non-breaking space area)
        '\u00c2\u00b7',      # Â· (middle dot)
        '\u00c2\u00a7',      # Â§ (section sign)
        '\u00c3\u0083',      # Ãƒ (various double-encoded chars)
    ]
    return any(p in text for p in patterns)


def fix_file(filepath):
    """Fix encoding in a file, preserving BOM if present."""
    with open(filepath, 'rb') as f:
        raw = f.read()

    has_bom = raw[:3] == b'\xef\xbb\xbf'
    content_bytes = raw[3:] if has_bom else raw

    text = content_bytes.decode('utf-8')

    if not needs_fixing(text):
        print(f'  SKIP (no mojibake detected): {filepath}')
        return False

    fixed = fix_mojibake(text)

    output = (b'\xef\xbb\xbf' if has_bom else b'') + fixed.encode('utf-8')
    with open(filepath, 'wb') as f:
        f.write(output)

    print(f'  FIXED: {filepath}')
    return True


if __name__ == '__main__':
    files_to_fix = sys.argv[1:] if len(sys.argv) > 1 else []

    if not files_to_fix:
        # Auto-discover all text files in the project
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        extensions = ('.html', '.md', '.puml', '.json', '.ps1', '.py')
        for root, dirs, files in os.walk(base):
            # Skip .git
            dirs[:] = [d for d in dirs if d != '.git']
            for fname in files:
                if any(fname.endswith(ext) for ext in extensions):
                    files_to_fix.append(os.path.join(root, fname))

    fixed_count = 0
    for fp in files_to_fix:
        try:
            if fix_file(fp):
                fixed_count += 1
        except Exception as e:
            print(f'  ERROR processing {fp}: {e}')

    print(f'\nDone. Fixed {fixed_count} file(s).')
