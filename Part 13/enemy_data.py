# Configuration for all 40 waves and enemy statistics
# Including Epic Bosses for Wave 10, 20, 30, 40 and Mini-Boss variations

ENEMY_DATA = {
  "weak": {
    "health": 10,
    "speed": 2,
    "reward": 1
  },
  "medium": {
    "health": 16,
    "speed": 3,
    "reward": 1
  },
  "strong": {
    "health": 25,
    "speed": 4,
    "reward": 2
  },
  "elite": {
    "health": 42,
    "speed": 5,
    "reward": 3
  },
  "void_phantom": {
    "health": 85,
    "speed": 6.2,
    "reward": 5
  },
  "boss_minion_golem": {
    "health": 140,
    "speed": 2.2,
    "reward": 8
  },
  "boss_minion_dread": {
    "health": 320,
    "speed": 3.0,
    "reward": 15
  },

  # -----------------------------------------------------------
  # WAVE 10 BOSS: TITAN GOLEM (Thạch Cự Nhân - Nham Thạch)
  # -----------------------------------------------------------
  "boss_titan": {
    "health": 750,
    "speed": 1.3,
    "reward": 150,
    "is_boss": True,
    "boss_name": "TITAN GOLEM",
    "boss_title": "BẢO HỘ THẠCH GIÁP",
    "deathrattle": ["boss_minion_golem", "boss_minion_golem", "boss_minion_golem"],
    "cc_resistance": 0.45, # 45% CC resistance
    "aura_color": (255, 120, 20)
  },

  # -----------------------------------------------------------
  # WAVE 20 BOSS: INFERNAL DREADNOUGHT (Chiến Hạm Hỏa Diệm)
  # -----------------------------------------------------------
  "boss_dreadnought": {
    "health": 2800,
    "speed": 1.5,
    "reward": 350,
    "is_boss": True,
    "boss_name": "INFERNAL DREADNOUGHT",
    "boss_title": "CHIẾN HẠM HỎA DIỆM",
    "deathrattle": ["boss_minion_dread", "boss_minion_dread", "boss_minion_golem", "boss_minion_golem"],
    "cc_resistance": 0.55,
    "enrage_hp_ratio": 0.45, # Cuồng nộ tăng tốc khi dưới 45% máu
    "aura_color": (240, 30, 40)
  },

  # -----------------------------------------------------------
  # WAVE 30 BOSS: VOID OVERLORD (Chúa Tể Hư Không)
  # -----------------------------------------------------------
  "boss_overlord": {
    "health": 8000,
    "speed": 1.6,
    "reward": 750,
    "is_boss": True,
    "boss_name": "VOID OVERLORD",
    "boss_title": "CHÚA TỂ HƯ KHÔNG",
    "deathrattle": ["boss_minion_dread", "boss_minion_dread", "void_phantom", "void_phantom", "void_phantom"],
    "cc_resistance": 0.65,
    "summon_type": "void_phantom",
    "summon_cooldown": 4500,
    "aura_color": (170, 50, 255)
  },

  # -----------------------------------------------------------
  # WAVE 40 GRAND FINAL BOSS: CHAOS LEVIATHAN (Cổ Long Diệt Thế)
  # -----------------------------------------------------------
  "boss_leviathan": {
    "health": 20000,
    "speed": 1.8,
    "reward": 1500,
    "is_boss": True,
    "boss_name": "CHAOS LEVIATHAN",
    "boss_title": "CỔ LONG DIỆT THẾ (FINAL BOSS)",
    "deathrattle": ["boss_titan", "boss_dreadnought", "boss_minion_dread", "boss_minion_dread"],
    "cc_resistance": 0.75,
    "enrage_hp_ratio": 0.4,
    "aura_color": (255, 215, 0)
  }
}

# 40 Waves of balanced, escalating difficulty
ENEMY_SPAWN_DATA = [
  # --- EARLY GAME (WAVES 1 - 9) ---
  { "weak": 15 },                                                      # 1
  { "weak": 25 },                                                      # 2
  { "weak": 20, "medium": 6 },                                         # 3
  { "weak": 25, "medium": 14 },                                        # 4
  { "weak": 10, "medium": 22, "strong": 3 },                           # 5
  { "weak": 15, "medium": 20, "strong": 6 },                           # 6
  { "weak": 20, "medium": 25, "strong": 8 },                           # 7
  { "weak": 10, "medium": 25, "strong": 14, "elite": 2 },              # 8
  { "weak": 12, "medium": 20, "strong": 18, "elite": 5 },              # 9

  # --- 👑 BOSS WAVE 1 (WAVE 10) ---
  { "medium": 15, "strong": 12, "elite": 4, "boss_titan": 1 },         # 10

  # --- MID GAME (WAVES 11 - 19) ---
  { "medium": 20, "strong": 18, "elite": 6 },                          # 11
  { "strong": 25, "elite": 10, "boss_minion_golem": 2 },               # 12
  { "strong": 30, "elite": 15, "boss_minion_golem": 3 },               # 13
  { "strong": 20, "elite": 20, "void_phantom": 4 },                    # 14
  { "strong": 15, "elite": 25, "void_phantom": 8 },                    # 15
  { "elite": 30, "void_phantom": 12, "boss_minion_golem": 3 },         # 16
  { "elite": 35, "void_phantom": 16, "boss_minion_dread": 2 },         # 17
  { "elite": 40, "void_phantom": 18, "boss_minion_dread": 3 },         # 18
  { "elite": 45, "void_phantom": 22, "boss_minion_golem": 4 },         # 19

  # --- 👑 BOSS WAVE 2 (WAVE 20) ---
  { "elite": 25, "void_phantom": 15, "boss_minion_golem": 4, "boss_dreadnought": 1 }, # 20

  # --- LATE GAME (WAVES 21 - 29) ---
  { "elite": 35, "void_phantom": 25, "boss_minion_dread": 4 },         # 21
  { "elite": 40, "void_phantom": 30, "boss_minion_dread": 5 },         # 22
  { "boss_titan": 1, "elite": 35, "void_phantom": 25 },                 # 23 (Mini Titan)
  { "elite": 45, "void_phantom": 35, "boss_minion_dread": 6 },         # 24
  { "boss_titan": 2, "elite": 30, "void_phantom": 30 },                 # 25 (Dual Titans)
  { "elite": 50, "void_phantom": 40, "boss_minion_dread": 8 },         # 26
  { "boss_titan": 1, "boss_dreadnought": 1, "elite": 35, "void_phantom": 30 }, # 27
  { "elite": 55, "void_phantom": 45, "boss_minion_dread": 10 },        # 28
  { "boss_dreadnought": 2, "elite": 40, "void_phantom": 35 },          # 29 (Dual Dreadnoughts)

  # --- 👑 BOSS WAVE 3 (WAVE 30) ---
  { "elite": 30, "void_phantom": 30, "boss_minion_dread": 6, "boss_overlord": 1 }, # 30

  # --- NIGHTMARE / ENDLESS TIER (WAVES 31 - 39) ---
  { "elite": 60, "void_phantom": 50, "boss_minion_dread": 10 },        # 31
  { "boss_dreadnought": 2, "void_phantom": 45, "boss_minion_dread": 8 }, # 32
  { "boss_titan": 3, "boss_dreadnought": 1, "void_phantom": 50 },      # 33
  { "void_phantom": 60, "elite": 50, "boss_minion_dread": 12 },        # 34
  { "boss_overlord": 2, "void_phantom": 40, "elite": 40 },             # 35 (Dual Void Emperors)
  { "void_phantom": 70, "elite": 60, "boss_minion_dread": 15 },        # 36
  { "boss_titan": 2, "boss_dreadnought": 2, "void_phantom": 50 },      # 37
  { "boss_overlord": 2, "boss_minion_dread": 8, "void_phantom": 60 },  # 38
  { "boss_titan": 2, "boss_dreadnought": 2, "boss_overlord": 1, "void_phantom": 50 }, # 39

  # --- 👑 GRAND FINAL BOSS (WAVE 40) ---
  { "void_phantom": 40, "elite": 40, "boss_leviathan": 1 }              # 40
]