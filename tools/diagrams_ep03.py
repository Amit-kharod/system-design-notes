"""Draws the Ep 3 (DNS) diagrams as SVG, in the Code Man light style.
usage: python3 tools/diagrams_ep03.py   (writes ep03-dns/diagrams/*.svg)
Real names (youtube.com, google.com, ICANN, Verisign, GoDaddy ...). codeman.com is a "suppose I bought it" example, so its
servers use the documentation range 203.0.113.x. No example.com anywhere."""
import os
from svgkit import D, NAVY, INK, BLUE, ICE, ICE2, RED, RED2, MIST, LINE, WHITE, BAND

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ep03-dns', 'diagrams')
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.svg'):
        os.remove(os.path.join(OUT, f))

# 1. the name, read right to left
d = D(960, 330, 'A name is read from the right: root, top-level domain, domain, subdomain')
parts = [('blog', 150, ICE2, ICE), ('.', 36, WHITE, LINE), ('codeman', 210, ICE2, ICE),
         ('.', 36, WHITE, LINE), ('com', 140, ICE2, ICE), ('.', 60, RED2, RED)]
xs = [60, 218, 258, 478, 518, 668]
for (t, w, fill, st), x in zip(parts, xs):
    d.chip(x, 82, w, 48, t, fill, st, RED if st == RED else NAVY, 20)
d.text(135, 154, 'subdomain', 12.5, BLUE, 700, 'middle')
d.text(363, 154, 'domain (the name you buy)', 12.5, BLUE, 700, 'middle')
d.text(588, 154, 'TLD', 12.5, BLUE, 700, 'middle')
d.text(698, 154, 'root', 12.5, RED, 800, 'middle')
d.arrow(850, 106, 760, 106, RED)
d.text(852, 88, 'read this way', 12, RED, 700, 'start')
d.text(852, 126, 'right to left', 12, RED, 700, 'start')
d.text(30, 196, 'Every level is a domain:', 13, NAVY, 800)
d.chip(30, 210, 130, 30, 'com', WHITE, LINE, INK, 13)
d.chip(168, 210, 190, 30, 'codeman.com', WHITE, LINE, INK, 13)
d.chip(366, 210, 230, 30, 'blog.codeman.com', WHITE, LINE, INK, 13)
d.text(30, 272, 'The full name really ends with a dot: blog.codeman.com. That last dot is the root, the top of the tree.', 12.5, MIST, 500)
d.text(30, 294, 'youtube.com works the same way: youtube (domain), com (TLD), and the hidden root dot.', 12.5, MIST, 500)
d.text(30, 316, 'In these notes codeman.com is only a "suppose I bought it" example: the real codeman.com belongs to someone else.', 12.5, MIST, 500)
d.save(OUT, '01-name-right-to-left.svg')

# 2. the old way: one file kept by the NIC
d = D(960, 470, 'The old way, 1970s and 1980s: one file, HOSTS.TXT, kept in one place')
d.card(30, 76, 230, 84, 'A new computer', ['its owner sends an email:', '"please add it to the list"'], ICE2, ICE, mono=False, tsize=13.5, lsize=12)
d.card(380, 66, 290, 104, 'NIC at SRI', ['Network Information Center,', 'Menlo Park, California', 'keeps HOSTS.TXT'], WHITE, RED, mono=False, tsize=14, lsize=12)
d.card(730, 76, 200, 84, 'Every computer', ['downloads the whole', 'file again and again'], ICE2, ICE, mono=False, tsize=13.5, lsize=12)
d.arrow(262, 118, 378, 118, BLUE)
d.arrow(672, 118, 728, 118, BLUE)
d.text(320, 106, 'email', 12, BLUE, 700, 'middle')
d.text(30, 204, 'The mailbox for requests was HOSTMASTER@SRI-NIC.ARPA. The file was rebuilt once or twice a week.', 12.5, MIST, 500)
d.text(30, 240, 'Why it broke', 13.5, NAVY, 800)
for i, (a, b) in enumerate((('The file kept growing', 'as more computers joined'), ('A new name took days', 'to reach every computer'), ('Thousands of computers', 'asked one office for the file'))):
    d.card(30 + i * 310, 254, 290, 58, a, [b], WHITE, LINE, mono=False, tsize=12.5, lsize=12)
d.text(30, 352, 'What came next', 13.5, NAVY, 800)
d.line(70, 400, 890, 400, MIST, 2)
tl = [(110, '1983', 'Paul Mockapetris', 'designs DNS'), (370, '1985', 'symbolics.com', 'the first .com name'),
      (630, '1990s', 'Network Solutions', 'sells domain names'), (850, '1999', 'many companies', 'GoDaddy, Hostinger ...')]
for x, a, b, c in tl:
    d.dot(x, 400, 7, BLUE)
    d.text(x, 380, a, 13, NAVY, 800, 'middle')
    d.text(x, 424, b, 12, INK, 700, 'middle')
    d.text(x, 442, c, 11.5, MIST, 600, 'middle')
d.save(OUT, '02-one-file-hosts-txt.svg')

# 3. who controls it: ICANN, the root list, the registries
d = D(960, 440, 'Who decides which TLDs exist: ICANN and its root list')
d.card(30, 96, 220, 84, 'ICANN', ['non-profit, since 1998', 'keeps the root list'], ICE2, ICE, mono=False, tsize=15, lsize=12)
d.arrow(252, 138, 298, 138, BLUE)
d.raw('<g class="box">')
d.box(300, 66, 230, 244, WHITE, LINE)
d.text(415, 90, 'Root list: 1,436 TLDs', 13, NAVY, 800, 'middle')
d.raw('</g>')
for i, t in enumerate(('.com', '.in', '.google', '.youtube')):
    d.chip(320, 106 + i * 40, 190, 30, t, ICE2 if i == 0 else WHITE, ICE if i == 0 else LINE, INK, 13)
d.text(415, 282, 'and 1,432 more, each with', 11.5, MIST, 600, 'middle')
d.text(415, 298, 'the servers that hold its list', 11.5, MIST, 600, 'middle')
regs = [(70, 'Verisign', ['registry of .com', 'about 17 crore .com names']),
        (150, 'NIXI', ['registry of .in', 'National Internet Exchange of India']),
        (230, 'Google', ['registry of .google and .youtube', 'its own TLDs, from the 2012 round'])]
for y, n, ls in regs:
    d.card(640, y, 290, 64, n, ls, ICE2 if n == 'Verisign' else WHITE, ICE if n == 'Verisign' else LINE, mono=False, tsize=13.5, lsize=11.5)
d.arrow(512, 121, 638, 102, BLUE)
d.arrow(512, 161, 638, 182, BLUE)
d.arrow(512, 201, 638, 262, BLUE)
d.arrow(512, 241, 638, 276, BLUE)
d.text(30, 350, 'A new TLD needs an application to ICANN:', 13.5, NAVY, 800)
d.card(30, 364, 440, 56, '2012 round', ['about 1,930 applications, USD 1,85,000 each'], WHITE, LINE, mono=False, tsize=13, lsize=12)
d.card(490, 364, 440, 56, '2026 round', ['USD 2,27,000 each, about 2 crore rupees'], WHITE, LINE, mono=False, tsize=13, lsize=12)
d.save(OUT, '03-icann-root-list-registries.svg')

# 4. registrar, registry, name server
d = D(960, 420, 'Buying codeman.com: three different jobs (suppose I bought it)')
cards = [(30, 'Registrar: GoDaddy', ['where you buy the name', 'keeps: the domain is yours,', 'until when, where to send the bill'], ICE2, ICE),
         (360, 'Registry: Verisign', ['keeps the whole .com list', 'codeman.com is one entry:', 'its name servers, no IP address'], WHITE, RED),
         (690, 'Name servers: GoDaddy', ['ns51.domaincontrol.com', 'ns52.domaincontrol.com', 'your own list: A, MX, TXT ...'], ICE2, ICE)]
for x, t, ls, fill, st in cards:
    d.card(x, 84, 240, 112, t, ls, fill, st, mono=False, tsize=13.5, lsize=12)
d.arrow(272, 140, 358, 140, BLUE)
d.arrow(602, 140, 688, 140, BLUE, dash=True)
d.text(315, 126, '2', 14, BLUE, 800, 'middle')
d.text(645, 126, '3', 14, BLUE, 800, 'middle')
d.text(30, 232, '1  You pay GoDaddy for one year of codeman.com.', 12.5, INK, 600)
d.text(30, 254, '2  GoDaddy asks Verisign if the name is free, and files it there.', 12.5, INK, 600)
d.text(30, 276, '3  GoDaddy tells Verisign: the list of codeman.com is on ns51 and ns52.domaincontrol.com.', 12.5, INK, 600)
d.raw('<g class="box">')
d.box(30, 300, 900, 40, WHITE, LINE, 8)
d.text(480, 325, 'Of the price, about USD 11 goes to Verisign and 20 cents to ICANN. The rest is GoDaddy\'s.', 12.5, NAVY, 700, 'middle')
d.raw('</g>')
d.text(30, 372, 'Registrar = where you buy. Registry = the TLD\'s list. Name server = your own list.', 13, RED, 800)
d.text(30, 396, 'Moving your list to another name server (for example Cloudflare) changes step 3 only: you stay a customer of GoDaddy.', 12.5, MIST, 500)
d.save(OUT, '04-registrar-registry-name-server.svg')

# 5. one NS row, column by column
d = D(960, 420, 'One row from the .com list, column by column')
d.raw('<g class="box">')
d.box(30, 58, 900, 84, WHITE, LINE)
d.raw('</g>')
cols = [(46, 'codeman.com.', RED), (222, '172800', RED), (330, 'IN', NAVY), (404, 'NS', RED), (480, 'ns51.domaincontrol.com.', RED)]
for x, t, c in cols:
    d.text(x, 92, t, 16, c, 700, 'start', True)
    d.text(x, 124, {46: 'codeman.com.', 222: '172800', 330: 'IN', 404: 'NS', 480: 'ns52.domaincontrol.com.'}[x], 16, MIST, 600, 'start', True)
labels = [(30, '1  NAME', ['the name this row', 'is about']),
          (212, '2  KEEP FOR (TTL)', ['seconds to remember it:', '1,72,800 = 2 days']),
          (394, '3  CLASS', ['always IN: Internet', '(old, never changes)']),
          (576, '4  TYPE', ['NS = Name Server:', 'who holds the list']),
          (758, '5  VALUE', ['the name server:', 'a GoDaddy computer'])]
centers = [100, 250, 340, 420, 590]
for (x, t, ls), c in zip(labels, centers):
    d.line(c, 134, x + 86, 196, MIST, 1.2)
    d.card(x, 198, 172, 84, t, ls, ICE2 if x in (212, 576) else WHITE, ICE if x in (212, 576) else LINE, mono=False, tsize=12.5, lsize=11.5)
d.text(30, 322, 'The second row is for the second name server, ns52. Both hold the same list, so if one stops, the other answers.', 12.5, INK, 600)
d.text(30, 346, '1,72,800 seconds ÷ 60 ÷ 60 ÷ 24 = 2 days.', 12.5, INK, 600)
d.text(30, 370, 'Verisign has no IP address for codeman.com. It only knows who to ask next.', 12.5, INK, 600)
d.text(30, 398, 'The same kind of row exists for youtube.com: youtube.com. 172800 IN NS ns1.google.com.', 12.5, MIST, 500)
d.save(OUT, '05-ns-row-columns.svg')

# 6. the delegation chain for blog.codeman.com
d = D(960, 470, 'Delegation: each list points to the next one (blog.codeman.com)')
chain = [(70, 'Root server', ['ICANN\'s root list'], 'The root list says:', 'com.  172800  IN  NS  a.gtld-servers.net.', '(13 rows, a to m)', False),
         (190, '.com server', ['Verisign\'s .com list'], 'The .com list says:', 'codeman.com.  172800  IN  NS  ns51.domaincontrol.com.', '(2 rows, ns51 and ns52)', False),
         (310, 'GoDaddy name server', ['codeman.com\'s own list'], 'The name server says:', 'blog.codeman.com.  3600  IN  A  203.0.113.20', 'the real answer, written by the owner', True)]
for y, n, ls, a, row, note, last in chain:
    d.card(30, y, 240, 80, n, ls, ICE2 if last else WHITE, ICE if last else LINE, mono=False, tsize=13.5, lsize=12)
    d.arrow(272, y + 40, 318, y + 40, BLUE)
    d.raw('<g class="box">')
    d.box(320, y, 610, 80, ICE2 if last else WHITE, ICE if last else LINE)
    d.text(336, y + 25, a, 12, MIST, 700)
    d.text(336, y + 47, row, 12.5, RED if last else INK, 800, 'start', True)
    d.text(336, y + 67, note, 11.5, MIST, 600)
    d.raw('</g>')
d.arrow(150, 152, 150, 188, BLUE)
d.arrow(150, 272, 150, 308, BLUE)
d.text(164, 175, 'points to', 11.5, BLUE, 700)
d.text(164, 295, 'points to', 11.5, BLUE, 700)
d.text(30, 422, 'Each level keeps only the next hop. Only the last list holds the address, and its owner (whoever bought the name) wrote it.', 12.5, MIST, 500)
d.text(30, 444, 'Handing a part of the list to someone else is called delegation. Each part, run by one owner, is a zone.', 12.5, MIST, 500)
d.save(OUT, '06-delegation-chain.svg')

# 7. the 13 root names and their operators, and anycast
d = D(960, 470, 'The 13 root names A to M: letters are only names, 12 organisations run them')
ops = [('A', ['Verisign']), ('B', ['USC-ISI']), ('C', ['Cogent']), ('D', ['Univ. of', 'Maryland']), ('E', ['NASA']),
       ('F', ['ISC']), ('G', ['US Dept of', 'Defense']), ('H', ['US Army', 'Research Lab']), ('I', ['Netnod']),
       ('J', ['Verisign']), ('K', ['RIPE NCC']), ('L', ['ICANN']), ('M', ['WIDE Project'])]
for i, (l, ls) in enumerate(ops):
    row, col = (0, i) if i < 7 else (1, i - 7)
    x = 30 + col * 130
    y = 66 + row * 88
    ver = 'Verisign' in ls
    d.card(x, y, 122, 76, l, ls, ICE2 if ver else WHITE, ICE if ver else LINE, mono=False, tsize=14, lsize=12)
d.text(30, 248, 'The names run from a.root-servers.net to m.root-servers.net. Verisign (shaded) runs two of them, A and J.', 11.5, MIST, 600)
d.text(30, 276, 'Behind each name: many copies of the same list. One address is shared, and the question goes to the nearest copy (anycast).', 13, NAVY, 800)
d.card(30, 292, 130, 56, 'Resolver', ['in Mumbai'], ICE2, ICE, mono=False, tsize=13, lsize=11.5)
for n, x in (('Mumbai', 210), ('Delhi', 460), ('Chennai', 710)):
    d.card(x, 292, 200, 56, f'copy in {n}', ['same address, same list'], WHITE, LINE if n != 'Mumbai' else RED, mono=False, tsize=12.5, lsize=11.5)
d.arrow(162, 320, 208, 320, RED)
d.text(310, 366, 'nearest: answers', 11.5, RED, 700, 'middle')
d.text(560, 366, 'farther: not asked', 11.5, MIST, 700, 'middle')
d.text(810, 366, 'farther: not asked', 11.5, MIST, 700, 'middle')
d.text(30, 400, '2,046 copies in all (15 Nov 2026), more than 60 of them in India. Why only 13 names: an answer had to fit in 512 bytes.', 12.5, MIST, 500)
d.text(30, 422, 'The .com list works the same way: 13 servers, a.gtld-servers.net to m.gtld-servers.net, all Verisign\'s, the same copy on each.', 12.5, MIST, 500)
d.text(30, 444, '"Nearest" means nearest by internet routing, which is usually, not always, the closest in kilometres.', 12.5, MIST, 500)
d.save(OUT, '07-root-names-anycast.svg')

# 8. the lookup as a conversation
d = D(960, 560, 'One lookup for blog.codeman.com: the phone asks once, the resolver asks three servers')
d.card(30, 80, 150, 56, 'Your phone', ['192.168.1.5'], ICE2, ICE, tsize=13.5, lsize=12)
d.card(270, 80, 190, 56, 'Resolver', ['your ISP\'s, e.g. Jio'], WHITE, LINE, mono=False, tsize=13.5, lsize=12)
d.arrow(184, 100, 266, 100, BLUE)
d.arrow(266, 120, 184, 120, RED)
d.text(225, 76, '1  recursive', 12, BLUE, 700, 'middle')
d.text(225, 150, '5  the answer', 12, RED, 700, 'middle')
d.text(30, 176, 'The phone asks once and wants the', 11.5, MIST, 600)
d.text(30, 194, 'whole answer: a recursive query.', 11.5, MIST, 600)
rows = [('Root server', 'ICANN\'s root list', 252, False, 'asks: which servers hold the .com list?', 'referral: a to m.gtld-servers.net'),
        ('.com server', 'Verisign', 336, False, 'asks: which servers hold codeman.com?', 'referral: ns51 and ns52.domaincontrol.com'),
        ('GoDaddy name server', 'ns51.domaincontrol.com', 420, True, 'asks: what is the IP of blog.codeman.com?', 'answer: 203.0.113.20, keep for 3,600 s')]
for i, (name, kind, y, last, q, a) in enumerate(rows):
    d.card(270, y - 28, 190, 58, name, [kind], ICE2 if last else WHITE, ICE if last else LINE, tsize=12.5, lsize=11.5, mono=False)
    d.raw('<g class="box">')
    d.box(490, y - 32, 440, 66, ICE2 if last else WHITE, ICE if last else LINE)
    d.text(502, y - 10, q, 11.5, MIST, 700)
    d.text(502, y + 14, a, 11.5, RED if last else INK, 800, 'start', True)
    d.raw('</g>')
    d.arrow(462, y, 488, y, MIST)
    d.text(250, y + 4, f'{i + 2}', 14, BLUE, 800, 'middle')
d.arrow(365, 138, 365, 222, BLUE)
d.arrow(365, 282, 365, 306, BLUE)
d.arrow(365, 366, 365, 390, BLUE)
d.text(380, 190, 'iterative: one server after another', 11.5, BLUE, 700)
d.text(30, 506, 'Each server only points to the next one (a referral). The last one owns the list, so its answer is final: authoritative.', 12.5, MIST, 500)
d.text(30, 526, 'youtube.com goes the same way, but Verisign\'s row points to Google\'s own four name servers, ns1.google.com to ns4.google.com.', 12.5, MIST, 500)
d.text(30, 546, 'The whole walk takes a few milliseconds.', 12.5, MIST, 500)
d.save(OUT, '08-resolver-walk.svg')

# 9. cache and TTL, and the 48-hour message
d = D(960, 480, 'Cache and TTL: the old answer stays for as long as the TTL says')
d.line(60, 200, 900, 200, MIST, 2)
for x, t in ((60, '0 s'), (480, '1,800 s'), (900, '3,600 s = 1 hour')):
    d.line(x, 194, x, 206, MIST, 2)
    d.text(x, 226, t, 12, MIST, 700, 'middle' if x != 900 else 'end')
d.box(60, 150, 840, 36, ICE2, ICE, 6)
d.text(480, 173, 'the resolver answers from its cache: it asks nobody', 13, NAVY, 700, 'middle')
d.dot(60, 120, 7)
d.text(76, 125, 'a resolver caches  blog.codeman.com  A  203.0.113.20  (TTL 3600)', 12.5, INK, 700)
d.dot(120, 90, 7, BLUE)
d.text(136, 95, 'one second later you switch the record to 203.0.113.30: this resolver does not know yet', 12.5, BLUE, 700)
d.dot(900, 120, 7, RED)
d.text(884, 125, 'expires', 12.5, RED, 800, 'end')
d.text(30, 262, 'Until the timer ends, this resolver keeps giving the old address. After it, it asks again and gets the new one.', 12.5, MIST, 500)
d.text(30, 284, 'Other resolvers cached at other moments, so they all switch at different times: that spread is "propagation".', 12.5, MIST, 500)
d.text(30, 336, 'The same idea for name servers: the 48-hour message', 13.5, NAVY, 800)
d.line(60, 408, 900, 408, MIST, 2)
for x, t in ((60, '0'), (480, '24 hours'), (900, '48 hours = 1,72,800 s')):
    d.line(x, 402, x, 414, MIST, 2)
    d.text(x, 434, t, 12, MIST, 700, 'middle' if x == 480 else ('start' if x == 60 else 'end'))
d.box(60, 358, 840, 36, RED2, RED, 6)
d.text(480, 381, 'a resolver that cached Verisign\'s old row may still ask GoDaddy\'s name servers, not Cloudflare\'s', 12.5, NAVY, 700, 'middle')
d.text(30, 462, 'You changed the name servers; Verisign\'s row has a TTL of 1,72,800 s, so some resolvers use the old row for up to 2 days.', 12, MIST, 500)
d.save(OUT, '09-cache-ttl.svg')

# 10. lowering the TTL before a move
d = D(960, 372, 'Moving to a new server: lower the TTL a day before, raise it after')
d.line(50, 168, 910, 168, MIST, 2)
steps = [(110, 'today', 'TTL 86,400 s', '(1 day)', LINE, WHITE),
         (330, '1 day or more before', 'lower TTL to 300 s', '(5 minutes)', ICE, ICE2),
         (570, 'switch day', 'record: new address', '203.0.113.30', RED, RED2),
         (810, 'a few days later', 'raise TTL back', '86,400 s', ICE, ICE2)]
for x, a, b, c, st, fill in steps:
    d.dot(x, 168, 8, RED if st == RED else BLUE)
    d.box(x - 100, 80, 200, 62, fill, st)
    d.text(x, 104, a, 12.5, NAVY, 800, 'middle')
    d.text(x, 122, b, 12, INK, 600, 'middle', True)
    d.text(x, 138, c, 11.5, MIST, 600, 'middle', True)
d.box(60, 214, 440, 34, WHITE, LINE, 6)
d.text(280, 236, 'every cache, once the old TTL runs out, now holds a 5-minute copy', 11.5, INK, 600, 'middle')
d.box(520, 214, 380, 34, WHITE, LINE, 6)
d.text(710, 236, 'after the switch, everyone has the new address in 5 minutes', 11.5, INK, 600, 'middle')
d.text(30, 292, 'Why a day before: a cache that stored the record just before you lowered it still holds it for up to 86,400 s.', 12.5, MIST, 500)
d.text(30, 314, 'The cost of a short TTL is more questions to your name servers, so raise it again once the move is done.', 12.5, MIST, 500)
d.text(30, 342, 'This is the practice RFC 1034 describes: reduce the TTL before an anticipated change, restore it afterwards.', 12.5, MIST, 500)
d.save(OUT, '10-ttl-before-move.svg')

# 11. traffic by location, rotation and failover
d = D(960, 420, 'DNS can answer by place, rotate the answers, and drop a dead server')
d.text(30, 86, 'By place (youtube.com)', 13.5, NAVY, 800)
d.card(30, 100, 170, 54, 'Resolver in Mumbai', [], WHITE, LINE, mono=False, tsize=12.5)
d.card(30, 172, 170, 54, 'Resolver in Delhi', [], WHITE, LINE, mono=False, tsize=12.5)
d.card(300, 128, 190, 72, 'Google name server', ['looks at who asks'], ICE2, ICE, mono=False, tsize=13, lsize=11.5)
d.arrow(202, 127, 298, 150, BLUE)
d.arrow(202, 199, 298, 180, BLUE)
d.text(520, 128, 'Mumbai gets the address of a Mumbai-side server', 12.5, INK, 700)
d.text(520, 156, 'Delhi gets the address of a Delhi-side server', 12.5, INK, 700)
d.text(520, 184, 'The name server sees the resolver, not your phone.', 11.5, MIST, 600)
d.text(30, 272, 'Rotating and failover (suppose codeman.com has three servers)', 13.5, NAVY, 800)
for i, (a, st) in enumerate((('203.0.113.21', 'ok'), ('203.0.113.22', 'ok'), ('203.0.113.23', 'dead'))):
    x = 30 + i * 200
    dead = st == 'dead'
    d.chip(x, 288, 180, 36, a, RED2 if dead else ICE2, RED if dead else ICE, RED if dead else INK, 12.5)
    d.text(x + 90, 344, 'removed from the answers' if dead else 'in the answers', 11.5, RED if dead else BLUE, 700, 'middle')
d.text(640, 298, 'Each new question gets the next', 12, INK, 600)
d.text(640, 316, 'address in turn. A health check', 12, INK, 600)
d.text(640, 334, 'finds the dead one: its address is no', 12, INK, 600)
d.text(640, 352, 'longer given out. Keep the TTL small.', 12, INK, 600)
d.text(30, 392, 'DNS hands out the address once. The requests that follow go straight to that server: DNS does not see each request.', 12.5, MIST, 500)
d.save(OUT, '11-dns-traffic.svg')

# 12. the 2021 outage
d = D(960, 352, 'October 2021: the servers ran, but nobody could find their names')
d.card(30, 82, 190, 60, 'Your phone', ['3 apps, all failing'], ICE2, ICE, mono=False, tsize=13.5, lsize=11.5)
d.card(300, 82, 170, 60, 'Resolver', ['asks for the name'], WHITE, LINE, mono=False, tsize=13.5, lsize=11.5)
d.card(550, 82, 190, 60, "Facebook's", ['DNS servers: running'], WHITE, RED, mono=False, tsize=13.5, lsize=11.5)
d.card(550, 188, 190, 56, 'Their app servers', ['also running'], WHITE, LINE, mono=False, tsize=13, lsize=11.5)
d.arrow(222, 112, 298, 112, BLUE)
d.arrow(472, 112, 548, 112, BLUE)
d.line(740, 112, 790, 112, RED, 2.5)
d.text(850, 104, 'cut off from', 12, RED, 800, 'middle')
d.text(850, 122, 'the internet', 12, RED, 800, 'middle')
d.text(30, 270, 'No address comes back, so no packet is ever sent.', 12.5, INK, 500)
d.text(30, 288, 'A wrong network change cut the DNS servers off from the internet.', 12.5, INK, 500)
d.text(760, 216, 'servers fine, but nobody', 12, MIST, 700)
d.text(760, 234, 'can find them by name', 12, MIST, 700)
d.text(30, 328, '4 October 2021 · about 6 hours · Facebook, Instagram and WhatsApp (Meta Engineering and Cloudflare reports)', 12.5, MIST, 500)
d.save(OUT, '12-outage.svg')

print('diagrams written to', OUT, sorted(os.listdir(OUT)))
