# Doodle Jump 遊戲說明

## 0. 遊戲引擎需求

- 使用 Pygame 進行遊戲開發

## 遊戲開發步驟

### 步驟 1: 基本視窗與主角

- 建立基本遊戲視窗 (400x600像素)
- 繪製一個綠色小方塊作為主角 (30x30像素)
- 主角初始位置放在底部中間
- 簡單的遊戲迴圈與退出功能

### 步驟 2: 主角移動控制

- 加入鍵盤左右控制功能
- 實現從螢幕左邊出去會從右邊出現的功能

### 步驟 3: 平台基本實現

- 新增平台物件(60x10像素的白色長條)
- 在玩家腳底下加入一個平台確保不會掉下去

### 步驟 4: 加入跳躍功能

- 實現主角與平台的碰撞檢測(玩家向上移動不會碰到，向下會碰到)
- 實現主角跳躍功能
- 控制跳躍的初始速度和重力(初始跳躍力12像素，重力0.5像素)
- 當跳躍到最高點會開始往下掉
- 加入重力效果，讓主角能自動往下掉落

### 步驟 5: 平台隨機生成與進階碰撞檢測

- 隨機生成 8-10 個平台
- 確保平台間距60像素
- 記得保留玩家腳底下的那個平台
- 優化碰撞偵測系統：
  - 根據下落速度自動計算檢測點數量（每5像素一個檢測點）
  - 在物體移動路徑上增加多個檢測點
  - 使用分段檢測確保高速移動時不會穿透
  - 即時補償位置偏移，避免穿透問題

### 步驟 6: 畫面捲動與平台生成

- 相機移動系統實作
  - 建立 update_camera() 函式用於處理相機和平台的動態更新
  - 定義畫面中間位置 screen_middle = bg_y // 2 作為相機參考點
  - 當玩家上升到螢幕中間位置以上時，固定玩家在螢幕中間
  - 計算移動距離 camera_move = screen_middle - player.rect.y
  - 將所有平台往下移動該距離，製造玩家往上移動的效果
- 平台管理機制完善
  - 將總平台數量增加到 random.randint(8, 10) + 10 個
  - 檢測並移除超出畫面底部的平台(使用多行for迴圈)
  - 使用 y_min 變數追蹤最高平台的位置
  - 當平台數量小於預設數量時，在最高平台上方60像素處自動生成新平台
  - 確保新生成的平台位置隨機但垂直間距保持一致

### 步驟 7: 分數與遊戲結束

- 加入文字字體"C:/Windows/Fonts/msjh.ttc"
- 加入分數系統，每上升10個像素加1分
- 加入遊戲結束判定 (當主角掉出畫面)
- 當遊戲結束的時候會顯示分數以及按下任意鍵重新開始遊戲

### 步驟 8: 彈簧道具

- 新增黃色彈簧道具物件 (20x10像素)
- 彈簧道具會隨機生成在平台上方，並且不會與平台重疊
- 彈簧要跟著平台一起移動
- 彈簧在離開視窗的時候會自動消失，可以參考平台的移除邏輯(使用多行for迴圈+remove())
- 彈簧的生成機率20%
- 目前玩家看的到隨機彈簧但是不具有任何功能
- 不要動到平台相關的程式碼

### 步驟 9: 實現彈簧功能

- 主角碰到彈簧時會有更高的跳躍力 (往上跳25像素)

### 步驟 10: 只能踩一次的平台

- 當分數超過1000分後，開始出現特殊平台
- 特殊平台的顏色為紅色，並且會隨機混入一般平台列表中
- 特殊平台的生成機率20%
- 當玩家踩到消失平台後，該平台會立即消失
- 不在此平台上生成彈簧

### 步驟 11: 加入圖片資源和精靈系統

- 在載入套件部分，添加 `os` 模組用於處理檔案路徑
- 在全域變數部分，設定執行路徑為當前檔案位置 `os.chdir(sys.path[0])`
- 建立 `load_doodle_sprites()` 函式用於載入圖片資源：
  - 載入主要精靈圖片 (src.png)
  - 切割不同平台的精靈（standard_platform, break_platform）
  - 切割彈簧精靈（spring_normal）
  - 載入玩家角色四個方向的圖片（左跳、左落、右跳、右落）
  - 使用字典儲存所有精靈資源
  - 實現完整的錯誤處理機制（包含找不到圖片和切割錯誤的處理）
  - 精靈圖片位置說明：
    - 標準平台：(0, 0, 116, 30)
    - 可破壞平台：(0, 145, 124, 33)
    - 普通彈簧：(376, 188, 71, 35)
    - 玩家圖片：載入 l.png (左跳)、ls.png (左落)、r.png (右跳)、rs.png (右落)
- 修改各物件類別以支援圖片繪製：  
  - Player 類別：
    - 添加 sprites 參數到 __init__，用於儲存精靈圖片
    - 添加 facing_right 屬性追蹤面向方向（預設向右）
    - 添加 jumping 屬性追蹤跳躍狀態（垂直速度小於0為跳躍中）
    - 修改 draw 方法：
      - 根據面向方向和跳躍狀態選擇對應精靈
      - 若有精靈圖片則使用精靈，否則使用矩形
      - 自動調整精靈大小以符合角色實際尺寸
    - 修改 move 方法自動更新 facing_right 屬性
    - 修改 apply_gravity 方法自動更新 jumping 屬性
  - Platform 類別：
    - 添加 sprites 參數到 __init__
    - 修改 draw 方法：
      - 特殊平台使用 break_platform 精靈
      - 一般平台使用 std_platform 精靈
      - 特殊平台且已被踩過時不繪製
      - 無精靈時使用矩形代替
  - Spring 類別：
    - 添加 sprites 參數到 __init__
    - 修改 draw 方法使用 spring_normal 精靈
    - 調整彈簧尺寸為 35x20 像素以符合精靈圖片大小
  - Hat 類別：
    - 添加 sprites 參數到 __init__
    - 修改 draw 方法使用 hat 精靈
    - 調整飛行帽子尺寸為 35x25 像素以符合設定
- 調整遊戲物件尺寸和屬性：
  - 主角調整：
    - 尺寸從 30x30 改為 50x50 像素以符合精靈圖片尺寸
    - 顏色保持為綠色 (0, 255, 0)
  - 平台調整：
    - 尺寸從 60x10 改為 80x20 像素以配合精靈圖片比例
    - 顏色從白色改為深灰色 (100, 100, 100)
  - 彈簧調整：
    - 尺寸從 20x10 改為 35x20 像素以符合精靈圖片
    - 顏色保持為黃色 (255, 215, 0)
  - 飛行帽子調整：
    - 尺寸設定為 35x25 像素
    - 顏色設定為藍色 (0, 0, 255)（無精靈時）
  
- 視覺風格全面優化：
  - 遊戲背景從黑色改為白色 (255, 255, 255)
  - 文字顏色從白色改為黑色 (0, 0, 0)，涵蓋：
    - 分數顯示
    - 遊戲結束訊息
    - 最高分顯示
  
- 程式結構優化和錯誤處理：
  - 圖片載入機制：
    - 將載入程式碼移至初始化階段
    - 確保在設定視窗模式之後執行
    - 添加 use_sprites 全域變數控制精靈系統
  - 錯誤處理機制：
    - 圖片載入失敗時自動切換為簡單圖形模式
    - 輸出具體的錯誤訊息以便偵錯
  - 物件生成優化：
    - 主角、平台和彈簧建立時都傳入精靈參數
    - 重置遊戲時確保傳入精靈參數
  
- 動畫系統實現：
  - 角色動畫控制：
    - 根據水平移動方向自動更新面向
    - 根據垂直速度判定跳躍/下落狀態
    - 自動選擇對應狀態的精靈圖片
  - 精靈渲染優化：
    - 確保圖片大小與物件實際尺寸一致
    - 使用 scale 調整精靈尺寸
    - 位置對齊採用中心點對齊方式

```python
def load_doodle_sprites():
    """
    載入遊戲所需的圖片資源\n
    - 從source圖片切割各種平台和彈簧精靈\n
    - 載入玩家角色四個方向的圖片\n
    return: 包含所有精靈的字典\n
    """
    # 載入主要圖片資源
    img_path = os.path.join("image", "src.png")
    source_image = pygame.image.load(img_path).convert_alpha()  # 載入圖片並轉換為帶Alpha通道的格式

    # 定義精靈在原始圖片中的座標和尺寸
    sprite_data = {
        # 各種平台的座標和尺寸 (x, y, 寬, 高)
        "std_platform": (0, 0, 116, 30),  # 標準平台
        "break_platform": (0, 145, 124, 33),  # 可破壞平台
        # 彈簧
        "spring_normal": (376, 188, 71, 35),  # 普通彈簧
        # 玩家角色圖片路徑
        "player_left_jumping": os.path.join("image", "l.png"),  # 左跳躍
        "player_left_falling": os.path.join("image", "ls.png"),  # 左下落
        "player_right_jumping": os.path.join("image", "r.png"),  # 右跳躍
        "player_right_falling": os.path.join("image", "rs.png"),  # 右下落
        # 飛行帽子
        "hat": (682, 485, 52, 39),  # 飛行帽子
    }  # 切割精靈圖片並存入字典
    sprites = {}
    for name, data in sprite_data.items():
        if name.startswith("player_"):
            # 直接從檔案載入玩家角色圖片
            try:
                sprites[name] = pygame.image.load(data).convert_alpha()
            except Exception as e:
                print(f"無法載入玩家圖片 {name}: {e}")
        else:
            try:
                # 從主圖片切割出所需的精靈
                x, y, width, height = data  # 解包四個值
                sprites[name] = source_image.subsurface(pygame.Rect(x, y, width, height))
            except ValueError as e:
                print(f"無法切割 {name}: {e}")  # 如果切割失敗，輸出錯誤訊息

    return sprites  # 返回包含所有精靈的字典
```

```python
# 載入圖片的實現範例
try:
    # 載入遊戲所需的所有精靈圖片（需要在設置視窗模式後進行）
    sprites = load_doodle_sprites()
    use_sprites = True  # 標記是否使用精靈圖片
    print(f"成功載入 {len(sprites)} 個精靈圖片")
except Exception as e:
    # 如果載入失敗，使用簡單的幾何圖形代替
    print(f"載入精靈圖片時發生錯誤: {e}")
    print("將使用簡單圖形進行遊戲")
    sprites = None
    use_sprites = False  # 標記不使用精靈圖片
```

```python
# 物件建立時使用精靈圖片的範例
player = Player(player_x, player_y, player_w, player_h, (0, 255, 0), sprites if use_sprites else None)
platform = Platform(platform_x, platform_y, platform_w, platform_h, (100, 100, 100), False, sprites if use_sprites else None)
spring = Spring(spring_x, spring_y, spring_w, spring_h, (255, 215, 0), sprites if use_sprites else None)
hat = Hat(hat_x, hat_y, 35, 25, (0, 0, 255), sprites if use_sprites else None)
```

### 步驟 12: 新增飛行帽子精靈和物件

- 修改load_doodle_sprites()函式:
  - 在sprite_data字典中加入飛行帽子的資訊:
    ```python
    sprite_data = {
        # ...existing code...
        "hat": (682, 485, 52, 39),  # 飛行帽子
    }
    ```

- 建立Hat類別:
  ```python
  class Hat:
      def __init__(self, x, y, width, height, color, sprites=None):
          self.rect = pygame.Rect(x, y, width, height)
          self.color = color
          self.sprites = sprites
          self.platform = None  # 紀錄帽子所在的平台

      def draw(self, screen):
          if self.sprites and "hat" in self.sprites:
              hat_img = self.sprites["hat"]
              hat_img = pygame.transform.scale(hat_img, (self.rect.width, self.rect.height))
              screen.blit(hat_img, self.rect)
          else:
              pygame.draw.rect(screen, self.color, self.rect)

      def update(self, platform_move):
          # 跟隨平台移動
          self.rect.y += platform_move
  ```

### 步驟 13: 實現飛行帽子功能

- 在全域變數和物件部分:
  - 設定飛行帽子每3000分會出現一次
  - 飛行帽子會隨機生成在平台上方，並且不會與平台重疊
  - 設定飛行帽子尺寸為 35x25 像素
  - 設定飛行帽子飛行時間為5秒
  - 設定飛行帽子效果：每幀上升1像素

- 遊戲邏輯更新:
  - 每3000分在平台上生成飛行帽子
  - 飛行帽子要跟著平台移動
  - 當玩家碰到飛行帽子時:
    - 讓玩家戴上飛行帽子
    - 飛行帽子會跟隨玩家移動
    - 玩家進入飛行狀態，持續5秒
    - 飛行狀態下每幀自動上升1像素
  - 飛行帽子離開畫面時自動移除
  - 飛完後飛行帽子會消失

- 視覺效果:
  - 飛行帽子顏色為藍色 (0, 0, 255)（無精靈時）
  - 飛行狀態下玩家閃爍提示效果（選擇性實現）
