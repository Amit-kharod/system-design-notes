"""Builds the branded HTML of an episode's notes (light page, Code Man colours). print_pdf.mjs turns it into a PDF.
usage: python3 tools/build_pdf.py <episode folder> "<Topic>" <N>
       e.g. python3 tools/build_pdf.py ep02-subnet-mask-nat "Subnet Mask, Private IP & NAT" 2
Needs the Python package `markdown`. Fonts: the folder in $NOTES_FONTS (inter.woff2, jbm.woff2) if it exists,
otherwise the system fonts. Links to other files of the repo become plain text in the PDF, or full links when
$NOTES_REPO_URL is set (for example https://github.com/<user>/system-design-notes)."""
import base64, html, os, posixpath, re, sys
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP, TOPIC, NUM = sys.argv[1], sys.argv[2], sys.argv[3]
FONTS = os.environ.get('NOTES_FONTS', os.path.join(ROOT, 'fonts'))
REPO = os.environ.get('NOTES_REPO_URL', '').rstrip('/')

# the cover of each episode: one line on what is inside, and the topic chips
COVERS = {
    'ep01-ip-address': (
        'From one bit to the routing table: why every number stops at 255, what 430 crore means, who hands the '
        'addresses out and how routers find the way. With worked examples, diagrams and interview questions.',
        ['bits', '2ⁿ', '0 to 255', '32 bits', '430 crore', 'IANA and registries', 'routers', 'routing table',
         'default route', 'interview questions']),
    'ep02-subnet-mask-nat': (
        'The subnet mask and the AND, subnets, DHCP, private addresses, NAT and ports, one IP for many people, '
        'and IPv6. With worked examples, diagrams, code and interview questions.',
        ['subnet mask', '/24', 'AND', 'gateway', 'broadcast', 'subnetting', 'DHCP', 'private IP', 'NAT', 'ports',
         'CGNAT', 'IPv6', 'interview questions']),
}
blurb, chips = COVERS.get(EP, ('Everything in the video, with worked examples, diagrams and interview questions.', []))

src = open(os.path.join(ROOT, EP, 'README.md'), encoding='utf-8').read()
src = re.sub(r'^# .*\n', '', src, count=1)                                   # the cover carries the title
src = re.sub(r'^\*\*System Design for Beginners.*\n', '', src, flags=re.M)
src = re.sub(r'^- (Video|PDF of these notes|Next episode|Previous episode):.*\n', '', src, flags=re.M)
contents = [re.sub(r'[`*]', '', h) for h in re.findall(r'^## (.+)$', src, flags=re.M)]


def inline(m):
    svg = open(os.path.join(ROOT, EP, m.group(2)), encoding='utf-8').read()
    return f'\n<figure>{svg.strip()}<figcaption>{html.escape(m.group(1))}</figcaption></figure>\n'


src = re.sub(r'!\[(.*?)\]\((diagrams/.*?\.svg)\)', inline, src)
src = re.sub(r'(\n>[^\n]*)\n\n(?=> \*\*Beyond the video)', r'\1\n\n<div class="gap"></div>\n\n', src)   # one box per aside, as on GitHub
body = markdown.markdown(src, extensions=['tables', 'sane_lists', 'fenced_code'])
body = body.replace('<p><strong>Beyond the video', '<p><strong class="beyond">Beyond the video')


def local_link(m):                                                           # links inside the repo
    href, text = m.group(1), m.group(2)
    if not REPO:
        return text
    path = posixpath.normpath(posixpath.join(EP, href))
    return f'<a href="{REPO}/blob/main/{path}">{text}</a>'


body = re.sub(r'<a href="(?!https?:|mailto:|#)([^"]+)">(.*?)</a>', local_link, body)


def font(name):
    p = os.path.join(FONTS, name)
    return base64.b64encode(open(p, 'rb').read()).decode() if os.path.exists(p) else None


faces = ''
if font('inter.woff2'):
    faces += f"@font-face{{font-family:Inter;src:url(data:font/woff2;base64,{font('inter.woff2')}) format('woff2');font-weight:100 900}}\n"
if font('jbm.woff2'):
    faces += f"@font-face{{font-family:'JetBrains Mono';src:url(data:font/woff2;base64,{font('jbm.woff2')}) format('woff2');font-weight:100 800}}\n"
title_pt = 46 if len(TOPIC) <= 16 else 38
toc = ''.join(f'<li>{html.escape(c)}</li>' for c in contents)
chip_html = ''.join(f'<span>{html.escape(c)}</span>' for c in chips)
SANS = "Inter,-apple-system,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',Menlo,Consolas,monospace"
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Ep {NUM}: {html.escape(TOPIC)} (notes)</title><style>
{faces}@page{{size:A4;margin:16mm 15mm 17mm}}
*{{box-sizing:border-box}} html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:{SANS};color:#243352;font-size:10.6pt;line-height:1.5;margin:0;background:#fff}}
.cover{{height:262mm;display:flex;flex-direction:column;justify-content:space-between;page-break-after:always;border-left:7px solid #8fd0f2;padding:6mm 0 4mm 10mm}}
.brand{{font-family:{MONO};font-size:10pt;letter-spacing:.14em;color:#2f6fa8;font-weight:700}}
.cover h1{{font-size:{title_pt}pt;line-height:1.04;margin:0 0 5mm;color:#1a2640;font-weight:900;letter-spacing:-.02em}}
.cover h1 span{{color:#e3262c}} .cover p{{font-size:12.5pt;color:#6b7a94;margin:0;max-width:140mm}}
.toc h4{{font-family:{MONO};font-size:9pt;letter-spacing:.12em;color:#2f6fa8;margin:0 0 2.5mm;font-weight:700}}
.toc ul{{columns:2;column-gap:10mm;margin:0;padding:0;list-style:none;font-size:10pt;color:#243352}} .toc li{{margin:0 0 1.4mm;break-inside:avoid}}
.chips span{{display:inline-block;font-family:{MONO};font-size:8.6pt;border:1px solid #c9d6e6;border-radius:99px;padding:3px 10px;margin:0 5px 5px 0;color:#243352;background:#f7f9fc}}
h2{{font-size:15.5pt;color:#1a2640;margin:8mm 0 2.5mm;padding-bottom:1.6mm;border-bottom:2px solid #8fd0f2;font-weight:800;page-break-after:avoid;break-after:avoid}}
h3{{font-size:12pt;color:#2f6fa8;margin:5mm 0 2mm;page-break-after:avoid;break-after:avoid}}
p{{margin:0 0 2.6mm}} ul,ol{{margin:0 0 2.6mm;padding-left:5.2mm}} li{{margin-bottom:1.1mm}}
strong{{color:#1a2640}} a{{color:#2f6fa8;text-decoration:none}} em{{color:#6b7a94}}
code{{font-family:{MONO};font-size:9.2pt;background:#eef4fa;border-radius:4px;padding:1px 4px;color:#1a2640;font-variant-ligatures:none;font-feature-settings:'liga' 0,'calt' 0}}
pre{{background:#f3f7fb;border:1px solid #dbe4ef;border-radius:6px;padding:3mm 3.5mm;margin:1.5mm 0 4mm;page-break-inside:avoid;break-inside:avoid;white-space:pre-wrap}}
pre code{{background:none;padding:0;font-size:8.5pt;line-height:1.45;color:#1a2640}}
blockquote{{margin:3mm 0 4mm;padding:2.6mm 4mm 1mm;background:#f2f8fd;border-left:4px solid #8fd0f2;border-radius:0 6px 6px 0;page-break-inside:avoid;break-inside:avoid}}
.beyond{{color:#2f6fa8!important}} .gap{{height:0}}
table{{border-collapse:collapse;width:100%;margin:1.5mm 0 4mm;font-size:9.6pt;page-break-inside:avoid;break-inside:avoid}}
th{{background:#1a2640;color:#fff;text-align:left;padding:5px 8px;font-weight:700}} td{{padding:4.5px 8px;border-bottom:1px solid #dbe4ef}}
tr:nth-child(even) td{{background:#f7f9fc}} blockquote table td{{background:#fff}}
figure{{margin:3mm 0 5mm;page-break-inside:avoid;break-inside:avoid;text-align:center}} figure svg{{width:100%;height:auto}}
figcaption{{font-size:8.6pt;color:#6b7a94;margin-top:1mm}}
</style></head><body>
<section class="cover"><div class="brand">CODE MAN · SYSTEM DESIGN FOR BEGINNERS</div>
<div><div class="brand" style="color:#e3262c;margin-bottom:4mm">EPISODE {NUM} · NOTES</div><h1>{html.escape(TOPIC)}<span>.</span></h1>
<p>{html.escape(blurb)}</p></div>
<div class="toc"><h4>INSIDE</h4><ul>{toc}</ul></div>
<div class="chips">{chip_html}</div></section>
{body}</body></html>"""
out = os.path.join(ROOT, EP, 'notes.html')
open(out, 'w', encoding='utf-8').write(page)
print(out, len(page) // 1024, 'KB')
