#!/usr/bin/env python3
"""Refresh the profile's SVG from the public GitHub contribution calendar."""
import argparse
import datetime as dt
import html
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tooltip = None
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'td' and 'data-date' in a:
            self.cells[a['id']] = {'date': a['data-date'], 'level': int(a['data-level']), 'count': None}
        if tag == 'tool-tip':
            self.tooltip = a.get('for')
            self.buffer = []

    def handle_data(self, data):
        if self.tooltip:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if tag == 'tool-tip' and self.tooltip:
            if self.tooltip in self.cells:
                value = ''.join(self.buffer).strip()
                m = re.match(r'([\d,]+) contributions?\b', value)
                if m:
                    self.cells[self.tooltip]['count'] = int(m.group(1).replace(',', ''))
                elif value.startswith('No contributions'):
                    self.cells[self.tooltip]['count'] = 0
            self.tooltip = None


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'idris-ach2002-profile'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')


def parse_calendar(content):
    parser = CalendarParser()
    parser.feed(content)
    days = sorted(parser.cells.values(), key=lambda day: day['date'])
    heading = re.search(r'id="js-contribution-activity-description"[^>]*>(.*?)</h2>', content, re.S)
    total_match = re.search(r'([\d,]+)\s+contributions?', heading.group(1) if heading else '')
    if not total_match or len(days) < 350 or any(day['count'] is None for day in days):
        raise ValueError('Incomplete GitHub contribution calendar; existing images were preserved.')
    total = int(total_match.group(1).replace(',', ''))
    if sum(day['count'] for day in days) != total:
        raise ValueError('GitHub calendar total does not match the daily counts.')
    return days, total


def activity_svg(days, total, dark=False):
    c = {'bg':'#0d1117', 'fg':'#e6edf3', 'muted':'#8b949e', 'line':'#30363d', 'accent':'#9bbbd8',
         'levels':['#161b22','#233b52','#365779','#5685ad','#8fb7d8']} if dark else {
         'bg':'#ffffff', 'fg':'#1f2937', 'muted':'#68778a', 'line':'#dce3eb', 'accent':'#315b82',
         'levels':['#eef2f6','#d5e2ee','#a9c3da','#709abb','#315b82']}
    first = dt.date.fromisoformat(days[0]['date'])
    start = first - dt.timedelta(days=(first.weekday()+1) % 7)
    active = sum(day['count'] > 0 for day in days)
    months = {1:'janv.',2:'févr.',3:'mars',4:'avr.',5:'mai',6:'juin',7:'juil.',8:'août',9:'sept.',10:'oct.',11:'nov.',12:'déc.'}
    font = 'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif"'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="223" viewBox="0 0 800 223" role="img" aria-label="{total} contributions GitHub sur la période affichée, {active} jours actifs">',
           f'<rect width="800" height="223" fill="{c["bg"]}"/>',
           f'<g {font}><text x="24" y="33" fill="{c["fg"]}" font-size="17" font-weight="600">Une année sur GitHub</text>',
           f'<text x="24" y="60" fill="{c["accent"]}" font-size="14" font-weight="600">{total:,}'.replace(',', ' ')+f' contributions</text>',
           f'<text x="190" y="60" fill="{c["muted"]}" font-size="13">{active} jours actifs</text>']
    for day in days:
        date = dt.date.fromisoformat(day['date'])
        col = (date-start).days // 7
        row = (date.weekday()+1) % 7
        x, y = 45 + col*13.5, 91 + row*13.5
        if date.day == 1:
            out.append(f'<text x="{x:.1f}" y="81" font-size="10" fill="{c["muted"]}">{months[date.month]}</text>')
        tooltip = html.escape(f'{day["date"]} · {day["count"]} contributions')
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="10.5" height="10.5" rx="2" fill="{c["levels"][day["level"]]}"><title>{tooltip}</title></rect>')
    for label,row in [('lun.',1),('mer.',3),('ven.',5)]:
        out.append(f'<text x="12" y="{99+row*13.5:.1f}" font-size="9" fill="{c["muted"]}">{label}</text>')
    period = f'{first.strftime("%d/%m/%Y")} — {days[-1]["date"][8:10]}/{days[-1]["date"][5:7]}/{days[-1]["date"][:4]}'
    out.append(f'<text x="24" y="204" fill="{c["muted"]}" font-size="10">{period} · Source : calendrier public GitHub</text>')
    out.append(f'<text x="607" y="204" fill="{c["muted"]}" font-size="10">Moins</text>')
    for index, fill in enumerate(c['levels']):
        out.append(f'<rect x="{644+index*13}" y="195" width="10" height="10" rx="2" fill="{fill}"/>')
    out.append(f'<text x="716" y="204" fill="{c["muted"]}" font-size="10">Plus</text></g></svg>')
    return ''.join(out)


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('--calendar-file', type=Path)
    args = argp.parse_args()
    content = args.calendar_file.read_text() if args.calendar_file else fetch('https://github.com/users/idris-ach2002/contributions')
    days, total = parse_calendar(content)
    assets = Path(__file__).resolve().parents[1] / 'assets'
    assets.mkdir(exist_ok=True)
    target = assets / 'activity-light.svg'
    target.write_text(activity_svg(days, total), encoding='utf-8')
    print(f'Updated profile activity: {total} contributions, {sum(d["count"] > 0 for d in days)} active days.')


if __name__ == '__main__':
    main()
