"""Generate Octo's launcher icon: a rounded GitHub-dark tile with a light
'cat/mark' silhouette. Produces:
  assets/icon/octo_icon.png      — full square (legacy launcher)
  assets/icon/octo_icon_fg.png   — transparent foreground (adaptive icon)
flutter_launcher_icons composes octo_icon_fg over the dark background color.
"""
import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "icon")
os.makedirs(OUT, exist_ok=True)

BG = (13, 17, 23, 255)      # #0D1117 GitHub canvas
FG = (201, 209, 217, 255)   # #C9D1D9 GitHub ink
SIZE = 1024


def draw_mark(d, ox, oy, scale):
    """A simplified Octocat-ish silhouette: rounded head + two ears + a body
    with a little tentacle sweep. Purely geometric so it reads at small sizes."""
    def P(x, y):
        return (ox + x * scale, oy + y * scale)

    # Head (big rounded blob)
    d.ellipse(P(-0.42, -0.55) + P(0.42, 0.28), fill=FG)
    # Ears
    d.polygon([P(-0.40, -0.42), P(-0.30, -0.72), P(-0.12, -0.48)], fill=FG)
    d.polygon([P(0.40, -0.42), P(0.30, -0.72), P(0.12, -0.48)], fill=FG)
    # Body
    d.ellipse(P(-0.34, 0.05) + P(0.34, 0.62), fill=FG)
    # Tentacle legs (three little rounded feet)
    for cx in (-0.22, 0.0, 0.22):
        d.ellipse(P(cx - 0.10, 0.50) + P(cx + 0.10, 0.74), fill=FG)

    # Punch out eyes so the head reads as a face (background color)
    for ex in (-0.16, 0.16):
        d.ellipse(P(ex - 0.075, -0.22) + P(ex + 0.075, -0.06), fill=BG)


def rounded(size, radius, color):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=color)
    return img


# --- full square icon (dark rounded tile + mark) ---
full = rounded(SIZE, int(SIZE * 0.22), BG)
d = ImageDraw.Draw(full)
draw_mark(d, SIZE / 2, SIZE * 0.46, SIZE * 0.52)
full.save(os.path.join(OUT, "octo_icon.png"))

# --- adaptive foreground: transparent, mark centered smaller (safe zone) ---
fg = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
d = ImageDraw.Draw(fg)
draw_mark(d, SIZE / 2, SIZE * 0.47, SIZE * 0.42)
fg.save(os.path.join(OUT, "octo_icon_fg.png"))

print("Wrote octo_icon.png and octo_icon_fg.png to", os.path.abspath(OUT))
