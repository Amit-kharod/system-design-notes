"""Draws the Ep 2 (Subnet Mask, Private IP & NAT) diagrams as SVG, in the Code Man light style.
usage: python3 tools/diagrams_ep02.py   (writes ep02-subnet-mask-nat/diagrams/*.svg)"""
import os
from svgkit import D, ind, NAVY, INK, BLUE, ICE, ICE2, RED, RED2, MIST, LINE, WHITE, BAND

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ep02-subnet-mask-nat', 'diagrams')
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.svg'):
        os.remove(os.path.join(OUT, f))

# 1. the mask and the AND
d = D(960, 344, 'The subnet mask marks the network bits, and the AND keeps only them')
rows = [('address', [192, 168, 1, 5]), ('mask  /24', [255, 255, 255, 0]), ('AND result', [192, 168, 1, 0])]
for r, (lab, vals) in enumerate(rows):
    y = 72 + r * 62
    d.text(30, y + 18, lab, 13, NAVY, 800)
    for i, v in enumerate(vals):
        on = NAVY if r == 1 else (BLUE if i < 3 else RED)
        d.bits(140 + i * 150, y, v, on=on, off=RED2 if (r == 2 and i == 3) else WHITE)
d.text(752, 90, '192.168.1.5', 13, INK, 700, 'start', True)
d.runs(752, 152, [('255.255.255.0', INK, 700), ('  = /24', BLUE, 800)], 13, mono=True)
d.runs(752, 214, [('192.168.1.0', RED, 800), ('  network', MIST, 600)], 13, mono=True)
d.bracket(140, 576, 250)
d.bracket(590, 726, 250, RED)
d.text(358, 280, '24 network bits (mask 1): kept as they are', 13, BLUE, 700, 'middle')
d.text(658, 280, '8 device bits (mask 0): become 0', 13, RED, 700, 'middle')
d.text(30, 320, 'Two addresses that give the same AND result are on the same network.', 12.5, MIST, 500)
d.save(OUT, '01-mask-and.svg')

# 2. same network or not
d = D(960, 356, 'Same network or not? Two ANDs and a compare')
d.text(30, 86, 'Your phone', 14, NAVY, 800)
d.runs(124, 86, [('192.168.1.5', INK, 700), ('  AND 255.255.255.0  =  ', MIST, 600), ('192.168.1.0', BLUE, 800), ('  (its own network)', MIST, 600)], 13.5, mono=True)
cases = [('The TV', '192.168.1.12', '192.168.1.0', ('= 192.168.1.0', 'same network'), ('send directly', 'to the TV'), False),
         ('Chat server', '198.51.100.20', '198.51.100.0', ('≠ 192.168.1.0', 'not at home'), ('send to the gateway', 'router 192.168.1.1'), True)]
for r, (name, ip, res, cmp_, dec, far) in enumerate(cases):
    y = 114 + r * 92
    d.card(30, y, 200, 62, name, [ip], ICE2, ICE, tsize=13.5, lsize=12.5)
    d.arrow(234, y + 31, 286, y + 31, BLUE, 'AND', ldy=-7)
    d.chip(290, y + 13, 180, 36, res, WHITE, LINE, INK, 13)
    d.arrow(474, y + 31, 526, y + 31, BLUE, 'compare', ldy=-7)
    d.raw('<g class="box">')
    d.box(530, y, 180, 62, WHITE, LINE)
    d.text(620, y + 27, cmp_[0], 13, INK, 700, 'middle', True)
    d.text(620, y + 47, cmp_[1], 12.5, RED if far else BLUE, 700, 'middle')
    d.raw('</g>')
    d.arrow(714, y + 31, 746, y + 31, BLUE)
    d.card(750, y, 180, 62, dec[0], [dec[1]], ICE2 if far else WHITE, ICE if far else LINE, RED if far else NAVY, tsize=13.5, lsize=12)
d.text(30, 314, "The gateway is the home router's inside address: the door out of the home network.", 12.5, MIST, 500)
d.text(30, 334, "The phone learns the gateway's address from DHCP, together with its own address and the mask.", 12.5, MIST, 500)
d.save(OUT, '02-same-network.svg')

# 3. inside a /24
d = D(960, 276, 'Inside 192.168.1.0/24: 256 addresses, 254 for devices')
used = {1: 'router', 5: 'phone', 8: 'phone 2', 12: 'TV'}
for n in range(13):
    x = 40 + n * 48
    if n == 0:
        fill, st, col = RED2, RED, RED
    elif n in used:
        fill, st, col = ICE2, ICE, NAVY
    else:
        fill, st, col = WHITE, LINE, INK
    d.chip(x, 96, 46, 40, f'.{n}', fill, st, col, 12.5)
    if n in used:
        d.text(x + 23, 86, used[n], 11, NAVY, 700, 'middle')
d.raw('<g class="box">')
d.box(666, 96, 144, 40, WHITE, LINE, 6, dash=True)
d.text(738, 120.5, '.13 to .253', 12, MIST, 600, 'middle', True)
d.raw('</g>')
d.chip(812, 96, 46, 40, '.254', WHITE, LINE, INK, 12)
d.chip(860, 96, 46, 40, '.255', RED2, RED, RED, 12)
d.text(40, 162, 'network address', 12.5, RED, 800)
d.text(40, 180, 'device bits 00000000', 11, MIST, 600, 'start', True)
d.text(906, 162, 'broadcast address', 12.5, RED, 800, 'end')
d.text(906, 180, 'device bits 11111111', 11, MIST, 600, 'end', True)
d.text(440, 162, 'white = free: the router lends these to devices that join', 11.5, MIST, 600, 'middle')
d.text(40, 220, '8 device bits → 2⁸ = 256 addresses. The first and the last are kept back: 256 − 2 = 254 for devices.', 13, INK, 500)
d.text(40, 250, 'With n device bits: 2ⁿ addresses, 2ⁿ − 2 for devices.', 14, NAVY, 800)
d.save(OUT, '03-block-anatomy.svg')

# 4. subnetting
d = D(960, 356, 'Subnetting: every extra network bit halves the blocks')
spec = [('/24', '255.255.255.0', [('.0 to .255   (256 addresses, 254 for devices)', False)]),
        ('/25', '255.255.255.128', [('.0 to .127   (128)', False), ('.128 to .255   (128)', False)]),
        ('/26', '255.255.255.192', [(f'.{a} – .{a + 63}   (64)', False) for a in (0, 64, 128, 192)]),
        ('/27', '255.255.255.224', [(f'.{a} – .{a + 31}', a == 128) for a in range(0, 256, 32)])]
for r, (p, m, parts) in enumerate(spec):
    y = 66 + r * 58
    d.text(30, y + 17, p, 15, NAVY, 800, 'start', True)
    d.text(30, y + 33, m, 10.5, MIST, 600, 'start', True)
    w = 760 / len(parts)
    for i, (t, hi) in enumerate(parts):
        d.chip(170 + i * w, y, w - 6, 36, t, RED2 if hi else (ICE2 if i % 2 == 0 else WHITE), RED if hi else ICE,
               RED if hi else INK, 12 if len(parts) < 8 else 11)
d.runs(30, 318, [('192.168.233.145/27:  ', NAVY, 800), ('145 is in the block .128 – .159, so the network is ', INK, 500),
                 ('.128', RED, 800), (' and the broadcast is ', INK, 500), ('.159', RED, 800)], 13)
d.text(30, 340, 'Addresses in a block = 2 to the power (32 − prefix).  For devices: that number − 2.', 12.5, MIST, 500)
d.save(OUT, '04-subnetting.svg')

# 5. DHCP
d = D(960, 412, 'DHCP: how the phone gets its address, in four messages')
d.card(70, 56, 200, 54, 'Your phone', ['no address yet'], ICE2, ICE, mono=False, lsize=11.5)
d.card(690, 56, 200, 54, 'Home router', ['the DHCP server'], WHITE, LINE, mono=False, lsize=11.5)
d.line(170, 112, 170, 352, LINE, 1.6, True)
d.line(790, 112, 790, 352, LINE, 1.6, True)
msgs = [('1  Discover', '“Is anyone giving out addresses?”', 'sent to everyone (255.255.255.255): the phone knows no address yet', 1),
        ('2  Offer', '“You can have 192.168.1.5.”', 'with the mask 255.255.255.0, the gateway 192.168.1.1, a DNS server and a lease time', -1),
        ('3  Request', '“I will take 192.168.1.5.”', 'also sent to everyone, so any other DHCP server knows its offer was not taken', 1),
        ('4  Acknowledge', '“It is yours until the lease ends.”', 'from now on the phone uses 192.168.1.5', -1)]
for i, (name, say, note, way) in enumerate(msgs):
    y = 150 + i * 58
    d.runs(480, y - 10, [(name + '    ', NAVY, 800), (say, INK, 500)], 13, 'middle')
    if way > 0:
        d.arrow(174, y, 784, y, BLUE)
    else:
        d.arrow(786, y, 176, y, BLUE)
    d.text(480, y + 18, note, 11.5, MIST, 500, 'middle')
d.runs(480, 388, [('Result:  ', NAVY, 800), ('192.168.1.5 · mask 255.255.255.0 · gateway 192.168.1.1', RED, 800), (', on lease', MIST, 600)], 13.5, 'middle')
d.save(OUT, '05-dhcp.svg')

# 6. the same private address in every home
d = D(960, 372, 'The same private address in every home, and no conflict')
d.raw('<g class="box">')
d.box(30, 56, 900, 48, WHITE, LINE)
d.runs(480, 85, [('The internet:  ', NAVY, 800), ('its routers never forward private addresses (10.x, 172.16.x to 172.31.x, 192.168.x)', INK, 500)], 13, 'middle')
d.raw('</g>')
for i, (name, pub) in enumerate([('Your home', '203.0.113.7'), ('Next door', '203.0.113.44'), ('Another city', '203.0.113.90')]):
    x = 40 + i * 300
    d.box(x, 136, 280, 180, BAND, 'none', 12)
    d.text(x + 14, 158, name, 12.5, NAVY, 800)
    d.card(x + 40, 170, 200, 54, 'Router', [('public ' + pub, BLUE)], WHITE, LINE, tsize=13, lsize=12)
    d.arrow(x + 140, 168, x + 140, 108, BLUE)
    d.chip(x + 20, 238, 240, 28, 'phone   192.168.1.5', RED2, RED, RED, 12.5)
    d.chip(x + 20, 274, 240, 28, 'TV      192.168.1.12', WHITE, LINE, INK, 12.5)
d.text(30, 348, 'Private blocks: 10.0.0.0/8 · 172.16.0.0/12 · 192.168.0.0/16. They never leave a home, so every home can reuse them.', 12.5, MIST, 500)
d.save(OUT, '06-private-reuse.svg')

# 7. NAT and its table
d = D(960, 452, 'NAT: one public address for the whole home, and the table that sorts the replies')
d.card(30, 66, 200, 58, 'Phone 1', ['192.168.1.5 : 51000'], ICE2, ICE, tsize=13.5, lsize=12)
d.card(30, 142, 200, 58, 'Phone 2', ['192.168.1.8 : 49200'], WHITE, LINE, tsize=13.5, lsize=12)
d.card(330, 82, 210, 104, 'Home router', ['inside   192.168.1.1', ('outside  203.0.113.7', BLUE)], WHITE, LINE, lsize=12)
d.card(740, 96, 190, 62, 'Chat server', ['198.51.100.20'], ICE2, ICE, tsize=13.5, lsize=12)
d.arrow(232, 95, 328, 116)
d.arrow(232, 171, 328, 152)
d.arrow(542, 118, 738, 118, BLUE)
d.text(640, 106, 'SENDER 203.0.113.7 : 51000', 11.5, RED, 800, 'middle', True)
d.arrow(738, 142, 544, 142, MIST)
d.text(640, 162, 'reply TO 203.0.113.7 : 51000', 11.5, MIST, 700, 'middle', True)
d.runs(480, 230, [("Phone 1's packet as it leaves home:   ", INK, 600), ('SENDER 192.168.1.5 : 51000', MIST, 700),
                  ('   →   ', MIST, 700), ('SENDER 203.0.113.7 : 51000', RED, 800)], 12.5, 'middle')
d.raw('<g class="box">')
d.box(130, 252, 700, 140, WHITE, LINE)
d.text(146, 276, "The router's NAT table", 13, NAVY, 800)
for x, h in ((146, 'inside address : port'), (420, 'outside port'), (640, 'talking to')):
    d.text(x, 298, h, 11, MIST, 700)
for i, (a, b, c, hi) in enumerate([('192.168.1.5 : 51000', '51000', '198.51.100.20', False),
                                     ('192.168.1.8 : 49200', '49200', '198.51.100.20', False),
                                     ('192.168.1.12 : 51000', '51001 (51000 was taken)', '198.51.100.20', True)]):
    yy = 306 + i * 26
    if hi:
        d.box(138, yy, 684, 22, ICE2, 'none', 5)
    for x, t in ((146, a), (420, b), (640, c)):
        d.text(x, yy + 16, t, 12, INK, 600, 'start', True)
d.raw('</g>')
d.text(30, 424, 'A reply to port 51000 goes to phone 1, a reply to 49200 to phone 2. An entry is made only when a packet goes out.', 12.5, MIST, 500)
d.save(OUT, '07-nat-table.svg')

# 8. conversations start from inside
d = D(960, 392, 'Conversations start from inside: the NAT table lets in only replies')
d.line(334, 62, 334, 372, LINE, 1.2)
d.text(30, 82, 'Someone outside knocks', 13.5, NAVY, 800)
d.card(40, 98, 260, 56, 'A computer outside', ['anywhere on the internet'], WHITE, LINE, mono=False, tsize=13, lsize=11.5)
d.arrow(150, 156, 150, 210, MIST)
d.text(160, 188, 'TO 203.0.113.7 : 6000', 11, MIST, 700, 'start', True)
d.card(40, 212, 260, 56, 'Your router', ['203.0.113.7'], WHITE, LINE, tsize=13, lsize=12)
d.text(170, 294, 'No entry for port 6000 in its table:', 12.5, RED, 800, 'middle')
d.text(170, 313, 'the packet is not forwarded.', 12.5, RED, 800, 'middle')
d.card(40, 328, 260, 40, 'Your phone  192.168.1.5', [], WHITE, LINE, MIST, tsize=12.5, dash=True)
d.text(354, 82, 'How your friend still gets your message', 13.5, NAVY, 800)
d.card(364, 124, 150, 58, 'You', ['your home'], ICE2, ICE, mono=False, tsize=13.5, lsize=11.5)
d.card(586, 124, 160, 58, 'Chat server', ['198.51.100.20'], WHITE, LINE, tsize=13.5, lsize=12)
d.card(806, 124, 134, 58, "Friend's phone", ['behind its router'], WHITE, LINE, mono=False, tsize=13, lsize=11)
d.path('M873 184 V222 H666 V186', MIST, dash=True)
d.text(770, 242, "1. opened earlier, from inside, and kept open", 11.5, MIST, 700, 'middle')
d.arrow(516, 152, 584, 152, BLUE)
d.text(550, 114, '2. your message', 11.5, BLUE, 700, 'middle')
d.arrow(748, 152, 804, 152, RED)
d.text(776, 106, '3. down the open connection', 11.5, RED, 700, 'middle')
d.text(354, 284, "4. The message reaches the friend's router like a reply. The router finds the entry for", 12.5, INK, 500)
d.text(354, 304, 'that connection in its NAT table and forwards it to the right phone.', 12.5, INK, 500)
d.text(354, 336, 'Chat apps keep a connection like this open all the time.', 12.5, MIST, 500)
d.save(OUT, '08-inbound.svg')

# 9. one public address, many devices
d = D(960, 316, 'A building of 100 homes: how many public addresses does it need?')
d.text(30, 84, '100 homes × 10 devices each (phones, laptops, a TV) = 1,000 devices', 14, INK, 600)
d.text(30, 132, 'Without NAT', 13, NAVY, 800)
d.box(230, 112, 640, 30, BLUE, 'none', 6)
d.text(856, 132, '1,000 public addresses: one per device', 12.5, WHITE, 800, 'end')
d.text(30, 182, 'With NAT', 13, NAVY, 800)
d.box(230, 162, 64, 30, RED, 'none', 6)
d.text(306, 182, '100: one per home, for its router', 12.5, RED, 800)
d.text(30, 232, 'With carrier-grade NAT', 13, NAVY, 800)
d.box(230, 212, 14, 30, WHITE, MIST, 4, dash=True)
d.text(256, 232, 'fewer still: many homes share one public address', 12.5, MIST, 700)
d.text(30, 286, 'So one public IP can be a whole home, office, college or neighbourhood. It is not one person.', 12.5, MIST, 500)
d.save(OUT, '09-shared-ip.svg')

# 10. carrier-grade NAT
d = D(960, 304, 'Carrier-grade NAT: a second, much bigger NAT inside the ISP')
d.text(30, 80, 'private  192.168.0.0/16', 12, BLUE, 700, 'start', True)
d.text(250, 80, 'shared  100.64.0.0/10', 12, BLUE, 700, 'start', True)
d.text(490, 80, 'public address, shared', 12, RED, 700)
d.card(30, 96, 150, 70, 'Your phone', ['192.168.1.5'])
d.card(250, 96, 170, 70, 'Home router', ['outside: 100.64.x.x'])
d.card(490, 96, 190, 70, "ISP's NAT (CGNAT)", ['public 203.0.113.7'], ICE2, ICE)
d.card(760, 96, 170, 70, 'Any server', ['sees 203.0.113.7'])
for x in (182, 422, 682):
    d.arrow(x, 131, x + 66, 131)
d.card(490, 192, 190, 44, 'many other customers', [], WHITE, LINE, MIST, tsize=13)
d.arrow(585, 190, 585, 170, MIST, dash=True)
d.text(30, 270, 'To the server, many unrelated people look like one address. So one IP address is not one person:', 12.5, MIST, 500)
d.text(30, 288, 'blocking or rate-limiting one IP can hit a whole neighbourhood.', 12.5, MIST, 500)
d.save(OUT, '10-cgnat.svg')

# 11. IPv4 and IPv6
d = D(960, 344, 'IPv6: the same idea, with 128 bits')
d.text(30, 88, 'IPv4', 15, NAVY, 900)
d.box(110, 70, 190, 26, BLUE, 'none', 6)
d.text(316, 88, '32 bits  →  2³² ≈ 4.3 × 10⁹ addresses (430 crore)', 13, INK, 600, 'start', True)
d.text(30, 136, 'IPv6', 15, NAVY, 900)
d.box(110, 118, 760, 26, NAVY, 'none', 6)
d.runs(110, 170, [('128 bits  →  2¹²⁸ ≈ 3.4 × 10³⁸ addresses:  ', INK, 600), ('2⁹⁶ times more, not 4 times', RED, 800)], 13)
for i, g in enumerate(['2001', '0db8', '85a3', '0000', '0000', '8a2e', '0370', '7334']):
    net = i < 4
    d.chip(110 + i * 96, 192, 86, 34, g, ICE2 if net else WHITE, ICE if net else LINE, INK, 13)
d.text(30, 214, 'written', 12, MIST, 600)
d.bracket(110, 476, 234)
d.bracket(494, 860, 234, NAVY)
d.text(293, 262, 'first 64 bits: the network', 12.5, BLUE, 700, 'middle')
d.text(677, 262, 'last 64 bits: the device', 12.5, NAVY, 700, 'middle')
d.text(30, 298, 'Each group is 4 hexadecimal digits (0-9, a-f) = 16 bits.   Short form: 2001:db8:85a3::8a2e:370:7334', 12.5, MIST, 500)
d.text(30, 320, 'Leading zeros in a group are dropped, and one run of all-zero groups is written ::', 12.5, MIST, 500)
d.save(OUT, '11-ipv4-vs-ipv6.svg')

print('diagrams written to', OUT, sorted(os.listdir(OUT)))
