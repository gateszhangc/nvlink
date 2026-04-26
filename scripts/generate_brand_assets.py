#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "assets" / "brand"

BG = (244, 240, 232, 255)
PANEL = (250, 247, 240, 255)
TEXT = (16, 20, 21, 255)
MUTED = (79, 88, 88, 255)
GREEN = (86, 140, 63, 255)
GREEN_SOFT = (118, 170, 98, 255)
COPPER = (176, 106, 49, 255)
LINE = (205, 200, 190, 255)
SHADOW = (40, 48, 40, 50)


def pick_font(paths: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
  for raw_path in paths:
    path = Path(raw_path)
    if path.exists():
      return ImageFont.truetype(str(path), size=size)
  return ImageFont.load_default()


DISPLAY_FONT = [
  "/System/Library/Fonts/Supplemental/Futura.ttc",
  "/System/Library/Fonts/Avenir Next.ttc",
  "/System/Library/Fonts/Avenir.ttc"
]
MONO_FONT = [
  "/System/Library/Fonts/SFNSMono.ttf",
  "/System/Library/Fonts/Supplemental/PTMono.ttc",
  "/System/Library/Fonts/Supplemental/Andale Mono.ttf"
]


def draw_mark(base: Image.Image, origin: tuple[int, int], scale: float) -> None:
  draw = ImageDraw.Draw(base)
  x0, y0 = origin
  lane_length = int(220 * scale)
  lane_gap = int(48 * scale)
  lane_height = int(18 * scale)
  radius = lane_height // 2
  node_radius = int(18 * scale)
  rail_width = max(4, int(7 * scale))

  shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
  shadow_draw = ImageDraw.Draw(shadow)

  for idx in range(3):
    y = y0 + idx * lane_gap
    shadow_draw.rounded_rectangle((x0 + 6, y + 8, x0 + lane_length + 6, y + lane_height + 8), radius=radius, fill=SHADOW)
  shadow_draw.line((x0 + 44, y0 + lane_gap + 8, x0 + lane_length - 38, y0 + lane_gap * 2 + 8), fill=SHADOW, width=rail_width)
  shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(2, int(8 * scale))))
  base.alpha_composite(shadow)

  for idx in range(3):
    y = y0 + idx * lane_gap
    fill = GREEN if idx != 1 else GREEN_SOFT
    draw.rounded_rectangle((x0, y, x0 + lane_length, y + lane_height), radius=radius, fill=fill)

  draw.line((x0 + 40, y0 + lane_gap, x0 + lane_length - 42, y0 + lane_gap * 2), fill=COPPER, width=rail_width)

  for idx, offset in enumerate((22, 110, 198)):
    cx = x0 + int(offset * scale)
    cy = y0 + lane_gap
    color = COPPER if idx == 1 else TEXT
    draw.ellipse((cx - node_radius, cy - node_radius, cx + node_radius, cy + node_radius), fill=PANEL, outline=color, width=max(2, int(4 * scale)))
    draw.ellipse((cx - node_radius // 3, cy - node_radius // 3, cx + node_radius // 3, cy + node_radius // 3), fill=color)

  draw.ellipse(
    (
      x0 + lane_length - node_radius * 2,
      y0 + lane_gap * 2 - node_radius * 2,
      x0 + lane_length,
      y0 + lane_gap * 2
    ),
    fill=COPPER
  )


def create_mark() -> None:
  image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
  draw_mark(image, (200, 340), 2.8)
  image.save(BRAND_DIR / "logo-mark.png")


def create_wordmark() -> None:
  image = Image.new("RGBA", (1400, 360), (0, 0, 0, 0))
  mark_panel = Image.new("RGBA", (360, 360), (0, 0, 0, 0))
  panel_draw = ImageDraw.Draw(mark_panel)
  panel_draw.rounded_rectangle((18, 18, 342, 342), radius=70, fill=(255, 255, 255, 190), outline=LINE, width=3)
  draw_mark(mark_panel, (58, 120), 1.12)
  image.alpha_composite(mark_panel, (0, 0))

  draw = ImageDraw.Draw(image)
  title_font = pick_font(DISPLAY_FONT, 120)
  meta_font = pick_font(MONO_FONT, 28)
  draw.text((390, 72), "NVLINK", font=title_font, fill=TEXT)
  draw.text((396, 214), "FABRIC EXPLAINED", font=meta_font, fill=MUTED)
  draw.line((396, 198, 930, 198), fill=LINE, width=4)
  image.save(BRAND_DIR / "logo-wordmark.png")


def create_favicon() -> None:
  favicon = Image.new("RGBA", (512, 512), BG)
  draw = ImageDraw.Draw(favicon)
  draw.rounded_rectangle((40, 40, 472, 472), radius=120, fill=PANEL, outline=LINE, width=4)
  draw_mark(favicon, (112, 184), 1.18)
  favicon.save(BRAND_DIR / "favicon.png")
  favicon.resize((180, 180), Image.Resampling.LANCZOS).save(BRAND_DIR / "apple-touch-icon.png")


def create_social_card() -> None:
  image = Image.new("RGBA", (1200, 630), BG)
  draw = ImageDraw.Draw(image)
  draw.rounded_rectangle((30, 30, 1170, 600), radius=42, fill=(251, 248, 242, 255), outline=LINE, width=4)
  draw.rounded_rectangle((72, 88, 420, 540), radius=36, fill=(255, 255, 255, 235), outline=LINE, width=3)
  draw_mark(image, (118, 258), 1.3)
  draw.line((500, 166, 1038, 166), fill=LINE, width=3)
  title_font = pick_font(DISPLAY_FONT, 92)
  body_font = pick_font(MONO_FONT, 28)
  meta_font = pick_font(MONO_FONT, 22)
  draw.text((500, 110), "NVLINK", font=title_font, fill=TEXT)
  draw.text((500, 230), "Bandwidth, NVSwitch, PCIe, Blackwell and Rubin", font=body_font, fill=MUTED)
  draw.text((500, 312), "Source-backed explainer reviewed April 26, 2026", font=meta_font, fill=GREEN)
  draw.text((500, 380), "nvlink.lol", font=body_font, fill=COPPER)
  image.save(BRAND_DIR / "social-card.png")


def main() -> None:
  BRAND_DIR.mkdir(parents=True, exist_ok=True)
  create_mark()
  create_wordmark()
  create_favicon()
  create_social_card()
  print(f"Brand assets generated in {BRAND_DIR}")


if __name__ == "__main__":
  main()

