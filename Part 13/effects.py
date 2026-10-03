import pygame as pg

class VisualEffect:
  def __init__(self, effect_type, pos, **kwargs):
    self.type = effect_type
    self.pos = pos
    self.kwargs = kwargs
    if self.type == "sniper_beam":
      self.lifetime = 6
      self.max_lifetime = 6
    elif self.type == "ice_wave":
      self.lifetime = 10
      self.max_lifetime = 10
    elif self.type == "explosion":
      self.lifetime = 12
      self.max_lifetime = 12
    elif self.type == "boss_explosion":
      self.lifetime = 24
      self.max_lifetime = 24
    elif self.type == "shockwave":
      self.lifetime = 16
      self.max_lifetime = 16
    elif self.type == "floating_text":
      self.lifetime = 36
      self.max_lifetime = 36
    else:
      self.lifetime = 8
      self.max_lifetime = 8

  def update(self):
    self.lifetime -= 1
    if self.type == "floating_text":
      # Float upwards smoothly
      self.pos = (self.pos[0], self.pos[1] - 0.7)
    return self.lifetime > 0

  def draw(self, surface):
    progress = 1.0 - (self.lifetime / self.max_lifetime)
    cx, cy = int(self.pos[0]), int(self.pos[1])
    
    if self.type == "explosion":
      max_rad = self.kwargs.get("radius", 65)
      rad = max(1, int(max_rad * (0.3 + 0.7 * progress)))
      # outer explosion wave
      pg.draw.circle(surface, (255, 110, 30), (cx, cy), rad, max(1, int(4 * (1.0 - progress))))
      # inner fire flash
      if progress < 0.6:
        inner_rad = max(1, int(rad * 0.55))
        pg.draw.circle(surface, (255, 230, 90), (cx, cy), inner_rad)

    elif self.type == "boss_explosion":
      # Epic multi-layer blast for Bosses
      max_rad = self.kwargs.get("radius", 130)
      rad = max(1, int(max_rad * (0.2 + 0.8 * progress)))
      # Outer golden-fire ring
      pg.draw.circle(surface, (255, 190, 40), (cx, cy), rad, max(1, int(6 * (1.0 - progress))))
      # Second shockwave
      rad2 = max(1, int(rad * 0.75))
      pg.draw.circle(surface, (255, 50, 30), (cx, cy), rad2, max(1, int(4 * (1.0 - progress))))
      # Third purple/electric shockwave
      rad3 = max(1, int(rad * 0.5))
      pg.draw.circle(surface, (255, 220, 100), (cx, cy), rad3, max(1, int(3 * (1.0 - progress))))
      # Inner super flash
      if progress < 0.5:
        pg.draw.circle(surface, (255, 255, 255), (cx, cy), max(1, int(rad * 0.35)))

    elif self.type == "shockwave":
      max_rad = self.kwargs.get("radius", 90)
      color = self.kwargs.get("color", (180, 50, 255))
      rad = max(1, int(max_rad * (0.2 + 0.8 * progress)))
      pg.draw.circle(surface, color, (cx, cy), rad, max(1, int(4 * (1.0 - progress))))

    elif self.type == "ice_wave":
      max_rad = self.kwargs.get("radius", 80)
      rad = max(1, int(max_rad * (0.2 + 0.8 * progress)))
      # frosty expanding ring
      pg.draw.circle(surface, (100, 220, 255), (cx, cy), rad, max(1, int(3 * (1.0 - progress))))
      # frosty center flash
      if progress < 0.5:
        pg.draw.circle(surface, (200, 245, 255), (cx, cy), max(1, int(rad * 0.35)))

    elif self.type == "sniper_beam":
      target_pos = self.kwargs.get("target_pos", self.pos)
      tx, ty = int(target_pos[0]), int(target_pos[1])
      # High-velocity tracer beam
      pg.draw.line(surface, (255, 240, 90), (cx, cy), (tx, ty), 3)
      pg.draw.line(surface, (255, 120, 40), (cx, cy), (tx, ty), 1)
      # Impact hit spark
      pg.draw.circle(surface, (255, 250, 200), (tx, ty), 5)
      pg.draw.circle(surface, (255, 80, 40), (tx, ty), 8, 1)

    elif self.type == "floating_text":
      text = self.kwargs.get("text", "")
      font = self.kwargs.get("font")
      color = self.kwargs.get("color", (255, 215, 0))
      if font and text:
        txt_surf = font.render(text, True, color)
        # Drop shadow
        sh_surf = font.render(text, True, (0, 0, 0))
        surface.blit(sh_surf, (cx - txt_surf.get_width() // 2 + 1, cy - txt_surf.get_height() // 2 + 1))
        surface.blit(txt_surf, (cx - txt_surf.get_width() // 2, cy - txt_surf.get_height() // 2))
