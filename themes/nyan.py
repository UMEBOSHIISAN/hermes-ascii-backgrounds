NAME = "nyan"
DESCRIPTION = "Cats everywhere: walking, napping, stretching, a cat in a box, yarn and paw prints"

PALETTE = {"bg": "#14101A", "fg": "#F3ECE6", "accent": "#FFB36B", "accent2": "#FFD3A8",
           "line": "#2C2433", "dim": "#BDAFB8"}
ORANGE, CREAM, PINK, LILAC, MINT = "#FFB36B", "#FFF1E0", "#FF9EC4", "#C8B6FF", "#9EF0D0"

BACKDROP = [(0, "#2a1d33"), (0.55, "#1b1424"), (1, "#14101A")]
PARTICLES = {"count": 60, "glyphs": ["o", ":", "*", "'", "."], "colors": [PINK, CREAM, LILAC],
             "size": (10, 16), "secs": (16, 32), "opacity": (0.18, 0.40), "dir": "down", "drift": 120}

ART = {
    "sit": ["  /\\_/\\", " ( o.o )", "  > ^ <", " /     \\", "(_)-(_)~"],
    "happy": [" /\\_/\\", "( ^w^ )", " (\")(\")"],
    "walk": ["    /\\_/\\", "   ( =.=)", " ~(  \"  )", "   \\_U_U"],
    "walk_r": [" /\\_/\\", "(=.= )", "(  \"  )~", "U_U_/"],
    "nap": ["      |\\      _,,,---,,_", "ZZZzz /,`.-'`'    -.  ;-;;,_",
            "     |,4-  ) )-,_. ,\\ (  `'-'", "    '---''(_/--'  `-'\\_)"],
    "box": ["   /\\_/\\", "  ( o.o )", " .-------.", " |  NYA  |", " '-------'"],
    "stretch": ["  /\\_/\\_____", " ( -.- )    )~", "  \\/\\/ \\/\\/"],
    "loaf": [" /\\_/\\", "( -.- )", "(______)"],
    "yarn": ["  .-.", " ( @ )~~", "  '-'"],
    "fish": ["><(((('>"],
    "bone": [">-|-|-|->"],
    "paws": ["o:", "   o:", "o:", "   o:"],
    # nyan cat: body + one rainbow stripe per color, all moving together
    "nyan": [",------,", "|   /\\_/\\", "|__( ^ .^)", " \"\"  \"\""],
    "stripe": ["=-=-=-=-=-=-=-"],
    "mouse": ["<:3 )~"],
    "chaser": [" /\\_/\\", "( >.< )~~", " (\")(\")"],
    "nya": [" .------.", "( nya~ )", " '--.,-'"],
    "meow": [" .------.", "( meow! )", " '-,.--'"],
    "purr": [" .-------.", "( purr... )", " '--.,--'"],
}

# (art, x, y, color, opacity, font_px, motion, seconds, delay)
SCENE = [
    ("walk",       0, 760, ORANGE, 0.45, 16, "left",  70,   0),
    ("walk_r",     0, 420, CREAM,  0.35, 14, "right", 85, -30),
    ("walk",       0, 240, LILAC,  0.28, 12, "left", 110, -60),
    ("nap",      560, 860, CREAM,  0.40, 15, "bob",    8,   0),
    ("box",     1320, 820, ORANGE, 0.45, 15, "bob",    5,  -2),
    ("sit",      130, 830, PINK,   0.45, 16, "bob",    6,  -1),
    ("happy",   1100, 860, MINT,   0.40, 15, "bob",    4,  -3),
    ("stretch",  960, 120, LILAC,  0.35, 15, "bob",    9,  -4),
    ("loaf",     300, 110, CREAM,  0.35, 15, "bob",    7,  -2),
    ("loaf",    1450, 330, PINK,   0.30, 13, "bob",    6,  -5),
    ("yarn",       0, 600, PINK,   0.40, 15, "right", 45, -10),
    ("yarn",       0, 180, MINT,   0.30, 13, "left",  60, -25),
    ("fish",       0, 520, CREAM,  0.30, 14, "left",  40, -15),
    ("bone",       0, 330, ORANGE, 0.25, 13, "right", 55, -35),
    ("paws",     760,   0, CREAM,  0.25, 14, "down",  50,   0),
    ("paws",    1240,   0, PINK,   0.22, 13, "down",  65, -30),
    # chase: mouse runs ahead, cat follows at the same speed
    ("mouse",      0, 690, CREAM,  0.45, 15, "left",  30,  -5),
    ("chaser",     0, 670, ORANGE, 0.45, 15, "left",  30, -7.5),
    # speech bubbles drift up
    ("nya",      420,   0, PINK,   0.35, 13, "up",    40,  -8),
    ("meow",    1050,   0, ORANGE, 0.30, 13, "up",    48, -28),
    ("purr",     700,   0, LILAC,  0.28, 12, "up",    56, -44),
]

# nyan cat with a rainbow: stripes trail the body, same speed and delay so they fly together
RAINBOW = ["#FF6B6B", "#FFB36B", "#FFE66B", "#7DFF9A", "#6BC8FF", "#C8B6FF"]
NYAN_Y, NYAN_SECS, NYAN_DELAY = 330, 26, -3
# x = -84 puts the stripes' right end right at the cat's back (body 10 chars @15px, stripe 14 chars @14px)
SCENE += [("stripe", -84, NYAN_Y + 4 + i * 9, c, 0.55, 14, "right", NYAN_SECS, NYAN_DELAY)
          for i, c in enumerate(RAINBOW)]
SCENE += [("nyan", 0, NYAN_Y, CREAM, 0.6, 15, "right", NYAN_SECS, NYAN_DELAY)]
