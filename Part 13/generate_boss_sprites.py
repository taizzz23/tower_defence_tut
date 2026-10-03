import pygame as pg
import math
import os

pg.init()
screen = pg.display.set_mode((1, 1), pg.NOFRAME)

output_dir = 'assets/images/enemies'
os.makedirs(output_dir, exist_ok=True)

def draw_circle_alpha(surface, color, center, radius, width=0):
  target_rect = pg.Rect(center[0] - radius, center[1] - radius, 2 * radius, 2 * radius)
  shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
  pg.draw.circle(shape_surf, color, (radius, radius), radius, width)
  surface.blit(shape_surf, target_rect)

# -------------------------------------------------------------
# 1. BOSS TITAN GOLEM (Wave 10) - Heavy Rock & Magma Colossus
# -------------------------------------------------------------
def create_boss_titan():
  size = 96
  surf = pg.Surface((size, size), pg.SRCALPHA)
  cx, cy = size // 2, size // 2

  # Outer Magma glow
  draw_circle_alpha(surf, (255, 90, 20, 45), (cx, cy), 42)
  draw_circle_alpha(surf, (255, 140, 30, 60), (cx, cy), 36)

  # Stone Body Plates (Obsidian & Granite)
  pg.draw.circle(surf, (45, 48, 55), (cx, cy), 32)
  pg.draw.circle(surf, (65, 70, 80), (cx, cy), 30)

  # Heavy Shoulder Pauldrons
  pg.draw.circle(surf, (35, 38, 44), (cx - 10, cy - 22), 16)
  pg.draw.circle(surf, (75, 80, 92), (cx - 10, cy - 22), 14)
  pg.draw.circle(surf, (35, 38, 44), (cx - 10, cy + 22), 16)
  pg.draw.circle(surf, (75, 80, 92), (cx - 10, cy + 22), 14)

  # Spikes on Pauldrons
  pg.draw.polygon(surf, (25, 28, 33), [(cx - 12, cy - 36), (cx - 6, cy - 22), (cx - 18, cy - 22)])
  pg.draw.polygon(surf, (25, 28, 33), [(cx - 12, cy + 36), (cx - 6, cy + 22), (cx - 18, cy + 22)])

  # Magma Cracks across the body
  cracks = [
    [(cx - 18, cy - 8), (cx - 6, cy - 2), (cx + 8, cy - 14), (cx + 18, cy - 10)],
    [(cx - 15, cy + 10), (cx - 2, cy + 5), (cx + 12, cy + 12), (cx + 20, cy + 8)],
    [(cx - 22, cy), (cx - 5, cy), (cx + 6, cy - 4), (cx + 14, cy + 2)],
    [(cx - 8, cy - 20), (cx - 2, cy - 12), (cx + 4, cy - 18)]
  ]
  for crack in cracks:
    pg.draw.lines(surf, (255, 80, 10), False, crack, 4)
    pg.draw.lines(surf, (255, 200, 50), False, crack, 2)

  # Glowing Magma Core (Chest)
  pg.draw.circle(surf, (220, 50, 10), (cx + 4, cy), 14)
  pg.draw.circle(surf, (255, 140, 20), (cx + 4, cy), 10)
  pg.draw.circle(surf, (255, 240, 100), (cx + 4, cy), 6)

  # Stone Brow & Head facing right
  pg.draw.polygon(surf, (45, 50, 58), [
    (cx + 16, cy - 14), (cx + 34, cy - 8), (cx + 38, cy), (cx + 34, cy + 8), (cx + 16, cy + 14)
  ])
  pg.draw.polygon(surf, (70, 76, 88), [
    (cx + 18, cy - 12), (cx + 32, cy - 6), (cx + 35, cy), (cx + 32, cy + 6), (cx + 18, cy + 12)
  ])

  # Glowing Lava Eyes
  pg.draw.circle(surf, (255, 40, 10), (cx + 26, cy - 6), 5)
  pg.draw.circle(surf, (255, 230, 80), (cx + 26, cy - 6), 3)
  pg.draw.circle(surf, (255, 40, 10), (cx + 26, cy + 6), 5)
  pg.draw.circle(surf, (255, 230, 80), (cx + 26, cy + 6), 3)

  # Granite rim highlight
  pg.draw.circle(surf, (140, 150, 165), (cx, cy), 32, 2)
  return surf

# -------------------------------------------------------------
# 2. BOSS DREADNOUGHT (Wave 20) - Infernal War Cruiser
# -------------------------------------------------------------
def create_boss_dreadnought():
  size = 104
  surf = pg.Surface((size, size), pg.SRCALPHA)
  cx, cy = size // 2, size // 2

  # Red Plasma Shield Aura
  draw_circle_alpha(surf, (230, 20, 40, 40), (cx, cy), 48)
  draw_circle_alpha(surf, (255, 80, 20, 60), (cx, cy), 42)

  # Thruster Exhausts at Left (back)
  pg.draw.rect(surf, (30, 32, 40), (cx - 44, cy - 24, 18, 12), border_radius=3)
  pg.draw.rect(surf, (30, 32, 40), (cx - 44, cy + 12, 18, 12), border_radius=3)
  # Thruster flame jets
  pg.draw.polygon(surf, (255, 100, 20), [(cx - 44, cy - 18), (cx - 58, cy - 18), (cx - 44, cy - 23)])
  pg.draw.polygon(surf, (255, 220, 80), [(cx - 44, cy - 18), (cx - 52, cy - 18), (cx - 44, cy - 21)])
  pg.draw.polygon(surf, (255, 100, 20), [(cx - 44, cy + 18), (cx - 58, cy + 18), (cx - 44, cy + 13)])
  pg.draw.polygon(surf, (255, 220, 80), [(cx - 44, cy + 18), (cx - 52, cy + 18), (cx - 44, cy + 15)])

  # Main Armored Hull (Aggressive wedge pointing right)
  hull_outer = [
    (cx - 36, cy - 28),
    (cx + 8, cy - 32),
    (cx + 36, cy - 16),
    (cx + 48, cy),
    (cx + 36, cy + 16),
    (cx + 8, cy + 32),
    (cx - 36, cy + 28),
    (cx - 24, cy)
  ]
  pg.draw.polygon(surf, (30, 32, 40), hull_outer)
  
  hull_inner = [
    (cx - 32, cy - 24),
    (cx + 6, cy - 28),
    (cx + 32, cy - 14),
    (cx + 44, cy),
    (cx + 32, cy + 14),
    (cx + 6, cy + 28),
    (cx - 32, cy + 24),
    (cx - 20, cy)
  ]
  pg.draw.polygon(surf, (150, 25, 35), hull_inner)

  # Armor plating stripes (Crimson & Charcoal)
  center_spine = [
    (cx - 20, cy - 12),
    (cx + 16, cy - 14),
    (cx + 34, cy),
    (cx + 16, cy + 14),
    (cx - 20, cy + 12)
  ]
  pg.draw.polygon(surf, (200, 40, 50), center_spine)
  pg.draw.polygon(surf, (40, 44, 55), [
    (cx - 16, cy - 8), (cx + 12, cy - 10), (cx + 26, cy), (cx + 12, cy + 10), (cx - 16, cy + 8)
  ])

  # Side Turbo-Cannons
  pg.draw.rect(surf, (70, 75, 88), (cx + 2, cy - 24, 24, 6), border_radius=2)
  pg.draw.rect(surf, (20, 22, 28), (cx + 22, cy - 25, 8, 8), border_radius=2)
  pg.draw.rect(surf, (70, 75, 88), (cx + 2, cy + 18, 24, 6), border_radius=2)
  pg.draw.rect(surf, (20, 22, 28), (cx + 22, cy + 17, 8, 8), border_radius=2)

  # Glowing Bridge Optics (Forward Sensor Cockpit)
  pg.draw.polygon(surf, (255, 230, 80), [(cx + 24, cy - 4), (cx + 38, cy), (cx + 24, cy + 4)])
  pg.draw.polygon(surf, (255, 255, 255), [(cx + 28, cy - 2), (cx + 36, cy), (cx + 28, cy + 2)])

  # Reactor Core on Top
  pg.draw.circle(surf, (255, 80, 20), (cx, cy), 9)
  pg.draw.circle(surf, (255, 220, 100), (cx, cy), 5)
  pg.draw.circle(surf, (255, 255, 255), (cx, cy), 2)

  # Hazard Stripes
  for hx in [-8, 0, 8]:
    pg.draw.line(surf, (255, 200, 40), (cx + hx, cy - 22), (cx + hx + 4, cy - 16), 2)
    pg.draw.line(surf, (255, 200, 40), (cx + hx, cy + 22), (cx + hx + 4, cy + 16), 2)

  # Edge highlights
  pg.draw.lines(surf, (255, 120, 120), True, hull_outer, 2)
  return surf

# -------------------------------------------------------------
# 3. BOSS VOID OVERLORD (Wave 30) - Eldritch Cosmic Entity
# -------------------------------------------------------------
def create_boss_overlord():
  size = 112
  surf = pg.Surface((size, size), pg.SRCALPHA)
  cx, cy = size // 2, size // 2

  # Void Cosmic Aura (Deep purple & neon cyan pulsating rings)
  draw_circle_alpha(surf, (60, 20, 100, 50), (cx, cy), 52)
  draw_circle_alpha(surf, (120, 40, 220, 65), (cx, cy), 44)
  draw_circle_alpha(surf, (0, 240, 255, 35), (cx, cy), 38)

  # Orbiting Void Dark Matter Orbs
  orb_angles = [30, 150, 270]
  for oa in orb_angles:
    rad = math.radians(oa)
    ox = int(cx + 42 * math.cos(rad))
    oy = int(cy + 42 * math.sin(rad))
    draw_circle_alpha(surf, (0, 255, 255, 100), (ox, oy), 10)
    pg.draw.circle(surf, (20, 10, 35), (ox, oy), 7)
    pg.draw.circle(surf, (160, 60, 255), (ox, oy), 4)
    pg.draw.circle(surf, (0, 255, 255), (ox, oy), 2)

  # Carapace / Mantle (Deep purple obsidian shell)
  carapace = [
    (cx - 36, cy - 30),
    (cx - 10, cy - 40),
    (cx + 20, cy - 30),
    (cx + 46, cy),
    (cx + 20, cy + 30),
    (cx - 10, cy + 40),
    (cx - 36, cy + 30),
    (cx - 24, cy)
  ]
  pg.draw.polygon(surf, (20, 12, 32), carapace)
  pg.draw.polygon(surf, (48, 22, 78), [
    (cx - 30, cy - 24), (cx - 8, cy - 32), (cx + 16, cy - 24), (cx + 40, cy),
    (cx + 16, cy + 24), (cx - 8, cy + 32), (cx - 30, cy + 24), (cx - 18, cy)
  ])

  # Menacing Void Horns
  pg.draw.polygon(surf, (25, 14, 40), [(cx - 4, cy - 32), (cx + 24, cy - 46), (cx + 14, cy - 24)])
  pg.draw.polygon(surf, (140, 60, 230), [(cx - 2, cy - 30), (cx + 22, cy - 44), (cx + 12, cy - 24)])
  pg.draw.polygon(surf, (25, 14, 40), [(cx - 4, cy + 32), (cx + 24, cy + 46), (cx + 14, cy + 24)])
  pg.draw.polygon(surf, (140, 60, 230), [(cx - 2, cy + 30), (cx + 22, cy + 44), (cx + 12, cy + 24)])

  # Neon Cyan Runes on Shell
  rune_lines = [
    [(cx - 18, cy - 16), (cx - 4, cy - 22), (cx + 12, cy - 18)],
    [(cx - 18, cy + 16), (cx - 4, cy + 22), (cx + 12, cy + 18)],
    [(cx - 12, cy - 8), (cx + 6, cy - 10), (cx + 24, cy - 4)],
    [(cx - 12, cy + 8), (cx + 6, cy + 10), (cx + 24, cy + 4)]
  ]
  for r_line in rune_lines:
    pg.draw.lines(surf, (0, 220, 255), False, r_line, 2)

  # Central Eye of the Void (Glaring rightward)
  pg.draw.circle(surf, (15, 8, 25), (cx + 10, cy), 16)
  pg.draw.circle(surf, (180, 40, 255), (cx + 10, cy), 13)
  pg.draw.circle(surf, (0, 240, 255), (cx + 12, cy), 9)
  # Vertical Cat/Demon Pupil
  pg.draw.ellipse(surf, (10, 5, 20), (cx + 12, cy - 8, 5, 16))
  pg.draw.circle(surf, (255, 255, 255), (cx + 15, cy - 3), 2)

  # Crown of Shadows
  pg.draw.lines(surf, (200, 100, 255), True, carapace, 2)
  return surf

# -------------------------------------------------------------
# 4. BOSS CHAOS LEVIATHAN (Wave 40) - Ancient Golden-Crimson Dragon Tyrant
# -------------------------------------------------------------
def create_boss_leviathan():
  size = 120
  surf = pg.Surface((size, size), pg.SRCALPHA)
  cx, cy = size // 2, size // 2

  # Supernova Solar & Chaos Flame Aura
  draw_circle_alpha(surf, (255, 50, 20, 45), (cx, cy), 58)
  draw_circle_alpha(surf, (255, 180, 20, 60), (cx, cy), 50)
  draw_circle_alpha(surf, (255, 240, 100, 75), (cx, cy), 40)

  # Giant Blazing Energy Wings (Upper and Lower)
  upper_wing = [(cx - 24, cy - 16), (cx - 10, cy - 54), (cx + 18, cy - 46), (cx + 8, cy - 18)]
  lower_wing = [(cx - 24, cy + 16), (cx - 10, cy + 54), (cx + 18, cy + 46), (cx + 8, cy + 18)]
  pg.draw.polygon(surf, (180, 30, 20), upper_wing)
  pg.draw.polygon(surf, (255, 140, 20), [(cx - 20, cy - 18), (cx - 8, cy - 48), (cx + 14, cy - 42), (cx + 6, cy - 18)])
  pg.draw.polygon(surf, (255, 230, 80), [(cx - 16, cy - 20), (cx - 6, cy - 42), (cx + 10, cy - 36), (cx + 4, cy - 20)])

  pg.draw.polygon(surf, (180, 30, 20), lower_wing)
  pg.draw.polygon(surf, (255, 140, 20), [(cx - 20, cy + 18), (cx - 8, cy + 48), (cx + 14, cy + 42), (cx + 6, cy + 18)])
  pg.draw.polygon(surf, (255, 230, 80), [(cx - 16, cy + 20), (cx - 6, cy + 42), (cx + 10, cy + 36), (cx + 4, cy + 20)])

  # Draconic Armored Body
  dragon_hull = [
    (cx - 44, cy - 18),
    (cx - 12, cy - 26),
    (cx + 24, cy - 22),
    (cx + 52, cy),
    (cx + 24, cy + 22),
    (cx - 12, cy + 26),
    (cx - 44, cy + 18),
    (cx - 32, cy)
  ]
  pg.draw.polygon(surf, (60, 15, 18), dragon_hull)
  pg.draw.polygon(surf, (170, 35, 30), [
    (cx - 38, cy - 14), (cx - 10, cy - 22), (cx + 20, cy - 18), (cx + 46, cy),
    (cx + 20, cy + 18), (cx - 10, cy + 22), (cx - 38, cy + 14), (cx - 28, cy)
  ])

  # Golden Dragon Scales along spine
  for sx in range(-24, 25, 12):
    scale_pts = [(cx + sx - 5, cy - 10), (cx + sx + 5, cy), (cx + sx - 5, cy + 10), (cx + sx - 8, cy)]
    pg.draw.polygon(surf, (255, 215, 0), scale_pts)
    pg.draw.polygon(surf, (255, 245, 160), [(cx + sx - 3, cy - 6), (cx + sx + 3, cy), (cx + sx - 3, cy + 6)])

  # Golden Crown Horns
  pg.draw.polygon(surf, (255, 195, 0), [(cx + 12, cy - 18), (cx + 38, cy - 36), (cx + 26, cy - 14)])
  pg.draw.polygon(surf, (255, 245, 120), [(cx + 14, cy - 17), (cx + 36, cy - 34), (cx + 25, cy - 14)])
  pg.draw.polygon(surf, (255, 195, 0), [(cx + 12, cy + 18), (cx + 38, cy + 36), (cx + 26, cy + 14)])
  pg.draw.polygon(surf, (255, 245, 120), [(cx + 14, cy + 17), (cx + 36, cy + 34), (cx + 25, cy + 14)])

  # Fierce Golden/Crimson Head
  head_pts = [(cx + 26, cy - 12), (cx + 52, cy), (cx + 26, cy + 12)]
  pg.draw.polygon(surf, (220, 45, 35), head_pts)
  pg.draw.polygon(surf, (255, 215, 0), [(cx + 28, cy - 9), (cx + 48, cy), (cx + 28, cy + 9)])

  # Blazing Dragon Eyes
  pg.draw.circle(surf, (255, 255, 255), (cx + 38, cy - 5), 4)
  pg.draw.circle(surf, (255, 0, 0), (cx + 39, cy - 5), 2)
  pg.draw.circle(surf, (255, 255, 255), (cx + 38, cy + 5), 4)
  pg.draw.circle(surf, (255, 0, 0), (cx + 39, cy + 5), 2)

  # Divine Reactor Chest Core
  pg.draw.circle(surf, (255, 100, 0), (cx, cy), 14)
  pg.draw.circle(surf, (255, 220, 50), (cx, cy), 10)
  pg.draw.circle(surf, (255, 255, 255), (cx, cy), 5)

  # Border glow
  pg.draw.lines(surf, (255, 220, 80), True, dragon_hull, 2)
  return surf

# -------------------------------------------------------------
# 5. VOID PHANTOM (Swift Stealth Creep)
# -------------------------------------------------------------
def create_void_phantom():
  size = 64
  surf = pg.Surface((size, size), pg.SRCALPHA)
  cx, cy = size // 2, size // 2

  draw_circle_alpha(surf, (150, 40, 255, 60), (cx, cy), 26)
  
  # Sleek dart shape pointing right
  body = [(cx - 22, cy - 14), (cx + 24, cy), (cx - 22, cy + 14), (cx - 14, cy)]
  pg.draw.polygon(surf, (30, 10, 50), body)
  pg.draw.polygon(surf, (180, 50, 255), [(cx - 18, cy - 10), (cx + 18, cy), (cx - 18, cy + 10), (cx - 10, cy)])
  pg.draw.polygon(surf, (0, 240, 255), [(cx - 10, cy - 4), (cx + 12, cy), (cx - 10, cy + 4)])

  # Tail trail streaks
  pg.draw.line(surf, (0, 255, 255), (cx - 24, cy - 8), (cx - 30, cy - 12), 2)
  pg.draw.line(surf, (0, 255, 255), (cx - 24, cy + 8), (cx - 30, cy + 12), 2)
  return surf

# -------------------------------------------------------------
# 6. MINI GOLEM (Rock Minion)
# -------------------------------------------------------------
def create_mini_golem():
  size = 56
  surf = pg.Surface((size, size), pg.SRCALPHA)
  cx, cy = size // 2, size // 2

  draw_circle_alpha(surf, (255, 100, 30, 40), (cx, cy), 24)
  pg.draw.circle(surf, (55, 60, 70), (cx, cy), 18)
  pg.draw.circle(surf, (80, 88, 100), (cx, cy), 15)

  # Magma crack
  pg.draw.lines(surf, (255, 120, 20), False, [(cx - 10, cy - 6), (cx, cy), (cx + 8, cy - 4)], 3)
  pg.draw.lines(surf, (255, 220, 80), False, [(cx - 10, cy - 6), (cx, cy), (cx + 8, cy - 4)], 1)

  # Magma eye
  pg.draw.circle(surf, (255, 50, 10), (cx + 10, cy), 4)
  pg.draw.circle(surf, (255, 240, 90), (cx + 10, cy), 2)
  return surf

# -------------------------------------------------------------
# 7. MINI DREAD FIGHTER (Dread Minion)
# -------------------------------------------------------------
def create_mini_dread():
  size = 56
  surf = pg.Surface((size, size), pg.SRCALPHA)
  cx, cy = size // 2, size // 2

  draw_circle_alpha(surf, (255, 30, 30, 40), (cx, cy), 24)
  fighter_pts = [(cx - 18, cy - 12), (cx + 20, cy), (cx - 18, cy + 12), (cx - 12, cy)]
  pg.draw.polygon(surf, (40, 42, 50), fighter_pts)
  pg.draw.polygon(surf, (200, 40, 50), [(cx - 14, cy - 8), (cx + 14, cy), (cx - 14, cy + 8), (cx - 8, cy)])
  pg.draw.circle(surf, (255, 230, 80), (cx + 4, cy), 3)
  return surf

# Generate and save all sprites
sprites = {
  'boss_titan.png': create_boss_titan(),
  'boss_dreadnought.png': create_boss_dreadnought(),
  'boss_overlord.png': create_boss_overlord(),
  'boss_leviathan.png': create_boss_leviathan(),
  'void_phantom.png': create_void_phantom(),
  'boss_minion_golem.png': create_mini_golem(),
  'boss_minion_dread.png': create_mini_dread()
}

for name, s in sprites.items():
  filepath = os.path.join(output_dir, name)
  pg.image.save(s, filepath)
  print(f"Generated {filepath} ({s.get_size()})")

print("All Boss & Creep sprites successfully generated!")
