NAME = "starry-night"
DESCRIPTION = "Night sky: twinkling stars, shooting stars, the moon, a cat and an owl"

PALETTE = {"bg": "#0B0D1A", "fg": "#ECE6F5", "accent": "#FFD66B", "accent2": "#FFE9A8",
           "line": "#232741", "dim": "#A9A6C2"}
GOLD, CREAM, LILAC, BLUE = "#FFD66B", "#FFF3C4", "#C9B6FF", "#9EC5FF"

BACKDROP = [(0, "#1a1440"), (0.55, "#0f1230"), (1, "#0B0D1A")]
TWINKLES = {"count": 105, "glyphs": ["*", ".", "+", "'", "o"], "colors": [CREAM, GOLD, LILAC, BLUE],
            "size": (8, 16), "opacity": (0.25, 0.7), "max_y": 0.85}

ART = {
    "moon": ["    _.._", "  .' .-'`", " /  /", " |  |", " \\  \\", "  '._'-._", "     ```"],
    "cat": ["  /\\_/\\", " ( o.o )", "  > ^ <", " /     \\", "(_)-(_)~"],
    "owl": ["  ,_,", " {o,o}", " /)__)", " -\"-\"-"],
    "shooting": ["*-----"],
    "cloud": ["   .--.", " .(    ).", "(___.__)__)"],
    "bat": ["/\\^_^/\\"],
    "sleepy_cat": ["  |\\      _,,,---,,_", "  /,`.-'`'    -.  ;-;;,_", " |,4-  ) )-,_. ,\\ (  `'-'", "'---''(_/--'  `-'\\_)  zZ"],
    "planet": ["   .-.", "  (   )~~", "~~ '-'"],
    "rocket": ["   /\\", "  |  |", "  |()|", " /|__|\\", "  ^^^^"],
}

SCENE = [
    ("moon",     1260, 120, CREAM, 0.55, 22, "bob",   10,   0),
    ("cat",       160, 860, LILAC, 0.45, 16, "bob",    7,   0),
    ("owl",      1420, 820, GOLD,  0.40, 15, "bob",    5,  -2),
    ("shooting", 1500, 60,  CREAM, 0.60, 16, "fly",    6,   0),
    ("shooting", 1100, 20,  GOLD,  0.50, 14, "fly",    9,  -4),
    ("shooting",  700, 90,  LILAC, 0.45, 13, "fly",   13,  -7),
    ("cloud",       0, 300, LILAC, 0.18, 16, "left",  140,  0),
    ("cloud",       0, 520, BLUE,  0.14, 14, "right", 170, -60),
    ("bat",         0, 230, LILAC, 0.30, 14, "left",   40, -10),
    ("bat",         0, 420, LILAC, 0.22, 12, "left",   55, -30),
    ("sleepy_cat",  560, 880, CREAM, 0.40, 15, "bob",    8,  -3),
    ("planet",      300, 160, BLUE,  0.40, 18, "bob",   12,  -5),
    ("rocket",      980,   0, GOLD,  0.35, 14, "up",    60, -20),
    ("owl",         120, 520, GOLD,  0.30, 13, "bob",    6,  -4),
]
