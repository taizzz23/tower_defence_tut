import pygame as pg
import math
import random

class MenuParticle:
  def __init__(self, screen_w, screen_h):
    self.screen_w = screen_w
    self.screen_h = screen_h
    self.reset()
    self.y = random.randint(0, screen_h)

  def reset(self):
    self.x = random.randint(0, self.screen_w)
    self.y = self.screen_h + random.randint(5, 30)
    self.speed_y = -random.uniform(0.6, 2.0)
    self.speed_x = random.uniform(-0.4, 0.4)
    self.radius = random.uniform(1.5, 3.5)
    self.color = random.choice([
      (255, 215, 80),  # Gold
      (100, 220, 255), # Icy Cyan
      (255, 120, 70),  # Fire Orange
      (220, 230, 255)  # Starlight
    ])

  def update(self):
    self.x += self.speed_x
    self.y += self.speed_y
    if self.y < -10 or self.x < -10 or self.x > self.screen_w + 10:
      self.reset()

  def draw(self, surface):
    pg.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))


class MenuButton:
  def __init__(self, rect, text, bg_color, hover_color, text_color=(255, 255, 255), font=None):
    self.rect = pg.Rect(rect)
    self.text = text
    self.bg_color = bg_color
    self.hover_color = hover_color
    self.text_color = text_color
    self.font = font
    self.hovered = False

  def draw(self, surface, mouse_pos):
    self.hovered = self.rect.collidepoint(mouse_pos)
    col = self.hover_color if self.hovered else self.bg_color
    draw_rect = self.rect.inflate(8, 4) if self.hovered else self.rect

    # Drop shadow
    shadow_rect = pg.Rect(draw_rect.x + 3, draw_rect.y + 4, draw_rect.width, draw_rect.height)
    pg.draw.rect(surface, (8, 10, 15), shadow_rect, border_radius=10)

    # Button fill
    pg.draw.rect(surface, col, draw_rect, border_radius=10)

    # Border glow
    border_col = (255, 235, 120) if self.hovered else (180, 190, 210)
    border_w = 2 if self.hovered else 1
    pg.draw.rect(surface, border_col, draw_rect, border_w, border_radius=10)

    # Text
    if self.font:
      txt_surf = self.font.render(self.text, True, self.text_color)
      txt_rect = txt_surf.get_rect(center=draw_rect.center)
      surface.blit(txt_surf, txt_rect)

  def is_clicked(self, mouse_pos, event):
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      return self.rect.collidepoint(mouse_pos)
    return False


class GameMenu:
  def __init__(self, screen_w, screen_h, map_image, turret_types, mini_icons):
    self.screen_w = screen_w
    self.screen_h = screen_h
    self.map_image = map_image
    self.turret_types = turret_types
    self.mini_icons = mini_icons

    # Fonts
    self.title_font = pg.font.SysFont("Consolas", 52, bold=True)
    self.sub_font = pg.font.SysFont("Consolas", 17, bold=True)
    self.btn_font = pg.font.SysFont("Consolas", 20, bold=True)
    self.info_font = pg.font.SysFont("Consolas", 15, bold=True)
    self.desc_font = pg.font.SysFont("Consolas", 13)

    # Floating particles
    self.particles = [MenuParticle(screen_w, screen_h) for _ in range(45)]

    # Main menu buttons (centered)
    center_x = screen_w // 2
    btn_w = 260
    btn_h = 50
    btn_x = center_x - btn_w // 2

    self.play_button = MenuButton(
      (btn_x, 435, btn_w, btn_h),
      "▶  BẮT ĐẦU CHƠI",
      (35, 140, 70), (45, 175, 85),
      font=self.btn_font
    )

    self.guide_button = MenuButton(
      (btn_x, 500, btn_w, btn_h),
      "📖  HƯỚNG DẪN",
      (40, 95, 160), (55, 125, 200),
      font=self.btn_font
    )

    self.quit_button = MenuButton(
      (btn_x, 565, btn_w, btn_h),
      "✖  THOÁT GAME",
      (150, 45, 45), (185, 60, 60),
      font=self.btn_font
    )

    # Back button in Guide screen
    self.back_button = MenuButton(
      (center_x - 110, 620, 220, 45),
      "◀  QUAY LẠI MENU",
      (50, 70, 95), (70, 95, 130),
      font=self.btn_font
    )

    # Background dark overlay surface
    self.dark_overlay = pg.Surface((screen_w, screen_h), pg.SRCALPHA)
    self.dark_overlay.fill((12, 16, 24, 215))

    # Load tower preview images
    self.tower_previews = {}
    for t_key in turret_types.keys():
      self.tower_previews[t_key] = {
        "base": pg.image.load(f'assets/images/new_turrets/{t_key}_base.png').convert_alpha(),
        "head": pg.image.load(f'assets/images/new_turrets/{t_key}_cursor.png').convert_alpha(),
      }

  def draw_main_menu(self, surface):
    mouse_pos = pg.mouse.get_pos()

    # 1. Background Map & Dark Overlay
    surface.blit(self.map_image, (0, 0))
    # If screen is wider than map, fill rest
    if self.screen_w > self.map_image.get_width():
      pg.draw.rect(surface, (20, 25, 35), (self.map_image.get_width(), 0, self.screen_w - self.map_image.get_width(), self.screen_h))
    surface.blit(self.dark_overlay, (0, 0))

    # 2. Animated floating particles
    for p in self.particles:
      p.update()
      p.draw(surface)

    # 3. Game Title with Drop Shadow
    center_x = self.screen_w // 2
    title_text = "TOWER DEFENCE"
    # Deep shadow
    shadow_surf = self.title_font.render(title_text, True, (5, 8, 12))
    surface.blit(shadow_surf, (center_x - shadow_surf.get_width() // 2 + 3, 58))
    # Main gold gradient title
    title_surf = self.title_font.render(title_text, True, (255, 215, 70))
    surface.blit(title_surf, (center_x - title_surf.get_width() // 2, 55))

    # Subtitle
    sub_text = "— BLOONS TD EDITION • CHIẾN THUẬT PHÒNG THỦ —"
    sub_surf = self.sub_font.render(sub_text, True, (120, 225, 255))
    surface.blit(sub_surf, (center_x - sub_surf.get_width() // 2, 118))

    # 4. Showcase of 4 Turrets
    showcase_y = 230
    types_list = [
      ("gunner", "GUNNER", "Súng Máy", (120, 210, 120)),
      ("bomb",   "BOMB",   "Pháo Nổ Lan", (255, 120, 80)),
      ("ice",    "ICE",    "Băng Tuyết", (90, 220, 255)),
      ("sniper", "SNIPER", "Bắn Tỉa Map", (255, 215, 60))
    ]
    spacing = 180
    start_x = center_x - int((len(types_list) - 1) * spacing / 2)

    # Rotating angle for heads in showcase
    spin_angle = (pg.time.get_ticks() / 25) % 360

    for i, (t_key, t_name, role_name, color) in enumerate(types_list):
      tx = start_x + i * spacing
      ty = showcase_y

      # Pedestal card box
      card_rect = pg.Rect(tx - 65, ty - 65, 130, 150)
      pg.draw.rect(surface, (25, 30, 42), card_rect, border_radius=12)
      pg.draw.rect(surface, (55, 65, 85), card_rect, 1, border_radius=12)

      # Draw Base
      base_img = self.tower_previews[t_key]["base"]
      surface.blit(base_img, (tx - 48, ty - 48))

      # Draw rotating head
      cursor_img = self.tower_previews[t_key]["head"]
      rot_head = pg.transform.rotate(cursor_img, spin_angle - 90)
      head_rect = rot_head.get_rect(center=(tx, ty))
      surface.blit(rot_head, head_rect)

      # Turret Name badge
      name_surf = self.info_font.render(t_name, True, color)
      surface.blit(name_surf, (tx - name_surf.get_width() // 2, ty + 38))

      # Role tag
      role_surf = self.desc_font.render(role_name, True, (180, 190, 205))
      surface.blit(role_surf, (tx - role_surf.get_width() // 2, ty + 58))

    # 5. Buttons
    self.play_button.draw(surface, mouse_pos)
    self.guide_button.draw(surface, mouse_pos)
    self.quit_button.draw(surface, mouse_pos)

    # 6. Version info footer
    ver_surf = self.desc_font.render("Phiên bản Bloons TD • Sẵn sàng chiến đấu", True, (120, 130, 150))
    surface.blit(ver_surf, (center_x - ver_surf.get_width() // 2, 685))

  def draw_guide(self, surface):
    mouse_pos = pg.mouse.get_pos()

    # Background
    surface.blit(self.map_image, (0, 0))
    if self.screen_w > self.map_image.get_width():
      pg.draw.rect(surface, (20, 25, 35), (self.map_image.get_width(), 0, self.screen_w - self.map_image.get_width(), self.screen_h))
    surface.blit(self.dark_overlay, (0, 0))

    for p in self.particles:
      p.update()
      p.draw(surface)

    center_x = self.screen_w // 2

    # Modal Card
    modal_w = 760
    modal_h = 570
    modal_x = center_x - modal_w // 2
    modal_y = 40
    modal_rect = pg.Rect(modal_x, modal_y, modal_w, modal_h)

    # Card body & glowing border
    pg.draw.rect(surface, (20, 26, 38), modal_rect, border_radius=16)
    pg.draw.rect(surface, (70, 130, 200), modal_rect, 2, border_radius=16)

    # Header
    head_surf = self.title_font.render("HƯỚNG DẪN CHIẾN THUẬT", True, (255, 220, 80))
    # Scale down title font slightly for header
    head_scaled = pg.transform.smoothscale(head_surf, (int(head_surf.get_width() * 0.65), int(head_surf.get_height() * 0.65)))
    surface.blit(head_scaled, (center_x - head_scaled.get_width() // 2, modal_y + 20))

    # Divider
    pg.draw.line(surface, (60, 80, 110), (modal_x + 30, modal_y + 68), (modal_x + modal_w - 30, modal_y + 68), 1)

    # 4 Towers Guide
    guide_items = [
      ("gunner", "GUNNER (175$)", "Súng máy 2 nòng song song, bắn cực nhanh, dồn sát thương đơn mục tiêu liên tục.", (120, 220, 120)),
      ("bomb",   "BOMB (250$)",   "Pháo cối nổ diện rộng (AOE Splash), sát thương lan 70px. Chuyên dọn các đợt quái đi đông.", (255, 120, 80)),
      ("ice",    "ICE (200$)",    "Tháp sương giá băng tuyết, làm chậm quái 50% trong 2.5s. Giúp các tháp khác tiêu diệt dễ dàng.", (90, 220, 255)),
      ("sniper", "SNIPER (300$)", "Xạ thủ Railgun bắn tỉa toàn map (tầm bắn vô hạn), dame cực lớn 1-shot quái thường từ xa.", (255, 215, 60)),
    ]

    item_y = modal_y + 85
    for t_key, title, desc, col in guide_items:
      # Icon
      if t_key in self.mini_icons:
        surface.blit(self.mini_icons[t_key], (modal_x + 40, item_y))

      # Title
      t_surf = self.info_font.render(title, True, col)
      surface.blit(t_surf, (modal_x + 85, item_y))

      # Description
      d_surf = self.desc_font.render(desc, True, (200, 210, 225))
      surface.blit(d_surf, (modal_x + 85, item_y + 22))

      item_y += 56

    # Divider
    pg.draw.line(surface, (60, 80, 110), (modal_x + 30, item_y + 10), (modal_x + modal_w - 30, item_y + 10), 1)

    # Controls Section
    ctrl_y = item_y + 25
    c_title = self.info_font.render("THAO TÁC ĐIỀU KHIỂN & MẸO CHƠI:", True, (255, 235, 130))
    surface.blit(c_title, (modal_x + 40, ctrl_y))

    tips = [
      "• Đặt & Nâng cấp tháp: Mua tháp từ Shop, click tháp trên sân để nâng cấp 3 nhánh chuyên sâu.",
      "• Nút Bán Tháp (💰 SELL): Thu hồi lại 70% tổng tiền đã đầu tư để tái cơ cấu đội hình.",
      "• Phím SPACE: Bắt đầu đợt mới hoặc bật/tắt tốc độ 2X. Phím ESC: Tạm dừng về Menu.",
      "• 👑 CẢNH BÁO TRÙM (WAVE 10, 20, 30, 40): Xuất hiện Siêu Trùm có thanh máu khủng,",
      "  kháng khống chế và kỹ năng đặc biệt (Phân tách quái con, Cuồng nộ, Triệu hồi Hư Không)!"
    ]

    tip_y = ctrl_y + 28
    for tip in tips:
      tip_surf = self.desc_font.render(tip, True, (190, 205, 220))
      surface.blit(tip_surf, (modal_x + 40, tip_y))
      tip_y += 22

    # Back button
    self.back_button.draw(surface, mouse_pos)
