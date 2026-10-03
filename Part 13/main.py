import pygame as pg
import json
import math
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c
from turret_data import TURRET_TYPES, UPGRADE_PATHS
from effects import VisualEffect
from menu import GameMenu, MenuButton

#initialise pygame
pg.init()
if not pg.mixer.get_init():
  import os
  os.environ['SDL_AUDIODRIVER'] = 'dummy'
  try:
    pg.mixer.init()
  except pg.error:
    pass

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence - Bloons TD Edition")

#game state variables
game_state = "menu" # "menu", "how_to_play", "playing"
game_over = False
game_outcome = 0 # -1 is loss & 1 is win
level_started = False
fast_forward = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret_type = "gunner"
selected_turret = None
effects = []

#load images
#map
map_image = pg.image.load('levels/level.png').convert_alpha()

#load custom turret preview & cursor images (no tanks!)
cursor_turrets = {}
mini_turret_icons = {}
for t_key in TURRET_TYPES.keys():
  cur_img = pg.image.load(f'assets/images/new_turrets/{t_key}_cursor.png').convert_alpha()
  cursor_turrets[t_key] = cur_img
  mini_turret_icons[t_key] = pg.transform.smoothscale(cur_img, (32, 32))

#enemies
enemy_images = {
  "weak": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
  "medium": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
  "strong": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
  "elite": pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha()
}

#buttons
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
fast_forward_image = pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()

#gui
heart_image = pg.image.load("assets/images/gui/heart.png").convert_alpha()
coin_image = pg.image.load("assets/images/gui/coin.png").convert_alpha()

#load sounds
try:
  shot_fx = pg.mixer.Sound('assets/audio/shot.wav')
  shot_fx.set_volume(0.5)
except Exception:
  shot_fx = None

#load json data for level
with open('levels/level.tmj') as file:
  world_data = json.load(file)

#load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas", 22, bold = True)
small_font = pg.font.SysFont("Consolas", 15, bold = True)
tiny_font = pg.font.SysFont("Consolas", 13)
micro_font = pg.font.SysFont("Consolas", 11, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

# Initialize Main Menu manager
game_menu = GameMenu(c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT, map_image, TURRET_TYPES, mini_turret_icons)
in_game_menu_btn = MenuButton((c.SCREEN_WIDTH + 175, 12, 110, 32), "🏠 MENU", (55, 38, 48), (85, 50, 65), font=small_font)
game_over_menu_btn = MenuButton((310, 360, 180, 42), "🏠 VỀ MENU", (45, 65, 95), (65, 90, 130), font=small_font)

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def display_data():
  #draw panel top
  pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 365))
  pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 365), 2)
  #display data
  draw_text("LV: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 12)
  screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 40))
  draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 44)
  screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 68))
  draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 72)
  #draw in-game menu button
  in_game_menu_btn.draw(screen, pg.mouse.get_pos())

def create_turret(mouse_pos, turret_type):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  if 0 <= mouse_tile_num < len(world.tile_map) and world.tile_map[mouse_tile_num] == 7:
    space_is_free = True
    for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
        space_is_free = False
        break
    if space_is_free:
      cost = TURRET_TYPES[turret_type]["cost"]
      if world.money >= cost:
        new_turret = Turret(None, mouse_tile_x, mouse_tile_y, shot_fx, turret_type)
        turret_group.add(new_turret)
        world.money -= cost
        return True
  return False

def select_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for turret in turret_group:
    if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
      return turret
  return None

def clear_selection():
  for turret in turret_group:
    turret.selected = False

#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

#buttons
cancel_button = Button(c.SCREEN_WIDTH + 75, 235, cancel_image, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 275, begin_image, True)
restart_button = Button(310, 305, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 50, 275, fast_forward_image, True)

# Shop cards definitions (2x2 grid in side panel)
shop_cards = [
  {"type": "gunner", "rect": pg.Rect(c.SCREEN_WIDTH + 14, 102, 130, 46)},
  {"type": "bomb",   "rect": pg.Rect(c.SCREEN_WIDTH + 154, 102, 130, 46)},
  {"type": "ice",    "rect": pg.Rect(c.SCREEN_WIDTH + 14, 153, 130, 46)},
  {"type": "sniper", "rect": pg.Rect(c.SCREEN_WIDTH + 154, 153, 130, 46)},
]

# BTD6 3-Path Upgrade Rectangles in bottom panel (y = 365 to 720)
upgrade_panel_rect = pg.Rect(c.SCREEN_WIDTH, 365, c.SIDE_PANEL, c.SCREEN_HEIGHT - 365)
path_btn_rects = [
  pg.Rect(c.SCREEN_WIDTH + 188, 420, 96, 52),
  pg.Rect(c.SCREEN_WIDTH + 188, 492, 96, 52),
  pg.Rect(c.SCREEN_WIDTH + 188, 564, 96, 52),
]
sell_btn_rect = pg.Rect(c.SCREEN_WIDTH + 14, 642, 270, 44)

#game loop
run = True
while run:

  clock.tick(c.FPS)

  #########################
  # 1. MAIN MENU STATE
  #########################
  if game_state == "menu":
    game_menu.draw_main_menu(screen)

  #########################
  # 2. HOW TO PLAY STATE
  #########################
  elif game_state == "how_to_play":
    game_menu.draw_guide(screen)

  #########################
  # 3. PLAYING STATE
  #########################
  elif game_state == "playing":
    if game_over == False:
      #check if player has lost
      if world.health <= 0:
        game_over = True
        game_outcome = -1 #loss
      #check if player has won
      if world.level > c.TOTAL_LEVELS:
        game_over = True
        game_outcome = 1 #win

      #update groups & effects
      enemy_group.update(world)
      turret_group.update(enemy_group, world, effects)

      for effect in effects[:]:
        if not effect.update():
          effects.remove(effect)

      #highlight selected turret
      if selected_turret:
        selected_turret.selected = True

    #draw level
    world.draw(screen)

    #draw groups
    enemy_group.draw(screen)
    for enemy in enemy_group:
      enemy.draw_health_bar(screen)
    for turret in turret_group:
      turret.draw(screen)

    #draw attack visual effects (explosions, sniper lasers, ice rings)
    for effect in effects:
      effect.draw(screen)

    #draw panel top stats
    display_data()

    if game_over == False:
      #check if level started or not
      if level_started == False:
        if begin_button.draw(screen):
          level_started = True
      else:
        #fast forward toggle
        if fast_forward_button.draw(screen):
          fast_forward = not fast_forward

        world.game_speed = 2 if fast_forward else 1

        # Visual indicator for 2X vs 1X
        if fast_forward:
          pg.draw.rect(screen, (50, 255, 100), fast_forward_button.rect.inflate(6, 6), 3, border_radius=8)
          draw_text("▶▶ 2X (ĐANG BẬT)", small_font, (50, 255, 100), c.SCREEN_WIDTH + 80, 332)
        else:
          draw_text("▶ 1X (TẮT)", tiny_font, (180, 190, 205), c.SCREEN_WIDTH + 110, 332)
        #spawn enemies
        if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
          if world.spawned_enemies < len(world.enemy_list):
            enemy_type = world.enemy_list[world.spawned_enemies]
            enemy = Enemy(enemy_type, world.waypoints, enemy_images)
            enemy_group.add(enemy)
            world.spawned_enemies += 1
            last_enemy_spawn = pg.time.get_ticks()

      #check if wave is finished
      if world.check_level_complete() == True:
        world.money += c.LEVEL_COMPLETE_REWARD
        world.level += 1
        level_started = False
        last_enemy_spawn = pg.time.get_ticks()
        world.reset_level()
        world.process_enemies()
        effects.clear()

      #draw shop header & 4 turret cards
      mouse_pos = pg.mouse.get_pos()
      for card in shop_cards:
        t_key = card["type"]
        t_info = TURRET_TYPES[t_key]
        rect = card["rect"]
        is_hovered = rect.collidepoint(mouse_pos)
        is_active = (placing_turrets and selected_turret_type == t_key)

        # Card background
        if is_active:
          bg_col = (55, 60, 75)
          border_col = (255, 220, 0)
          border_w = 2
        elif is_hovered:
          bg_col = (50, 52, 65)
          border_col = (180, 180, 210)
          border_w = 1
        else:
          bg_col = (36, 38, 48)
          border_col = (80, 80, 95)
          border_w = 1

        pg.draw.rect(screen, bg_col, rect, border_radius = 6)
        pg.draw.rect(screen, border_col, rect, border_w, border_radius = 6)

        # Turret icon
        screen.blit(mini_turret_icons[t_key], (rect.x + 5, rect.y + 7))

        # Turret title & cost
        draw_text(t_info["name"], small_font, "white", rect.x + 42, rect.y + 7)
        draw_text(f"{t_info['cost']}$", small_font, (255, 215, 60), rect.x + 42, rect.y + 25)

      # Turret placement status / helper
      if placing_turrets:
        t_info = TURRET_TYPES[selected_turret_type]
        draw_text(f"ĐANG ĐẶT: {t_info['name']}", small_font, "gold", c.SCREEN_WIDTH + 15, 208)
        draw_text("Click ô cỏ để đặt tháp", tiny_font, "grey90", c.SCREEN_WIDTH + 15, 225)
        if cancel_button.draw(screen):
          placing_turrets = False

        # Preview range circle and cursor turret
        if mouse_pos[0] <= c.SCREEN_WIDTH and mouse_pos[1] <= c.SCREEN_HEIGHT:
          base_rng = t_info.get("base_stats", {}).get("range", 95)
          p_range = min(base_rng, 350)
          range_surf = pg.Surface((p_range * 2, p_range * 2), pg.SRCALPHA)
          tint = t_info.get("color_tint", (255, 255, 255))
          pg.draw.circle(range_surf, (*tint, 70), (p_range, p_range), p_range)
          pg.draw.circle(range_surf, (*tint, 180), (p_range, p_range), p_range, 1)
          screen.blit(range_surf, (mouse_pos[0] - p_range, mouse_pos[1] - p_range))

          cur_img = cursor_turrets[selected_turret_type]
          cur_rect = cur_img.get_rect()
          cur_rect.center = mouse_pos
          screen.blit(cur_img, cur_rect)

      elif selected_turret:
        t_name = selected_turret.type_data["name"]
        draw_text(f"ĐÃ CHỌN: {t_name}", small_font, "gold", c.SCREEN_WIDTH + 15, 208)
        draw_text(f"Nhánh: [{selected_turret.paths[0]}-{selected_turret.paths[1]}-{selected_turret.paths[2]}] (Xem bên dưới)", tiny_font, "grey90", c.SCREEN_WIDTH + 15, 226)

      else:
        draw_text("Chọn tháp từ Shop để đặt", tiny_font, "grey80", c.SCREEN_WIDTH + 15, 208)
        draw_text("Click tháp trên sân để nâng cấp 3 nhánh", tiny_font, "grey80", c.SCREEN_WIDTH + 15, 226)

      ######################################################################
      # BTD6 3-PATH UPGRADE & SELL CONSOLE (REPLACES THE OLD TD TEXT AREA)
      ######################################################################
      pg.draw.rect(screen, (25, 27, 36), upgrade_panel_rect)
      pg.draw.line(screen, (70, 78, 98), (c.SCREEN_WIDTH, 365), (c.SCREEN_WIDTH + c.SIDE_PANEL, 365), 2)

      if selected_turret:
        t_key = selected_turret.turret_type
        paths_config = UPGRADE_PATHS[t_key]

        # Top Header of Console
        draw_text(f"{selected_turret.type_data['name']} [ {selected_turret.paths[0]} - {selected_turret.paths[1]} - {selected_turret.paths[2]} ]", small_font, (255, 220, 80), c.SCREEN_WIDTH + 14, 372)
        rng_str = "INF" if selected_turret.range > 9000 else str(selected_turret.range)
        draw_text(f"DMG: {selected_turret.damage} | RNG: {rng_str} | SPD: {selected_turret.cooldown}ms", tiny_font, (190, 200, 215), c.SCREEN_WIDTH + 14, 392)

        # 3 Path Rows (BTD6 Style)
        row_y_offsets = [414, 486, 558]
        for p_idx in range(3):
          r_y = row_y_offsets[p_idx]
          row_rect = pg.Rect(c.SCREEN_WIDTH + 10, r_y, 280, 66)

          # Draw Row container
          pg.draw.rect(screen, (18, 20, 26), row_rect, border_radius = 8)
          pg.draw.rect(screen, (48, 54, 68), row_rect, 1, border_radius = 8)

          # Left side: 3 Tier Pips / Squares (BTD6 Green/Hollow boxes)
          current_tier = selected_turret.paths[p_idx]
          for pip_i in range(3):
            pip_rect = pg.Rect(row_rect.x + 8 + pip_i * 14, row_rect.y + 7, 10, 10)
            if pip_i < current_tier:
              pg.draw.rect(screen, (45, 220, 60), pip_rect, border_radius=2) # Green filled
              pg.draw.rect(screen, (20, 100, 30), pip_rect, 1, border_radius=2)
            else:
              pg.draw.rect(screen, (40, 44, 55), pip_rect, border_radius=2) # Dark hollow
              pg.draw.rect(screen, (70, 75, 90), pip_rect, 1, border_radius=2)

          # Path Title
          p_title = paths_config[p_idx]["name"]
          draw_text(p_title, micro_font, (175, 190, 210), row_rect.x + 55, row_rect.y + 6)

          # Next Upgrade Name & Description
          if current_tier < 3:
            t_data = paths_config[p_idx]["tiers"][current_tier]
            draw_text(t_data["name"], small_font, "white", row_rect.x + 8, row_rect.y + 24)
            draw_text(t_data["desc"], tiny_font, (100, 225, 245), row_rect.x + 8, row_rect.y + 44)
          else:
            last_t = paths_config[p_idx]["tiers"][2]
            draw_text(f"MAX: {last_t['name']}", small_font, (255, 215, 0), row_rect.x + 8, row_rect.y + 24)
            draw_text(last_t["desc"], tiny_font, (170, 185, 200), row_rect.x + 8, row_rect.y + 44)

          # Right side: Action Button (BTD6 Green Button / Grey Max)
          btn_rect = path_btn_rects[p_idx]
          if current_tier < 3:
            cost = paths_config[p_idx]["tiers"][current_tier]["cost"]
            can_afford = world.money >= cost
            hovered = btn_rect.collidepoint(mouse_pos)

            if can_afford and hovered:
              b_col = (45, 195, 75)
              border_col = (180, 255, 190)
            elif can_afford:
              b_col = (35, 155, 60)
              border_col = (120, 240, 140)
            else:
              b_col = (65, 38, 45) # Dimmed red
              border_col = (100, 50, 60)

            pg.draw.rect(screen, b_col, btn_rect, border_radius = 8)
            pg.draw.rect(screen, border_col, btn_rect, 1, border_radius = 8)

            txt_up = micro_font.render("NÂNG CẤP", True, (255, 255, 255))
            screen.blit(txt_up, (btn_rect.centerx - txt_up.get_width() // 2, btn_rect.y + 10))

            txt_cost = small_font.render(f"${cost}", True, (255, 215, 60) if can_afford else (230, 120, 120))
            screen.blit(txt_cost, (btn_rect.centerx - txt_cost.get_width() // 2, btn_rect.y + 28))

          else:
            # Max tier button (grey)
            pg.draw.rect(screen, (40, 45, 55), btn_rect, border_radius = 8)
            pg.draw.rect(screen, (70, 75, 90), btn_rect, 1, border_radius = 8)
            txt_max1 = micro_font.render("ĐÃ ĐẠT", True, (160, 170, 185))
            txt_max2 = small_font.render("★ MAX ★", True, (255, 215, 0))
            screen.blit(txt_max1, (btn_rect.centerx - txt_max1.get_width() // 2, btn_rect.y + 10))
            screen.blit(txt_max2, (btn_rect.centerx - txt_max2.get_width() // 2, btn_rect.y + 28))

        # Bottom SELL TOWER Button (BTD6 Orange Button!)
        sell_refund = selected_turret.get_sell_value()
        sell_hovered = sell_btn_rect.collidepoint(mouse_pos)
        sell_col = (255, 115, 25) if sell_hovered else (230, 85, 15)
        pg.draw.rect(screen, (10, 10, 15), (sell_btn_rect.x + 2, sell_btn_rect.y + 3, sell_btn_rect.width, sell_btn_rect.height), border_radius=10)
        pg.draw.rect(screen, sell_col, sell_btn_rect, border_radius=10)
        pg.draw.rect(screen, (255, 220, 150), sell_btn_rect, 1, border_radius=10)
        sell_txt = small_font.render(f"💰 BÁN THÁP (+{sell_refund}$)", True, "white")
        screen.blit(sell_txt, (sell_btn_rect.centerx - sell_txt.get_width() // 2, sell_btn_rect.centery - sell_txt.get_height() // 2))

      else:
        # Idle panel: Tactical Overview of 3 Upgrade Paths
        card_r = pg.Rect(c.SCREEN_WIDTH + 10, 375, 280, 325)
        pg.draw.rect(screen, (20, 22, 30), card_r, border_radius=12)
        pg.draw.rect(screen, (55, 65, 85), card_r, 1, border_radius=12)

        draw_text("3 HƯỚNG NÂNG CẤP (BTD6)", small_font, (255, 215, 70), card_r.x + 15, card_r.y + 15)
        pg.draw.line(screen, (50, 60, 80), (card_r.x + 15, card_r.y + 38), (card_r.x + card_r.width - 15, card_r.y + 38), 1)

        lines = [
          ("⚔️ Nhánh 1: Sức Mạnh", "Tăng sát thương cực đại & phá giáp"),
          ("⚡ Nhánh 2: Tốc Độ", "Nạp đạn siêu tốc, bắn liên tục"),
          ("🎯 Nhánh 3: Đa Kỹ Năng", "Bắn tỏa 3 tia, đạn nảy, bão tuyết"),
          ("💰 Hoàn Tiền Bán Tháp", "Nhận lại 70% tổng tiền đã nâng cấp")
        ]

        ly = card_r.y + 50
        for l_title, l_desc in lines:
          draw_text(l_title, small_font, (120, 220, 255), card_r.x + 15, ly)
          draw_text(l_desc, tiny_font, (180, 190, 205), card_r.x + 15, ly + 20)
          ly += 48

        draw_text("👉 Click vào tháp trên sân", small_font, (255, 235, 120), card_r.x + 25, card_r.y + 265)
        draw_text("để mở bảng nâng cấp 3 nhánh!", tiny_font, (200, 210, 225), card_r.x + 25, card_r.y + 288)

    else:
      # Game Over / Win Dialog
      pg.draw.rect(screen, "dodgerblue", (200, 180, 400, 240), border_radius = 24)
      pg.draw.rect(screen, "grey100", (200, 180, 400, 240), 2, border_radius = 24)
      if game_outcome == -1:
        draw_text("GAME OVER", large_font, "grey0", 310, 215)
      elif game_outcome == 1:
        draw_text("YOU WIN!", large_font, "grey0", 315, 215)
      
      # Restart button
      if restart_button.draw(screen):
        game_over = False
        level_started = False
        placing_turrets = False
        selected_turret = None
        effects.clear()
        last_enemy_spawn = pg.time.get_ticks()
        world = World(world_data, map_image)
        world.process_data()
        world.process_enemies()
        enemy_group.empty()
        turret_group.empty()

      # Return to Menu button
      game_over_menu_btn.draw(screen, pg.mouse.get_pos())

  #########################
  # EVENT HANDLER
  #########################
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False

    mouse_pos = pg.mouse.get_pos()

    # Events in Main Menu
    if game_state == "menu":
      if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if game_menu.play_button.is_clicked(mouse_pos, event):
          game_state = "playing"
        elif game_menu.guide_button.is_clicked(mouse_pos, event):
          game_state = "how_to_play"
        elif game_menu.quit_button.is_clicked(mouse_pos, event):
          run = False

    # Events in How to Play
    elif game_state == "how_to_play":
      if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and game_menu.back_button.is_clicked(mouse_pos, event)) or \
         (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
        game_state = "menu"

    # Events in Playing
    elif game_state == "playing":
      # Press ESC to pause and go to menu
      if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
        game_state = "menu"
        placing_turrets = False
        selected_turret = None
        clear_selection()
        continue

      # Press SPACE to start wave or toggle 2X speed
      if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
        if not level_started:
          level_started = True
        else:
          fast_forward = not fast_forward

      if event.type == pg.MOUSEBUTTONDOWN:
        if event.button == 1:
          # Check in-game menu button
          if in_game_menu_btn.is_clicked(mouse_pos, event):
            game_state = "menu"
            placing_turrets = False
            selected_turret = None
            clear_selection()
            continue

          # Check return to menu from game over screen
          if game_over and game_over_menu_btn.is_clicked(mouse_pos, event):
            game_state = "menu"
            game_over = False
            level_started = False
            placing_turrets = False
            selected_turret = None
            effects.clear()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            enemy_group.empty()
            turret_group.empty()
            continue

          # If a turret is selected, check clicks on the 3-Path Upgrade buttons or SELL button
          if selected_turret:
            # Check 3 Path Upgrade buttons
            path_upgraded = False
            for p_idx in range(3):
              if path_btn_rects[p_idx].collidepoint(mouse_pos):
                tier_info = selected_turret.get_path_tier_info(p_idx)
                if tier_info and world.money >= tier_info["cost"]:
                  cost = selected_turret.upgrade_path(p_idx)
                  world.money -= cost
                path_upgraded = True
                break
            if path_upgraded:
              continue

            # Check Sell button
            if sell_btn_rect.collidepoint(mouse_pos):
              refund = selected_turret.get_sell_value()
              world.money += refund
              selected_turret.kill()
              selected_turret = None
              clear_selection()
              continue

          # Check shop cards click
          card_clicked = False
          for card in shop_cards:
            if card["rect"].collidepoint(mouse_pos):
              selected_turret_type = card["type"]
              placing_turrets = True
              selected_turret = None
              clear_selection()
              card_clicked = True
              break

          # Check click on map
          if not card_clicked and mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
            if placing_turrets:
              success = create_turret(mouse_pos, selected_turret_type)
              if success:
                placing_turrets = False
            else:
              selected_turret = None
              clear_selection()
              selected_turret = select_turret(mouse_pos)

        # Right click: Cancel placement or deselect
        elif event.button == 3:
          placing_turrets = False
          selected_turret = None
          clear_selection()

  #update display
  pg.display.flip()

pg.quit()