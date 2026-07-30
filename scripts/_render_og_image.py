#!/usr/bin/env python3
"""One-off helper: render docs/assets/og-image.png (1200x630) from the same
design language as assets/banner.svg. Not part of the regular build (no
external SVG rasterizer is available in this environment), kept here for
reference in case the OG image needs regenerating after a brand refresh.

Usage: python3 scripts/_render_og_image.py
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
FONT_PATH = "/System/Library/Fonts/STHeiti Medium.ttc"

GRAD_STOPS = [
    (0.0, (0x22, 0xD3, 0xEE)),
    (0.55, (0x2D, 0xD4, 0xA7)),
    (1.0, (0x86, 0xEF, 0xAC)),
]


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_color(t):
    for (t0, c0), (t1, c1) in zip(GRAD_STOPS, GRAD_STOPS[1:]):
        if t0 <= t <= t1:
            local_t = (t - t0) / (t1 - t0) if t1 > t0 else 0
            return lerp(c0, c1, local_t)
    return GRAD_STOPS[-1][1]


def make_background():
    # diagonal gradient: project each pixel onto the diagonal axis
    xs = np.linspace(0, 1, W)
    ys = np.linspace(0, 1, H)
    xx, yy = np.meshgrid(xs, ys)
    t = (xx + yy) / 2
    arr = np.zeros((H, W, 3), dtype=np.uint8)
    # sample the gradient at coarse steps for speed, then map
    steps = 256
    lut = np.array([gradient_color(i / (steps - 1)) for i in range(steps)], dtype=np.uint8)
    idx = np.clip((t * (steps - 1)).astype(int), 0, steps - 1)
    arr = lut[idx]
    return Image.fromarray(arr, mode="RGB")


def draw_sparkle(draw, cx, cy, size, fill):
    pts = [
        (cx, cy - size), (cx + size * 0.18, cy - size * 0.18),
        (cx + size, cy), (cx + size * 0.18, cy + size * 0.18),
        (cx, cy + size), (cx - size * 0.18, cy + size * 0.18),
        (cx - size, cy), (cx - size * 0.18, cy - size * 0.18),
    ]
    draw.polygon(pts, fill=fill)


def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def main():
    bg = make_background().convert("RGBA")

    # soft radial glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for cx, cy, r in [(1080, 120, 160), (90, 520, 130)]:
        for rr in range(r, 0, -4):
            alpha = int(60 * (1 - rr / r))
            gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 255, 255, alpha))
    bg = Image.alpha_composite(bg, glow)

    draw = ImageDraw.Draw(bg)
    draw_sparkle(draw, 1120, 60, 18, (255, 255, 255, 220))
    draw_sparkle(draw, 70, 150, 13, (255, 255, 255, 220))

    # logo badge
    logo = Image.open("assets/ezsou-logo.png").convert("RGBA").resize((172, 172), Image.LANCZOS)
    mask = Image.new("L", (172, 172), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, 172, 172], fill=255)
    badge = Image.new("RGBA", (188, 188), (0, 0, 0, 0))
    ImageDraw.Draw(badge).ellipse([0, 0, 188, 188], fill=(255, 255, 255, 255))
    badge.paste(logo, (8, 8), mask)
    bg.alpha_composite(badge, (90, 110))

    font_title = ImageFont.truetype(FONT_PATH, 58)
    font_sub = ImageFont.truetype(FONT_PATH, 28)
    font_chip = ImageFont.truetype(FONT_PATH, 22)

    draw.text((92, 320), "Awesome Telegram", font=font_title, fill=(8, 51, 68, 255))
    draw.text((92, 392), "Chinese 2026", font=font_title, fill=(8, 51, 68, 255))
    draw.text((94, 462), "中文 Telegram 优质资源导航 · 机器人 · 频道 · 群组", font=font_sub, fill=(15, 59, 51, 255))

    chip_box = [92, 512, 452, 566]
    rounded_rect(draw, chip_box, 27, (255, 255, 255, 230))
    draw.ellipse([108, 523, 141, 556], fill=(14, 165, 160, 255))
    draw.ellipse([115, 528, 132, 545], outline=(255, 255, 255, 255), width=3)
    draw.line([128, 541, 136, 549], fill=(255, 255, 255, 255), width=3)
    draw.text((152, 526), "本项目由 易搜 维护", font=font_chip, fill=(15, 59, 51, 255))

    bg.convert("RGB").save("docs/assets/og-image.png", optimize=True)
    print("wrote docs/assets/og-image.png")


if __name__ == "__main__":
    main()
