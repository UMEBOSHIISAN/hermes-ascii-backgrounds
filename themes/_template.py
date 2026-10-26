# Copy this file to themes/<your_theme>.py, rename NAME, and draw!
#   python3 build.py <your-theme>            # try it in Hermes
#   python3 tools/make_gif.py <your-theme>   # make previews/<your-theme>.gif for the README
# Files starting with "_" are ignored, so this template never shows up as a theme.

NAME = "my-theme"                       # skin name: hermes config set display.skin my-theme
DESCRIPTION = "One cute line about your theme"

# Chat colors. Keep fg readable on bg (high contrast); accent is used for links.
PALETTE = {"bg": "#101018", "fg": "#EEEAF4", "accent": "#FF9EC4", "accent2": "#FFD0E2",
           "line": "#262433", "dim": "#B0AABF"}
PINK, CREAM, MINT = "#FF9EC4", "#FFF1E0", "#9EF0D0"

# Background gradient, top -> bottom: (offset 0..1, color)
BACKDROP = [(0, "#2a1d33"), (1, "#101018")]

# Optional layers — delete any you don't want.
# RAYS = "#9ff6ff"                       # light shafts from above
# RAIN = {"columns": 30, "glyphs": "01<>*+", "color": MINT}   # matrix-style falling columns
TWINKLES = {"count": 40, "glyphs": ["*", ".", "+"], "colors": [CREAM, PINK],
            "size": (8, 14), "opacity": (0.2, 0.6)}          # glyphs that blink in place
PARTICLES = {"count": 30, "glyphs": ["o", "."], "colors": [MINT],
             "size": (10, 16), "secs": (12, 24), "opacity": (0.15, 0.35),
             "dir": "up", "drift": 30}                        # glyphs drifting up / down

# ASCII art. Each entry is a list of lines. Backslashes must be doubled ("\\").
ART = {
    "cat": [" /\\_/\\", "( o.o )", " > ^ <"],
    "fish": ["><(((>"],
}

# Who appears where:
# (art, x, y, color, opacity, font_px, motion, seconds, delay)
#   motion: "left" / "right"  swim across the screen (x shifts the path; use it to glue parts together)
#           "up" / "down"     drift vertically from x
#           "bob"             float in place at (x, y)
#           "fly"             diagonal streak starting at (x, y), like a shooting star
#   The scene is 1600 x 1000. Keep opacity around 0.2-0.5 so chat text stays readable.
SCENE = [
    ("cat",  200, 820, PINK,  0.45, 16, "bob",    6,   0),
    ("fish",   0, 400, MINT,  0.35, 15, "right", 40,   0),
]
