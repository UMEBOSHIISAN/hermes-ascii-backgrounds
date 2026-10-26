NAME = "aquarium"
DESCRIPTION = "Deep sea: whales, jellyfish, an octopus, a turtle and fish under matrix rain"

PALETTE = {"bg": "#0E1116", "fg": "#ECE8DF", "accent": "#00FF41", "accent2": "#7DFF9A",
           "line": "#262B33", "dim": "#B9B4A9"}
GREEN, GREEN2, CYAN, PINK, GOLD = "#00FF41", "#7DFF9A", "#8CCBFF", "#FF9AD5", "#c9a96e"

BACKDROP = [(0, "#0d3a44"), (0.45, "#0a1f2a"), (1, "#0E1116")]
RAYS = "#9ff6ff"
RAIN = {"columns": 38, "glyphs": "01<>{}[]/\\|=+*~^:;.o0O", "color": GREEN}
PARTICLES = {"count": 24, "glyphs": ["o", "O", ".", "o"], "colors": [GREEN2, CYAN],
             "size": (10, 18), "secs": (12, 24), "opacity": (0.15, 0.3), "dir": "up", "drift": 30}

ART = {
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
    "jelly_s": ["  .--.", " ( ^^ )", "  '--'", "  )()(", " ( )( )"],
    "octo": ["   .---.", "  ( ^ ^ )", "  (  o  )", "  /|/|\\|\\", " ~ ~ ~ ~ ~"],
    "turtle": ["    _____     ____", "  /      \\  |  o |", " |        |/ ___\\|", " |_________/", " |_|_| |_|_|"],
    "fish_l": ["<')))><"],
    "fish_r": ["><(((>"],
    "fish_s": ["<><"],
}

# (art, x, y, color, opacity, font_px, motion, seconds, delay)
# motion: left / right (swim across), up / down (drift), bob (float in place), fly (diagonal)
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
    ("octo",   1300,   860, GOLD,   0.26, 14, "bob",    6,   0),
    ("turtle",    0,   380, GREEN2, 0.20, 13, "right",130, -30),
    ("fish_r",    0,   300, CYAN,   0.30, 16, "right", 35,   0),
    ("fish_r",    0,   330, CYAN,   0.24, 13, "right", 35,  -1),
    ("fish_l",    0,   470, PINK,   0.26, 15, "left",  45, -15),
    ("fish_l",    0,   740, GREEN2, 0.24, 14, "left",  50, -30),
    ("fish_s",    0,   150, GREEN,  0.28, 14, "right", 28,  -8),
    ("fish_s",    0,   900, CYAN,   0.22, 13, "left",  33, -12),
]
