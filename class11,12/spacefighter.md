```markdown
# Galaxy Lancer 遊戲說明

## 0. 遊戲引擎需求

- 使用 Pygame 進行遊戲開發

## 遊戲開發步驟

### 步驟 1: 基本遊戲模板與捲動背景

- 建立基本遊戲程式架構，程式碼組織分為七大區塊：
  - 載入套件區塊：引入必要的pygame、sys和os套件，以及pygame.locals中的常數
  - 定義函式區塊：宣告遊戲中使用的自訂函式，包括 `roll_bg()` 函式實現背景捲動效果
  - 初始化設定區塊：
    - 使用`os.chdir(sys.path[0])`切換至程式所在目錄
    - 使用`pygame.init()`初始化pygame
    - 建立時鐘物件控制遊戲速度
  - 載入圖片區塊：載入太空背景圖片 (image/space.png)
  - 遊戲視窗設定區塊：
    - 設定視窗標題為"Galaxy Lancer"
    - 取得背景圖片尺寸作為遊戲視窗大小
    - 初始化捲動背景所需變數 `roll_y = 0`
  - 玩家設定區塊：設定玩家初始狀態和相關變數
  - 主程式區塊：包含遊戲主迴圈
- 實現捲動背景功能：
  - 捲動邏輯：
    - 持續更新 `roll_y` 變數 (每次增加 10 像素)
    - 使用模運算確保無縫循環 `roll_y = (roll_y + 10) % bg_y`
    - 在上下兩部分繪製背景圖片實現連續捲動
- 提供基本遊戲迴圈功能：
  - 使用`clock.tick(60)`設定時鐘頻率為每秒60幀
  - 實現退出遊戲功能 (按X關閉視窗)
  - 提供按鍵事件處理：
    - F1鍵切換至全螢幕模式
    - ESC鍵返回視窗模式
  - 使用`pygame.display.update()`更新畫面

### 步驟 2: 加入玩家物件及太空船

- 創建 `Player` 類別管理玩家太空船：
  - 初始化函式 `__init__` 設定：
    - 位置與尺寸 (x, y, width, height)，預設尺寸為 80x80
    - 顏色 (用於測試或無圖片時)
    - 速度 (預設水平移動速度)
    - 太空船圖片 (sprites字典)
  - 設計 `draw` 方法在螢幕上繪製太空船
  - 設計 `handle_input` 方法封裝所有移動相關邏輯：
    - 接收按鍵狀態作為參數
    - 內部處理移動方向計算
    - 自動處理邊界檢測
    - 更新太空船位置
- 載入太空船圖片 (image/fighter_M.png)其他方向的圖片先不載入
  - 之後可能會載入多張圖片給太空船使用
  - 所以要用字典的方式存圖片物件

  ```python
  # 載入背景圖片
  img_bg = pygame.image.load("image/space.png")
  # 載入太空船圖片
  img_player_m = pygame.image.load("image/fighter_M.png")  # 載入太空船中間飛行圖片
  # 建立太空船圖片字典
  player_sprites = {"fighter_M": img_player_m}
  ```

- 實現四方向移動控制：
  - 使用上下左右方向鍵控制太空船移動
  - 每次按鍵移動設定的速度值，每次移動 10 像素
- 添加邊界檢測：
  - 在類別內部處理所有邊界檢測邏輯
  - 根據太空船尺寸進行邊界計算
- 太空船初始位置設為畫面中央，尺寸為 80x80
- 簡化主程式結構：
  - 只需獲取按鍵狀態
  - 將按鍵狀態傳給太空船物件處理
  - 保持主迴圈邏輯清晰簡潔
### 步驟 3: 實現轉向效果

- 載入太空船左右轉向圖片 (image/fighter_L.png, image/fighter_R.png)
- 將太空船圖片組織為字典，包含三種狀態：
  - 中間直飛 (image/fighter_M.png)
  - 左轉 (image/fighter_L.png)
  - 右轉 (image/fighter_R.png)
- 增強 `Player` 類別：
  - 添加 `facing_direction` 屬性記錄當前方向狀態
  - 在 `handle_input` 方法中根據移動方向自動更新方向狀態
  - 在 `draw` 方法中根據方向狀態選擇適當的太空船圖片
  - 當按左鍵時顯示左轉圖片
  - 當按右鍵時顯示右轉圖片
  - 其他情況顯示直飛圖片
- 動態計算太空船圖片的尺寸，以適應不同狀態的圖片大小

### 步驟 4: 添加火焰推進效果

- 載入太空船火焰圖片 (image/starship_burner.png)
- 擴展 `Player` 類別：
  - 新增初始化參數 `burner_img`，讓使用者可自訂傳入火焰圖片
  - 在 `__init__` 方法中將 `burner_img` 設為火焰動畫用圖片
  - 添加火焰動畫相關屬性及方法
  - 設定變數 `burn_shift` 控制火焰上下晃動
  - 每幀更新位移值：`burn_shift = (burn_shift + 1) % 12`  # 循環0~11
  - 火焰寬度動態設為太空船寬度的1/4，高度等比例縮放
  - 火焰固定在太空船底部，但有微小的位移變化
- 修改 `Player` 類的 `draw` 方法：
  - 先繪製火焰，再繪製太空船，確保正確的圖層順序
  - 計算火焰與太空船的相對位置關係，並根據太空船寬度動態調整火焰寬度
- 獲取火焰圖片的尺寸以便精確定位
### 步驟 5: 建立飛彈類別

- 創建 `Missile` 類別來管理飛彈：
  - 初始化函式 `__init__` 設定：
    - 位置與尺寸 (x, y, width, height)
    - 速度 (移動速度)
    - 圖片 (飛彈精靈圖片)
    - 狀態 (活躍狀態)
  - 設計 `draw` 方法在螢幕上繪製飛彈
  - 設計 `handle_movement` 方法封裝所有移動相關邏輯：
    - 自動更新位置
    - 處理邊界檢測
    - 控制活躍狀態
  - 設計 `launch` 方法封裝發射邏輯：
    - 設定初始位置（根據玩家「中心點」發射，x=player.rect.centerx, y=player.rect.centery）
    - 設定活躍狀態
    - 重設移動相關參數
- 載入飛彈圖片 (image/bullet.png)
- 簡化主程式發射邏輯：
  - 檢測空白鍵按下
  - 呼叫飛彈的 launch 方法
  - 飛彈物件自行處理後續移動和狀態更新
- 主程式繪圖順序：
  - 先繪製飛彈，再繪製玩家太空船，這樣飛彈會被太空船蓋住底部，看起來像是從太空船身體中間發射出去
### 步驟 6: 實現飛彈連發功能

- 設計飛彈連發機制：
  - 設定飛彈最大同時存在數量常數 `MISSILE_MAX`（如 10），建立一個飛彈物件列表，每個物件皆為 `Missile` 實例。
  - 每次發射時，從飛彈列表中尋找第一個未啟動（`active=False`）的飛彈物件，呼叫其 `launch()` 方法發射，並啟動冷卻計時。
  - 設計飛彈冷卻時間變數 `msl_cooldown`，每次發射後設為最大值 `msl_cooldown_max`，每幀自動遞減，冷卻歸零才能再次發射。
  - 這樣可防止玩家無限連發，並確保同時在畫面上的飛彈數量不超過上限。
- 主程式邏輯：
  - 每幀自動遞減 `msl_cooldown`，確保冷卻機制生效。
  - 處理按鍵事件時，若按下空白鍵且冷卻為零，則遍歷飛彈清單，找到未啟動的飛彈物件進行發射，並重設冷卻。
  - 每幀遍歷飛彈清單，呼叫每個飛彈的 `move()` 方法進行移動，並呼叫 `draw()` 方法繪製所有活躍中的飛彈。
- 這種設計可大幅提升效能，避免頻繁建立/銷毀物件，並讓飛彈發射更流暢自然。
### 步驟 7: 添加敵機類別

- 創建 `Enemy` 類別管理敵機：
  - `__init__` 初始化函式：
    - 位置與尺寸 (x, y, width, height)
    - 速度 (敵機移動速度)
    - 圖片 (img)
    - 以 `pygame.Rect` 建立敵機的矩形區域，方便碰撞與移動管理
  - `move` 方法：
    - 控制敵機垂直向下移動（`self.rect.y += self.speed`）
    - 若敵機超出畫面底部（`self.rect.top > bg_y`），則自動呼叫 `reset()`，將敵機重置到畫面上方隨機位置
  - `reset` 方法：
    - 隨機產生敵機的 X 座標（`random.randint(0, bg_x - self.rect.width)`），Y 座標設為畫面上方外（`-self.rect.height`）
  - `draw` 方法：
    - 若有圖片則繪製圖片，否則以紅色矩形顯示
    - 圖片會根據敵機尺寸自動縮放
- 載入敵機圖片 (image/enemy1.png)
  - 於圖片載入區塊加入：

    ```python
    img_enemy1 = pygame.image.load("image/enemy1.png")
    ```

- 在主程式區塊建立一個敵機物件，初始位置隨機，速度固定，並讓其自動移動與重生：
  - 設定敵機寬高、速度
  - 隨機 X 座標，Y 座標設為畫面上方外
  - 建立敵機物件：

    ```python
    enemy = Enemy(enemy_x, enemy_y, enemy_w, enemy_h, enemy_speed, img_enemy1)
    ```

- 在主程式中呼叫 `enemy.move()` 與 `enemy.draw(screen)` 來更新與繪製敵機
  - 每幀先移動敵機，再繪製敵機
  - 敵機會自動在畫面底部重生，形成無限下落的效果
- 這樣設計可讓敵機持續出現在畫面上，為後續碰撞與分數系統做準備
### 步驟 8: 增加多種敵機類型

- 載入多種敵機圖片：
  - 在圖片載入區塊，載入多張敵機圖片，例如：

    ```python
    img_enemy1 = pygame.image.load("image/enemy1.png")  # 載入敵機圖片1
    img_enemy2 = pygame.image.load("image/enemy2.png")  # 載入敵機圖片2
    ```

  - 建立敵機圖片列表，方便之後隨機選擇：

    ```python
    enemy_images = [img_enemy1, img_enemy2]
    ```

- 修改 `Enemy` 類別，讓每台敵機都能隨機選擇不同圖片：
  - 在 `__init__` 初始化時，將圖片參數改為隨機從 `enemy_images` 選取：

    ```python
    self.img = random.choice(enemy_images)
    ```

  - 在 `reset` 方法中，敵機重生時也隨機選擇一張圖片：

    ```python
    self.img = random.choice(enemy_images)
    ```

- 建立敵機物件時，省略圖片參數，讓 `Enemy` 類別自動隨機選擇圖片：
  - 例如：

    ```python
    enemy = Enemy(enemy_x, enemy_y, enemy_w, enemy_h, enemy_speed)
    ```

- 主程式中，敵機的移動與繪製方式不變：
  - 每幀呼叫 `enemy.move()` 與 `enemy.draw(screen)`，敵機會自動在畫面底部重生並隨機換一種外觀。
- 這樣設計可讓敵機每次出現時都可能是不同造型，讓遊戲畫面更豐富多變。
### 步驟 9: 實現敵機群系統

- 設定敵機數量與屬性：
  - 設定敵機數量常數 `emy_num = 5`，可依需求調整。
  - 設定敵機寬度 `enemy_w = 60`、高度 `enemy_h = 60`、下落速度 `enemy_speed = 5`。
- 建立敵機物件列表：
  - 建立空列表 `emy_list = []` 用於儲存所有敵機物件。
  - 使用 for 迴圈依序建立多個敵機物件：
    - 每個敵機的 x 座標隨機（`random.randint(0, bg_x - enemy_w)`），確保不會超出視窗。
    - y 座標設為 `-enemy_h - random.randint(0, bg_y)`，讓敵機分布於畫面上方外的不同位置，避免同時出現一整排。

- 主程式中敵機群的更新與繪製：
  - 每幀遍歷 `emy_list`，分別呼叫每台敵機的 `move()` 與 `draw(screen)` 方法。
  - 敵機會自動在畫面底部重生，形成無限下落的效果。
- 這樣設計可讓敵機持續出現在畫面上，並且分布隨機，為後續碰撞與分數系統做準備。
### 步驟 10: 子彈碰撞檢測
- 新增一個 `CollisionManager` 類別，專門負責處理遊戲中的碰撞檢測邏輯。
- 主要功能：
  - 檢查玩家飛彈是否擊中敵機。
  - 後續可擴充：檢查玩家與敵機碰撞、敵機子彈與玩家碰撞等
- `CollisionManager` 的初始化方法 `__init__` 需接收以下參數：
  - `enemy_list`：敵機物件列表（每個為 Enemy 實例）
  - `missile_list`：飛彈物件列表（每個為 Missile 實例）
- 建立`is_hit`方法:使用距離公式（x1-x2）^2 + (y1-y2)^2 < r^2 判斷兩個物件是否碰撞。
  - `is_hit` 方法接收兩個物件（如飛彈和敵機）和 半徑 `r`作為參數，計算兩者中心點距離是否小於 `r`。
- 建立`check_collision`方法:
  - 遍歷所有飛彈與敵機，使用 `is_hit` 方法檢查是否有碰撞。
  - 若有碰撞，敵機設為reset狀態，飛彈設為不活躍。
  ### 步驟 11: 聲音與分數系統
- 新增 `score_Manager` 類別，新增一個 `score` 屬性來記錄玩家分數，初始值為 0。
  初始化函式設定：
  -  分數變數 self.score
  -  顯示字體 self.font,
  -  顯示位置 self.pos 與顏色 self.color,
  方法：
  - 增加方法 `add_score(points)` 來增加分數。
  - 增加方法 `deduct_score` 來減分數。
  - 增加方法 `score_reset` 來reset分數。
  - 增加方法 `draw_score` 來在螢幕上繪製分數。
- 新增 `sound_Manager` 類別。
  - 在 `__init__` 方法中載入音效檔案。
  - 新增 `play_sound` 方法來播放音效。
- 在主程式中，新增一個顯示分數的函式 `draw_score`：
  - 使用 `font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 32)` 創建字體物件
- 載入音效檔案：
  - 在圖片載入區塊，載入音效檔案：
    ```python
    sound_explosion = pygame.mixer.Sound("class13\image\hit.mp3")  # 載入爆炸音效
    ```
### 步驟 12: 添加火焰推進效果(敵機)
- 擴展 `Enemy` 類別：
  - 新增初始化參數 `burner_img`，讓使用者可自訂傳入火焰圖片
  - 在 `__init__` 方法中將 `burner_img` 設為火焰動畫用圖片
  - 添加火焰動畫相關屬性及方法
  - 設定變數 `burn_shift` 控制火焰上下晃動
  - 每幀更新位移值：`burn_shift = (burn_shift + 1) % 12`  # 循環0~11
  - 火焰寬度動態設為太空船寬度的1/4，高度等比例縮放
  - 火焰固定在太空船底部，但有微小的位移變化
  - 使用 `pygame.transform.rotate()` 方法動態調整火焰圖片方向(向上)
  - 把火焰繪製於敵機尾端(頂部中間位置)
- 修改 `Player` 類的 `draw` 方法：
  - 先繪製火焰，再繪製太空船，確保正確的圖層順序
  - 計算火焰與太空船的相對位置關係，並根據太空船寬度動態調整火焰寬度
- 獲取火焰圖片的尺寸以便精確定位
### 步驟 13: 敵機爆炸效果
- 擴展 `Enemy` 類別：
  - 新增 `is_exploded` 屬性來記錄敵機是否已經爆炸。
  - 新增 `exp_count` 屬性來記錄目前偵數。
  - 新增 `exp_max` 屬性來記錄爆炸圖片的最大偵數(每張圖顯示5偵，共5張圖，共25偵)。
  - 新增 `explode()` 方法來處理敵機爆炸邏輯：
    - 當敵機被擊中時，設定 `is_exploded` 為 `True`。
    - 每次呼叫 `explode()` 時，增加 `exp_count`。
    - 當 `exp_count` 超過 `exp_max` 時，重置敵機狀態。
    - `move()` :爆炸時不再移動，直到爆炸結束。
    - `reset()` :重置敵機狀態。
  - 新增 `draw_explosion()` 方法來繪製爆炸效果：    
    - 根據 `exp_count` 顯示對應的爆炸圖片。

- 擴展 `CollisionManager` 類別：
  - 在 `check_collision` 方法中，當檢測到飛彈與敵機碰撞時，呼叫敵機的 `explode()` 方法。
- 新增 `explosion_imgs` 列表來儲存爆炸圖片(`explosion1.png`到`explosion5.png`)。
### 步驟 14: 實現太空船無敵效果

-   類別 Player

    -   新增屬性：
        -   invincible：布林值，表示太空船是否處於無敵狀態
        -   invincible_time：整數，記錄無敵剩餘幀數
    -   新增方法：
        -   take_damage(invincible_duration=60)：當太空船未處於無敵狀態時，呼叫此方法會啟動無敵狀態，並將 invincible_time 設為指定幀數（預設 60，約 1 秒）。可於此方法中加入受傷音效或特效
        -   update()：每幀自動遞減 invincible_time，當歸零時自動解除無敵狀態
    -   更新方法：
        -   draw(screen)：無敵期間太空船會閃爍顯示（例如每 4 幀隱藏一次），以提示玩家目前處於無敵狀態，其餘繪圖邏輯不變

-   類別 CollisionManager

    -   新增/更新方法：
        -   check_collisions()：
            -   檢查太空船與敵機碰撞時，若太空船未處於無敵狀態，則呼叫 player.take_damage() 並啟動無敵
            -   敵機同時觸發爆炸動畫

-   在主程式主迴圈中，每幀呼叫 player.update() 以更新無敵狀態。

這樣設計可確保太空船被敵機碰撞後短暫無敵，並以閃爍效果提示玩家，防止連續受傷。