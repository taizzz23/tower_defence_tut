import pygame as pg
import math
import os

pg.init()
# We can use a dummy video mode for headless image rendering
screen = pg.display.set_mode((1, 1), pg.NOFRAME)

# Base size: 48x48 (tile size)
# Turret frame size: 96x96 (center at 48, 48)
FRAME_SIZE = 96
STEPS = 8

os.makedirs('assets/images/new_turrets', exist_ok=True)

def draw_circle_alpha(surface, color, center, radius, width=0):
  target_rect = pg.Rect(center[0] - radius, center[1] - radius, 2 * radius, 2 * radius)
  shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
  pg.draw.circle(shape_surf, color, (radius, radius), radius, width)
  surface.blit(shape_surf, target_rect)

# -------------------------------------------------------------
# 1. GUNNER (Gatling / Dual Cannon)
# -------------------------------------------------------------
def render_gunner_base(level):
  surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cx, cy = 48, 48
  # Outer stone ring
  pg.draw.circle(surf, (40, 44, 52), (cx, cy), 20)
  pg.draw.circle(surf, (80, 88, 102), (cx, cy), 18)
  pg.draw.circle(surf, (120, 130, 145), (cx, cy), 14)
  # Rivets
  for a in range(0, 360, 45):
    rad = math.radians(a)
    rx = int(cx + 16 * math.cos(rad))
    ry = int(cy + 16 * math.sin(rad))
    pg.draw.circle(surf, (30, 32, 38), (rx, ry), 2)
  # Center pivot
  pg.draw.circle(surf, (50, 55, 65), (cx, cy), 8)
  pg.draw.circle(surf, (200, 210, 225), (cx, cy), 4)
  return surf

def render_gunner_head(level, frame):
  surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cx, cy = 48, 48
  # Recoil calculation (recoil back when frame is 0..3, recover 4..7)
  recoil_left = 0
  recoil_right = 0
  muzzle_flash = False
  if frame == 0:
    recoil_left = 6
    muzzle_flash = True
  elif frame == 1:
    recoil_left = 4
  elif frame == 2:
    recoil_right = 6
    muzzle_flash = True
  elif frame == 3:
    recoil_right = 4
  elif frame == 4:
    recoil_left = 2
  elif frame == 5:
    recoil_right = 2

  # Gun body (facing UP / North)
  body_color = (65, 75, 90) if level < 3 else (50, 70, 95)
  highlight = (100, 115, 135)
  barrel_color = (35, 40, 48)

  # Dual Barrels (left and right)
  barrel_len = 22 + level * 2
  # Left barrel
  pg.draw.rect(surf, barrel_color, (cx - 7, cy - barrel_len + recoil_left, 4, barrel_len))
  pg.draw.rect(surf, (200, 160, 60), (cx - 8, cy - barrel_len + recoil_left, 6, 4)) # brass tip
  # Right barrel
  pg.draw.rect(surf, barrel_color, (cx + 3, cy - barrel_len + recoil_right, 4, barrel_len))
  pg.draw.rect(surf, (200, 160, 60), (cx + 2, cy - barrel_len + recoil_right, 6, 4)) # brass tip

  # Turret housing
  pg.draw.circle(surf, (30, 35, 42), (cx, cy + 2), 12)
  pg.draw.rect(surf, body_color, (cx - 10, cy - 8, 20, 16), border_radius=4)
  pg.draw.rect(surf, highlight, (cx - 8, cy - 6, 16, 4), border_radius=2)
  # Ammo drums on sides
  pg.draw.circle(surf, (180, 140, 50), (cx - 11, cy + 2), 5)
  pg.draw.circle(surf, (180, 140, 50), (cx + 11, cy + 2), 5)

  # Muzzle flash
  if muzzle_flash:
    fx = cx - 5 if frame == 0 else cx + 5
    fy = cy - barrel_len - 4
    pg.draw.circle(surf, (255, 230, 100), (fx, fy), 6)
    pg.draw.circle(surf, (255, 255, 255), (fx, fy), 3)

  return surf

# -------------------------------------------------------------
# 2. BOMB (Heavy Mortar / Cannon)
# -------------------------------------------------------------
def render_bomb_base(level):
  surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cx, cy = 48, 48
  # Fortified iron base
  pg.draw.circle(surf, (25, 25, 30), (cx, cy), 21)
  pg.draw.circle(surf, (60, 40, 35), (cx, cy), 18)
  pg.draw.circle(surf, (90, 50, 40), (cx, cy), 14)
  # Heavy support braces
  for a in [45, 135, 225, 315]:
    rad = math.radians(a)
    bx = int(cx + 17 * math.cos(rad))
    by = int(cy + 17 * math.sin(rad))
    pg.draw.circle(surf, (180, 80, 50), (bx, by), 3)
  pg.draw.circle(surf, (30, 30, 35), (cx, cy), 7)
  return surf

def render_bomb_head(level, frame):
  surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cx, cy = 48, 48
  # Recoil
  recoil = 0
  flash = False
  if frame == 0:
    recoil = 8
    flash = True
  elif frame == 1:
    recoil = 6
  elif frame == 2:
    recoil = 4
  elif frame == 3:
    recoil = 2

  barrel_w = 14 + level
  barrel_h = 24 + level * 2

  # Counter-weight at back
  pg.draw.circle(surf, (20, 20, 25), (cx, cy + 6 + recoil), 13)
  pg.draw.circle(surf, (45, 45, 55), (cx, cy + 6 + recoil), 10)

  # Cannon barrel (pointing UP)
  bx = cx - barrel_w // 2
  by = cy - barrel_h + recoil
  pg.draw.rect(surf, (35, 35, 42), (bx, by, barrel_w, barrel_h), border_radius=3)
  # Barrel metal bands / stripes
  pg.draw.rect(surf, (200, 75, 40), (bx - 1, by + 4, barrel_w + 2, 4))
  pg.draw.rect(surf, (200, 75, 40), (bx - 1, by + barrel_h - 8, barrel_w + 2, 4))
  # Big muzzle ring
  pg.draw.rect(surf, (70, 75, 85), (bx - 2, by, barrel_w + 4, 6), border_radius=2)
  # Dark barrel hole
  pg.draw.ellipse(surf, (10, 10, 15), (bx + 1, by - 1, barrel_w - 2, 4))

  if flash:
    # Big explosion puff at muzzle
    pg.draw.circle(surf, (255, 140, 30), (cx, by - 4), 12)
    pg.draw.circle(surf, (255, 230, 100), (cx, by - 4), 7)
    pg.draw.circle(surf, (255, 255, 255), (cx, by - 4), 3)

  return surf

# -------------------------------------------------------------
# 3. ICE (Frost Spire / Crystal Obelisk)
# -------------------------------------------------------------
def render_ice_base(level):
  surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cx, cy = 48, 48
  # Hexagonal frost rune pedestal
  points = []
  for i in range(6):
    angle = math.radians(i * 60)
    px = cx + 19 * math.cos(angle)
    py = cy + 19 * math.sin(angle)
    points.append((px, py))
  pg.draw.polygon(surf, (30, 60, 90), points)
  inner_points = []
  for i in range(6):
    angle = math.radians(i * 60)
    px = cx + 15 * math.cos(angle)
    py = cy + 15 * math.sin(angle)
    inner_points.append((px, py))
  pg.draw.polygon(surf, (70, 140, 190), inner_points)
  pg.draw.circle(surf, (160, 230, 255), (cx, cy), 9)
  pg.draw.circle(surf, (255, 255, 255), (cx, cy), 4)
  return surf

def render_ice_head(level, frame):
  surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cx, cy = 48, 48
  # Pulse scale when firing
  scale = 1.0
  glow = False
  if frame in (0, 1):
    scale = 1.25
    glow = True
  elif frame in (2, 3):
    scale = 1.15
  elif frame in (4, 5):
    scale = 1.05

  # Shard angle rotation based on frame
  shard_rot = math.radians(frame * 45)

  # Central Crystal (Diamond pointing UP)
  top_y = cy - int(24 * scale)
  bot_y = cy + int(12 * scale)
  w = int(10 * scale)

  crystal_pts = [
    (cx, top_y),        # Top tip
    (cx + w, cy - 4),    # Right
    (cx, bot_y),        # Bottom
    (cx - w, cy - 4)     # Left
  ]
  # Crystal body
  pg.draw.polygon(surf, (40, 160, 230), crystal_pts)
  # Highlight facet
  left_facet = [(cx, top_y), (cx, bot_y), (cx - w, cy - 4)]
  pg.draw.polygon(surf, (140, 220, 255), left_facet)
  # Center bright streak
  pg.draw.line(surf, (255, 255, 255), (cx, top_y + 2), (cx, bot_y - 2), 2)

  # Orbiting ice shards (2 or 4 depending on level)
  num_shards = 2 if level < 3 else 4
  for i in range(num_shards):
    ang = shard_rot + (i * (2 * math.pi / num_shards))
    dist = 18 * scale
    sx = int(cx + dist * math.cos(ang))
    sy = int(cy - 4 + dist * 0.7 * math.sin(ang))
    pg.draw.circle(surf, (180, 240, 255), (sx, sy), 3)
    pg.draw.circle(surf, (255, 255, 255), (sx, sy), 1)

  if glow:
    draw_circle_alpha(surf, (120, 230, 255, 100), (cx, cy - 6), int(26 * scale))
    draw_circle_alpha(surf, (255, 255, 255, 140), (cx, cy - 6), int(14 * scale))

  return surf

# -------------------------------------------------------------
# 4. SNIPER (Long-range Railgun / Sniper Spire)
# -------------------------------------------------------------
def render_sniper_base(level):
  surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cx, cy = 48, 48
  # Fortified military watch-post base
  pg.draw.rect(surf, (35, 40, 30), (cx - 19, cy - 19, 38, 38), border_radius=6)
  pg.draw.rect(surf, (60, 70, 50), (cx - 16, cy - 16, 32, 32), border_radius=4)
  pg.draw.circle(surf, (40, 48, 36), (cx, cy), 11)
  # Corner bolts
  for ox, oy in [(-13, -13), (13, -13), (-13, 13), (13, 13)]:
    pg.draw.circle(surf, (200, 180, 70), (cx + ox, cy + oy), 2)
  return surf

def render_sniper_head(level, frame):
  surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cx, cy = 48, 48
  recoil = 0
  flash = False
  if frame == 0:
    recoil = 9
    flash = True
  elif frame == 1:
    recoil = 6
  elif frame == 2:
    recoil = 3
  elif frame == 3:
    recoil = 1

  gun_len = 34 + level * 2

  # Stock & receiver
  pg.draw.rect(surf, (30, 35, 28), (cx - 6, cy - 2 + recoil, 12, 16), border_radius=2)
  # Main Long Barrel (pointing UP)
  by = cy - gun_len + recoil
  pg.draw.rect(surf, (22, 24, 20), (cx - 3, by, 6, gun_len), border_radius=1)
  # Carbon / gold barrel accents
  pg.draw.rect(surf, (210, 180, 50), (cx - 4, by + 10, 8, 4))
  # Muzzle brake
  pg.draw.rect(surf, (50, 55, 45), (cx - 5, by, 10, 5), border_radius=1)
  # High-tech Scope on side
  pg.draw.rect(surf, (15, 18, 15), (cx + 4, cy - 14 + recoil, 5, 16), border_radius=2)
  # Red laser diode at scope front
  pg.draw.circle(surf, (255, 30, 30), (cx + 6, cy - 14 + recoil), 2)

  if flash:
    # Sharp muzzle flare
    pg.draw.polygon(surf, (255, 240, 100), [(cx, by - 12), (cx - 6, by), (cx + 6, by)])
    pg.draw.circle(surf, (255, 80, 30), (cx, by - 2), 6)

  return surf

# -------------------------------------------------------------
# BUILD SPRITESHEETS FOR EACH TURRET & LEVEL
# -------------------------------------------------------------
TURRET_RENDERERS = {
  "gunner": (render_gunner_base, render_gunner_head),
  "bomb":   (render_bomb_base, render_bomb_head),
  "ice":    (render_ice_base, render_ice_head),
  "sniper": (render_sniper_base, render_sniper_head),
}

for t_name, (base_func, head_func) in TURRET_RENDERERS.items():
  # Save base image
  base_surf = base_func(1)
  pg.image.save(base_surf, f"assets/images/new_turrets/{t_name}_base.png")

  # Generate preview cursor image (Base + Head at frame 0)
  cursor_surf = pg.Surface((FRAME_SIZE, FRAME_SIZE), pg.SRCALPHA)
  cursor_surf.blit(base_surf, (0, 0))
  head_0 = head_func(1, 4) # idle frame
  cursor_surf.blit(head_0, (0, 0))
  pg.image.save(cursor_surf, f"assets/images/new_turrets/{t_name}_cursor.png")

  # Generate 4 upgrade levels of head spritesheets (8 frames each: 8 * 96 = 768px wide)
  for lvl in range(1, 5):
    sheet = pg.Surface((FRAME_SIZE * STEPS, FRAME_SIZE), pg.SRCALPHA)
    for frame in range(STEPS):
      x_off = frame * FRAME_SIZE
      head_f = head_func(lvl, frame)
      sheet.blit(head_f, (x_off, 0))
    pg.image.save(sheet, f"assets/images/new_turrets/{t_name}_level_{lvl}.png")

print("All turret spritesheets successfully generated!")
