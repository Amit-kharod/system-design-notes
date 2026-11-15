"""Draws the Ep 4 (TCP vs UDP) diagrams as SVG, in the Code Man light style.
usage: python3 tools/diagrams_ep04.py   (writes ep04-tcp-udp/diagrams/*.svg)
Real names: i.instagram.com (shown as 57.144.x.x), the phone 192.168.1.5 at home."""
import os
from svgkit import D, NAVY, INK, BLUE, ICE, ICE2, RED, RED2, MIST, LINE, WHITE, BAND

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ep04-tcp-udp', 'diagrams')
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.svg'):
        os.remove(os.path.join(OUT, f))

# 1. two ways to send
d = D(960, 360, 'Two ways to send data: TCP for the Instagram DM, UDP for the Instagram call')
d.text(30, 84, 'TCP  (Transmission Control Protocol): the DM "Kal 5 baje CP pe milte hain :)"', 14, NAVY, 800)
d.card(30, 100, 140, 56, 'Phone', ['Instagram app'], ICE2, ICE, mono=False, tsize=13, lsize=11.5)
d.card(790, 100, 140, 56, 'Server', ['i.instagram.com'], ICE2, ICE, mono=False, tsize=13, lsize=11.5)
for i, t in enumerate(('Kal 5 baje', 'CP pe mil', 'te hain :)')):
    d.chip(230 + i * 170, 114, 140, 28, t, WHITE, BLUE, NAVY, 12, False)
d.arrow(172, 128, 226, 128, BLUE)
d.arrow(744, 128, 786, 128, BLUE)
d.text(480, 176, 'whole, in order; anything lost is sent again', 12.5, BLUE, 700, 'middle')
d.text(30, 232, 'UDP  (User Datagram Protocol): the Instagram video call', 14, NAVY, 800)
d.card(30, 248, 140, 56, 'Phone', ['Instagram app'], ICE2, ICE, mono=False, tsize=13, lsize=11.5)
d.card(790, 248, 140, 56, 'Server', ['call server'], ICE2, ICE, mono=False, tsize=13, lsize=11.5)
for i in range(4):
    if i == 2:
        d.chip(230 + i * 130, 262, 100, 28, 'lost', RED2, RED, RED, 12, False)
    else:
        d.chip(230 + i * 130, 262, 100, 28, f'voice {i + 1}', WHITE, BLUE, NAVY, 12, False)
d.arrow(172, 276, 226, 276, BLUE)
d.arrow(724, 276, 786, 276, BLUE)
d.text(480, 324, 'sent once, no waiting; a lost one stays lost and the call goes on', 12.5, RED, 700, 'middle')
d.save(OUT, '01-two-ways.svg')

# 2. ports and the four numbers
d = D(960, 400, 'IP address = station, port = platform: four numbers name one connection')
d.box(30, 84, 280, 190, ICE2, ICE); d.text(48, 108, 'Your phone  192.168.1.5', 13, NAVY, 800)
d.chip(50, 126, 240, 30, 'Instagram   port 51000', WHITE, BLUE, NAVY, 12)
d.chip(50, 166, 240, 30, 'YouTube     port 52000', WHITE, LINE, INK, 12)
d.chip(50, 206, 240, 30, 'WhatsApp    port 53000', WHITE, LINE, INK, 12)
d.box(650, 84, 280, 190, ICE2, ICE); d.text(668, 108, 'i.instagram.com  57.144.x.x', 13, NAVY, 800)
d.chip(670, 126, 240, 30, 'HTTPS (Instagram)  port 443', WHITE, BLUE, NAVY, 12)
d.chip(670, 166, 240, 30, 'HTTP               port 80', WHITE, LINE, INK, 12)
d.arrow(294, 141, 646, 141, BLUE)
d.text(470, 124, 'one packet', 12.5, BLUE, 700, 'middle')
d.text(30, 306, 'The IP address brings the packet to the right device. The port brings it to the right app inside.', 12.5, MIST, 500)
d.raw('<g class="box">')
d.box(30, 322, 900, 62, WHITE, RED, 10, 1.6)
d.text(48, 348, 'The four numbers of this connection:', 12.5, NAVY, 800)
d.runs(48, 372, [('192.168.1.5', INK), (' : ', MIST), ('51000', RED), ('   to   ', MIST), ('i.instagram.com (57.144.x.x)', INK), (' : ', MIST), ('443', RED)], 13.5, 'start', True, 700)
d.raw('</g>')
d.save(OUT, '02-ports-four-numbers.svg')

# 3. the IANA list
d = D(960, 350, 'Servers use fixed ports, kept in IANA\'s public list (Internet Assigned Numbers Authority)')
rows = [(('80', 'HTTP: web pages, no security'), ('25', 'SMTP: email servers talk to each other')),
        (('443', 'HTTPS: encrypted HTTP; websites, app APIs'), ('5432', 'PostgreSQL: a database')),
        (('53', 'DNS: Domain Name System questions'), ('3306', 'MySQL: a database')),
        (('22', 'SSH: Secure Shell, login to a server'), ('80 / 443', 'WebSocket, SSL / TLS: no ports of their own'))]
for r, (a, b) in enumerate(rows):
    y = 84 + r * 48
    for (num, name), x in ((a, 30), (b, 500)):
        d.chip(x, y, 90, 36, num, RED2 if num == '443' else ICE2, RED if num == '443' else ICE, NAVY, 13, True, 800)
        d.chip(x + 96, y, 334, 36, name, WHITE, LINE, INK, 12, False)
d.text(30, 294, 'APIs (Application Programming Interfaces: the way between an app and its server) and WebSocket ride on 443 or 80.', 12.5, MIST, 500)
d.text(30, 318, 'Ports 0 to 1,023 are the well-known ports, kept for services like these.', 12.5, MIST, 500)
d.save(OUT, '03-port-table.svg')

# 4. port ranges and the phone's pick
d = D(960, 290, 'The 65,536 port numbers (0 to 65,535): where the server\'s and the phone\'s ports come from')
rng = [('Well-known ports', '0 to 1,023', 'fixed services: 22, 53, 80, 443', ICE2, ICE),
       ('Registered ports', '1,024 to 49,151', 'listed: 3306, 5432', WHITE, LINE),
       ('Dynamic ports', '49,152 to 65,535', 'IANA\'s range for free ports', RED2, RED)]
x = 30
for (n, r, note, fill, st), w in zip(rng, [150, 410, 340]):
    d.card(x, 84, w - 6, 74, n, [r], fill, st, mono=False, tsize=13.5, lsize=12)
    d.text(x + (w - 6) / 2, 186, note, 12, MIST, 600, 'middle')
    x += w
d.text(30, 232, 'Android picks the phone\'s free port from 32,768 to 60,999: the Instagram connection got 51000.', 12.5, NAVY, 700)
d.text(30, 258, 'When the connection closes, the port is free again. The bars are not to scale.', 12, MIST, 500)
d.save(OUT, '04-port-ranges.svg')

# 5. the handshake
d = D(960, 640, 'The three-way handshake on the real example (the starting numbers 1000 and 5000 are made easy)')
d.card(100, 66, 200, 48, 'Phone', ['192.168.1.5'], ICE2, ICE, mono=True, tsize=13.5, lsize=11.5)
d.card(660, 66, 200, 48, 'i.instagram.com', ['57.144.x.x'], ICE2, ICE, mono=True, tsize=13.5, lsize=11.5)
d.line(200, 118, 200, 540, MIST, 1.6, True)
d.line(760, 118, 760, 540, MIST, 1.6, True)
steps = [('FROM 192.168.1.5:51000 · TO 57.144.x.x:443', 'SYN · SEQ 1000 · DATA empty', True, 'step 1', BLUE),
         ('FROM 57.144.x.x:443 · TO 192.168.1.5:51000', 'SYN ACK · SEQ 5000 · ACK 1001', False, 'step 2', RED),
         ('FROM 192.168.1.5:51000 · TO 57.144.x.x:443', 'ACK · SEQ 1001 · ACK 5001', True, 'step 3', BLUE)]
for i, (a, b, fwd, lab, col) in enumerate(steps):
    y0 = 128 + i * 134
    d.chip(250, y0, 460, 26, a, WHITE, col, NAVY, 11.5)
    d.chip(250, y0 + 32, 460, 26, b, ICE2 if fwd else RED2, col, NAVY, 11.5)
    if fwd:
        d.arrow(204, y0 + 74, 756, y0 + 106, BLUE)
    else:
        d.arrow(756, y0 + 74, 204, y0 + 106, RED)
    d.text(30, y0 + 92, lab, 12.5, col, 800)
d.text(30, 566, 'Now both sides know each other\'s starting number, and both have confirmed it: a TCP connection exists.', 13, NAVY, 700)
d.text(30, 594, 'ACK 1001 = "I got your 1000, the next byte I need is 1001".  The message is in none of the three segments.', 12.5, MIST, 600)
d.text(30, 618, 'Cost: one full round trip passes before the first byte of the message can go.', 12.5, MIST, 600)
d.path('M 830 190 V 520', RED, True, 2, False)
d.text(842, 350, '1 round', 12, RED, 700)
d.text(842, 368, 'trip', 12, RED, 700)
d.save(OUT, '05-handshake.svg')

# 6. the message cut into segments
MSG = 'Kal 5 baje CP pe milte hain :)'
assert len(MSG) == 30
d = D(960, 420, 'The DM is 30 bytes, one byte per character: cut into three segments of 10 bytes')
d.text(30, 76, 'Byte numbers start at 1001 (the phone\'s counting began at 1000).   \u00b7 = a space', 12, MIST, 600)
for i, ch in enumerate(MSG):
    hot = 17 <= i <= 21                                   # "milte" is cut between "mil" and "te"
    seg = i // 10
    d.chip(30 + i * 30, 92, 28, 30, '\u00b7' if ch == ' ' else ch, RED2 if hot else (ICE2, WHITE, ICE2)[seg], RED if hot else (ICE, LINE, ICE)[seg], NAVY, 13, True, 700, 4)
for i in (0, 9, 10, 19, 20, 29):
    d.text(30 + i * 30 + 14, 142, str(1001 + i), 10.5, MIST, 700, 'middle', True)
segs = [('Segment 1 \u00b7 SEQ 1001', 'bytes 1001 to 1010', '"Kal 5 baje"'),
        ('Segment 2 \u00b7 SEQ 1011', 'bytes 1011 to 1020', '" CP pe mil"'),
        ('Segment 3 \u00b7 SEQ 1021', 'bytes 1021 to 1030', '"te hain :)"')]
for k, (t, l1, l2) in enumerate(segs):
    d.card(30 + k * 300, 162, 294, 84, t, [l1, l2], (ICE2, WHITE, ICE2)[k], (ICE, LINE, ICE)[k], mono=True, tsize=13, lsize=12)
    d.arrow(177 + k * 300, 306, 177 + k * 300, 250, RED, dash=True, w=1.8)
    d.chip(30 + k * 300, 308, 294, 32, f'ACK {1011 + k * 10}: "next byte I need is {1011 + k * 10}"', WHITE, RED, RED, 12, True, 700)
d.text(30, 372, '"milte" is cut in two: TCP counts bytes, not words.', 13, RED, 800)
d.text(30, 396, 'A real segment carries about 1,400 bytes; 10 is only here to make the counting easy to see.', 12.5, MIST, 500)
d.save(OUT, '06-segments.svg')

# 7. lost segment
d = D(960, 620, 'A lost segment: ACK 1011 again and again, then the resend')
d.card(40, 66, 170, 44, 'Phone (sender)', [], ICE2, ICE, tsize=13)
d.card(750, 66, 170, 44, 'Server (receiver)', [], ICE2, ICE, tsize=13)
rows = [('segment 1 \u00b7 SEQ 1001 \u00b7 "Kal 5 baje"', 'ACK 1011  "got up to 1010, send 1011"', False),
        ('segment 2 \u00b7 SEQ 1011 \u00b7 " CP pe mil"', 'lost on the way', True),
        ('segment 3 \u00b7 SEQ 1021 \u00b7 "te hain :)"', 'ACK 1011  duplicate: "still waiting for 1011"', False),
        ('segment 2 sent again \u00b7 SEQ 1011', 'ACK 1031  "all of 1001 to 1030 received"', False)]
for i, (f, b, lost) in enumerate(rows):
    y0 = 134 + i * 86
    if lost:
        d.arrow(214, y0 + 26, 520, y0 + 26, RED, f, lcol=RED)
        d.text(560, y0 + 31, 'X  lost', 14, RED, 800)
        d.text(580, y0 + 58, 'no ACK is sent', 12, RED, 600, 'middle')
    else:
        d.arrow(214, y0 + 26, 746, y0 + 26, BLUE, f, lcol=BLUE)
        d.arrow(746, y0 + 58, 214, y0 + 58, RED if i == 2 else BLUE, b, lcol=RED if i == 2 else MIST, ldy=-8)
d.text(30, 492, 'Three extra copies of ACK 1011 make the phone resend at once (fast retransmit). A timer does the same if no ACK comes in time.', 12.5, NAVY, 700)
d.text(30, 520, 'In this tiny message only one duplicate appears; in a long message every segment behind the lost one brings another.', 12, MIST, 500)
d.text(30, 546, 'The server keeps segment 3 on the side and cannot hand "te hain :)" to the app yet: that wait is head-of-line blocking.', 12.5, MIST, 500)
d.text(30, 572, 'Like a toll plaza: one car stuck at the front holds up every car behind it.', 12.5, MIST, 500)
d.save(OUT, '07-lost-segment.svg')

# 8. speed: congestion control
d = D(960, 400, 'Speed: how many segments TCP sends before it waits for ACKs (one bar = one round trip)')
base = 300
vals = [(10, '10', False), (20, '20', False), (40, '40', False), (80, '80', False), (0, 'loss', True), (56, 'lower', False), (62, 'a bit more', False), (68, 'more', False)]
for i, (v, lab, lost) in enumerate(vals):
    x = 40 + i * 110
    if lost:
        d.chip(x, base - 36, 90, 36, 'loss', RED2, RED, RED, 13, False, 800)
    else:
        h = v * 2.4
        d.box(x, base - h, 90, h, ICE2, ICE, 6)
        d.text(x + 45, base - h - 8, lab, 12.5, NAVY, 800, 'middle')
d.line(30, base, 930, base, LINE, 1.4)
d.text(30, 336, 'Slow start: about 10 segments first, then double after every round trip that comes back clean.', 12.5, NAVY, 700)
d.text(30, 360, 'A loss means a jam on the road: TCP cuts its speed, then grows again slowly. That is congestion control.', 12.5, NAVY, 700)
d.text(30, 384, 'This is why a big download starts slow. Flow control is separate: the server\'s window says how much room it has left.', 12, MIST, 500)
d.save(OUT, '08-speed.svg')

# 9. TCP header
d = D(960, 470, 'The TCP header: at least 20 bytes in front of the data (one row = 32 bits = 4 bytes)')
X0, CW = 190, 20
def hrow(y, fields, label):
    x = X0
    for name, bits, hot in fields:
        w = bits * CW
        d.chip(x, y, w - 2, 44, name, ICE2 if hot else WHITE, ICE if hot else LINE, NAVY, 12.5, False, 700)
        x += w
    d.text(X0 + 640 + 20, y + 28, label, 12.5, MIST, 700)
d.text(X0, 84, '0', 11, MIST, 600); d.text(X0 + 320, 84, '16', 11, MIST, 600, 'middle'); d.text(X0 + 640, 84, '31', 11, MIST, 600, 'end')
hrow(94, [('Source port (2 B)', 16, True), ('Destination port (2 B)', 16, True)], '2 + 2 bytes')
hrow(144, [('Sequence number (4 B)', 32, True)], '4 bytes')
hrow(194, [('Acknowledgment number (4 B)', 32, True)], '4 bytes')
hrow(244, [('Offset, flags (SYN, ACK, FIN...)', 16, False), ('Window', 16, False)], '4 bytes')
hrow(294, [('Checksum', 16, False), ('Urgent pointer', 16, False)], '4 bytes')
d.box(X0, 344, 638, 36, WHITE, LINE, 8, 1.4, True)
d.text(X0 + 319, 367, 'Options (optional, up to 40 more bytes)', 12.5, MIST, 600, 'middle')
d.text(30, 412, '2 + 2 + 4 + 4 + 4 + 4 = 20 bytes', 14, RED, 800)
d.text(30, 438, 'The ports are the same two as in UDP. Everything after them is what TCP adds for order and resend.', 12.5, MIST, 500)
d.save(OUT, '09-tcp-header.svg')

# 10. UDP header and comparison
d = D(960, 380, 'The UDP header: 8 bytes, four fields of 2 bytes each')
d.text(X0, 84, '0', 11, MIST, 600); d.text(X0 + 320, 84, '16', 11, MIST, 600, 'middle'); d.text(X0 + 640, 84, '31', 11, MIST, 600, 'end')
hrow(94, [('Source port (2 B)', 16, True), ('Destination port (2 B)', 16, True)], '2 + 2 bytes')
hrow(144, [('Length (2 B)', 16, False), ('Checksum (2 B)', 16, False)], '2 + 2 bytes')
d.text(30, 232, 'Side by side (bar length = header size):', 13, NAVY, 800)
d.text(30, 262, 'UDP', 12.5, INK, 800)
d.box(90, 246, 8 * 16, 22, ICE2, ICE, 5)
d.text(90 + 8 * 16 + 10, 262, '8 bytes', 12.5, BLUE, 800)
d.text(30, 296, 'TCP', 12.5, INK, 800)
d.box(90, 280, 20 * 16, 22, RED2, RED, 5)
d.text(90 + 20 * 16 + 10, 296, '20 bytes or more', 12.5, RED, 800)
d.text(30, 340, 'Length counts the bytes in this datagram. The checksum is computed from the data: a changed bit makes the total not match.', 12.5, MIST, 500)
d.save(OUT, '10-udp-header.svg')

# 11. call packets
d = D(960, 340, 'A call: 20 ms of sound per packet, 50 packets every second')
d.text(30, 84, 'Instagram call, sent by the phone (one chip = 20 ms):', 13, NAVY, 800)
for i in range(12):
    if i == 6:
        d.chip(30 + i * 75, 98, 68, 34, 'lost', RED2, RED, RED, 12, False)
    else:
        d.chip(30 + i * 75, 98, 68, 34, f'#{i + 1}', WHITE, BLUE, NAVY, 12)
d.text(30, 184, 'What the listener hears (the app fills the gap):', 13, NAVY, 800)
for i in range(12):
    if i == 6:
        d.chip(30 + i * 75, 198, 68, 34, 'filled', ICE2, ICE, BLUE, 12, False)
    else:
        d.chip(30 + i * 75, 198, 68, 34, f'#{i + 1}', WHITE, BLUE, NAVY, 12)
d.text(30, 278, '1,000 ms ÷ 20 ms = 50 packets per second.', 13.5, RED, 800)
d.text(30, 304, 'A resend would arrive at least one round trip later, after its moment of speech is over; waiting for it would also stall #8, #9, #10.', 12.5, MIST, 500)
d.save(OUT, '11-call-packets.svg')

# 12. who uses which
d = D(960, 420, 'Who uses which')
d.box(30, 76, 430, 170, ICE2, ICE); d.text(60, 108, 'TCP: every byte must arrive', 14, NAVY, 800)
for i, t in enumerate(('websites, app APIs (443)', 'UPI payments', 'chat messages (Instagram DM)', 'file downloads')):
    d.text(60, 140 + i * 24, '•  ' + t, 13, INK, 600)
d.box(500, 76, 430, 170, WHITE, LINE); d.text(530, 108, 'UDP: on time beats complete', 14, NAVY, 800)
for i, t in enumerate(('video and voice calls', 'online game positions', 'DNS questions (port 53)', 'QUIC (YouTube, Instagram)')):
    d.text(530, 140 + i * 24, '•  ' + t, 13, INK, 600)
d.text(30, 282, 'DNS uses both, on the same port 53:', 13, NAVY, 800)
d.chip(30, 298, 190, 34, 'question over UDP 53', WHITE, BLUE, NAVY, 12, False)
d.arrow(224, 315, 306, 315, BLUE)
d.chip(310, 298, 220, 34, 'answer too big: TC = 1', RED2, RED, RED, 12, False)
d.arrow(534, 315, 616, 315, RED)
d.chip(620, 298, 230, 34, 'ask again over TCP 53', ICE2, ICE, NAVY, 12, False)
d.text(30, 372, 'Rule of thumb: where every byte must arrive, TCP. Where being on time matters more than being complete, UDP.', 12.5, MIST, 500)
d.save(OUT, '12-who-uses-which.svg')

# 13. QUIC lanes
d = D(960, 440, 'One lost packet in the feed: TCP stalls every photo, QUIC only one')
d.text(30, 84, 'Over TCP: all photos share one ordered line', 13.5, NAVY, 800)
d.chip(30, 100, 70, 30, 'photo 1', WHITE, LINE, INK, 12, False)
d.chip(112, 100, 70, 30, 'photo 2', WHITE, LINE, INK, 12, False)
d.chip(194, 100, 70, 30, 'lost', RED2, RED, RED, 12, False)
for i, t in enumerate(('photo 4', 'photo 5', 'photo 6')):
    d.chip(276 + i * 82, 100, 70, 30, t, RED2, RED, MIST, 12, False)
d.text(30, 160, 'Everything behind the lost packet waits for the resend, even photos that arrived fine.', 12.5, RED, 700)
d.text(30, 214, 'Over QUIC (on UDP): every photo has its own stream', 13.5, NAVY, 800)
for i, (t, lost) in enumerate((('photo 1', False), ('photo 2', True), ('photo 3', False))):
    y = 232 + i * 40
    d.text(30, y + 20, t, 12.5, INK, 700)
    for j in range(4):
        if lost and j == 2:
            d.chip(120 + j * 82, y, 70, 28, 'lost', RED2, RED, RED, 12, False)
        elif lost and j == 3:
            d.chip(120 + j * 82, y, 70, 28, 'waits', RED2, RED, MIST, 12, False)
        else:
            d.chip(120 + j * 82, y, 70, 28, 'ok', ICE2, ICE, NAVY, 12, False)
d.text(30, 372, 'Only photo 2 pauses until its packet is resent. QUIC does its own numbering, ACKs, resend and encryption on top of UDP.', 12.5, BLUE, 700)
d.text(30, 400, 'Stacks:  HTTP/1.1, HTTP/2 · TCP · IP        and        HTTP/3 · QUIC · UDP · IP', 12.5, MIST, 600)
d.save(OUT, '13-quic-lanes.svg')
print('ok')
