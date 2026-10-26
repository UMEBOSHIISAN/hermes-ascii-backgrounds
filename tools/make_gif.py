#!/usr/bin/env python3
"""Render an animated GIF of a theme for the README (optional, for maintainers).

    python3 tools/make_gif.py cosmos          # -> previews/cosmos.gif
    python3 tools/make_gif.py --all

Needs Google Chrome (headless) and ffmpeg. Builds the theme's SVG into a temp
HERMES_HOME first, so your real ~/.hermes is never touched.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
W, H = 800, 500
FRAMES, STEP = 48, 0.35   # 48 frames, 0.35 s of animation apart (~17 s of motion)
FPS = 12                  # played back faster than real time so the GIF feels lively

PAGE = """<!doctype html><html><body style="margin:0;background:#000;overflow:hidden">
<div style="width:{w}px;height:{h}px">{svg}</div>
<script>
  const s = document.querySelector('svg');
  s.setAttribute('width', '{w}'); s.setAttribute('height', '{h}');
  s.pauseAnimations(); s.setCurrentTime({t});
</script></body></html>"""


def render(name, out_dir):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        env = dict(os.environ, HERMES_HOME=str(tmp / "home"))
        subprocess.run([sys.executable, str(ROOT / "build.py"), name], check=True, env=env,
                       capture_output=True)
        svg = (tmp / "home" / "skins" / "assets" / name / "background.svg").read_text(encoding="utf-8")
        frames = tmp / "frames"
        frames.mkdir()
        for i in range(FRAMES):
            page = tmp / f"f{i}.html"
            page.write_text(PAGE.format(w=W, h=H, svg=svg, t=20 + i * STEP), encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            f"--window-size={W},{H}", "--virtual-time-budget=500",
                            f"--screenshot={frames / f'{i:03d}.png'}", page.as_uri()],
                           check=True, capture_output=True)
        out = out_dir / f"{name}.gif"
        vf = f"fps={FPS},split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse=dither=bayer:bayer_scale=4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                        "-i", str(frames / "%03d.png"), "-vf", vf, "-loop", "0", str(out)], check=True)
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("theme", nargs="?")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    if not Path(CHROME).exists() or not shutil.which("ffmpeg"):
        sys.exit("Needs Google Chrome (set $CHROME to its binary) and ffmpeg.")
    names = sorted(p.stem.replace("_", "-") for p in (ROOT / "themes").glob("*.py")
                   if not p.stem.startswith("_")) if args.all else [args.theme]
    out_dir = ROOT / "previews"
    out_dir.mkdir(exist_ok=True)
    for name in names:
        out = render(name, out_dir)
        print(f"wrote {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
