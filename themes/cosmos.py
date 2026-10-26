NAME = "cosmos"
DESCRIPTION = "Deep space: Saturn, a drifting astronaut, a UFO, comets and a space cat in a helmet"

PALETTE = {"bg": "#07060F", "fg": "#ECEAF7", "accent": "#7DE3FF", "accent2": "#B8F0FF",
           "line": "#1F1C33", "dim": "#A5A1C4"}
CYAN, VIOLET, PINK, GOLD, WHITE, MINT = "#7DE3FF", "#B49CFF", "#FF8AD8", "#FFD36B", "#F4F2FF", "#8CFFC8"

BACKDROP = [(0, "#1b0f3a"), (0.4, "#0e1630"), (0.75, "#0a0d1c"), (1, "#07060F")]
TWINKLES = {"count": 65, "glyphs": ["*", ".", "+", "'", "o", "x"], "colors": [WHITE, CYAN, VIOLET, GOLD],
            "size": (7, 15), "opacity": (0.25, 0.75)}
# warp dust: tiny specks streaming down like flying through space
PARTICLES = {"count": 26, "glyphs": [".", "'", "|"], "colors": [CYAN, VIOLET],
             "size": (8, 13), "secs": (5, 11), "opacity": (0.12, 0.30), "dir": "down", "drift": 0}

ART = {
    "saturn": ["          _____", "      ,-:` \\;',`'-,", "    .'-;_,;  ':-;_,'.",
               "   /;   '/    ,  _`.-\\", "  | '`. (`     /` ` \\`|", "  |:.  `\\`-.   \\_   / |",
               "  |     (   `,  .`\\ ;'|", "   \\     | .'     `-'/", "    `.   ;/        .'",
               "      `'-._____.-'`"],
    "ring": ["========================================"],
    "astronaut": ["     _..._", "   .'     '.", "  /  .---.  \\", " |  ( ^ ^ )  |",
                  "  \\  '---'  /", "  _'-.___.-'_", " /|  [ = ]  |\\", "  |   | |   |", "  '---' '---'"],
    "ufo": ["       _.---._", "    .'  o o  '.", " .-'-------------'-.", "'-.___.-'''-.___.-'", "    /   |   \\"],
    "alien": [" .-\"-.", "( o o )", " \\ - /", " /| |\\"],
    "satellite": ["[|||]-o-[|||]"],
    "comet": ["*=~~-----"],
    "rocket": ["   /\\", "  |  |", "  |()|", " /|__|\\", "  ^^^^", "  '\"'"],
    "space_cat": ["  .-----.", " / /\\_/\\ \\", "| ( o.o ) |", " \\ > ^ < /", "  '-----'~"],
    "moon": ["  .--.", " ( o  )", "  '--'"],
}

# (art, x, y, color, opacity, font_px, motion, seconds, delay)
SCENE = [
    ("saturn",     1200,  80, GOLD,   0.45, 14, "bob",    14,   0),
    ("ring",       1137, 175, VIOLET, 0.35, 14, "bob",    14,   0),
    ("moon",        260, 140, WHITE,  0.40, 16, "bob",    10,  -3),
    ("astronaut",     0, 420, WHITE,  0.40, 15, "right", 120,   0),
    ("ufo",           0, 220, MINT,   0.45, 15, "left",   45, -10),
    ("alien",       150, 830, MINT,   0.40, 15, "bob",     5,   0),
    ("space_cat",  1350, 780, PINK,   0.50, 16, "bob",     7,  -2),
    ("satellite",     0, 620, CYAN,   0.35, 14, "left",   70, -30),
    ("comet",      1500,  40, CYAN,   0.55, 16, "fly",     7,   0),
    ("comet",      1100,  10, PINK,   0.45, 14, "fly",    11,  -5),
    ("rocket",      820,   0, GOLD,   0.40, 15, "up",     35, -12),
    ("rocket",      460,   0, VIOLET, 0.25, 11, "up",     50, -38),
]
