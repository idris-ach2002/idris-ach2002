#!/usr/bin/env python3
"""Build the white project gallery from its editable JSON selection."""
from pathlib import Path
import html
import json

repo = Path(__file__).resolve().parents[1]
projects = json.loads((repo/'projects.json').read_text())
assets = repo/'assets'
icons = {
    'fileflow': '<path d="M8 10V3h17l7 7v24H8V22M25 3v8h7M2 17h20m-5-5 5 5-5 5"/>',
    'portfolio': '<rect x="2" y="3" width="34" height="23" rx="3"/><path d="M2 10h34M12 32h14M19 26v6M14 15l-4 3 4 3m10-6 4 3-4 3"/><circle cx="7" cy="6.5" r=".6"/>',
    'ais': '<path d="M3 24h32l-6 9H10zM12 24V13h14v11M18 13V5m0 0 9 4-9 4M1 37c4-3 8 3 12 0s8 3 12 0 8 3 12 0"/>',
    'graphes': '<path d="m5 8 14 10 13-11M19 18l-14 14m14-14 15 15M5 8v24m27-25 2 26"/><circle cx="5" cy="8" r="4"/><circle cx="19" cy="18" r="4"/><circle cx="32" cy="7" r="4"/><circle cx="5" cy="32" r="4"/><circle cx="34" cy="33" r="4"/>',
    'huffman': '<path d="m19 5-10 13m10-13 10 13M9 18l-6 14m6-14 7 14m13-14-6 14m6-14 7 14"/><circle cx="19" cy="5" r="3"/><circle cx="9" cy="18" r="3"/><circle cx="29" cy="18" r="3"/><circle cx="3" cy="32" r="2.5"/><circle cx="16" cy="32" r="2.5"/><circle cx="23" cy="32" r="2.5"/><circle cx="36" cy="32" r="2.5"/>',
    'megablast': '<path d="m19 2 9 21 7 8-12-3-4-7-4 7-12 3 7-8zM19 29v8m-5-6v4m10-4v4"/><circle cx="19" cy="14" r="2.5"/>'
}
font = '-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif'
for index, project in enumerate(projects, 1):
    esc = html.escape
    name = project['title']
    size = 22 if len(name) > 21 else 24
    elements = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="395" height="230" viewBox="0 0 395 230" role="img" aria-label="'+esc(name,quote=True)+'">',
        '<rect x=".5" y=".5" width="394" height="229" rx="7" fill="white" stroke="#dce3eb"/>',
        '<path d="M22 26h16" stroke="#315b82" stroke-width="2"/>',
        f'<g font-family="{font}">',
        f'<text x="47" y="29" font-size="9" letter-spacing=".8" fill="#71869c">{esc(project["category"])}</text>',
        f'<text x="22" y="72" font-size="{size}" font-weight="600" fill="#233143">{esc(name)}</text>',
        f'<text x="22" y="106" font-size="13.5" fill="#475569">{esc(project["description"][0])}</text>',
        f'<text x="22" y="127" font-size="13.5" fill="#475569">{esc(project["description"][1])}</text>',
        f'<text x="22" y="153" font-size="9.5" fill="#7a8797">{esc(project["note"])}</text>',
        f'<text x="22" y="179" font-size="11" font-weight="600" fill="#315b82">{esc(project["stack"])}</text>',
        '<text x="22" y="210" font-size="11" fill="#315b82">Explorer le projet</text>',
        '<path d="M121 212l9-9m-7 0h7v7" fill="none" stroke="#315b82" stroke-width="1.2" stroke-linecap="round"/>',
        f'<text x="352" y="212" font-size="9" fill="#8c9aaa">{index:02}</text></g>',
        '<g transform="translate(334,12) scale(.74)" fill="white" stroke="#527697" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'+icons[project['slug']]+'</g></svg>'
    ]
    (assets/f'project-{project["slug"]}.svg').write_text(''.join(elements),encoding='utf-8')
print(f'Built {len(projects)} linked project vignettes.')
