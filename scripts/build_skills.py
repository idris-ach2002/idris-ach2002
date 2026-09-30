#!/usr/bin/env python3
"""Compose the profile's technology logos into three clean rows."""
from pathlib import Path
import copy
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
assets = Path(__file__).resolve().parents[1] / 'assets'
root = ET.Element(f'{{{SVG}}}svg', {
    'width':'800', 'height':'276', 'viewBox':'0 0 800 276', 'role':'img',
    'aria-label':'Environnement technique : langages, web et applications, données et outils'
})
ET.SubElement(root, f'{{{SVG}}}rect', {'width':'800','height':'276','fill':'white'})
font = '-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif'
sets = [
    ('languages','01','Langages','Java · Rust · JavaScript · TypeScript · Haskell · C · C++ · PHP · Python'),
    ('web','02','Web & applications','React · Angular · Spring · Symfony · HTML · CSS · Vite · Tailwind'),
    ('tools','03','Données & outils','PostgreSQL · SQLite · Git · Docker · Linux · GitHub Actions · Cloudflare · Tauri')
]
for row, (key, number, title, caption) in enumerate(sets):
    y = row*92
    group = ET.SubElement(root, f'{{{SVG}}}g', {'font-family':font})
    label = ET.SubElement(group, f'{{{SVG}}}text', {'x':'0','y':str(y+25),'fill':'#7790a8','font-size':'10','letter-spacing':'1.5'})
    label.text = number + ' /'
    heading = ET.SubElement(group, f'{{{SVG}}}text', {'x':'0','y':str(y+49),'fill':'#263648','font-size':'17','font-weight':'600'})
    heading.text = title
    label = ET.SubElement(group, f'{{{SVG}}}text', {'x':'243','y':str(y+72),'fill':'#64748b','font-size':'10.5'})
    label.text = caption
    source = ET.fromstring((assets/f'skills-{key}-light.svg').read_text())
    for index, source_icon in enumerate(source):
        icon = copy.deepcopy(source_icon)
        prefix = f'{key}-{index}-'
        original_ids = {e.attrib['id'] for e in icon.iter() if 'id' in e.attrib}
        for element in icon.iter():
            for attribute, value in list(element.attrib.items()):
                if attribute == 'id':
                    element.attrib[attribute] = prefix+value
                else:
                    for original_id in original_ids:
                        value = value.replace(f'url(#{original_id})',f'url(#{prefix}{original_id})')
                        if value == f'#{original_id}': value = f'#{prefix}{original_id}'
                    element.attrib[attribute] = value
        icon.set('transform',f'translate({243+index*56},{y+10}) scale(0.15625)')
        group.append(icon)
    if row < 2:
        ET.SubElement(group, f'{{{SVG}}}path', {'d':f'M0 {y+91}h800','stroke':'#e2e8f0'})
(assets/'skills-profile-light.svg').write_text(ET.tostring(root,encoding='unicode'),encoding='utf-8')

mobile = copy.deepcopy(root)
mobile.set('width','400')
mobile.set('height','426')
mobile.set('viewBox','0 0 400 426')
mobile[0].set('width','400')
mobile[0].set('height','426')
for row, group in enumerate(list(mobile)[1:]):
    y = row*142
    texts = [e for e in group if e.tag == f'{{{SVG}}}text']
    texts[0].set('y',str(y+18))
    texts[1].set('x','32')
    texts[1].set('y',str(y+19))
    texts[1].set('font-size','16')
    texts[2].set('x','0')
    texts[2].set('y',str(y+130))
    texts[2].set('font-size','9')
    icons = [e for e in group if e.tag == f'{{{SVG}}}g']
    for index, icon in enumerate(icons):
        icon.set('transform',f'translate({(index%5)*57},{y+34+(index//5)*46}) scale(0.15625)')
    for separator in [e for e in group if e.tag == f'{{{SVG}}}path']:
        separator.set('d',f'M0 {y+141}h400')
(assets/'skills-profile-mobile.svg').write_text(ET.tostring(mobile,encoding='unicode'),encoding='utf-8')
print('Composed personal skills graphic.')
