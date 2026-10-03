# 🏰 Tower Defence — Bloons TD Edition

Một tựa game thủ thành (Tower Defence) cổ điển được phát triển bằng **Python** và **pygame-ce**, lấy cảm hứng sâu sắc từ các cơ chế và phong cách đồ họa đặc sắc của **Bloons Tower Defense 6 (BTD6)**.

---

## 🌟 Tính Năng Nổi Bật

### 1. 🎮 Giao Diện Menu Chính Sống Động
- **Menu mở đầu hiện đại**: Nền bản đồ điện ảnh với hiệu ứng các hạt ánh sáng (*Floating Particles*) bay bồng bềnh khắp màn hình.
- **Bục trưng bày tháp xoay 360°**: 4 bục trưng bày tương ứng với 4 loại tháp tự động xoay nòng theo thời gian thực.
- **Bảng hướng dẫn chiến thuật (*How to Play*)**: Giới thiệu chi tiết thông số, khắc chế của từng tháp và mẹo chơi.
- **Tạm dừng linh hoạt**: Nút `🏠 MENU` và phím tắt `ESC` cho phép bạn quay về Menu bất cứ lúc nào.

### 2. 🌿 Đồ Họa Bản Đồ Nâng Cấp Chiều Sâu 3D
- **Thảm cỏ sinh động**: Chuyển màu tự nhiên, điểm xuyết hàng trăm khóm hoa dại (*hoa cúc trắng, hoa anh túc đỏ, lưu ly xanh*) và từng ngọn cỏ li ti.
- **Đường đất lún lát sỏi 3D**: Mặt đường phủ sỏi cuội nhiều kích cỡ, có viền đổ bóng từ mép cỏ tạo chiều sâu không gian.
- **Cảnh quan tự nhiên**: Cụm cây cổ thụ râm mát, hồ nước pha lê uốn lượn có hoa súng hồng, hàng rào gỗ và tảng đá phủ rêu.
- **Cổng chiến trường**: Cổng đá xuất phát quái vật có đuốc cháy rực lửa và cổng thành phòng thủ kiên cố.

### 3. 🛡️ 4 Loại Tháp Thủ Thành Chuyên Biệt (Không còn xe tăng!)
Mỗi tháp được thiết kế tách rời giữa **Bệ tháp cố định (Base)** và **Nòng vũ khí xoay linh hoạt (Weapon Head)**:

| Loại Tháp | Giá | Tầm bắn | Đặc tính nổi bật | Hiệu ứng hình ảnh |
| :--- | :---: | :---: | :--- | :--- |
| **`GUNNER`** | 175$ | 95 | Súng máy 2 nòng song song, bắn nhanh, dồn sát thương đơn mục tiêu cực mạnh. | Nòng thép bọc đồng giật nảy luân phiên và chớp lửa. |
| **`BOMB`** | 250$ | 85 | **Pháo nổ lan (AOE Splash 70px)**: Bắn đạn nổ diện rộng dọn sạch cả đàn quái đi đông. | Khẩu pháo cối khổng lồ giật lùi kèm vòng nổ lửa bùng sáng. |
| **`ICE`** | 200$ | 85 | **Sương giá làm chậm 50%**: Phát ra sóng băng tuyết làm chậm tất cả quái trong tầm 2.5s. | Đại tinh thể pha lê băng rung động bung tỏa sóng sương giá; quái hiện viền hoa tuyết. |
| **`SNIPER`** | 300$ | Vô hạn | **Bắn tỉa toàn map (Infinite Range)**: Tự động ngắm bắn quái đi đầu với sát thương cực khủng. | Súng Railgun nòng siêu dài chớp tia laser đỏ/vàng thẳng tới mục tiêu. |

### 4. 📈 Hệ Thống Nâng Cấp 3 Nhánh (BTD6 3-Path Upgrades)
Thay thế khu vực logo cũ bằng **Bảng điều khiển 3 hướng nâng cấp độc quyền**:
- **Nhánh 1 (Power)**: Tập trung tăng sát thương cực đại và khả năng phá giáp.
- **Nhánh 2 (Speed)**: Giảm mạnh thời gian hồi chiêu, bắn liên thanh dồn dập.
- **Nhánh 3 (Special / Range)**: Mở khóa các kỹ năng độc đáo (*Bắn tỏa 3 tia cùng lúc, Nổ hạt nhân diện rộng, Bão băng toàn khu, Đạn nảy đa mục tiêu*).
- **💰 Nút BÁN THÁP (SELL TOWER)**: Nút màu cam hoàn lại **70% tổng giá trị** bạn đã đầu tư vào tháp.

### 5. 🩸 Thanh Máu Quái Vật & Tua Nhanh Tiện Lợi
- **Thanh máu trực quan**: Nổi phía trên đầu mỗi quái vật (xanh lá / đỏ), tự động hiện viền băng tuyết màu xanh lơ khi bị làm chậm.
- **Nút Fast Forward x2 (Toggle)**: Nhấp chuột một lần để bật hoặc tắt duy trì tốc độ gấp đôi, không cần đè chuột.
- **Phím tắt `SPACE`**: Bắt đầu trận đấu hoặc bật/tắt nhanh tốc độ 2X.

---

## 🛠️ Yêu Cầu & Cài Đặt

### Yêu cầu hệ thống:
- **Python**: Phiên bản 3.10 trở lên (Tương thích tốt trên cả Python 3.14 mới nhất).
- Hệ điều hành: Windows, macOS hoặc Linux.

### Cài đặt thư viện:
Cài đặt thư viện `pygame-ce` (phiên bản Community Edition tối ưu nhất):
```powershell
pip install pygame-ce
```

*(Nếu mạng quốc tế chậm hoặc bị ngắt kết nối, sử dụng mirror):*
```powershell
pip install pygame-ce -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 🚀 Hướng Dẫn Khởi Chạy Game

Mở cửa sổ dòng lệnh (Terminal / PowerShell) tại thư mục dự án và chạy:
```powershell
cd "Part 13"
python main.py
```

---

## 🕹️ Hướng Dẫn Thao Tác

| Thao Tác | Phím / Chuột | Chức Năng |
| :--- | :---: | :--- |
| **Chọn tháp** | `Chuột trái` | Nhấp vào 1 trong 4 thẻ tháp trong Shop ở thanh điều khiển bên phải. |
| **Đặt tháp** | `Chuột trái` | Di chuột trên bản đồ (sẽ có vòng tròn tầm bắn xem trước) và click vào ô cỏ. |
| **Nâng cấp tháp** | `Chuột trái` | Click vào tháp đã đặt trên sân để mở bảng 3 nhánh nâng cấp ở góc dưới. |
| **Bán tháp** | `Chuột trái` | Click nút `[ 💰 BÁN THÁP ]` ở đáy bảng điều khiển để thu hồi 70% tiền. |
| **Hủy thao tác** | `Chuột phải` | Hủy chế độ đặt tháp hoặc bỏ chọn tháp hiện tại. |
| **Bắt đầu / Tua nhanh** | `Phím SPACE` | Bắt đầu đợt quái mới hoặc bật/tắt tốc độ x2 (Fast Forward). |
| **Tạm dừng / Menu** | `Phím ESC` | Tạm dừng trận đấu và quay lại Menu chính. |

---

## 📂 Cấu Trúc Thư Mục Dự Án (Part 13)

```text
tower_defence_tut/
├── README.md                          # Tài liệu hướng dẫn dự án
├── .gitignore                         # Danh sách file và thư mục bỏ qua (cache, v.v.)
└── Part 13/                           # Phiên bản game hoàn chỉnh nhất
    ├── main.py                        # Vòng lặp chính, xử lý game loop, sự kiện & Shop UI
    ├── menu.py                        # Giao diện Menu chính, hiệu ứng hạt & bảng hướng dẫn
    ├── turret.py                      # Lớp Turret: quản lý tháp, xoay nòng, 3 nhánh nâng cấp & bán
    ├── turret_data.py                 # Cấu hình chỉ số gốc & cây 3 nhánh nâng cấp (UPGRADE_PATHS)
    ├── enemy.py                       # Lớp Enemy: di chuyển theo waypoints, thanh máu & làm chậm
    ├── enemy_data.py                  # Dữ liệu xuất hiện của quái vật qua từng wave
    ├── world.py                       # Quản lý thế giới, nạp dữ liệu map & đếm quái
    ├── effects.py                     # Quản lý hiệu ứng đồ họa chiến đấu (nổ lan, laser, sóng băng)
    ├── constants.py                   # Các hằng số cài đặt màn hình, máu, tiền & FPS
    ├── button.py                      # Lớp Button xử lý nút bấm cơ bản
    ├── generate_turret_sprites.py     # Script tạo đồ họa spritesheet cho 4 loại tháp mới
    ├── enhance_map.py                 # Script vẽ & hoàn thiện bản đồ 3D chi tiết
    ├── assets/                        # Tài nguyên âm thanh, hình ảnh quái & giao diện
    │   ├── audio/                     # Âm thanh bắn súng
    │   └── images/                    # Sprite quái, nút bấm, GUI và tháp mới
    │       └── new_turrets/           # Spritesheet của Gunner, Bomb, Ice, Sniper
    └── levels/                        # Bản đồ game (level.png, level.tmj)
```

---

## 💡 Mẹo Chiến Thuật Cho Người Mới
1. **Phối hợp Băng + Pháo**: Đặt Tháp Băng (`ICE`) ở các khúc cua gập ghềnh để gom đàn quái lại, sau đó đặt Tháp Pháo (`BOMB`) ngay cạnh để phát huy tối đa sát thương nổ lan diện rộng.
2. **Sniper ở góc xa**: Vì Tháp Bắn Tỉa (`SNIPER`) có tầm bắn vô hạn toàn map, hãy đặt Sniper ở những ô cỏ xa xôi hẻo lánh, dành các ô đất vàng gần đường đi cho Gunner và Ice.
3. **Nâng cấp chuyên sâu**: Thay vì nâng dàn trải, hãy chọn 1 nhánh thế mạnh của tháp để nâng lên cấp tối đa (Tier 3) để mở khóa kỹ năng đột phá (*ví dụ: Gunner bắn 3 tia hoặc Sniper đạn nảy*).
