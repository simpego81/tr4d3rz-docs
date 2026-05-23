#!/usr/bin/env python3
"""
extract_archimate_data.py — Extracts ArchiMate data from HTML files into JSON

Scans all device HTML files in docs/, extracts KB (Knowledge Base) and RELS
(Relationships) from JavaScript, unifies them, and generates archimate_data.json.

Usage:
    python extract_archimate_data.py

Output:
    docs/archimate_data.json — Unified ArchiMate data for all devices
"""

import json
import re
import glob
from pathlib import Path
from datetime import datetime, timezone


def extract_js_object(html_content, object_name):
    """
    Extract a JavaScript object from HTML using regex.

    Args:
        html_content: HTML file content as string
        object_name: Name of the JS variable (e.g., "KB" or "RELS")

    Returns:
        String representation of the JS object, or None if not found
    """
    # Pattern to match: const OBJECT_NAME = { ... };
    # For KB: matches until closing brace at same depth
    # For RELS: matches array [ ... ]

    if object_name == "KB":
        # Find "const KB = {"
        pattern = r'const\s+KB\s*=\s*(\{)'
        match = re.search(pattern, html_content)
        if not match:
            return None

        start_pos = match.start(1)
        depth = 0
        i = start_pos

        while i < len(html_content):
            char = html_content[i]
            if char == '{':
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0:
                    # Found closing brace
                    return html_content[start_pos:i+1]
            i += 1

        return None

    elif object_name == "RELS":
        # Find "const RELS = ["
        pattern = r'const\s+RELS\s*=\s*(\[)'
        match = re.search(pattern, html_content)
        if not match:
            return None

        start_pos = match.start(1)
        depth = 0
        i = start_pos

        while i < len(html_content):
            char = html_content[i]
            if char == '[':
                depth += 1
            elif char == ']':
                depth -= 1
                if depth == 0:
                    return html_content[start_pos:i+1]
            i += 1

        return None

    return None


def parse_kb_js_to_dict(kb_js_str):
    """
    Parse JavaScript KB object to Python dict.

    The KB structure is:
    {
      "element_id": {
        "title": "...",
        "type": "...",
        ...
      }
    }

    We need to convert JS object literal syntax to valid JSON.
    """
    if not kb_js_str:
        return {}

    # Remove leading/trailing whitespace
    kb_js_str = kb_js_str.strip()

    # Remove trailing semicolon if present
    kb_js_str = kb_js_str.rstrip(';')

    try:
        # Try parsing as-is first (might already be valid JSON with double quotes)
        kb_dict = json.loads(kb_js_str)
        return kb_dict
    except json.JSONDecodeError:
        # If that fails, try converting single quotes to double quotes
        try:
            kb_js_str = kb_js_str.replace("'", '"')
            kb_dict = json.loads(kb_js_str)
            return kb_dict
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse KB as JSON: {e}")
            print(f"First 200 chars: {kb_js_str[:200]}")
            return {}


def parse_rels_js_to_list(rels_js_str):
    """
    Parse JavaScript RELS array to Python list.

    The RELS structure is:
    [
      { from: 'id1', to: 'id2', type: 'Realization', label: '' },
      ...
    ]
    """
    if not rels_js_str:
        return []

    # Remove leading/trailing whitespace
    rels_js_str = rels_js_str.strip()

    # Remove trailing semicolon
    rels_js_str = rels_js_str.rstrip(';')

    # Replace single quotes with double quotes (RELS uses single quotes)
    rels_js_str = rels_js_str.replace("'", '"')

    # Fix JavaScript object notation: { from: "..." } → { "from": "..." }
    # Add quotes around unquoted keys
    rels_js_str = re.sub(r'(\w+):', r'"\1":', rels_js_str)

    try:
        rels_list = json.loads(rels_js_str)
        return rels_list
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse RELS as JSON: {e}")
        print(f"First 200 chars: {rels_js_str[:200]}")
        return []


def extract_device_name(html_path):
    """Extract device name from HTML filename (e.g., 'rpi1.html' → 'rpi1')"""
    return Path(html_path).stem


def main():
    """Main extraction logic"""

    print("TR4D3RZ ArchiMate Data Extractor")
    print("=" * 50)

    # Find all HTML files in docs/ (excluding index.html)
    html_files = glob.glob("docs/*.html")
    html_files = [f for f in html_files if Path(f).stem != "index"]

    print(f"Found {len(html_files)} device HTML files")

    # Unified data structures
    unified_elements = {}  # { element_id: { ...metadata, devices: [...] } }
    unified_relationships = []  # List of { from, to, type, label, devices: [...] }
    relationship_set = set()  # To track unique relationships

    devices_processed = []

    # Process each HTML file
    for html_path in sorted(html_files):
        device_name = extract_device_name(html_path)
        print(f"\nProcessing: {device_name}")

        # Read HTML content
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Extract KB
        kb_js = extract_js_object(html_content, "KB")
        if kb_js:
            kb_dict = parse_kb_js_to_dict(kb_js)
            print(f"  [OK] Extracted {len(kb_dict)} elements from KB")

            # Add elements to unified collection
            for element_id, element_data in kb_dict.items():
                if element_id not in unified_elements:
                    # First time seeing this element
                    unified_elements[element_id] = element_data.copy()
                    unified_elements[element_id]['devices'] = [device_name]
                else:
                    # Element already exists, just add device
                    if device_name not in unified_elements[element_id]['devices']:
                        unified_elements[element_id]['devices'].append(device_name)
        else:
            print(f"  [WARN] No KB found")

        # Extract RELS
        rels_js = extract_js_object(html_content, "RELS")
        if rels_js:
            rels_list = parse_rels_js_to_list(rels_js)
            print(f"  [OK] Extracted {len(rels_list)} relationships from RELS")

            # Add relationships to unified collection (avoid duplicates)
            for rel in rels_list:
                # Create a unique key for the relationship
                rel_key = (rel['from'], rel['to'], rel['type'])

                if rel_key not in relationship_set:
                    # New relationship
                    relationship_set.add(rel_key)
                    rel_copy = rel.copy()
                    rel_copy['devices'] = [device_name]
                    unified_relationships.append(rel_copy)
                else:
                    # Relationship exists, add device
                    for existing_rel in unified_relationships:
                        if (existing_rel['from'] == rel['from'] and
                            existing_rel['to'] == rel['to'] and
                            existing_rel['type'] == rel['type']):
                            if device_name not in existing_rel['devices']:
                                existing_rel['devices'].append(device_name)
                            break
        else:
            print(f"  [WARN] No RELS found")

        devices_processed.append(device_name)

    # Build final JSON structure
    archimate_data = {
        "elements": unified_elements,
        "relationships": unified_relationships,
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_elements": len(unified_elements),
            "total_relationships": len(unified_relationships),
            "devices": devices_processed,
            "extractor_version": "1.0.0"
        }
    }

    # Save to JSON file
    output_path = "docs/archimate_data.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(archimate_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 50)
    print(f"[SUCCESS] Extraction complete!")
    print(f"  Total unique elements: {len(unified_elements)}")
    print(f"  Total unique relationships: {len(unified_relationships)}")
    print(f"  Devices processed: {len(devices_processed)}")
    print(f"\n  Output: {output_path}")

    # Print layer distribution
    layer_counts = {}
    for elem in unified_elements.values():
        layer = elem.get('layer', 'Unknown')
        layer_counts[layer] = layer_counts.get(layer, 0) + 1

    print("\n  Element distribution by layer:")
    for layer in ['Motivation', 'Business', 'Application', 'Technology']:
        count = layer_counts.get(layer, 0)
        print(f"    {layer:12}: {count:3} elements")

    # Print Technology_Device count (for R5 ring)
    tech_devices = sum(1 for elem in unified_elements.values()
                      if elem.get('type') == 'Technology_Device')
    print(f"\n  Technology_Device elements (R5 ring): {tech_devices}")


if __name__ == "__main__":
    main()
