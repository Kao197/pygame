## Python Pygame 課程筆記

### 一、載入套件
使用 Pygame 進行遊戲開發前，需先安裝並匯入必要模組。
```python
import pygame as py  # pip install pygame -U
import sys
import random as r  # 隨機模組
```

---

### 二、物件類別
#### 1. 磚塊類別 (Brick)
建立磚塊類別，包含初始化與繪製功能。

**程式碼範例：**
```python
class Brick:
    def __init__(self, x, y, width, height, color):
        self.rect = py.Rect(x, y, width, height)  # 磚塊矩形區域
        self.color = color  # 磚塊顏色
        self.hit = False  # 判斷磚塊是否被擊中

    def draw(self, display_area):
        if not self.hit:
            py.draw.rect(display_area, self.color, self.rect)
```

---

### 三、初始化設定
使用 `py.init()` 進行 Pygame 初始化。

**程式碼範例：**
```python
py.init()
```

---

### 四、遊戲視窗設定
設定遊戲視窗大小及標題。

**程式碼範例：**
```python
bg_x = 800
bg_y = 600
bg_size = (bg_x, bg_y)
py.display.set_caption("打磚塊")
screen = py.display.set_mode((bg_size))
```

---

### 五、磚塊生成
透過迴圈生成多個磚塊，並隨機指定顏色。

**程式碼範例：**
```python
bricks_row = 9  # 磚塊橫排數量
bricks_col = 11  # 磚塊直排數量
bricks_w = 58  # 磚塊寬度
bricks_h = 26  # 磚塊高度
bricks_gap = 2  # 磚塊間距
bricks = []  # 磚塊物件列表
for col in range(bricks_col):
    for row in range(bricks_row):
        x = col * (bricks_w + bricks_gap) + 70
        y = row * (bricks_h + bricks_gap) + 60
        color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))
        brick = Brick(x, y, bricks_w, bricks_h, color)
        bricks.append(brick)
```

---

### 六、主程式迴圈
透過事件處理與畫面更新，保持遊戲運行。

**程式碼範例：**
```python
while True:
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()
    for brick in bricks:
        brick.draw(screen)
    py.display.update()
```

---

### 七、課程總結
透過此程式，我們學習了以下技巧：
1. Pygame 的初始化與基本設定。
2. 物件類別的設計與繪製方法。
3. 利用隨機顏色生成多個磚塊。
4. 主程式迴圈的設計與事件處理。

