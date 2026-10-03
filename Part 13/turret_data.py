TURRET_TYPES = {
  "gunner": {
    "name": "GUNNER",
    "desc": "Bắn nhanh, sát thương đơn",
    "cost": 175,
    "color_tint": (255, 255, 255),
    "base_stats": {"range": 95, "cooldown": 900, "damage": 8}
  },
  "bomb": {
    "name": "BOMB",
    "desc": "Pháo nổ lan (AOE Splash)",
    "cost": 250,
    "color_tint": (255, 115, 80),
    "splash_radius": 70,
    "splash_damage": 10,
    "base_stats": {"range": 85, "cooldown": 1400, "damage": 16}
  },
  "ice": {
    "name": "ICE",
    "desc": "Băng giá làm chậm 50%",
    "cost": 200,
    "color_tint": (90, 215, 255),
    "slow_factor": 0.5,
    "slow_duration": 2500,
    "base_stats": {"range": 85, "cooldown": 1200, "damage": 4}
  },
  "sniper": {
    "name": "SNIPER",
    "desc": "Bắn tỉa toàn map, dame khủng",
    "cost": 300,
    "color_tint": (255, 215, 60),
    "base_stats": {"range": 9999, "cooldown": 2000, "damage": 35}
  }
}

UPGRADE_PATHS = {
  "gunner": [
    # Path 1: Sát thương
    {
      "name": "SÁT THƯƠNG",
      "tiers": [
        {"name": "Đạn Thép", "desc": "+5 Sát thương", "cost": 90, "stat": {"damage": 5}},
        {"name": "Đạn Phá Giáp", "desc": "+8 Sát thương", "cost": 150, "stat": {"damage": 8}},
        {"name": "Đạn Vonfram", "desc": "+14 Sát thương", "cost": 240, "stat": {"damage": 14}},
      ]
    },
    # Path 2: Tốc độ bắn
    {
      "name": "TỐC ĐỘ BẮN",
      "tiers": [
        {"name": "Lên Đạn Nhanh", "desc": "-20% thời gian chờ", "cost": 80, "stat": {"cooldown_pct": 0.20}},
        {"name": "Nòng Siêu Tốc", "desc": "-25% thời gian chờ", "cost": 130, "stat": {"cooldown_pct": 0.25}},
        {"name": "Gatling Blitz", "desc": "-35% thời gian chờ", "cost": 210, "stat": {"cooldown_pct": 0.35}},
      ]
    },
    # Path 3: Tầm xa & Bắn chùm
    {
      "name": "TẦM XA & ĐA TIA",
      "tiers": [
        {"name": "Ống Ngắm Xa", "desc": "+25 Tầm bắn", "cost": 75, "stat": {"range": 25}},
        {"name": "Kính Radar", "desc": "+35 Tầm bắn", "cost": 120, "stat": {"range": 35}},
        {"name": "Bắn 3 Tia", "desc": "Bắn cùng lúc 3 quái", "cost": 260, "stat": {"multi_shot": 3}},
      ]
    }
  ],
  "bomb": [
    # Path 1: Sức công phá
    {
      "name": "SỨC CÔNG PHÁ",
      "tiers": [
        {"name": "Đạn Pháo Lớn", "desc": "+8 DMG, +5 Splash", "cost": 110, "stat": {"damage": 8, "splash_damage": 5}},
        {"name": "Thuốc Nổ Cực Hạn", "desc": "+14 DMG, +10 Splash", "cost": 180, "stat": {"damage": 14, "splash_damage": 10}},
        {"name": "Tên Lửa MOAB", "desc": "+24 DMG, +18 Splash", "cost": 270, "stat": {"damage": 24, "splash_damage": 18}},
      ]
    },
    # Path 2: Bán kính nổ
    {
      "name": "BÁN KÍNH NỔ",
      "tiers": [
        {"name": "Sóng Xung Kích", "desc": "+20px Bán kính nổ", "cost": 90, "stat": {"splash_radius": 20}},
        {"name": "Nổ Diện Rộng", "desc": "+30px Bán kính nổ", "cost": 150, "stat": {"splash_radius": 30}},
        {"name": "Bom Hạt Nhân", "desc": "+45px Nổ cực lớn", "cost": 240, "stat": {"splash_radius": 45}},
      ]
    },
    # Path 3: Tiếp đạn nhanh
    {
      "name": "TIẾP ĐẠN NHANH",
      "tiers": [
        {"name": "Băng Đạn Nhanh", "desc": "-20% thời gian chờ", "cost": 100, "stat": {"cooldown_pct": 0.20}},
        {"name": "Nạp Tự Động", "desc": "-25% thời gian chờ", "cost": 160, "stat": {"cooldown_pct": 0.25}},
        {"name": "Pháo Liên Thanh", "desc": "-35% thời gian chờ", "cost": 250, "stat": {"cooldown_pct": 0.35}},
      ]
    }
  ],
  "ice": [
    # Path 1: Đóng băng sâu
    {
      "name": "ĐÓNG BĂNG SÂU",
      "tiers": [
        {"name": "Sương Giá Sâu", "desc": "Làm chậm 65% tốc độ", "cost": 95, "stat": {"slow_factor": 0.35}},
        {"name": "Tê Cóng Kéo Dài", "desc": "+1.5s Thời gian chậm", "cost": 140, "stat": {"slow_duration": 1500}},
        {"name": "Không Độ Tuyệt Đối", "desc": "Làm chậm 80% tốc độ!", "cost": 230, "stat": {"slow_factor": 0.20}},
      ]
    },
    # Path 2: Tầm đóng băng
    {
      "name": "BÃO BĂNG TOÀN KHU",
      "tiers": [
        {"name": "Gió Lạnh Rộng", "desc": "+20 Tầm đóng băng", "cost": 80, "stat": {"range": 20}},
        {"name": "Bão Tuyết Cực Bắc", "desc": "+30 Tầm đóng băng", "cost": 130, "stat": {"range": 30}},
        {"name": "Bão Tuyết Địa Cầu", "desc": "+45 Tầm đóng băng", "cost": 210, "stat": {"range": 45}},
      ]
    },
    # Path 3: Sát thương băng
    {
      "name": "GAI BĂNG SÁT THƯƠNG",
      "tiers": [
        {"name": "Mưa Gai Nhọn", "desc": "+5 Sát thương băng", "cost": 90, "stat": {"damage": 5}},
        {"name": "Vỡ Mảnh Băng", "desc": "+9 Sát thương băng", "cost": 150, "stat": {"damage": 9}},
        {"name": "Băng Tiễn Tối Thượng", "desc": "+16 Sát thương băng", "cost": 240, "stat": {"damage": 16}},
      ]
    }
  ],
  "sniper": [
    # Path 1: Đại sát thương
    {
      "name": "SÁT THƯƠNG CỰC ĐẠI",
      "tiers": [
        {"name": "Đạn Điểm Xuyên", "desc": "+25 Sát thương", "cost": 140, "stat": {"damage": 25}},
        {"name": "Tỉa Chí Mạng", "desc": "+45 Sát thương", "cost": 210, "stat": {"damage": 45}},
        {"name": "Đạn Phá Thiết Giáp", "desc": "+75 Sát thương!", "cost": 330, "stat": {"damage": 75}},
      ]
    },
    # Path 2: Tốc độ bắn tỉa
    {
      "name": "TỐC ĐỘ BẮN TỈA",
      "tiers": [
        {"name": "Lên Nòng Mượt", "desc": "-25% thời gian chờ", "cost": 110, "stat": {"cooldown_pct": 0.25}},
        {"name": "Tỉa Bán Tự Động", "desc": "-30% thời gian chờ", "cost": 180, "stat": {"cooldown_pct": 0.30}},
        {"name": "Full-Auto Railgun", "desc": "-40% Bắn liên thanh", "cost": 280, "stat": {"cooldown_pct": 0.40}},
      ]
    },
    # Path 3: Đạn nảy đa mục tiêu
    {
      "name": "ĐẠN NẢY ĐA MỤC TIÊU",
      "tiers": [
        {"name": "Mắt Đại Bàng", "desc": "+10 Sát thương", "cost": 120, "stat": {"damage": 10}},
        {"name": "Đạn Nảy Đôi", "desc": "Nảy sang 1 quái kế bên", "cost": 190, "stat": {"bouncing": 1}},
        {"name": "Mưa Đạn Xuyên Thấu", "desc": "Nảy sang 3 quái kế bên!", "cost": 290, "stat": {"bouncing": 3}},
      ]
    }
  ]
}

# Compatibility alias for earlier parts
TURRET_DATA = [
  {"range": 95, "cooldown": 900, "damage": 8},
  {"range": 115, "cooldown": 700, "damage": 12},
  {"range": 130, "cooldown": 500, "damage": 16},
  {"range": 155, "cooldown": 350, "damage": 22},
]