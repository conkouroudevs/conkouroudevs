"""Builds the profile README images into assets/.

Static art is drawn here; the Lab notes plate reads design/contributions.json,
which the lab-notes workflow refreshes daily. Standard library only.
"""
import base64
import datetime
import json
import pathlib
import textwrap

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
INK, PAPER, MUTED, ACC = "#14213d", "#f3efe3", "#55607a", "#c2410c"

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


def card(name, w, h, body, fonts, margin=False):
    """Paper card: graph grid, ink border, hard shadow. Written to assets/<name>.svg."""
    line = f'<path d="M44 2V{h - 2}" stroke="#d9908a" stroke-width="2"/>' if margin else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 6} {h + 6}" width="{w + 6}" height="{h + 6}">'
           f'<style>{font_css(fonts)}</style>'
           '<defs><pattern id="g" width="28" height="28" patternUnits="userSpaceOnUse">'
           f'<path d="M28 0H0V28" fill="none" stroke="{INK}" stroke-opacity=".07"/></pattern></defs>'
           f'<rect x="6" y="6" width="{w}" height="{h}" fill="{INK}"/>'
           f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="{PAPER}"/>'
           f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="url(#g)"/>'
           f'{line}{body}'
           f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="none" stroke="{INK}" stroke-width="2"/>'
           '</svg>')
    OUT.mkdir(exist_ok=True)
    (OUT / f"{name}.svg").write_text(svg, encoding="utf-8")


def heading(n, title, note=None):
    out = T(26, 38, f"ENTRY {n}", "mo", 12, ACC, extra='letter-spacing="1.4"')
    out += T(112, 42, title, "fr", 30, INK)
    if note:
        out += T(112 + 18 * len(title) + 14, 40, note, "ca", 24, MUTED)
    return out


def button(name, label, w, filled):
    fill, fg = (INK, PAPER) if filled else (PAPER, INK)
    shadow = f'<rect x="4" y="4" width="{w}" height="46" fill="{ACC}"/>' if filled else ""
    OUT.joinpath(f"{name}.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 4} 50" width="{w + 4}" height="50">'
        f'<style>{font_css(["i6"])}</style>{shadow}'
        f'<rect x="1" y="1" width="{w - 2}" height="44" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        f'{T(w / 2, 29, label, "i6", 15, fg, "middle")}</svg>', encoding="utf-8")


def hero():
    b = T(68, 54, "ENTRY 01 · FULL-STACK DEVELOPER · IGAMING · NICOSIA, CYPRUS", "mo", 11.5, MUTED, extra='letter-spacing="1.3"')
    b += T(68, 122, "From chemical engineering", "fr", 46, INK)
    b += T(68, 176, "to production software.", "fr", 46, INK)
    b += ('<g transform="rotate(-1.5 68 250)">' + T(68, 246, "the mindset carried over.", "ca", 46, ACC) +
          f'<path d="M68 258 C100 251,125 265,160 257 S225 251,260 258 S330 264,365 256 S410 252,520 258" '
          f'fill="none" stroke="{ACC}" stroke-width="2.5" stroke-linecap="round"/></g>')
    b += ('<g transform="rotate(7 680 236)">'
          f'<rect x="602" y="206" width="156" height="60" fill="{PAPER}" stroke="{ACC}" stroke-width="3"/>'
          f'<rect x="607" y="211" width="146" height="50" fill="none" stroke="{ACC}" stroke-width="1"/>' +
          T(680, 232, "OPEN TO ROLES", "mo", 11.5, ACC, "middle", 'letter-spacing="1"') +
          T(680, 250, "EU / UK · REMOTE", "mo", 11.5, ACC, "middle", 'letter-spacing="1"') + "</g>")
    card("hero", 794, 300, b, ["fr", "ca", "mo"], margin=True)


def about():
    paras = [
        "Full-stack developer with 3+ years shipping production software for enterprise SaaS and the iGaming industry: Python backends (Django, FastAPI, Flask), Java services and modern JavaScript frontends, on PostgreSQL, MySQL and MongoDB.",
        "I started in engineering (MSc Biological & Bioprocess Engineering, University of Sheffield; BEng Chemical Engineering, Lancaster University), building computational models and optimising complex systems. I bring the same approach to software: understand the problem, design it properly, then build it.",
        "I work across the full stack, from APIs and backend services to web and mobile frontends, with Django, FastAPI, Next.js and Flutter.",
    ]
    b = T(68, 38, "ENTRY 02", "mo", 12, ACC, extra='letter-spacing="1.4"') + T(160, 42, "About me", "fr", 30, INK)
    y = 92
    for p in paras:
        for line in textwrap.wrap(p, 88):
            b += T(68, y, line, "i4", 16, INK)
            y += 25
        y += 12
    b += T(68, y + 6, "OPEN TO FRONT-END OR FULL-STACK ROLES · EU / UK · REMOTE-FRIENDLY", "mo", 11.5, ACC, extra='letter-spacing="1"')
    card("about", 794, y + 36, b, ["fr", "mo", "i4"], margin=True)


def reaction():
    def box(x, w, label, title, lines, hot=False):
        s = f'<rect x="{x + 5}" y="29" width="{w}" height="112" fill="{ACC}"/>' if hot else ""
        s += f'<rect x="{x}" y="24" width="{w}" height="112" fill="{PAPER}" stroke="{ACC if hot else INK}" stroke-width="2"/>'
        s += T(x + 16, 50, label, "mo", 10, MUTED, extra='letter-spacing="1.2"') + T(x + 16, 82, title, "fr", 21, INK)
        for i, ln in enumerate(lines):
            s += T(x + 16, 104 + 17 * i, ln, "i4", 11.5, MUTED)
        return s
    b = box(22, 180, "REACTANT A", "Engineering", ["MSc Bioprocess, Sheffield", "BEng Chemical, Lancaster"])
    b += T(221, 88, "+", "fr", 36, INK, "middle")
    b += box(240, 180, "REACTANT B", "Software", ["Python, Java,", "JavaScript, Flutter"])
    b += T(468, 70, "3+ years", "ca", 26, ACC, "middle")
    b += f'<path d="M432 86H500M492 80L502 86L492 92" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    b += box(516, 256, "PRODUCT", "Production systems", ["Enterprise SaaS and iGaming"], hot=True)
    card("reaction", 794, 166, b, ["fr", "ca", "mo", "i4"])


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
        b += T(26, y, label, "mo", 11, MUTED, extra='letter-spacing="1.4"')
        for i, (sym, name) in enumerate(tiles):
            x, ty = 26 + i * 94, y + 12
            b += (f'<rect x="{x}" y="{ty}" width="84" height="96" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
                  f'<rect x="{x}" y="{ty}" width="84" height="8" fill="{color}"/>' +
                  T(x + 8, ty + 26, f"{n:02d}", "mo", 10, MUTED) + T(x + 42, ty + 62, sym, "fr", 30, INK, "middle") +
                  T(x + 42, ty + 84, name, "i6", 10.5, INK, "middle"))
            n += 1
        y += 140
    card("stack", 794, 490, b, ["fr", "ca", "mo", "i6"])


def lab_notes():
    days = json.loads((ROOT / "design/contributions.json").read_text())["days"]
    cols = -(-len(days) // 7)
    level = lambda c: 0 if c == 0 else 1 if c <= 2 else 2 if c <= 5 else 3 if c <= 10 else 4
    fill = ["none", "#c3cfe8", "#8da2d0", "#4a68a8", INK]
    ring = ["#bdb6a0", "#9fb0d4", "#6f87bd", "#2c4a8f", INK]
    x0, top, pitch, r = 42, 94, (794 - 52 - 16) / cols, 5.2
    best = max(range(len(days)), key=lambda i: days[i][1])
    b = heading("04", "Lab notes", "(contributions, last 12 months)")
    for d, ch in enumerate("ABCDEFG"):
        b += T(26, top + d * pitch + pitch / 2 + 3, ch, "mo", 9, MUTED)
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
    b += T(26, 232, "one well = one day. darker = more work.", "ca", 24, ACC)
    b += T(600, 227, "less", "mo", 10, MUTED, "end") + T(710, 227, "more", "mo", 10, MUTED)
    for i in range(5):
        b += f'<circle cx="{616 + i * 20}" cy="224" r="6" fill="{fill[i]}" stroke="{ring[i]}" stroke-width="1.2"/>'
    card("lab-notes", 794, 252, b, ["fr", "ca", "mo"])


if __name__ == "__main__":
    hero()
    about()
    reaction()
    stack()
    lab_notes()
    button("btn-linkedin", "LinkedIn", 128, True)
    button("btn-email", "Email me", 120, False)
