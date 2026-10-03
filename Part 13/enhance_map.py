import pygame as pg
import random
import math
import shutil
import os

pg.init()
screen = pg.display.set_mode((1, 1), pg.NOFRAME)

# Backup original level.png if not already backed up
if not os.path.exists('levels/level_backup.png'):
  shutil.copyfile('levels/level.png', 'levels/level_backup.png')

orig_img = pg.image.load('levels/level_backup.png')
w, h = orig_img.get_size() # 720, 720

# Create high-detail surface
map_surf = pg.Surface((w, h))

# Step 1: Detect path vs grass from original image
# In the original image: grass is bright green (G > 150 and R < 100), path is brown/tan (R > 130 and B < 120)
is_path = [[False for _ in range(h)] for _ in range(w)]
for x in range(w):
  for y in range(h):
    c = orig_img.get_at((x, y))
    # If reddish/tan/dirt
    if c.r > 120 and c.r > c.b + 30:
      is_path[x][y] = True

# Step 2: Draw beautiful textured grass foundation
random.seed(42) # Deterministic aesthetic generation

for y in range(h):
  # Subtle vertical forest gradient
  grad = y / h
  base_r = int(42 + grad * 8)
  base_g = int(162 - grad * 12)
  base_b = int(72 + grad * 10)
  pg.draw.line(map_surf, (base_r, base_g, base_b), (0, y), (w, y))

# Add organic grass patches & noise
patch_surf = pg.Surface((w, h), pg.SRCALPHA)
for _ in range(1200):
  px = random.randint(0, w - 1)
  py = random.randint(0, h - 1)
  if not is_path[px][py]:
    rad = random.randint(8, 24)
    # Lighter or darker green patch
    if random.random() < 0.5:
      col = (65, 195, 95, 35) # Sunlit patch
    else:
      col = (30, 115, 55, 30) # Shadow patch
    pg.draw.circle(patch_surf, col, (px, py), rad)
map_surf.blit(patch_surf, (0, 0))

# Step 3: Draw dirt path with depth & sunken road effect
path_base_surf = pg.Surface((w, h), pg.SRCALPHA)

# Path colors: warm earthy dirt
DIRT_BASE = (195, 142, 92)
DIRT_DARK = (155, 105, 65)
DIRT_LIGHT = (215, 165, 115)
SOIL_EDGE = (105, 68, 42)

for x in range(w):
  for y in range(h):
    if is_path[x][y]:
      # Check if near edge of path (distance to grass)
      is_edge = False
      for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-2,0), (2,0), (0,-2), (0,2)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not is_path[nx][ny]:
          is_edge = True
          break

      if is_edge:
        path_base_surf.set_at((x, y), (*SOIL_EDGE, 240))
      else:
        # Subtle texture noise
        noise = (math.sin(x * 0.15) * math.cos(y * 0.15) + (random.random() - 0.5) * 0.4)
        if noise > 0.3:
          path_base_surf.set_at((x, y), (*DIRT_LIGHT, 255))
        elif noise < -0.3:
          path_base_surf.set_at((x, y), (*DIRT_DARK, 255))
        else:
          path_base_surf.set_at((x, y), (*DIRT_BASE, 255))

map_surf.blit(path_base_surf, (0, 0))

# Step 4: Drop shadow from grass onto path (gives 3D sunken depth)
shadow_surf = pg.Surface((w, h), pg.SRCALPHA)
for x in range(w):
  for y in range(h):
    if not is_path[x][y]:
      # Cast subtle shadow to bottom-right onto path
      for sox, soy in [(1, 2), (2, 3), (3, 4)]:
        sx, sy = x + sox, y + soy
        if 0 <= sx < w and 0 <= sy < h and is_path[sx][sy]:
          shadow_surf.set_at((sx, sy), (20, 25, 35, 45))
map_surf.blit(shadow_surf, (0, 0))

# Step 5: Cobblestones & stepping stones embedded in path
stone_surf = pg.Surface((w, h), pg.SRCALPHA)
stone_colors = [
  (175, 165, 150),
  (145, 135, 125),
  (190, 178, 160),
  (130, 120, 110),
  (210, 195, 175)
]

for _ in range(850):
  sx = random.randint(10, w - 10)
  sy = random.randint(10, h - 10)
  # Check if deep inside path (not on very edge)
  if is_path[sx][sy]:
    deep_in_path = True
    for ox, oy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
      if not (0 <= sx + ox < w and 0 <= sy + oy < h and is_path[sx + ox][sy + oy]):
        deep_in_path = False
        break
    if deep_in_path:
      s_rad = random.randint(3, 7)
      s_col = random.choice(stone_colors)
      # Stone shadow
      pg.draw.circle(stone_surf, (50, 35, 25, 120), (sx + 1, sy + 2), s_rad)
      # Stone body
      pg.draw.circle(stone_surf, s_col, (sx, sy), s_rad)
      # Stone top highlight
      pg.draw.circle(stone_surf, (240, 235, 220, 160), (sx - 1, sy - 1), max(1, s_rad - 2))

map_surf.blit(stone_surf, (0, 0))

# Step 6: Organic Grass Details (Blades, Wild Flowers, Clovers)
detail_surf = pg.Surface((w, h), pg.SRCALPHA)

# Wild flowers
flower_types = [
  ((255, 255, 255), (255, 215, 0)), # Daisy (white with yellow dot)
  ((255, 75, 80),   (255, 240, 100)), # Poppy (red with yellow dot)
  ((100, 180, 255), (255, 255, 255)), # Forget-me-not (blue with white dot)
  ((235, 140, 255), (255, 255, 200)), # Lavender/Violet
]

for _ in range(400):
  fx = random.randint(10, w - 10)
  fy = random.randint(10, h - 10)
  if not is_path[fx][fy]:
    petal_col, center_col = random.choice(flower_types)
    # Petals (tiny 4-dot cross)
    pg.draw.circle(detail_surf, petal_col, (fx - 1, fy), 2)
    pg.draw.circle(detail_surf, petal_col, (fx + 1, fy), 2)
    pg.draw.circle(detail_surf, petal_col, (fx, fy - 1), 2)
    pg.draw.circle(detail_surf, petal_col, (fx, fy + 1), 2)
    # Center dot
    pg.draw.circle(detail_surf, center_col, (fx, fy), 1)

# Grass tufts (little 2-3 blade green spikes)
for _ in range(800):
  gx = random.randint(5, w - 5)
  gy = random.randint(5, h - 5)
  if not is_path[gx][gy]:
    blade_col = random.choice([(70, 200, 110), (95, 225, 130), (50, 150, 80)])
    pg.draw.line(detail_surf, blade_col, (gx, gy), (gx - 2, gy - 4), 1)
    pg.draw.line(detail_surf, blade_col, (gx, gy), (gx + 1, gy - 5), 1)
    pg.draw.line(detail_surf, blade_col, (gx, gy), (gx + 3, gy - 3), 1)

map_surf.blit(detail_surf, (0, 0))

# Step 7: Decorative Environment Props (Trees, Pond, Ancient Stones)
props_surf = pg.Surface((w, h), pg.SRCALPHA)

# Helper: Draw Stylized Fluffy Tree
def draw_tree(surface, cx, cy, radius, tree_type="oak"):
  # Soft drop shadow
  sh_rect = pg.Rect(cx - radius + 6, cy - radius // 2 + 10, int(radius * 2.2), int(radius * 1.2))
  pg.draw.ellipse(surface, (15, 35, 20, 100), sh_rect)
  # Wooden trunk
  trunk_w = max(4, radius // 4)
  pg.draw.rect(surface, (95, 60, 35), (cx - trunk_w // 2, cy + radius // 3, trunk_w, radius // 2), border_radius=2)
  # Leaves canopy layers
  leaf_colors = [
    (35, 110, 50),  # Dark shadow base
    (48, 145, 65),  # Mid tone
    (75, 190, 85),  # Sunlit foliage
    (115, 225, 120) # Top highlight
  ]
  # Outer dark foliage
  pg.draw.circle(surface, leaf_colors[0], (cx, cy), radius)
  pg.draw.circle(surface, leaf_colors[1], (cx - 2, cy - 3), int(radius * 0.9))
  # Clustered fluffy puffs
  for ox, oy, r_ratio in [(-radius//3, -radius//4, 0.65), (radius//3, -radius//4, 0.6), (0, -radius//3, 0.7)]:
    pg.draw.circle(surface, leaf_colors[2], (cx + ox, cy + oy), int(radius * r_ratio))
    pg.draw.circle(surface, leaf_colors[3], (cx + ox - 2, cy + oy - 2), int(radius * r_ratio * 0.55))

# Helper: Draw Natural Crystal Pond in open corner
def draw_pond(surface, px, py):
  # Sandy shore
  pg.draw.ellipse(surface, (205, 180, 130), (px - 45, py - 30, 90, 60))
  # Water body
  pg.draw.ellipse(surface, (45, 140, 210), (px - 40, py - 26, 80, 52))
  # Deep center water
  pg.draw.ellipse(surface, (30, 105, 180), (px - 28, py - 18, 56, 36))
  # Water highlights
  pg.draw.arc(surface, (160, 230, 255), (px - 25, py - 15, 45, 25), 0.5, 2.5, 2)
  # Water lily pads
  for lx, ly in [(px - 15, py - 5), (px + 12, py + 4), (px - 5, py + 10)]:
    pg.draw.circle(surface, (50, 175, 75), (lx, ly), 5)
    pg.draw.circle(surface, (255, 140, 190), (lx, ly), 2) # pink flower

# Helper: Draw Wooden Fence
def draw_fence(surface, start_x, start_y, num_posts=3, direction="h"):
  post_col = (115, 80, 45)
  rail_col = (145, 105, 60)
  for i in range(num_posts):
    if direction == "h":
      fx = start_x + i * 16
      fy = start_y
      # Shadow
      pg.draw.ellipse(surface, (20, 30, 20, 80), (fx - 2, fy + 8, 8, 4))
      # Post
      pg.draw.rect(surface, post_col, (fx, fy, 4, 10), border_radius=1)
      # Rails
      if i < num_posts - 1:
        pg.draw.rect(surface, rail_col, (fx + 2, fy + 2, 16, 2))
        pg.draw.rect(surface, rail_col, (fx + 2, fy + 6, 16, 2))
    else:
      fx = start_x
      fy = start_y + i * 16
      pg.draw.rect(surface, post_col, (fx, fy, 4, 10), border_radius=1)

# Helper: Draw Ancient Mossy Stones
def draw_mossy_stone(surface, rx, ry, w_r=12):
  pg.draw.circle(surface, (20, 25, 30, 90), (rx + 2, ry + 4), w_r)
  pg.draw.circle(surface, (140, 140, 145), (rx, ry), w_r)
  pg.draw.circle(surface, (180, 185, 190), (rx - 2, ry - 2), w_r - 3)
  # Moss on top
  pg.draw.circle(surface, (70, 165, 80, 200), (rx - 3, ry - 3), max(2, w_r // 3))

# Plant Props carefully in open, non-interfering areas:
# 1. Top-left corner (x: 20-70, y: 20-70) - open grass
draw_tree(props_surf, 48, 48, 22)
draw_tree(props_surf, 75, 40, 16)
draw_mossy_stone(props_surf, 32, 70, 7)

# 2. Beautiful Pond in top-middle area (around x: 280, y: 48)
draw_pond(props_surf, 280, 48)

# 3. Middle-left pocket (x: 180, y: 190)
draw_tree(props_surf, 180, 190, 20)
draw_fence(props_surf, 150, 220, num_posts=4, direction="h")

# 4. Center-right open pocket (x: 520, y: 240)
draw_tree(props_surf, 520, 235, 22)
draw_tree(props_surf, 545, 260, 16)
draw_mossy_stone(props_surf, 490, 250, 8)

# 5. Bottom-middle open pocket (x: 200, y: 665)
draw_fence(props_surf, 160, 680, num_posts=5, direction="h")
draw_tree(props_surf, 120, 680, 20)

# 6. Bottom-right corner (x: 650, y: 680)
draw_tree(props_surf, 660, 680, 22)
draw_mossy_stone(props_surf, 625, 685, 9)

# 7. ENTRANCE GATE (Top-right, spawn point at x=624, y=0)
# A stone fortress entrance with warning torch embers
portal_surf = pg.Surface((w, h), pg.SRCALPHA)
pg.draw.rect(portal_surf, (50, 55, 65), (600, 0, 16, 28), border_radius=3)
pg.draw.rect(portal_surf, (50, 55, 65), (632, 0, 16, 28), border_radius=3)
pg.draw.rect(portal_surf, (70, 75, 88), (595, 0, 58, 8), border_radius=2)
# Torches on entrance posts
pg.draw.circle(portal_surf, (255, 140, 30), (608, 12), 4)
pg.draw.circle(portal_surf, (255, 240, 100), (608, 12), 2)
pg.draw.circle(portal_surf, (255, 140, 30), (640, 12), 4)
pg.draw.circle(portal_surf, (255, 240, 100), (640, 12), 2)
props_surf.blit(portal_surf, (0, 0))

# 8. EXIT BASE (Bottom-left, endpoint at x=0, y=624)
base_gate = pg.Surface((w, h), pg.SRCALPHA)
# Fortified defense gate
pg.draw.rect(base_gate, (60, 45, 30), (0, 600, 18, 48), border_radius=4)
pg.draw.rect(base_gate, (110, 80, 45), (0, 605, 12, 38))
# Shield banner
pg.draw.polygon(base_gate, (40, 120, 220), [(12, 615), (24, 615), (18, 630)])
pg.draw.polygon(base_gate, (255, 215, 0), [(14, 617), (22, 617), (18, 627)])
props_surf.blit(base_gate, (0, 0))

map_surf.blit(props_surf, (0, 0))

# Step 8: Subtle Vignette & Sunlight Atmosphere
vignette = pg.Surface((w, h), pg.SRCALPHA)
# Soft warm sunlight gradient from top-left
for r in range(120, 0, -5):
  alpha = int((120 - r) * 0.15)
  pg.draw.circle(vignette, (255, 245, 200, alpha), (100, 100), r * 6)

# Outer corner subtle vignette
for i in range(16):
  v_col = (10, 15, 25, int((16 - i) * 2.5))
  pg.draw.rect(vignette, v_col, (i, i, w - i*2, h - i*2), 1)

map_surf.blit(vignette, (0, 0))

# Save enhanced map to levels/level.png
pg.image.save(map_surf, 'levels/level.png')
print("Enhanced map successfully generated and saved to levels/level.png!")
