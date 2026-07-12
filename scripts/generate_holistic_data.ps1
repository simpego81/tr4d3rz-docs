# generate_holistic_data.ps1 — Generates archimate_data.json for holistic_view.html
Set-Location "$PSScriptRoot\.."
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$deviceList = @(
    @{ name = "android";  puml = "diagrams/per-device/device_android.puml" },
    @{ name = "browser";  puml = "diagrams/per-device/device_browser.puml" },
    @{ name = "esp";      puml = "diagrams/per-device/device_esp.puml"     },
    @{ name = "linux";    puml = "diagrams/per-device/device_linux.puml"   },
    @{ name = "mimx";     puml = "diagrams/per-device/device_mimx.puml"    },
    @{ name = "phone";    puml = "diagrams/per-device/device_phone.puml"   },
    @{ name = "ra8";      puml = "diagrams/per-device/device_ra8.puml"     },
    @{ name = "rasp2";    puml = "diagrams/per-device/device_rasp2.puml"   },
    @{ name = "stm32f1";  puml = "diagrams/per-device/device_stm32f1.puml" },
    @{ name = "stm32f3";  puml = "diagrams/per-device/device_stm32f3.puml" },
    @{ name = "str";      puml = "diagrams/per-device/device_str.puml"     },
    @{ name = "tablet";   puml = "diagrams/per-device/device_tablet.puml"  },
    @{ name = "m24lr";    puml = "diagrams/per-device/device_m24lr.puml"   }
)

# ── Data structures for aggregation ────────────────────────────────────────
$globalElements = @{}    # ID → { type, title, devices[] }
$globalRelations = @()   # Array of { from, to, type, label, devices[] }

# ── Extract elements from PUML ─────────────────────────────────────────────
function Extract-Elements($puml, $deviceName) {
    $elements = @{}
    # Match all ArchiMate element declarations
    # Format: ElementType(id, "Title\nWith\nNewlines")
    $elemRegex = [regex]'(Motivation_\w+|Business_\w+|Application_\w+|Technology_\w+)\s*\(\s*(\w+)\s*,\s*"([^"]+)"\s*\)'

    foreach ($m in $elemRegex.Matches($puml)) {
        $type  = $m.Groups[1].Value
        $id    = $m.Groups[2].Value
        $title = $m.Groups[3].Value -replace '\\n', ' ' -replace '\s+', ' '

        $elements[$id] = @{
            type  = $type
            title = $title.Trim()
        }
    }

    return $elements
}

# ── Extract relationships from PUML ────────────────────────────────────────
function Extract-Relations($puml, $deviceName) {
    $relations = @()
    # Format: Rel_Type(from, to) or Rel_Type(from, to, "label")
    $relRegex = [regex]'Rel_(\w+?)(?:_(?:Up|Down|Left|Right|Up2|Down2))?\s*\(\s*(\w+)\s*,\s*(\w+)(?:\s*,\s*"([^"]*)")?\)'

    foreach ($m in $relRegex.Matches($puml)) {
        $type  = $m.Groups[1].Value
        $from  = $m.Groups[2].Value
        $to    = $m.Groups[3].Value
        $label = if ($m.Groups[4].Success) { $m.Groups[4].Value } else { "" }

        $relations += @{
            from  = $from
            to    = $to
            type  = $type
            label = $label
        }
    }

    return $relations
}

# ── Extract KB metadata from HTML ──────────────────────────────────────────
function Extract-KB-From-HTML($htmlPath) {
    if (-not (Test-Path $htmlPath)) { return @{} }

    $html = [System.IO.File]::ReadAllText((Resolve-Path $htmlPath), [System.Text.Encoding]::UTF8)
    $kbStart = $html.IndexOf('const KB = {')
    if ($kbStart -lt 0) { return @{} }

    $kbStart += 'const KB = '.Length
    $depth = 0; $i = $kbStart
    while ($i -lt $html.Length) {
        $c = $html[$i]
        if ($c -eq '{') { $depth++ }
        elseif ($c -eq '}') { $depth--; if ($depth -eq 0) { break } }
        $i++
    }

    $kbText = $html.Substring($kbStart, $i - $kbStart + 1)

    # Extract each element from KB using regex
    $kb = @{}
    $elemRegex = [regex]'"(\w+)":\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'

    foreach ($m in $elemRegex.Matches($kbText)) {
        $id = $m.Groups[1].Value
        $props = $m.Groups[2].Value

        # Extract properties
        $title     = if ($props -match '"title":\s*"([^"]*)"')      { $matches[1] } else { "" }
        $type      = if ($props -match '"type":\s*"([^"]*)"')       { $matches[1] } else { "" }
        $layer     = if ($props -match '"layer":\s*"([^"]*)"')      { $matches[1] } else { "" }
        $aspect    = if ($props -match '"aspect":\s*"([^"]*)"')     { $matches[1] } else { "" }
        $type_desc = if ($props -match '"type_desc":\s*"([^"]*)"')  { $matches[1] } else { "" }
        $role      = if ($props -match '"role":\s*"([^"]*)"')       { $matches[1] } else { "" }
        $tech      = if ($props -match '"tech":\s*"([^"]*)"')       { $matches[1] } else { "" }
        $relations = if ($props -match '"relations":\s*"([^"]*)"')  { $matches[1] } else { "" }

        $kb[$id] = @{
            title     = $title
            type      = $type
            layer     = $layer
            aspect    = $aspect
            type_desc = $type_desc
            role      = $role
            tech      = $tech
            relations = $relations
        }
    }

    return $kb
}

# ══════════════════════════════════════════════════════════════════════════
# Main aggregation loop
# ══════════════════════════════════════════════════════════════════════════

Write-Host "Analyzing PUML files..."

foreach ($dev in $deviceList) {
    $pumlPath = $dev.puml
    $htmlPath = "docs\$($dev.name).html"

    if (-not (Test-Path $pumlPath)) {
        Write-Warning "SKIP: $pumlPath not found"
        continue
    }

    $puml = [System.IO.File]::ReadAllText((Resolve-Path $pumlPath), [System.Text.Encoding]::UTF8)
    $kb   = Extract-KB-From-HTML $htmlPath

    # Extract elements and track devices
    $elements = Extract-Elements $puml $dev.name
    foreach ($id in $elements.Keys) {
        if (-not $globalElements.ContainsKey($id)) {
            $globalElements[$id] = @{
                type    = $elements[$id].type
                title   = $elements[$id].title
                devices = @()
                # Metadata from KB (if available)
                layer     = if ($kb[$id]) { $kb[$id].layer } else { "" }
                aspect    = if ($kb[$id]) { $kb[$id].aspect } else { "" }
                type_desc = if ($kb[$id]) { $kb[$id].type_desc } else { "" }
                role      = if ($kb[$id]) { $kb[$id].role } else { "" }
                tech      = if ($kb[$id]) { $kb[$id].tech } else { "" }
                relations = if ($kb[$id]) { $kb[$id].relations } else { "" }
            }
        }

        # Add device to this element (avoid duplicates)
        if ($globalElements[$id].devices -notcontains $dev.name) {
            $globalElements[$id].devices += $dev.name
        }
    }

    # Extract relations and track devices
    $relations = Extract-Relations $puml $dev.name
    foreach ($rel in $relations) {
        # Find if this relation already exists
        $existing = $globalRelations | Where-Object {
            $_.from -eq $rel.from -and $_.to -eq $rel.to -and $_.type -eq $rel.type
        } | Select-Object -First 1

        if ($existing) {
            # Add device to existing relation
            if ($existing.devices -notcontains $dev.name) {
                $existing.devices += $dev.name
            }
        } else {
            # New relation
            $globalRelations += @{
                from    = $rel.from
                to      = $rel.to
                type    = $rel.type
                label   = $rel.label
                devices = @($dev.name)
            }
        }
    }

    Write-Host "  $($dev.name): $($elements.Count) elements, $($relations.Count) relations"
}

# ══════════════════════════════════════════════════════════════════════════
# Build JSON structure
# ══════════════════════════════════════════════════════════════════════════

Write-Host ""
Write-Host "Building JSON structure..."

$json = @{
    metadata = @{
        generated = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        version   = "2.0"
        total_elements = $globalElements.Count
        total_relationships = $globalRelations.Count
    }
    elements = @{}
    relationships = @()
}

# Convert elements to JSON structure
foreach ($id in $globalElements.Keys) {
    $elem = $globalElements[$id]
    $json.elements[$id] = @{
        title     = $elem.title
        type      = $elem.type
        layer     = $elem.layer
        aspect    = $elem.aspect
        type_desc = $elem.type_desc
        role      = $elem.role
        tech      = $elem.tech
        relations = $elem.relations
        devices   = $elem.devices | Sort-Object
    }
}

# Convert relations to JSON structure
$json.relationships = $globalRelations | ForEach-Object {
    @{
        from    = $_.from
        to      = $_.to
        type    = $_.type
        label   = $_.label
        devices = $_.devices | Sort-Object
    }
}

# ══════════════════════════════════════════════════════════════════════════
# Write JSON file
# ══════════════════════════════════════════════════════════════════════════

$jsonPath = "docs\archimate_data.json"
$jsonText = $json | ConvertTo-Json -Depth 10

# Write JSON file (UTF-8 without BOM)
$fullPath = if (Test-Path $jsonPath) { (Resolve-Path $jsonPath).Path } else { Join-Path (Get-Location) $jsonPath }
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($fullPath, $jsonText, $utf8NoBom)

Write-Host "OK Generated: $jsonPath"
Write-Host "  - $($json.elements.Count) unique elements"
Write-Host "  - $($json.relationships.Count) unique relationships"
