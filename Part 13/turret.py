import pygame as pg
import math
import constants as c
from turret_data import TURRET_TYPES, UPGRADE_PATHS
from effects import VisualEffect

TURRET_ASSETS = {}

def get_turret_assets(turret_type):
  if turret_type not in TURRET_ASSETS:
    base = pg.image.load(f'assets/images/new_turrets/{turret_type}_base.png').convert_alpha()
    sheets = [pg.image.load(f'assets/images/new_turrets/{turret_type}_level_{lvl}.png').convert_alpha() for lvl in range(1, 5)]
    TURRET_ASSETS[turret_type] = {"base": base, "sheets": sheets}
  return TURRET_ASSETS[turret_type]

class Turret(pg.sprite.Sprite):
  def __init__(self, sprite_sheets, tile_x, tile_y, shot_fx, turret_type="gunner"):
    pg.sprite.Sprite.__init__(self)
    self.turret_type = turret_type
    self.type_data = TURRET_TYPES.get(turret_type, TURRET_TYPES["gunner"])
    self.color_tint = self.type_data.get("color_tint", (255, 255, 255))
    
    # 3-Path Upgrades tracking: [Path 1 tier, Path 2 tier, Path 3 tier]
    self.paths = [0, 0, 0]
    self.total_spent = self.type_data.get("cost", 200)
    self.upgrade_level = 1

    # Base Stats
    base = self.type_data.get("base_stats", {"range": 95, "cooldown": 900, "damage": 8})
    self.range = base["range"]
    self.cooldown = base["cooldown"]
    self.damage = base["damage"]
    self.splash_radius = self.type_data.get("splash_radius", 70)
    self.splash_damage = self.type_data.get("splash_damage", 10)
    self.slow_factor = self.type_data.get("slow_factor", 0.5)
    self.slow_duration = self.type_data.get("slow_duration", 2500)
    self.multi_shot = 1
    self.bouncing = 0

    self.last_shot = pg.time.get_ticks()
    self.selected = False
    self.target = None

    #position variables
    self.tile_x = tile_x
    self.tile_y = tile_y
    self.x = (self.tile_x + 0.5) * c.TILE_SIZE
    self.y = (self.tile_y + 0.5) * c.TILE_SIZE
    self.shot_fx = shot_fx

    #load custom base and weapon spritesheets
    assets = get_turret_assets(self.turret_type)
    self.base_image = assets["base"]
    self.sprite_sheets = assets["sheets"]
    self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
    self.frame_index = 0
    self.update_time = pg.time.get_ticks()

    #update image
    self.angle = 90
    self.original_image = self.animation_list[self.frame_index]
    self.image = pg.transform.rotate(self.original_image, self.angle - 90)
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)

    self.create_range_circle()

  def get_sell_value(self):
    # Returns 70% of total gold invested
    return max(50, int(self.total_spent * 0.70))

  def can_upgrade_path(self, path_idx):
    return self.paths[path_idx] < 3

  def get_path_tier_info(self, path_idx):
    current_tier = self.paths[path_idx]
    path_data = UPGRADE_PATHS[self.turret_type][path_idx]
    if current_tier < 3:
      return path_data["tiers"][current_tier]
    return None

  def upgrade_path(self, path_idx):
    if not self.can_upgrade_path(path_idx):
      return 0
    
    tier_info = self.get_path_tier_info(path_idx)
    if not tier_info:
      return 0

    cost = tier_info["cost"]
    self.total_spent += cost
    self.paths[path_idx] += 1
    stat = tier_info.get("stat", {})

    # Apply stat enhancements
    if "damage" in stat:
      self.damage += stat["damage"]
    if "cooldown_pct" in stat:
      self.cooldown = max(200, int(self.cooldown * (1.0 - stat["cooldown_pct"])))
    if "range" in stat:
      self.range += stat["range"]
    if "splash_radius" in stat:
      self.splash_radius += stat["splash_radius"]
    if "splash_damage" in stat:
      self.splash_damage += stat["splash_damage"]
    if "slow_factor" in stat:
      self.slow_factor = min(self.slow_factor, stat["slow_factor"])
    if "slow_duration" in stat:
      self.slow_duration += stat["slow_duration"]
    if "multi_shot" in stat:
      self.multi_shot = stat["multi_shot"]
    if "bouncing" in stat:
      self.bouncing = stat["bouncing"]

    # Evolve visual appearance based on total upgrades bought
    total_tiers = sum(self.paths)
    new_lvl = min(4, 1 + total_tiers // 2)
    if new_lvl != self.upgrade_level:
      self.upgrade_level = new_lvl
      self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
      self.original_image = self.animation_list[self.frame_index]

    self.create_range_circle()
    return cost

  def create_range_circle(self):
    disp_range = min(self.range, 350)
    self.range_image = pg.Surface((disp_range * 2, disp_range * 2))
    self.range_image.fill((0, 0, 0))
    self.range_image.set_colorkey((0, 0, 0))
    
    ring_color = self.color_tint if self.color_tint != (255, 255, 255) else (200, 200, 200)
    pg.draw.circle(self.range_image, ring_color, (disp_range, disp_range), disp_range)
    self.range_image.set_alpha(80)
    self.range_rect = self.range_image.get_rect()
    self.range_rect.center = (self.x, self.y)

  def load_images(self, sprite_sheet):
    size = sprite_sheet.get_height()
    animation_list = []
    for x in range(c.ANIMATION_STEPS):
      temp_img = sprite_sheet.subsurface(x * size, 0, size, size)
      animation_list.append(temp_img)
    return animation_list

  def update(self, enemy_group, world, effects=None):
    if self.target:
      self.play_animation()
    else:
      if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):
        self.pick_target(enemy_group, effects)

  def pick_target(self, enemy_group, effects=None):
    if self.turret_type == "sniper":
      best_enemy = None
      best_progress = -1
      for enemy in enemy_group:
        if enemy.health > 0:
          dist_to_next = (enemy.target - enemy.pos).length() if hasattr(enemy, 'target') else 0
          progress = enemy.target_waypoint * 10000 - dist_to_next
          if progress > best_progress:
            best_progress = progress
            best_enemy = enemy

      if best_enemy:
        self.target = best_enemy
        x_dist = self.target.pos[0] - self.x
        y_dist = self.target.pos[1] - self.y
        self.angle = math.degrees(math.atan2(-y_dist, x_dist))
        self.target.health -= self.damage
        if self.shot_fx:
          self.shot_fx.play()
        if effects is not None:
          effects.append(VisualEffect("sniper_beam", (self.x, self.y), target_pos=tuple(self.target.pos)))

        # Bouncing bullet path upgrade
        if self.bouncing > 0:
          bounce_targets = []
          for other in enemy_group:
            if other != self.target and other.health > 0:
              d = (other.pos - self.target.pos).length()
              if d <= 120:
                bounce_targets.append(other)
          for b_target in bounce_targets[:self.bouncing]:
            b_target.health -= int(self.damage * 0.6)
            if effects is not None:
              effects.append(VisualEffect("sniper_beam", tuple(self.target.pos), target_pos=tuple(b_target.pos)))

    elif self.turret_type == "ice":
      enemies_in_range = []
      for enemy in enemy_group:
        if enemy.health > 0:
          dist = math.hypot(enemy.pos[0] - self.x, enemy.pos[1] - self.y)
          if dist < self.range:
            enemies_in_range.append(enemy)

      if len(enemies_in_range) > 0:
        self.target = enemies_in_range[0]
        x_dist = self.target.pos[0] - self.x
        y_dist = self.target.pos[1] - self.y
        self.angle = math.degrees(math.atan2(-y_dist, x_dist))
        
        for enemy in enemies_in_range:
          enemy.health -= self.damage
          enemy.apply_slow(self.slow_duration, self.slow_factor)

        if self.shot_fx:
          self.shot_fx.play()
        if effects is not None:
          effects.append(VisualEffect("ice_wave", (self.x, self.y), radius=self.range))

    elif self.turret_type == "bomb":
      for enemy in enemy_group:
        if enemy.health > 0:
          dist = math.hypot(enemy.pos[0] - self.x, enemy.pos[1] - self.y)
          if dist < self.range:
            self.target = enemy
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            self.angle = math.degrees(math.atan2(-y_dist, x_dist))

            self.target.health -= self.damage
            for other in enemy_group:
              if other != self.target and other.health > 0:
                s_dist = math.hypot(other.pos[0] - self.target.pos[0], other.pos[1] - self.target.pos[1])
                if s_dist <= self.splash_radius:
                  other.health -= self.splash_damage

            if self.shot_fx:
              self.shot_fx.play()
            if effects is not None:
              effects.append(VisualEffect("explosion", tuple(self.target.pos), radius=self.splash_radius))
            break

    else:
      # Gunner
      targets = []
      for enemy in enemy_group:
        if enemy.health > 0:
          dist = math.hypot(enemy.pos[0] - self.x, enemy.pos[1] - self.y)
          if dist < self.range:
            targets.append(enemy)
            if len(targets) >= self.multi_shot:
              break

      if len(targets) > 0:
        self.target = targets[0]
        x_dist = self.target.pos[0] - self.x
        y_dist = self.target.pos[1] - self.y
        self.angle = math.degrees(math.atan2(-y_dist, x_dist))
        
        for t in targets:
          t.health -= self.damage
        if self.shot_fx:
          self.shot_fx.play()

  def play_animation(self):
    self.original_image = self.animation_list[self.frame_index]
    if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
      self.update_time = pg.time.get_ticks()
      self.frame_index += 1
      if self.frame_index >= len(self.animation_list):
        self.frame_index = 0
        self.last_shot = pg.time.get_ticks()
        self.target = None

  def draw(self, surface):
    # 1. Draw stationary base pedestal
    surface.blit(self.base_image, (self.x - 48, self.y - 48))
    # 2. Draw rotating weapon head
    self.image = pg.transform.rotate(self.original_image, self.angle - 90)
    self.rect = self.image.get_rect()
    self.rect.center = (self.x, self.y)
    surface.blit(self.image, self.rect)
    # 3. Draw range circle if selected
    if self.selected:
      surface.blit(self.range_image, self.range_rect)