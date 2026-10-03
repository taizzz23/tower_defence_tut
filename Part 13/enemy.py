import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
  def __init__(self, enemy_type, waypoints, images):
    pg.sprite.Sprite.__init__(self)
    self.waypoints = waypoints
    self.pos = Vector2(self.waypoints[0])
    self.target_waypoint = 1
    self.health = ENEMY_DATA.get(enemy_type)["health"]
    self.max_health = ENEMY_DATA.get(enemy_type)["health"]
    self.speed = ENEMY_DATA.get(enemy_type)["speed"]
    self.slow_timer = 0
    self.slow_factor = 1.0
    self.angle = 0
    self.original_image = images.get(enemy_type)
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def apply_slow(self, duration_ms, factor=0.5):
    self.slow_timer = duration_ms
    self.slow_factor = factor

  def update(self, world):
    # Update slow timer
    if self.slow_timer > 0:
      self.slow_timer -= (1000 / c.FPS) * world.game_speed
      if self.slow_timer <= 0:
        self.slow_factor = 1.0
        self.slow_timer = 0

    self.move(world)
    self.rotate()
    self.check_alive(world)

  def move(self, world):
    #define a target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      #enemy has reached the end of the path
      self.kill()
      world.health -= 1
      world.missed_enemies += 1

    #calculate distance to target
    dist = self.movement.length()
    effective_speed = self.speed * self.slow_factor * world.game_speed
    #check if remaining distance is greater than the enemy speed
    if dist >= effective_speed:
      self.pos += self.movement.normalize() * effective_speed
    else:
      if dist != 0:
        self.pos += self.movement.normalize() * dist
      self.target_waypoint += 1

  def rotate(self):
    #calculate distance to next waypoint
    dist = self.target - self.pos
    #use distance to calculate angle
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    #rotate image and update rectangle
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def check_alive(self, world):
    if self.health <= 0:
      world.killed_enemies += 1
      world.money += c.KILL_REWARD
      self.kill()

  def draw_health_bar(self, surface):
    bar_width = 30
    bar_height = 4
    x = int(self.pos.x - bar_width // 2)
    y = int(self.pos.y - 24)
    health_ratio = max(0, self.health / self.max_health)
    
    # draw background bar (red for missing health)
    pg.draw.rect(surface, "red", (x, y, bar_width, bar_height))
    # draw current health (green)
    pg.draw.rect(surface, "green", (x, y, int(bar_width * health_ratio), bar_height))
    
    # if enemy is slowed by Ice, draw ice indicator and cyan border
    if self.slow_timer > 0:
      pg.draw.rect(surface, (80, 220, 255), (x - 1, y - 1, bar_width + 2, bar_height + 2), 1)
      # small frost snowflake dot next to bar
      pg.draw.circle(surface, (130, 235, 255), (x - 4, y + 2), 3)
      pg.draw.circle(surface, (255, 255, 255), (x - 4, y + 2), 1)
    else:
      pg.draw.rect(surface, "black", (x, y, bar_width, bar_height), 1)