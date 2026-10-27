# Changelog 🐾

## v0.1.0 — 2026-10-27 · First release

The first collection of animated ASCII-art backgrounds for Hermes Desktop.

### 🎨 Themes
- 🐋 **aquarium** — whales, jellyfish, an octopus, a turtle and fish in the deep sea, under matrix-green ASCII rain and light rays
- 🐱 **nyan** — a rainbow nyan cat, a cat chasing a mouse, a cat in a box, napping cats, yarn, paw prints and "nya~" bubbles
- 🚀 **cosmos** — Saturn, a drifting astronaut, a UFO and an alien, comets, rockets and a space cat in a helmet
- 🌙 **starry-night** — twinkling stars, shooting stars, the moon, a planet, a rocket, a sleepy cat and owls

### ✨ Features
- `build.py` turns a theme into a Hermes skin (`~/.hermes/skins/<name>.yaml`) — Python stdlib only, respects `$HERMES_HOME`
- One small file per theme in `themes/`, plus `themes/_template.py` to start your own
- Motions: `left` / `right`, `up` / `down`, `bob`, `fly`; layers: twinkles, particles, matrix rain, light rays
- `tools/make_gif.py` renders README GIFs with headless Chrome + ffmpeg
- No changes to Hermes itself — uses the skin `customCSS` field

### 📝 Notes
- Backslashes in the embedded SVG are encoded as `%5C`; without this the background silently fails to load
- Hermes caps `customCSS` at 32 KiB; `build.py` stops with a message if a theme is too big
- If colors look tinted, set Translucency to 0 in Hermes' Appearance settings (the wallpaper shows through)

### History
- Started as a single-theme repo, `hermes-ascii-aquarium` (old URL redirects here)
