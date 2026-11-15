# System Design (Hindi): Notes

Notes for the **System Design (Hindi)** video series by **Code Man**.

The videos explain each topic step by step in Hindi. These notes are the written version: a little deeper, in simple English, with diagrams, worked examples, code and interview questions. Use them to revise after a video or before an interview.

## Episodes

| Ep | Topic | Video | Notes | PDF |
|---|---|---|---|---|
| 1 | IP Address | [Watch](https://youtu.be/SKMoZyz1eAI) | [Read](ep01-ip-address/README.md) | [Download](ep01-ip-address/ep01-ip-address.pdf) |
| 2 | Subnet Mask, Private IP & NAT | [Watch](https://youtu.be/T-njBlfwpW8) (from Tue 17 Nov, 8:00 PM IST) | [Read](ep02-subnet-mask-nat/README.md) | [Download](ep02-subnet-mask-nat/ep02-subnet-mask-nat.pdf) |
| 3 | DNS (Domain Name System) | coming soon | coming with the video | |

More episodes are added as the videos come out. The whole series is in one playlist: [System Design (Hindi) on YouTube](https://www.youtube.com/playlist?list=PLL6fhUZc55nw).

## What every set of notes has

- **In one minute**: the whole topic in a few lines.
- **The topic, built up from the basics**: every term explained the first time it appears, with its full form.
- **Beyond the video**: the parts the video had no time for.
- **Diagrams** you can redraw in an interview.
- **Worked examples** with real numbers, and code you can run.
- **Interview questions**, each with where it comes from. "Reported" means a candidate wrote about it publicly; "Our question" is one we wrote to test the idea.
- **Try it yourself**: small checks you can run on your own phone or laptop.
- **One-page revision** and the **sources** behind every fact.

## How to use them

1. Watch the video first, and answer every question before its 5-second timer runs out.
2. Read the notes the same day.
3. Before an interview, read only "In one minute", the interview questions and the one-page revision.

## Found a mistake?

Open an issue with the episode number and the line. Corrections are welcome.

## Building the PDF

The diagrams are drawn by code, and the PDF is printed from the same Markdown file, so the notes and the PDF never differ. You need Python 3 with the `markdown` package, and Node.js with `playwright-core` and a Chromium (`npm i playwright-core && npx playwright install chromium`). For Ep 1 (for Ep 2, use `diagrams_ep02.py`, the folder `ep02-subnet-mask-nat`, the topic "Subnet Mask, Private IP & NAT" and the number 2):

```bash
python3 tools/diagrams_ep01.py
```

```bash
node tools/check_diagrams.mjs ep01-ip-address/diagrams
```

```bash
python3 tools/build_pdf.py ep01-ip-address "IP Address" 1
```

```bash
node tools/print_pdf.mjs ep01-ip-address/notes.html ep01-ip-address/ep01-ip-address.pdf "Code Man · System Design · Ep 1: IP Address"
```

For the fonts, put `inter.woff2` and `jbm.woff2` (Inter and JetBrains Mono, both free under the SIL Open Font License) in a `fonts/` folder, or set `NOTES_FONTS`; without them a system font is used. The first command draws the diagrams, the second checks that no text runs off a diagram, out of its box or over other text, the third writes `notes.html`, and the fourth prints the PDF.
