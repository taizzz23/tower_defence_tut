import pygame as pg
from pygame.math import Vector2
import math
import random
import constants as c
from enemy_data import ENEMY_DATA
from effects import VisualEffect

class Enemy(pg.sprite.Sprite):
  def __init__(self, enemy_type, waypoints, images, start_waypoint=1, start_pos=None):
    pg.sprite.Sprite.__init__(self)
    self.enemy_type = enemy_type
    self.waypoints = waypoints
    self.images = images
    
    if start_pos is not None:
      self.pos = Vector2(start_pos)
    else:
      self.pos = Vector2(self.waypoints[0])
      
    self.target_waypoint = max(1, min(start_waypoint, len(self.waypoints) - 1))
    
    data = ENEMY_DATA.get(enemy_type, {
      "health": 10,
      "speed": 2,
      "reward": 1
    })
    
    self.health = data.get("health", 10)
    self.max_health = data.get("health", 10)
    self.base_speed = data.get("speed", 2)
    self.speed = self.base_speed
    self.reward = data.get("reward", c.KILL_REWARD)
    
    # Boss specific traits
    self.is_boss = data.get("is_boss", False)
    self.boss_name = data.get("boss_name", "BOSS")
    self.boss_title = data.get("boss_title", "")
    self.deathrattle = data.get("deathrattle", [])
    self.cc_resistance = data.get("cc_resistance", 0.0)
    self.enrage_hp_ratio = data.get("enrage_hp_ratio", 0.0)
    self.is_enraged = False
    self.aura_color = data.get("aura_color", (255, 120, 20) if self.is_boss else None)
    self.summon_type = data.get("summon_type", None)
    self.summon_cooldown = data.get("summon_cooldown", 5000)
    self.summon_timer = 0
    
    self.slow_timer = 0
    self.slow_factor = 1.0
    self.angle = 0
    
    self.original_image = images.get(enemy_type)
    if self.original_image is None:
      # Fallback to weak enemy image if missing
      self.original_image = images.get("weak")
      
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def apply_slow(self, duration_ms, factor=0.5):
    # Bosses with cc_resistance reduce slow intensity
    effective_factor = factor + (1.0 - factor) * self.cc_resistance
    self.slow_timer = duration_ms
    self.slow_factor = effective_factor

  def update(self, world, enemy_group=None, effects=None, font=None):
    # Update slow timer
    if self.slow_timer > 0:
      self.slow_timer -= (1000 / c.FPS) * world.game_speed
      if self.slow_timer <= 0:
        self.slow_factor = 1.0
        self.slow_timer = 0

    # Boss Enrage Mechanic
    if self.enrage_hp_ratio > 0 and not self.is_enraged:
      if (self.health / self.max_health) <= self.enrage_hp_ratio:
        self.is_enraged = True
        self.speed = self.base_speed * 1.35
        if effects is not None:
          effects.append(VisualEffect("shockwave", tuple(self.pos), color=(255, 40, 20), radius=75))
          if font:
            effects.append(VisualEffect("floating_text", (self.pos.x, self.pos.y - 35),
                                        text="🔥 CUỒNG NỘ +35% TỐC ĐỘ!", font=font, color=(255, 60, 60)))

    # Boss Summoning Mechanic (e.g. Void Overlord)
    if self.summon_type and enemy_group is not None and self.health > 0:
      self.summon_timer += (1000 / c.FPS) * world.game_speed
      if self.summon_timer >= self.summon_cooldown:
        self.summon_timer = 0
        # Summon 2 minions at current position along path
        for _ in range(2):
          s_off = Vector2(random.uniform(-12, 12), random.uniform(-12, 12))
          minion = Enemy(self.summon_type, self.waypoints, self.images,
                         start_waypoint=self.target_waypoint, start_pos=self.pos + s_off)
          enemy_group.add(minion)
          world.total_enemies += 1
          
        if effects is not None:
          effects.append(VisualEffect("shockwave", tuple(self.pos), color=(180, 50, 255), radius=85))
          if font:
            effects.append(VisualEffect("floating_text", (self.pos.x, self.pos.y - 30),
                                        text="⚡ TRIỆU HỒI HƯ KHÔNG!", font=font, color=(200, 100, 255)))

    self.move(world)
    self.rotate()
    self.check_alive(world, enemy_group, effects, font)

  def move(self, world):
    # Define target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      # Enemy reached the castle gate
      self.kill()
      # Bosses breach castle for massive damage!
      damage = 10 if self.is_boss else 1
      world.health -= damage
      world.missed_enemies += 1
      if self.is_boss:
        world.screen_shake = 16
      return

    # Calculate distance to target
    dist = self.movement.length()
    effective_speed = self.speed * self.slow_factor * world.game_speed
    
    if dist >= effective_speed:
      self.pos += self.movement.normalize() * effective_speed
    else:
      if dist != 0:
        self.pos += self.movement.normalize() * dist
      self.target_waypoint += 1

  def rotate(self):
    dist = self.target - self.pos
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def check_alive(self, world, enemy_group=None, effects=None, font=None):
    if self.health <= 0:
      world.killed_enemies += 1
      world.money += self.reward
      
      # Visual celebration upon death
      if self.is_boss:
        world.screen_shake = 12
        if effects is not None:
          effects.append(VisualEffect("boss_explosion", tuple(self.pos), radius=140))
          if font:
            effects.append(VisualEffect("floating_text", (self.pos.x, self.pos.y - 45),
                                        text=f"👑 +{self.reward}$ TIÊU DIỆT TRÙM!", font=font, color=(255, 215, 0)))
      else:
        if effects is not None and self.reward > 1 and font:
          effects.append(VisualEffect("floating_text", (self.pos.x, self.pos.y - 25),
                                      text=f"+{self.reward}$", font=font, color=(255, 230, 100)))

      # Spawn Deathrattle Children Minions
      if self.deathrattle and enemy_group is not None:
        for child_type in self.deathrattle:
          c_off = Vector2(random.uniform(-14, 14), random.uniform(-14, 14))
          child = Enemy(child_type, self.waypoints, self.images,
                        start_waypoint=self.target_waypoint, start_pos=self.pos + c_off)
          enemy_group.add(child)
          world.total_enemies += 1

      self.kill()

  def draw_aura(self, surface):
    """Draw pulsating glowing aura under boss sprites."""
    if not self.is_boss or not self.aura_color:
      return
    
    ticks = pg.time.get_ticks()
    pulse = (math.sin(ticks * 0.006) + 1.0) * 0.5 # 0.0 to 1.0
    base_rad = 38 if not self.is_enraged else 44
    rad = int(base_rad + 8 * pulse)
    
    r, g, b = self.aura_color
    aura_surf = pg.Surface((rad * 2, rad * 2), pg.SRCALPHA)
    
    # Outer pulsating aura ring
    alpha = int(70 + 60 * pulse) if not self.is_enraged else int(110 + 90 * pulse)
    pg.draw.circle(aura_surf, (r, g, b, alpha), (rad, rad), rad)
    pg.draw.circle(aura_surf, (255, 255, 255, int(alpha * 0.7)), (rad, rad), int(rad * 0.65))
    
    surface.blit(aura_surf, (self.pos.x - rad, self.pos.y - rad))

  def draw_health_bar(self, surface, font=None):
    health_ratio = max(0.0, self.health / self.max_health)
    
    if self.is_boss:
      # Epic Boss In-Field Health Bar
      bar_width = 56
      bar_height = 6
      x = int(self.pos.x - bar_width // 2)
      y = int(self.pos.y - 32)
      
      # Outer shadow
      pg.draw.rect(surface, (10, 10, 15), (x - 2, y - 2, bar_width + 4, bar_height + 4), border_radius=3)
      # Missing health (dark crimson)
      pg.draw.rect(surface, (80, 15, 20), (x, y, bar_width, bar_height), border_radius=2)
      # Current health (Golden/crimson gradient)
      fill_color = (255, 215, 50) if health_ratio > 0.4 else (255, 60, 40)
      if self.is_enraged:
        fill_color = (255, 40, 20)
      pg.draw.rect(surface, fill_color, (x, y, int(bar_width * health_ratio), bar_height), border_radius=2)
      # Gold border
      border_col = (255, 215, 0) if not self.is_enraged else (255, 90, 40)
      pg.draw.rect(surface, border_col, (x - 1, y - 1, bar_width + 2, bar_height + 2), 1, border_radius=2)
      
      # Mini Crown badge
      pg.draw.circle(surface, (255, 215, 0), (x - 4, y + 3), 3)

    else:
      # Regular Creep Health Bar
      bar_width = 30
      bar_height = 4
      x = int(self.pos.x - bar_width // 2)
      y = int(self.pos.y - 24)
      
      pg.draw.rect(surface, "red", (x, y, bar_width, bar_height))
      pg.draw.rect(surface, "green", (x, y, int(bar_width * health_ratio), bar_height))
      
      if self.slow_timer > 0:
        pg.draw.rect(surface, (80, 220, 255), (x - 1, y - 1, bar_width + 2, bar_height + 2), 1)
        pg.draw.circle(surface, (130, 235, 255), (x - 4, y + 2), 3)
      else:
        pg.draw.rect(surface, "black", (x, y, bar_width, bar_height), 1)