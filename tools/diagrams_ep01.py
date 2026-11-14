"""Draws the Ep 1 (IP Address) diagrams as SVG, in the Code Man light style.
usage: python3 tools/diagrams_ep01.py   (writes ep01-ip-address/diagrams/*.svg)"""
import os
from svgkit import D, ind, ip_int, NAVY, INK, BLUE, ICE, ICE2, RED, RED2, MIST, LINE, WHITE, BAND

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ep01-ip-address', 'diagrams')
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.svg'):
        os.remove(os.path.join(OUT, f))

# 2. the parts of an address
d = D(960, 330, 'One address = four numbers of 8 bits each')
for i, o in enumerate([192, 168, 1, 5]):
    x = 60 + i * 218
    d.box(x, 62, 150, 58, ICE2, ICE)
    d.text(x + 75, 101, o, 30, NAVY, 900, 'middle', True)
    if i < 3:
        d.text(x + 184, 104, '.', 34, MIST, 900, 'middle')
    d.bits(x + 8, 140, o)
    d.text(x + 75, 188, '8 bits', 12, MIST, 600, 'middle')
d.bracket(60, 864, 206)
d.text(462, 238, f'32 bits in total  →  2³² = {ind(2**32)} possible addresses (about 430 crore)', 13.5, BLUE, 700, 'middle')
d.text(60, 278, 'Place values of 8 bits:', 13, INK, 700)
for i, v in enumerate([128, 64, 32, 16, 8, 4, 2, 1]):
    lit = i < 2
    d.box(250 + i * 62, 258, 54, 30, NAVY if lit else WHITE, LINE, 6)
    d.text(277 + i * 62, 278, v, 13, WHITE if lit else INK, 700, 'middle', True)
d.text(760, 278, '128 + 64 = 192', 14, RED, 800, 'start', True)
d.text(60, 314, 'All eight bits 1: 128+64+32+16+8+4+2+1 = 255.  All eight 0: 0.  So every number is 0 to 255.', 12.5, MIST, 500)
d.save(OUT, '02-address-anatomy.svg')

# 1. every new bit doubles the count
d = D(960, 362, 'Every new bit doubles the count')
three = [format(i, '03b') for i in range(8)]
cols = [(80, 44, ['0', '1'], '1 bit', '2', '2¹'),
        (200, 52, [format(i, '02b') for i in range(4)], '2 bits', '4', '2²'),
        (330, 60, three, '3 bits', '8', '2³')]
for cx, w, combos, head, count, power in cols:
    d.text(cx, 82, head, 13, NAVY, 800, 'middle')
    for r, c in enumerate(combos):
        d.chip(cx - w / 2, 96 + r * 24, w, 20, c, size=13)
    d.text(cx, 318, count, 18, NAVY, 900, 'middle')
    d.text(cx, 338, power, 12, MIST, 600, 'middle')
d.text(555, 82, '4 bits', 13, NAVY, 800, 'middle')
for k, cx in enumerate((500, 610)):
    for r, c in enumerate(three):
        d.raw('<g class="box">')
        d.box(cx - 35, 96 + r * 24, 70, 20, ICE2 if k else WHITE, ICE if k else LINE, 6)
        d.runs(cx, 96 + r * 24 + 14.7, [(str(k), RED, 800), (c, INK)], 13, 'middle', True)
        d.raw('</g>')
d.runs(555, 318, [('8 + 8 = ', NAVY), ('16', RED)], 18, 'middle', weight=900)
d.text(555, 338, '2⁴', 12, MIST, 600, 'middle')
for x1, x2 in ((108, 168), (232, 294), (366, 456)):
    d.arrow(x1, 186, x2, 186, MIST, '+1 bit', ldy=-9)
x0 = 690
d.text(x0, 112, 'Add a bit in front of the 8 old', 13, INK, 500)
d.text(x0, 131, 'combinations: it can be 0 or 1.', 13, INK, 500)
d.text(x0, 150, 'So all 8 appear twice:', 13, INK, 500)
d.runs(x0, 169, [('8 with a 0', INK, 500), (' + ', MIST, 500), ('8 with a 1', INK, 500), (' = 16.', INK, 500)], 13)
d.text(x0, 214, 'n bits  →  2ⁿ combinations', 15, NAVY, 800)
d.text(x0, 242, '2, 4, 8, 16, 32, 64, 128, 256', 13, INK, 600, 'start', True)
d.text(x0, 268, '8 bits  →  2⁸ = 256', 13, INK, 600, 'start', True)
d.text(x0, 292, f'32 bits →  2³² ≈ 430 crore', 13, INK, 600, 'start', True)
d.save(OUT, '01-bits-doubling.svg')

# 3. one 32-bit number
d = D(960, 330, 'To a computer, the address is one 32-bit number')
x0, cw, gap = 140, 20, 14
for b, o in enumerate([192, 168, 1, 5]):
    bx = x0 + b * (8 * cw + gap)
    d.text(bx + 4 * cw - 1, 86, o, 14, MIST, 700, 'middle', True)
    if b < 3:
        d.text(bx + 8 * cw + gap / 2 - 1, 88, '.', 18, MIST, 900, 'middle')
    d.bits(bx, 96, o, cw=cw, ch=24, size=12)
d.bracket(x0, x0 + 32 * cw + 3 * gap - 2, 128)
d.runs(480, 162, [('read as one number:  ', INK, 600), (ind(3232235781), RED, 800), ('  (about 323 crore)', MIST, 600)], 15, 'middle')
d.text(480, 188, f'192 × 2²⁴  +  168 × 2¹⁶  +  1 × 2⁸  +  5  =  {ind(3232235781)}', 12.5, MIST, 600, 'middle', True)
bx0, bw = 96, 768
d.box(bx0, 244, bw, 14, ICE2, ICE, 7)
mx = bx0 + bw * 3232235781 / 2**32
d.line(mx, 222, mx, 244, RED, 2)
d.dot(mx, 251, 7)
d.text(mx, 216, '192.168.1.5', 13, RED, 800, 'middle', True)
d.text(bx0, 280, '0   (0.0.0.0)', 12, MIST, 600, 'start', True)
d.text(bx0 + bw, 280, f'{ind(2**32 - 1)}   (255.255.255.255)', 12, MIST, 600, 'end', True)
d.text(480, 312, f'2³² = {ind(2**32)} addresses in all: about 430 crore, the hard limit of IPv4.', 13, INK, 600, 'middle')
d.save(OUT, '03-one-number.svg')

# 4. who hands out addresses
d = D(960, 452, 'Who hands out IP addresses: from the top down, always in blocks')
d.card(370, 60, 220, 76, 'IANA', ['Internet Assigned Numbers', 'Authority: the global pool'], ICE2, ICE, mono=False, lsize=11.5)
d.text(612, 94, 'gives large blocks to the', 12, MIST, 600)
d.text(612, 111, 'five regional registries', 12, MIST, 600)
rirs = [('AFRINIC', ['Africa']), ('APNIC', ['Asia-Pacific,', 'India included']), ('ARIN', ['North America']),
        ('LACNIC', ['Latin America and', 'the Caribbean']), ('RIPE NCC', ['Europe, Middle East,', 'parts of Central Asia'])]
for i, (name, lines) in enumerate(rirs):
    x = 40 + i * 178
    ap = name == 'APNIC'
    d.card(x, 176, 168, 64, name, lines, ICE2 if ap else WHITE, ICE if ap else LINE, mono=False, tsize=13.5, lsize=11)
    d.arrow(480, 136, x + 84, 174, BLUE if ap else MIST, w=2 if ap else 1.3)
d.card(218, 292, 168, 62, 'ISP', ['Jio, Airtel, ...'], WHITE, LINE, mono=False, lsize=11.5)
d.arrow(302, 240, 302, 290)
d.card(30, 292, 160, 62, 'IRINN', ["India's national registry"], WHITE, LINE, mono=False, lsize=11)
d.arrow(250, 240, 140, 290, MIST, dash=True, w=1.5)
d.arrow(190, 323, 216, 323, MIST, dash=True, w=1.5)
d.text(160, 266, 'or through', 11, MIST, 600, 'end')
d.card(218, 384, 168, 56, 'Your connection', [('one address', RED)], ICE2, ICE, mono=False, lsize=12)
d.arrow(302, 354, 302, 382)
x0 = 436
d.text(x0, 300, 'At every step the blocks get smaller:', 13, NAVY, 800)
for i, t in enumerate(['IANA → registries: huge blocks', 'registry → ISP: large blocks',
                       'ISP → your connection: one address',
                       'A block = addresses that start with the same bits.']):
    d.text(x0, 326 + i * 22, ('•  ' if i < 3 else '') + t, 12.5, INK if i < 3 else MIST, 500)
d.text(x0, 426, 'At home that one address goes to your WiFi router (Ep 2).', 12.5, MIST, 500)
d.save(OUT, '04-who-gives-addresses.svg')

# 5. the packet's path and the routing tables
d = D(960, 432, 'The path of one packet, and what each routing table holds')
for x1, x2, lab in ((16, 330, 'home network'), (336, 756, "ISP's network"), (762, 944, "chat server's network")):
    d.box(x1, 54, x2 - x1, 106, BAND, 'none', 10)
    d.text(x1 + 10, 72, lab, 11, MIST, 700)
nodes = [(26, 130, 'Your phone', '192.168.1.5', True), (268, 130, 'Home router', 'the WiFi box', False),
         (444, 120, 'ISP router A', 'Jio / Airtel', False), (610, 120, 'Router B', 'the next hop', False),
         (786, 150, 'Chat server', '198.51.100.20', True)]
for i, (x, w, t, sub, end) in enumerate(nodes):
    d.card(x, 84, w, 62, t, [sub], ICE2 if end else WHITE, ICE if end else LINE, tsize=13.5, lsize=12)
    if i < 4:
        d.arrow(x + w + 2, 115, nodes[i + 1][0] - 2, 115)
d.raw('<g class="box">')
d.box(540, 166, 396, 28, WHITE, LINE, 6)
d.runs(550, 185, [('packet:  SENDER 192.168.1.5  ', INK), ('RECEIVER 198.51.100.20', RED, 800)], 12, mono=True)
d.raw('</g>')


def table(x, y, w, title, rows):
    d.raw('<g class="box">')
    d.box(x, y, w, 46 + len(rows) * 26, WHITE, LINE)
    d.text(x + 14, y + 22, title, 12.5, NAVY, 800)
    d.text(x + 14, y + 42, 'network', 11, MIST, 700)
    d.text(x + w * 0.52, y + 42, 'next hop', 11, MIST, 700)
    for i, (a, b, hi) in enumerate(rows):
        yy = y + 48 + i * 26
        if hi:
            d.box(x + 6, yy, w - 12, 22, ICE2, 'none', 5)
        d.text(x + 14, yy + 16, a, 12, INK, 600, 'start', True)
        d.text(x + w * 0.52, yy + 16, b, 12, INK, 600, 'start', True)
    d.raw('</g>')


table(26, 214, 440, 'Home router: 2 lines', [('192.168.1.x (home)', 'deliver directly', False),
                                              ('everything else', 'ISP router (default route)', True)])
table(496, 214, 440, 'ISP router A: two of its lines', [('198.51.100.x', 'router B', True), ('192.0.2.x', 'router C', False)])
d.line(333, 148, 333, 212, MIST, 1.2, True)
d.line(504, 148, 520, 212, MIST, 1.2, True)
d.text(26, 340, "No router knows the whole path. Each one reads the receiver's address, finds that network in its table,", 13, INK, 500)
d.text(26, 360, 'and hands the packet to the next hop. Router B then does the same lookup with its own table.', 13, INK, 500)
d.text(26, 394, f'The big routers of the internet carry about 11 lakh IPv4 lines ({ind(1091990)} on 12 Nov 2026), not 430 crore:', 12.5, MIST, 500)
d.text(26, 413, 'one line covers a whole block of addresses.', 12.5, MIST, 500)
d.save(OUT, '05-packet-path.svg')

# 6. why blocks: one line per network
d = D(960, 372, 'Why blocks matter: one table line covers a whole network')
d.runs(300, 104, [('198.51.100', BLUE, 800), ('.', MIST, 800), ('20', RED, 800)], 30, mono=True)
d.bracket(300, 480, 116)
d.bracket(498, 534, 116, RED)
d.text(390, 146, 'network: which block', 12.5, BLUE, 700, 'middle')
d.text(516, 146, 'device: which one inside it', 12.5, RED, 700, 'start')
d.raw('<g class="box">')
d.box(40, 178, 380, 150, WHITE, LINE)
d.text(56, 202, 'One line per address', 13, NAVY, 800)
rows = ['198.51.100.0    →  router B', '198.51.100.1    →  router B', '198.51.100.2    →  router B', '   ...', '198.51.100.255  →  router B']
for i, r in enumerate(rows):
    d.text(56, 228 + i * 19, r, 12, INK if i != 3 else MIST, 600, 'start', True)
d.raw('</g>')
d.text(230, 352, '256 lines for one network; 430 crore for all', 12.5, MIST, 600, 'middle')
d.arrow(428, 252, 532, 252, BLUE, 'read only the', ldy=-14)
d.text(480, 270, 'network part', 11.5, MIST, 600, 'middle')
d.raw('<g class="box">')
d.box(540, 178, 380, 150, WHITE, LINE)
d.text(556, 202, 'One line per network', 13, NAVY, 800)
d.box(552, 222, 356, 30, ICE2, ICE, 6)
d.text(566, 242, '198.51.100.x    →  router B', 12.5, INK, 700, 'start', True)
d.text(556, 282, 'Big routers keep about 11 lakh lines,', 12.5, INK, 500)
d.text(556, 302, 'not 430 crore.', 12.5, INK, 500)
d.raw('</g>')
d.text(730, 352, '1 line for the whole network', 12.5, MIST, 600, 'middle')
d.save(OUT, '06-one-line-per-block.svg')

# 7. the IP range lookup (Google question)
d = D(960, 352, "Finding an IP's location: one number, sorted ranges, binary search")
q = '192.0.2.70'
d.runs(40, 86, [('1.  The IP becomes one number:   ', NAVY, 800), (q, INK, 700), ('  →  ', MIST), (ind(ip_int(q)), RED, 800)], 14)
d.text(40, 124, '2.  The ranges, sorted by their first address (each start is also one number):', 14, NAVY, 800)
rng = [('192.0.2.0', '.63', 'Pune'), ('192.0.2.64', '.127', 'Delhi'), ('192.0.2.128', '.191', 'Chennai'), ('192.0.2.192', '.255', 'Kolkata')]
for i, (s0, e0, place) in enumerate(rng):
    x = 40 + i * 222
    hit = place == 'Delhi'
    d.raw('<g class="box">')
    d.box(x, 138, 206, 64, ICE2 if hit else WHITE, RED if hit else LINE, 8, 2 if hit else 1.4)
    d.text(x + 103, 160, f'{s0} – {e0}', 12, INK, 600, 'middle', True)
    d.text(x + 103, 181, place, 13.5, RED if hit else NAVY, 800, 'middle')
    d.text(x + 103, 197, 'starts at ' + ind(ip_int(s0)), 10.5, MIST, 600, 'middle', True)
    d.raw('</g>')
d.text(40, 240, '3.  Binary search: look at the middle, keep the half that can hold the IP.', 14, NAVY, 800)
d.text(40, 266, 'step 1: the middle range (Chennai) starts at .128, and 70 < 128, so keep the left half.', 12.5, INK, 500)
d.runs(40, 288, [('step 2: Delhi starts at .64: 70 ≥ 64, and 70 is not past .127, so the answer is ', INK, 500), ('Delhi', RED, 800), ('.', INK, 500)], 12.5)
d.text(40, 326, '4 ranges: 2 steps.  10 lakh ranges: about 20 steps, because each step halves what is left.', 12.5, MIST, 600)
d.save(OUT, '07-ip-range-lookup.svg')

print('diagrams written to', OUT, sorted(os.listdir(OUT)))
