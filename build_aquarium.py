#!/usr/bin/env python3
"""Hermes Desktop 用スキン「ascii-aquarium」を生成する。

アスキーアートのクジラ・クラゲ・小魚が泳ぐ海の背景と、マトリックス風の文字の雨。

生き物の絵・数・速さはこのファイルの ART / SCENE を編集して再実行する:
    python3 build_aquarium.py   # ~/.hermes/skins/ascii-aquarium.yaml を書き出す
その後 Hermes Desktop を再起動すると反映される。
customCSS は 32KiB 上限なので、超えたら生き物を減らす（スクリプトが止まる）。
"""
import os
import random
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
HERMES_HOME = Path(os.environ.get("HERMES_HOME") or Path.home() / ".hermes")
SKINS = HERMES_HOME / "skins"
OUT = SKINS / "ascii-aquarium.yaml"

# 配色（ダーク＋マトリックスグリーン）
BG, BG2, FG, SUB, LINE = "#0E1116", "#161A21", "#ECE8DF", "#B9B4A9", "#262B33"
GREEN, GREEN2, CYAN, PINK, GOLD = "#00FF41", "#7DFF9A", "#8CCBFF", "#FF9AD5", "#c9a96e"

ART = {
    # 左向きに泳ぐクジラ（右→左へ移動）
    "whale": [
        "       .  o  .",
        "        \\ | /",
        "    .-''''''''-.      _",
        "  .'  ^      ^  '.__.' )",
        " (   >  \\__/  <      <",
        "  '.__________.-''-._)",
    ],
    "whale_kid": [
        "    . o",
        "  .-'''-.   _",
        " ( ^   ^ )_/ )",
        "  '-.__.-'  <",
    ],
    "jelly": [
        "   .-\"\"\"-.",
        "  /  ^ ^  \\",
        " (    w    )",
        "  '-.___.-'",
        "   ( ) ( )",
        "    ) ( ) (",
        "   (   ) ( )",
        "    )     (",
    ],
    "jelly_s": [
        "  .--.",
        " ( ^^ )",
        "  '--'",
        "  )()(",
        " ( )( )",
    ],
    "octo": [
        "   .---.",
        "  ( ^ ^ )",
        "  (  o  )",
        "  /|/|\\|\\",
        " ~ ~ ~ ~ ~",
    ],
    "fish_l": ["<')))><"],
    "fish_r": ["><(((>"],
    "fish_s": ["<><"],
    "turtle": [
        "    _____     ____",
        "  /      \\  |  o |",
        " |        |/ ___\\|",
        " |_________/",
        " |_|_| |_|_|",
    ],
}

W, H = 1600, 1000  # viewBox。表示は slice で画面いっぱいに伸縮

# (art, x, y, color, opacity, font_px, motion, seconds, delay)
# motion: left=右→左に横断 / right=左→右に横断 / up=下→上へ漂う / bob=その場でゆらゆら
SCENE = [
    ("whale",     0,   560, GREEN,  0.30, 18, "left",  95,   0),
    ("whale",     0,   220, GREEN2, 0.18, 13, "left", 140, -60),
    ("whale_kid", 0,   640, GREEN2, 0.30, 15, "left",  95,  -4),
    ("whale_kid", 0,   820, GREEN,  0.18, 12, "left", 120, -80),
    ("jelly",   180,     0, PINK,   0.26, 15, "up",    70,   0),
    ("jelly",  1180,     0, CYAN,   0.22, 13, "up",    90, -40),
    ("jelly",   760,     0, PINK,   0.16, 11, "up",   110, -75),
    ("jelly_s", 420,     0, CYAN,   0.26, 14, "up",    55, -20),
    ("jelly_s",1420,     0, PINK,   0.24, 13, "up",    65, -50),
    ("jelly_s", 980,     0, GREEN2, 0.20, 12, "up",    80, -10),
    ("octo",   1300,   860, GOLD,   0.26, 14, "bob",    6,   0),
    ("turtle",    0,   380, GREEN2, 0.20, 13, "right",130, -30),
    ("fish_r",    0,   300, CYAN,   0.30, 16, "right", 35,   0),
    ("fish_r",    0,   330, CYAN,   0.24, 13, "right", 35,  -1),
    ("fish_r",    0,   315, CYAN,   0.20, 11, "right", 35,  -2),
    ("fish_l",    0,   470, PINK,   0.26, 15, "left",  45, -15),
    ("fish_l",    0,   740, GREEN2, 0.24, 14, "left",  50, -30),
    ("fish_s",    0,   150, GREEN,  0.28, 14, "right", 28,  -8),
    ("fish_s",    0,   175, GREEN,  0.22, 12, "right", 28,  -9),
    ("fish_s",    0,   900, CYAN,   0.22, 13, "left",  33, -12),
]

BUBBLES = [(x, s, d) for x, s, d in [
    (90, 14, 0), (300, 18, -5), (520, 12, -9), (640, 20, -2), (870, 16, -11),
    (1050, 13, -6), (1240, 19, -3), (1380, 15, -8), (1520, 17, -12), (1120, 22, -15),
]]


def block(name, color, opacity, size):
    lines = ART[name]
    tspans = "".join(
        f'<tspan x="0" dy="{0 if i == 0 else 1.15}em">{escape(line, {chr(34): "&quot;"})}</tspan>'
        for i, line in enumerate(lines)
    )
    return (
        f'<text font-size="{size}" fill="{color}" fill-opacity="{opacity}" '
        f'xml:space="preserve">{tspans}</text>'
    ), max(len(l) for l in lines) * size * 0.6, len(lines) * size * 1.15


def creature(art, x, y, color, opacity, size, motion, secs, delay):
    text, w, h = block(art, color, opacity, size)
    begin = f'begin="{delay}s"'
    if motion in ("left", "right"):
        a, b = (W + 40, -w - 40) if motion == "left" else (-w - 40, W + 40)
        wobble = (
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0 0;0 -12;0 0;0 12;0 0" dur="{max(6, secs // 8)}s" repeatCount="indefinite"/>'
        )
        move = (
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="{a:.0f} {y}" to="{b:.0f} {y}" dur="{secs}s" {begin} repeatCount="indefinite"/>'
        )
        return f"<g>{move}<g>{wobble}{text}</g></g>"
    if motion == "up":
        move = (
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="{x} {H + 40}" to="{x} {-h - 40}" dur="{secs}s" {begin} repeatCount="indefinite"/>'
        )
        sway = (
            f'<animateTransform attributeName="transform" type="translate" additive="sum" '
            f'values="0 0;-18 0;0 0;18 0;0 0" dur="9s" repeatCount="indefinite"/>'
        )
        return f"<g>{move}<g>{sway}{text}</g></g>"
    # bob
    return (
        f'<g transform="translate({x} {y})"><g>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 0;0 -14;0 0" dur="{secs}s" repeatCount="indefinite"/>{text}</g></g>'
    )


def bubbles():
    out = []
    for x, secs, delay in BUBBLES:
        out.append(
            f'<text font-size="14" fill="{GREEN2}" fill-opacity="0.22" xml:space="preserve">'
            f'<tspan x="0">o</tspan><tspan x="8" dy="1.6em">.</tspan><tspan x="-4" dy="1.4em">O</tspan>'
            f'<animateTransform attributeName="transform" type="translate" from="{x} {H + 30}" '
            f'to="{x + 30} -60" dur="{secs}s" begin="{delay}s" repeatCount="indefinite"/></text>'
        )
    return "".join(out)


def ocean():
    """深い海のグラデーション＋水面から差し込む光の筋。"""
    rays = "".join(
        f'<polygon points="{x},-20 {x + w},-20 {x + w * 3 + 260},{H} {x + 160},{H}" '
        f'fill="url(#ray)" opacity="{o}">'
        f'<animate attributeName="opacity" values="{o};{o * 0.35:.3f};{o}" dur="{d}s" repeatCount="indefinite"/>'
        f"</polygon>"
        for x, w, o, d in [(120, 70, 0.55, 11), (520, 40, 0.4, 14), (880, 90, 0.5, 9), (1280, 50, 0.35, 13)]
    )
    return (
        "<defs>"
        '<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#0d3a44"/><stop offset="0.45" stop-color="#0a1f2a"/>'
        f'<stop offset="1" stop-color="{BG}"/></linearGradient>'
        '<linearGradient id="ray" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#9ff6ff" stop-opacity="0.14"/>'
        '<stop offset="1" stop-color="#9ff6ff" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="rain" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>'
        f'<stop offset="0.85" stop-color="{GREEN}" stop-opacity="0.9"/>'
        f'<stop offset="1" stop-color="{GREEN2}" stop-opacity="1"/></linearGradient>'
        "</defs>"
        f'<rect width="{W}" height="{H}" fill="url(#sea)"/>{rays}'
    )


def rain():
    """マトリックス風にアスキー文字がばらばら降ってくる列。"""
    rng = random.Random(20261027)
    glyphs = "01<>{}[]/\\|=+*~^:;.o0Owave"
    cols = []
    for i in range(38):
        x = i * (W / 38) + rng.uniform(-6, 6)
        size = rng.choice([11, 12, 13, 14, 16])
        n = rng.randint(10, 26)
        chars = escape("".join(rng.choice(glyphs) for _ in range(n)))
        length = n * size * 1.1
        secs = rng.randint(9, 26)
        cols.append(
            f'<text x="{x:.0f}" y="0" font-size="{size}" fill="url(#rain)" '
            f'fill-opacity="{rng.uniform(0.10, 0.28):.2f}" '
            f'style="writing-mode:vertical-rl;text-orientation:upright">{chars}'
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="0 {-length:.0f}" to="0 {H + 20}" dur="{secs}s" begin="{-rng.randint(0, secs)}s" '
            f'repeatCount="indefinite"/></text>'
        )
    return "".join(cols)


def svg():
    body = ocean() + rain() + "".join(creature(*c) for c in SCENE) + bubbles()
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'preserveAspectRatio="xMidYMid slice" '
        f'font-family="JetBrains Mono, Menlo, ui-monospace, monospace">{body}</svg>'
    )


CSS = """/* ascii-aquarium — build_aquarium.py で生成（このCSSを直接編集しない） */
:root {{
  --aq-bg: {BG};
  --aq-bg2: {BG2};
  --aq-fg: {FG};
  --aq-acc: {GREEN};
  --aq-acc2: {GREEN2};
}}
[data-chat-surface] {{
  background:
    url("data:image/svg+xml;charset=utf-8,{SVG}") center / cover no-repeat,
    url("{SVG_FILE_URL}") center / cover no-repeat,
    radial-gradient(110% 80% at 90% 10%, rgba(0, 255, 65, 0.10) 0%, transparent 60%),
    radial-gradient(90% 70% at 5% 100%, var(--aq-bg2) 0%, transparent 70%),
    var(--aq-bg) !important;
  color: var(--aq-fg);
}}
[data-chat-surface] [data-slot="composer-bounds"] {{
  background: transparent !important;
}}
[data-chat-surface] a:hover {{
  color: var(--aq-acc2);
}}
"""

HEADER = f"""name: ascii-aquarium
description: ASCII aquarium — whales, jellyfish and matrix rain under the sea
colors:
  background: "{BG}"
  status_bar_bg: "{BG}"
  banner_text: "{FG}"
  banner_title: "{FG}"
  banner_accent: "{GREEN}"
  ui_accent: "{GREEN}"
  response_border: "{GREEN}"
  banner_border: "{LINE}"
  banner_dim: "{SUB}"
customCSS: |
"""


def main():
    # base64 より小さい URL エンコード。属性は ' に寄せ、CSS 側の "..." と衝突させない
    data = svg().replace('"', "'")
    for ch, enc in (("%", "%25"), ("#", "%23"), ("<", "%3C"), (">", "%3E"), ("\\", "%5C")):
        data = data.replace(ch, enc)
    # 同じ SVG を別ファイルにも書き、file:// でも読めるようにする（どちらか効けば表示される）
    svg_file = SKINS / "assets" / "ascii-aquarium" / "aquarium.svg"
    svg_file.parent.mkdir(parents=True, exist_ok=True)
    svg_file.write_text(svg(), encoding="utf-8")
    css = CSS.format(BG=BG, BG2=BG2, FG=FG, GREEN=GREEN, GREEN2=GREEN2, SVG=data,
                     SVG_FILE_URL=svg_file.as_uri())
    if len(css.encode()) > 32768:
        raise SystemExit(f"customCSS が {len(css.encode())} bytes で 32KiB 上限超え。SCENE を減らして")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HEADER + "".join("  " + l + "\n" for l in css.splitlines()), encoding="utf-8")
    print(f"wrote {OUT} (customCSS {len(css.encode())} bytes)")


if __name__ == "__main__":
    main()
