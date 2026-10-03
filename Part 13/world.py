import pygame as pg
import random
import constants as c
from enemy_data import ENEMY_SPAWN_DATA, ENEMY_DATA

class World():
  def __init__(self, data, map_image):
    self.level = 1
    self.game_speed = 1
    self.health = c.HEALTH
    self.money = c.MONEY
    self.tile_map = []
    self.waypoints = []
    self.level_data = data
    self.image = map_image
    
    # Wave queue and progress tracking
    self.spawn_queue = []
    self.spawned_count = 0
    self.total_enemies = 0
    self.killed_enemies = 0
    self.missed_enemies = 0
    self.screen_shake = 0

    # Backwards-compatibility alias
    self.enemy_list = []
    self.spawned_enemies = 0

  def process_data(self):
    #look through data to extract relevant info
    for layer in self.level_data["layers"]:
      if layer["name"] == "tilemap":
        self.tile_map = layer["data"]
      elif layer["name"] == "waypoints":
        for obj in layer["objects"]:
          waypoint_data = obj["polyline"]
          self.process_waypoints(waypoint_data)

  def process_waypoints(self, data):
    #iterate through waypoints to extract individual sets of x and y coordinates
    for point in data:
      temp_x = point.get("x")
      temp_y = point.get("y")
      self.waypoints.append((temp_x, temp_y))

  def process_enemies(self):
    wave_idx = min(self.level - 1, len(ENEMY_SPAWN_DATA) - 1)
    enemies_dict = ENEMY_SPAWN_DATA[wave_idx]
    
    all_creeps = []
    for enemy_type, count in enemies_dict.items():
      for _ in range(count):
        all_creeps.append(enemy_type)
        
    # Separate major bosses from standard creeps for dramatic pacing
    bosses = [e for e in all_creeps if ENEMY_DATA.get(e, {}).get("is_boss", False)]
    regulars = [e for e in all_creeps if not ENEMY_DATA.get(e, {}).get("is_boss", False)]
    random.shuffle(regulars)
    
    if bosses:
      # Let 1/3 of the creeps march first, then the Boss appears with fanfare!
      mid = len(regulars) // 3
      self.spawn_queue = regulars[:mid] + bosses + regulars[mid:]
    else:
      self.spawn_queue = regulars

    # Synchronize tracking variables
    self.enemy_list = self.spawn_queue
    self.spawned_count = 0
    self.spawned_enemies = 0
    self.total_enemies = len(self.spawn_queue)
    self.killed_enemies = 0
    self.missed_enemies = 0

  def has_boss_this_wave(self):
    wave_idx = min(self.level - 1, len(ENEMY_SPAWN_DATA) - 1)
    enemies_dict = ENEMY_SPAWN_DATA[wave_idx]
    for e_type in enemies_dict.keys():
      if ENEMY_DATA.get(e_type, {}).get("is_boss", False):
        return True
    return False

  def get_boss_info_this_wave(self):
    wave_idx = min(self.level - 1, len(ENEMY_SPAWN_DATA) - 1)
    enemies_dict = ENEMY_SPAWN_DATA[wave_idx]
    for e_type in enemies_dict.keys():
      data = ENEMY_DATA.get(e_type, {})
      if data.get("is_boss", False):
        return data
    return None

  def check_level_complete(self):
    return (self.killed_enemies + self.missed_enemies) >= self.total_enemies

  def reset_level(self):
    self.spawn_queue = []
    self.enemy_list = []
    self.spawned_count = 0
    self.spawned_enemies = 0
    self.killed_enemies = 0
    self.missed_enemies = 0

  def draw(self, surface):
    surface.blit(self.image, (0, 0))