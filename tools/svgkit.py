"""Shared drawing kit for the notes' diagrams: light Code Man style (navy text, blue arrows, ice-blue fills,
red for the one thing to notice). Every diagram is plain SVG, so GitHub shows it and the PDF embeds it.
Used by tools/diagrams_ep01.py, tools/diagrams_ep02.py, ..."""
import os

NAVY, INK, BLUE, ICE, ICE2 = '#1a2640', '#243352', '#2f6fa8', '#8fd0f2', '#e6f4fc'
RED, RED2, MIST, LINE, PAPER, WHITE, BAND = '#e3262c', '#fdeced', '#6b7a94', '#c9d6e6', '#f7f9fc', '#ffffff', '#eef4fa'
SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Menlo, Consolas, monospace"


def esc(t):
    return str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def ind(n):
    """A whole number in the Indian format: 4294967296 -> 4,29,49,67,296."""
    s = str(n)
    if len(s) <= 3:
        return s
    head, tail, parts = s[:-3], s[-3:], []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ','.join(parts + [tail])


def ip_int(ip):
    a, b, c, d = (int(x) for x in ip.split('.'))
    return (a << 24) | (b << 16) | (c << 8) | d


class D:
    """One diagram: a rounded paper card with a title. Coordinates are SVG user units (the width is usually 960)."""

    def __init__(s, w, h, title, sub=None):
        s.w, s.h, s.e = w, h, []
        s.e.append(f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{PAPER}" stroke="{LINE}"/>')
        s.text(28, 38, title, 17, NAVY, 800)
        if sub:
            s.text(28, 60, sub, 12.5, MIST, 500)

    def raw(s, svg):
        s.e.append(svg)

    def text(s, x, y, t, size=14, fill=INK, weight=500, anchor='start', mono=False):
        s.e.append(f'<text x="{x}" y="{y}" font-family="{MONO if mono else SANS}" font-size="{size}" '
                   f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" xml:space="preserve">{esc(t)}</text>')

    def runs(s, x, y, parts, size=14, anchor='start', mono=False, weight=600):
        """One line in several colours: parts = [(text, colour), (text, colour, weight), ...]."""
        sp = ''.join(f'<tspan fill="{p[1]}" font-weight="{p[2] if len(p) > 2 else weight}">{esc(p[0])}</tspan>'
                     for p in parts)
        s.e.append(f'<text x="{x}" y="{y}" font-family="{MONO if mono else SANS}" font-size="{size}" '
                   f'text-anchor="{anchor}" xml:space="preserve">{sp}</text>')

    def box(s, x, y, w, h, fill=WHITE, stroke=LINE, r=10, sw=1.4, dash=False):
        d = ' stroke-dasharray="5 4"' if dash else ''
        s.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" '
                   f'stroke-width="{sw}"{d}/>')

    def card(s, x, y, w, h, title, lines=(), fill=WHITE, stroke=LINE, tcol=NAVY, mono=True, lcol=INK, tsize=14,
             lsize=12.5, dash=False):
        """A box with a bold title and centred lines. Its texts are checked to stay inside it (class box)."""
        s.e.append('<g class="box">')
        s.box(x, y, w, h, fill, stroke, dash=dash)
        top = y + (h - (20 + 18 * len(lines))) / 2 + 15 if lines else y + h / 2 + tsize * 0.36
        s.text(x + w / 2, top, title, tsize, tcol, 800, 'middle')
        for i, l in enumerate(lines):
            col = lcol
            if isinstance(l, tuple):
                l, col = l
            s.text(x + w / 2, top + 20 + i * 18, l, lsize, col, 500, 'middle', mono)
        s.e.append('</g>')

    def chip(s, x, y, w, h, t, fill=WHITE, stroke=LINE, col=INK, size=12.5, mono=True, weight=600, r=6):
        s.e.append('<g class="box">')
        s.box(x, y, w, h, fill, stroke, r)
        s.text(x + w / 2, y + h / 2 + size * 0.36, t, size, col, weight, 'middle', mono)
        s.e.append('</g>')

    def arrow(s, x1, y1, x2, y2, col=BLUE, label=None, dash=False, lcol=MIST, lsize=11.5, ldy=-8, w=2):
        d = ' stroke-dasharray="6 5"' if dash else ''
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d} '
                   f'marker-end="url(#a{col[1:]})"/>')
        if label:
            s.text((x1 + x2) / 2, (y1 + y2) / 2 + ldy, label, lsize, lcol, 600, 'middle')

    def path(s, d, col=BLUE, dash=False, w=2, head=True):
        da = ' stroke-dasharray="6 5"' if dash else ''
        mk = f' marker-end="url(#a{col[1:]})"' if head else ''
        s.e.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}"{da}{mk}/>')

    def line(s, x1, y1, x2, y2, col=LINE, w=1.4, dash=False):
        d = ' stroke-dasharray="4 4"' if dash else ''
        s.e.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}"{d}/>')

    def bits(s, x, y, value, n=8, cw=17, ch=26, on=NAVY, off=WHITE, size=12.5):
        for i, c in enumerate(format(value, f'0{n}b')):
            lit = c == '1'
            s.e.append(f'<rect x="{x + i * cw}" y="{y}" width="{cw - 2}" height="{ch}" rx="4" '
                       f'fill="{on if lit else off}" stroke="{LINE}"/>')
            s.text(x + i * cw + (cw - 2) / 2, y + ch / 2 + size * 0.36, c, size, WHITE if lit else INK, 700,
                   'middle', True)

    def bracket(s, x1, x2, y, col=BLUE, down=True):
        t = 9 if down else -9
        s.e.append(f'<path d="M{x1} {y} v{t} h{x2 - x1} v{-t}" fill="none" stroke="{col}" stroke-width="2"/>')

    def dot(s, x, y, r=6, fill=RED):
        s.e.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>')

    def save(s, folder, name):
        os.makedirs(folder, exist_ok=True)
        marks = ''.join(f'<marker id="a{c[1:]}" markerWidth="9" markerHeight="9" refX="7.5" refY="4.5" orient="auto">'
                        f'<path d="M0,0 L9,4.5 L0,9 z" fill="{c}"/></marker>' for c in (BLUE, RED, MIST, NAVY, INK))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}" '
               f'role="img"><defs><style>text{{font-variant-ligatures:none;font-feature-settings:"liga" 0,"calt" 0}}</style>'
               f'{marks}</defs>' + ''.join(s.e) + '</svg>')
        with open(os.path.join(folder, name), 'w', encoding='utf-8') as f:
            f.write(svg + '\n')
