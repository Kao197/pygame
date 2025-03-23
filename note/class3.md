## Python 打磚塊遊戲課程筆記

### 一、載入套件
本程式使用了以下套件：
1. `pygame`：用於建立視窗、繪製圖形及管理遊戲事件。
2. `sys`：用於程式退出。
3. `random`：用於生成隨機顏色。

程式碼：
```python
import pygame as py
import sys
import random as r
```

---

### 二、物件類別
遊戲中的主要物件有兩個：磚塊（Brick）和球（Ball）。

#### 1. 磚塊類別（Brick）
磚塊類別包含屬性和方法：
- 屬性：矩形區域（rect）、顏色（color）、是否被擊中（hit）。
- 方法：
  - `__init__()`：初始化磚塊屬性。
  - `draw()`：繪製未被擊中的磚塊。

#### 2. 球類別（Ball）
球類別包含屬性和方法：
- 屬性：位置（x, y）、半徑（radius）、顏色（color）、速度（speed_x, speed_y）、是否移動（is_moving）。
- 方法：
  - `__init__()`：初始化球的屬性。
  - `draw()`：繪製球。
  - `move()`：控制球的移動。
  - `check_collision()`：檢查球與邊界、底板、磚塊的碰撞並反彈。

---

### 三、初始化設定
使用 `pygame.init()` 進行初始化，並透過 `pygame.time.Clock()` 設定每秒幀數（FPS）。

視窗設定：
- 視窗大小：800x600
- 視窗標題：打磚塊

程式碼：
```python
py.init()
FPS = py.time.Clock()
bg_x = 800
bg_y = 600
py.display.set_caption("打磚塊")
screen = py.display.set_mode((bg_x, bg_y))
```

---

### 四、磚塊排列設定
- 磚塊排數：9
- 磚塊列數：11
- 磚塊大小：58x26
- 磚塊間距：2
- 磚塊顏色：隨機

透過巢狀迴圈建立磚塊，並將其加入磚塊列表（bricks）。

---

### 五、底板與球的設定
- 底板（Pad）：長條形磚塊，放置於視窗底部。
- 球（Ball）：圓形物件，初始位置於底板正上方。

球的速度：水平5、垂直-5。

---

### 六、遊戲邏輯與主程式
遊戲邏輯主要包含以下部分：
1. 事件監聽：處理退出及滑鼠點擊事件。
2. 底板控制：底板隨滑鼠移動。
3. 球的運動與碰撞檢測：確保球在邊界及物件之間反彈。
4. 磚塊繪製與刪除：當磚塊被擊中後，將其設為不可見。
5. 畫面更新：清除並重新繪製所有物件。

---

### 七、程式執行
利用 `py.display.update()` 刷新畫面，以達到每秒60幀（FPS）。

程式碼片段：
```python
for event in py.event.get():
    if event.type == py.QUIT:
        sys.exit()
    if event.type == py.MOUSEBUTTONDOWN:
        if not ball.is_moving:
            ball.is_moving = True
```

---

### 八、總結
本程式透過 Pygame 建立了一個打磚塊遊戲，展示了物件導向程式設計及碰撞偵測的應用。程式運行流暢且具備互動性，適合作為 Pygame 基礎專案練習。

