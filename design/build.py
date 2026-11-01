"""Builds the profile README images into assets/.

The whole notebook is one SVG (assets/page.svg) so GitHub's page background never
shows between sections. The Lab notes plate reads design/contributions.json, which
the lab-notes workflow refreshes daily. Standard library only.
"""
import base64
import datetime
import json
import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
INK, PAPER, MUTED, ACC = "#14213d", "#f3efe3", "#55607a", "#c2410c"
W, X = 794, 68  # page width, left edge of content (right of the margin line)

FACES = {  # key: (family, weight, file)
    "fr": ("Fraunces", 700, "Fraunces-700"),
    "ca": ("Caveat", 600, "Caveat-600"),
    "mo": ("JetBrains Mono", 500, "JetBrainsMono-500"),
    "i4": ("Inter", 400, "Inter-400"),
    "i6": ("Inter", 600, "Inter-600"),
}
STACKS = {
    "fr": "Fraunces, Georgia, serif",
    "ca": "Caveat, cursive",
    "mo": "'JetBrains Mono', monospace",
    "i4": "Inter, Arial, sans-serif",
    "i6": "Inter, Arial, sans-serif",
}
PARAS = [
    "Full-stack developer with 3+ years shipping production software for enterprise SaaS and the iGaming industry: Python backends (Django, FastAPI, Flask), Java services and modern JavaScript frontends, on PostgreSQL, MySQL and MongoDB.",
    "I started in engineering (MSc Biological & Bioprocess Engineering, University of Sheffield; BEng Chemical Engineering, Lancaster University), building computational models and optimising complex systems. I bring the same approach to software: understand the problem, design it properly, then build it.",
    "I work across the full stack, from APIs and backend services to web and mobile frontends, with Django, FastAPI, Next.js and Flutter.",
]


def font_css(keys):
    css = ""
    for k in keys:
        fam, wt, f = FACES[k]
        b64 = base64.b64encode((ROOT / "design/fonts" / f"{f}.woff2").read_bytes()).decode()
        css += f"@font-face{{font-family:'{fam}';font-weight:{wt};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
    return css


def T(x, y, s, font, size, fill, anchor="start", extra=""):
    s = s.replace("&", "&amp;")
    return (f'<text x="{x}" y="{y}" font-family="{STACKS[font]}" font-weight="{FACES[font][1]}" '
            f'font-size="{size}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')


def heading(n, title, note=None):
    out = T(X, 38, f"ENTRY {n}", "mo", 12, ACC, extra='letter-spacing="1.4"')
    out += T(X + 88, 42, title, "fr", 30, INK)
    if note:
        out += T(X + 88 + 17 * len(title) + 16, 40, note, "ca", 24, MUTED)
    return out


def hero():
    b = T(X, 54, "ENTRY 01 · FULL-STACK DEVELOPER · IGAMING · NICOSIA, CYPRUS", "mo", 11.5, MUTED, extra='letter-spacing="1.3"')
    b += T(X, 122, "From chemical engineering", "fr", 46, INK)
    b += T(X, 176, "to production software.", "fr", 46, INK)
    b += ('<g transform="rotate(-1.5 68 250)">' + T(X, 246, "the mindset carried over.", "ca", 46, ACC) +
          f'<path d="M68 258 C100 251,125 265,160 257 S225 251,260 258 S330 264,365 256 S410 252,520 258" '
          f'fill="none" stroke="{ACC}" stroke-width="2.5" stroke-linecap="round"/></g>')
    b += ('<g transform="rotate(7 680 236)">'
          f'<rect x="602" y="206" width="156" height="60" fill="{PAPER}" stroke="{ACC}" stroke-width="3"/>'
          f'<rect x="607" y="211" width="146" height="50" fill="none" stroke="{ACC}" stroke-width="1"/>' +
          T(680, 232, "OPEN TO ROLES", "mo", 11.5, ACC, "middle", 'letter-spacing="1"') +
          T(680, 250, "EU / UK · REMOTE", "mo", 11.5, ACC, "middle", 'letter-spacing="1"') + "</g>")
    return b, 300


def about():
    b = heading("02", "About me")
    y = 92
    for p in PARAS:
        for line in textwrap.wrap(p, 88):
            b += T(X, y, line, "i4", 16, INK)
            y += 25
        y += 12
    b += T(X, y + 6, "OPEN TO FRONT-END OR FULL-STACK ROLES · EU / UK · REMOTE-FRIENDLY", "mo", 11.5, ACC, extra='letter-spacing="1"')
    return b, y + 36


def reaction():
    def box(x, w, label, title, lines, hot=False):
        s = f'<rect x="{x + 5}" y="29" width="{w}" height="104" fill="{ACC}"/>' if hot else ""
        s += f'<rect x="{x}" y="24" width="{w}" height="104" fill="{PAPER}" stroke="{ACC if hot else INK}" stroke-width="2"/>'
        s += T(x + 14, 48, label, "mo", 10, MUTED, extra='letter-spacing="1.2"') + T(x + 14, 78, title, "fr", 19, INK)
        for i, ln in enumerate(lines):
            s += T(x + 14, 100 + 16 * i, ln, "i4", 11.5, MUTED)
        return s
    b = box(X, 150, "REACTANT A", "Engineering", ["MSc Bioprocess", "BEng Chemical"])
    b += T(X + 168, 86, "+", "fr", 34, INK, "middle")
    b += box(X + 186, 150, "REACTANT B", "Software", ["Python, Java,", "JavaScript, Flutter"])
    b += T(X + 376, 66, "3+ years", "ca", 24, ACC, "middle")
    b += f'<path d="M{X + 344} 84H{X + 408}M{X + 400} 78L{X + 410} 84L{X + 400} 90" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    b += box(X + 428, 266, "PRODUCT", "Production systems", ["Enterprise SaaS and iGaming"], hot=True)
    return b, 156


def stack():
    groups = [
        ("FRONTEND & MOBILE", INK, [("Nx", "Next.js"), ("Re", "React"), ("Ts", "TypeScript"), ("Js", "JavaScript"),
                                    ("Fl", "Flutter"), ("Da", "Dart"), ("Ht", "HTML5"), ("Cs", "CSS3")]),
        ("BACKEND & DATA", "#0f766e", [("Py", "Python"), ("Dj", "Django"), ("Fa", "FastAPI"), ("Fk", "Flask"),
                                       ("Jv", "Java"), ("Pg", "PostgreSQL"), ("My", "MySQL"), ("Mo", "MongoDB")]),
        ("TOOLS", ACC, [("Gi", "Git"), ("Dk", "Docker"), ("Lx", "Linux")]),
    ]
    b, n, y = heading("03", "Reagents", "(the tech stack)"), 1, 76
    for label, color, tiles in groups:
        b += T(X, y, label, "mo", 11, MUTED, extra='letter-spacing="1.4"')
        for i, (sym, name) in enumerate(tiles):
            x, ty = X + i * 87.5, y + 12
            b += (f'<rect x="{x}" y="{ty}" width="78" height="92" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
                  f'<rect x="{x}" y="{ty}" width="78" height="8" fill="{color}"/>' +
                  T(x + 8, ty + 25, f"{n:02d}", "mo", 10, MUTED) + T(x + 39, ty + 60, sym, "fr", 29, INK, "middle") +
                  T(x + 39, ty + 81, name, "i6", 10, INK, "middle"))
            n += 1
        y += 136
    return b, 466


def lab_notes():
    days = json.loads((ROOT / "design/contributions.json").read_text())["days"]
    cols = -(-len(days) // 7)
    level = lambda c: 0 if c == 0 else 1 if c <= 2 else 2 if c <= 5 else 3 if c <= 10 else 4
    fill = ["none", "#c3cfe8", "#8da2d0", "#4a68a8", INK]
    ring = ["#bdb6a0", "#9fb0d4", "#6f87bd", "#2c4a8f", INK]
    x0, top, pitch, r = X + 16, 94, (W - 26 - X - 16) / cols, 4.8
    best = max(range(len(days)), key=lambda i: days[i][1])
    b = heading("04", "Lab notes", "(contributions, last 12 months)")
    for d, ch in enumerate("ABCDEFG"):
        b += T(X, top + d * pitch + pitch / 2 + 3, ch, "mo", 9, MUTED)
    last = datetime.date.fromisoformat(days[0][0]).month
    for w in range(1, cols):
        dt = datetime.date.fromisoformat(days[w * 7][0])
        if dt.month != last:
            b += T(x0 + w * pitch, 84, dt.strftime("%b"), "mo", 11, MUTED)
            last = dt.month
    for i, (date, c) in enumerate(days):
        cx, cy = x0 + (i // 7) * pitch + pitch / 2, top + (i % 7) * pitch + pitch / 2
        b += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill[level(c)]}" stroke="{ring[level(c)]}" stroke-width="1.2"><title>{c} contributions, {date}</title></circle>'
        if i == best:
            b += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r + 3}" fill="none" stroke="{ACC}" stroke-width="2"/>'
    b += T(X, 232, "one well = one day. darker = more work.", "ca", 24, ACC)
    b += T(590, 227, "less", "mo", 10, MUTED, "end") + T(700, 227, "more", "mo", 10, MUTED)
    for i in range(5):
        b += f'<circle cx="{606 + i * 20}" cy="224" r="6" fill="{fill[i]}" stroke="{ring[i]}" stroke-width="1.2"/>'
    return b, 256


def page():
    body, y = "", 0
    for i, section in enumerate((hero, about, reaction, stack, lab_notes)):
        b, h = section()
        if i:
            body += f'<path d="M1 {y}H{W - 1}" stroke="{INK}" stroke-width="2"/>'
        body += f'<g transform="translate(0 {y})">{b}</g>'
        y += h
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W + 6} {y + 6}" width="{W + 6}" height="{y + 6}">'
           f'<style>{font_css(list(FACES))}</style>'
           '<defs><pattern id="g" width="28" height="28" patternUnits="userSpaceOnUse">'
           f'<path d="M28 0H0V28" fill="none" stroke="{INK}" stroke-opacity=".07"/></pattern></defs>'
           f'<rect x="6" y="6" width="{W}" height="{y}" fill="{INK}"/>'
           f'<rect x="1" y="1" width="{W - 2}" height="{y - 2}" fill="{PAPER}"/>'
           f'<rect x="1" y="1" width="{W - 2}" height="{y - 2}" fill="url(#g)"/>'
           f'<path d="M44 2V{y - 2}" stroke="#d9908a" stroke-width="2"/>'
           f'{body}'
           f'<rect x="1" y="1" width="{W - 2}" height="{y - 2}" fill="none" stroke="{INK}" stroke-width="2"/>'
           '</svg>')
    OUT.mkdir(exist_ok=True)
    (OUT / "page.svg").write_text(svg, encoding="utf-8")


def button(name, label, w, filled):
    fill, fg = (INK, PAPER) if filled else (PAPER, INK)
    shadow = f'<rect x="4" y="4" width="{w}" height="46" fill="{ACC}"/>' if filled else ""
    (OUT / f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 4} 50" width="{w + 4}" height="50">'
        f'<style>{font_css(["i6"])}</style>{shadow}'
        f'<rect x="1" y="1" width="{w - 2}" height="44" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        f'{T(w / 2, 29, label, "i6", 15, fg, "middle")}</svg>', encoding="utf-8")


if __name__ == "__main__":
    page()
    button("btn-linkedin", "LinkedIn", 128, True)
    button("btn-email", "Email me", 120, False)
