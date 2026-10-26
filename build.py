#!/usr/bin/env python3
"""Build animated ASCII-art background skins for Hermes Desktop.

    python3 build.py                 # list themes
    python3 build.py aquarium        # write ~/.hermes/skins/aquarium.yaml
    python3 build.py --all           # write every theme
    python3 build.py --all --previews  # also refresh previews/*.png (macOS)

Each theme is one file in themes/. Copy one to make your own.
Standard library only. Respects $HERMES_HOME.
"""
import argparse
import importlib.util
import os
import random
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
THEMES = ROOT / "themes"
W, H = 1600, 1000  # SVG viewBox; scaled with "slice" to fill the chat area
CSS_CAP = 32768    # Hermes caps a skin's customCSS at 32 KiB


# ── SVG pieces ──────────────────────────────────────────────────────────────

def art_text(lines, color, opacity, size):
    tspans = "".join(
        f'<tspan x="0" dy="{0 if i == 0 else 1.15}em">{escape(line, {chr(34): "&quot;"})}</tspan>'
        for i, line in enumerate(lines)
    )
    width = max(len(l) for l in lines) * size * 0.6
    height = len(lines) * size * 1.15
    text = (f'<text font-size="{size}" fill="{color}" fill-opacity="{opacity}" '
            f'xml:space="preserve">{tspans}</text>')
    return text, width, height


def translate(frm, to, secs, delay=0):
    return (f'<animateTransform attributeName="transform" type="translate" from="{frm}" to="{to}" '
            f'dur="{secs}s" begin="{delay}s" repeatCount="indefinite"/>')


def wobble(values, secs):
    return (f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="{values}" dur="{secs}s" repeatCount="indefinite"/>')


def creature(art, lines, x, y, color, opacity, size, motion, secs, delay=0):
    text, w, h = art_text(lines, color, opacity, size)
    if motion in ("left", "right"):
        # x shifts the whole path, so parts of one creature (e.g. a rainbow trail) can travel together
        a, b = (W + 40 + x, -w - 40 + x) if motion == "left" else (-w - 40 + x, W + 40 + x)
        bob = wobble("0 0;0 -12;0 0;0 12;0 0", max(6, secs // 8))
        return f'<g>{translate(f"{a:.0f} {y}", f"{b:.0f} {y}", secs, delay)}<g>{bob}{text}</g></g>'
    if motion in ("up", "down"):
        a, b = (H + 40, -h - 40) if motion == "up" else (-h - 40, H + 40)
        sway = wobble("0 0;-18 0;0 0;18 0;0 0", 9)
        return f'<g>{translate(f"{x} {a:.0f}", f"{x} {b:.0f}", secs, delay)}<g>{sway}{text}</g></g>'
    if motion == "fly":  # diagonal streak, e.g. a shooting star
        return f'<g>{translate(f"{x} {y}", f"{x - 900} {y + 520}", secs, delay)}{text}</g>'
    # "bob": stays put and gently floats
    return (f'<g transform="translate({x} {y})"><g>'
            f'{wobble("0 0;0 -14;0 0", secs)}{text}</g></g>')


def backdrop(stops, rays):
    grad = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    out = (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">{grad}</linearGradient>'
           f'<linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="{rays or "#ffffff"}" stop-opacity="0.14"/>'
           f'<stop offset="1" stop-color="{rays or "#ffffff"}" stop-opacity="0"/></linearGradient></defs>'
           f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    if rays:
        for x, w, o, d in [(120, 70, 0.55, 11), (520, 40, 0.4, 14), (880, 90, 0.5, 9), (1280, 50, 0.35, 13)]:
            out += (f'<polygon points="{x},-20 {x + w},-20 {x + w * 3 + 260},{H} {x + 160},{H}" '
                    f'fill="url(#ray)" opacity="{o}"><animate attributeName="opacity" '
                    f'values="{o};{o * 0.35:.3f};{o}" dur="{d}s" repeatCount="indefinite"/></polygon>')
    return out


def rain(cfg, seed):
    """Matrix-style columns of glyphs falling top to bottom."""
    if not cfg:
        return ""
    rng = random.Random(seed)
    out = []
    n = cfg["columns"]
    for i in range(n):
        x = i * (W / n) + rng.uniform(-6, 6)
        size = rng.choice([11, 12, 13, 14, 16])
        count = rng.randint(10, 26)
        chars = escape("".join(rng.choice(cfg["glyphs"]) for _ in range(count)))
        secs = rng.randint(9, 26)
        out.append(
            f'<text x="{x:.0f}" y="0" font-size="{size}" fill="{cfg["color"]}" '
            f'fill-opacity="{rng.uniform(0.10, 0.28):.2f}" '
            f'style="writing-mode:vertical-rl;text-orientation:upright">{chars}'
            f'{translate(f"0 {-count * size * 1.1:.0f}", f"0 {H + 20}", secs, -rng.randint(0, secs))}</text>')
    return "".join(out)


def particles(cfg, seed):
    """Loose glyphs drifting up or down (bubbles, snow, petals...)."""
    if not cfg:
        return ""
    rng = random.Random(seed + 1)
    out = []
    for _ in range(cfg["count"]):
        x = rng.uniform(0, W)
        glyph = escape(rng.choice(cfg["glyphs"]))
        color = rng.choice(cfg["colors"])
        size = rng.randint(*cfg["size"])
        secs = rng.randint(*cfg["secs"])
        drift = rng.uniform(-cfg.get("drift", 40), cfg.get("drift", 40))
        a, b = (H + 30, -40) if cfg["dir"] == "up" else (-40, H + 30)
        out.append(
            f'<text font-size="{size}" fill="{color}" fill-opacity="{rng.uniform(*cfg["opacity"]):.2f}">'
            f'{glyph}{translate(f"{x:.0f} {a}", f"{x + drift:.0f} {b}", secs, -rng.randint(0, secs))}</text>')
    return "".join(out)


def twinkles(cfg, seed):
    """Fixed glyphs that fade in and out (stars, fireflies)."""
    if not cfg:
        return ""
    rng = random.Random(seed + 2)
    out = []
    for _ in range(cfg["count"]):
        x, y = rng.uniform(0, W), rng.uniform(0, H * cfg.get("max_y", 1.0))
        o = rng.uniform(*cfg["opacity"])
        out.append(
            f'<text x="{x:.0f}" y="{y:.0f}" font-size="{rng.randint(*cfg["size"])}" '
            f'fill="{rng.choice(cfg["colors"])}" fill-opacity="{o:.2f}">{escape(rng.choice(cfg["glyphs"]))}'
            f'<animate attributeName="fill-opacity" values="{o:.2f};0.02;{o:.2f}" '
            f'dur="{rng.randint(3, 8)}s" begin="{-rng.randint(0, 8)}s" repeatCount="indefinite"/></text>')
    return "".join(out)


def build_svg(t):
    seed = sum(map(ord, t.NAME))
    body = (backdrop(t.BACKDROP, getattr(t, "RAYS", None))
            + twinkles(getattr(t, "TWINKLES", None), seed)
            + rain(getattr(t, "RAIN", None), seed)
            + "".join(creature(c[0], t.ART[c[0]], *c[1:]) for c in t.SCENE)
            + particles(getattr(t, "PARTICLES", None), seed))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'preserveAspectRatio="xMidYMid slice" '
            f'font-family="JetBrains Mono, Menlo, ui-monospace, monospace">{body}</svg>')


# ── skin YAML ───────────────────────────────────────────────────────────────

def data_url(svg):
    # URL-encode instead of base64 (smaller). A backslash in a CSS string is an
    # escape character, so it MUST be encoded or the image silently breaks.
    data = svg.replace('"', "'")
    for ch, enc in (("%", "%25"), ("#", "%23"), ("<", "%3C"), (">", "%3E"), ("\\", "%5C")):
        data = data.replace(ch, enc)
    return "data:image/svg+xml;charset=utf-8," + data


def build_skin(t, skins_dir):
    p = t.PALETTE
    svg = build_svg(t)
    svg_file = skins_dir / "assets" / t.NAME / "background.svg"
    svg_file.parent.mkdir(parents=True, exist_ok=True)
    svg_file.write_text(svg, encoding="utf-8")
    css = f"""/* {t.NAME} — generated by hermes-desktop-backgrounds/build.py (do not edit by hand) */
[data-chat-surface] {{
  background:
    url("{data_url(svg)}") center / cover no-repeat,
    url("{svg_file.as_uri()}") center / cover no-repeat,
    {p["bg"]} !important;
  color: {p["fg"]};
}}
[data-chat-surface] [data-slot="composer-bounds"] {{
  background: transparent !important;
}}
[data-chat-surface] a:hover {{
  color: {p["accent2"]};
}}
"""
    size = len(css.encode())
    if size > CSS_CAP:
        raise SystemExit(f"{t.NAME}: customCSS is {size} bytes (cap {CSS_CAP}). Trim SCENE / RAIN / PARTICLES.")
    head = f"""name: {t.NAME}
description: {t.DESCRIPTION}
colors:
  background: "{p["bg"]}"
  status_bar_bg: "{p["bg"]}"
  banner_text: "{p["fg"]}"
  banner_title: "{p["fg"]}"
  banner_accent: "{p["accent"]}"
  ui_accent: "{p["accent"]}"
  response_border: "{p["accent"]}"
  banner_border: "{p["line"]}"
  banner_dim: "{p["dim"]}"
customCSS: |
"""
    out = skins_dir / f"{t.NAME}.yaml"
    out.write_text(head + "".join("  " + l + "\n" for l in css.splitlines()), encoding="utf-8")
    return out, size, svg_file


def load_themes():
    themes = {}
    for f in sorted(THEMES.glob("*.py")):
        if f.name.startswith("_"):  # _template.py etc.
            continue
        spec = importlib.util.spec_from_file_location(f"theme_{f.stem}", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        themes[mod.NAME] = mod
    return themes


def preview(svg_file, dest):
    """Static snapshot via macOS Quick Look (frame 0 of the animation)."""
    with tempfile.TemporaryDirectory() as tmp:
        # Quick Look renders a square thumbnail; "meet" fits the whole 16:10 scene, then crop it out.
        src = Path(tmp) / "preview.svg"
        src.write_text(svg_file.read_text(encoding="utf-8").replace("xMidYMid slice", "xMidYMid meet"),
                       encoding="utf-8")
        subprocess.run(["qlmanage", "-t", "-s", "1200", "-o", tmp, str(src)], check=True, capture_output=True)
        png = Path(tmp) / "preview.svg.png"
        subprocess.run(["sips", "--cropToHeightWidth", "750", "1200", str(png)], check=True, capture_output=True)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(png.read_bytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("theme", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--previews", action="store_true", help="refresh previews/*.png (macOS only)")
    args = ap.parse_args()

    themes = load_themes()
    if not args.theme and not args.all:
        for name, t in themes.items():
            print(f"  {name:14} {t.DESCRIPTION}")
        print("\nUsage: python3 build.py <theme>   (then: hermes config set display.skin <theme>)")
        return
    picked = list(themes) if args.all else [args.theme]
    if args.theme and args.theme not in themes:
        sys.exit(f"Unknown theme '{args.theme}'. Available: {', '.join(themes)}")

    skins = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes") / "skins"
    skins.mkdir(parents=True, exist_ok=True)
    for name in picked:
        out, size, svg_file = build_skin(themes[name], skins)
        print(f"wrote {out}  (customCSS {size} bytes)")
        if args.previews:
            preview(svg_file, ROOT / "previews" / f"{name}.png")
    if len(picked) == 1:
        print(f"\nNext: hermes config set display.skin {picked[0]}   then restart Hermes Desktop")


if __name__ == "__main__":
    main()
