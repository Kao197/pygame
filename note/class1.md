# Pygame 基礎課程筆記

## 1. 匯入模組
在使用 Pygame 之前，首先需要安裝並匯入 Pygame 模組。以下為安裝與匯入的方法：

### 安裝 Pygame
在終端機或命令提示字元中輸入以下指令來安裝 Pygame：
```
pip install pygame -U
```

### 匯入模組
匯入 Pygame 並使用縮寫 `py` 來方便後續使用：
```python
import pygame as py
import sys
import math
```
- `sys`：用於程式結束操作。
- `math`：用於數學運算，如弧度轉換。

## 2. 初始化
初始化是使用 Pygame 的第一步，使用 `py.init()` 來完成初始化：
```python
py.init()
```
設定畫面寬度與高度：
```python
width = 640
height = 320
```

## 3. 建立視窗及物件
建立視窗及設定標題：
```python
screen = py.display.set_mode((width, height))
py.display.set_caption("Pygame範例")
```
- `set_mode((width, height))`：設定視窗大小。
- `set_caption("標題")`：設定視窗標題。

## 4. 建立畫布
畫布是繪製圖形的區域，使用 `Surface` 物件建立畫布並填充背景顏色：
```python
bg = py.Surface((width, height))
bg.fill((255, 255, 255))
```
- `(255, 255, 255)`：代表白色（RGB 顏色格式）。

## 5. 繪製圖形
Pygame 提供多種繪圖函式，以下是幾種常見圖形繪製方法：

### 方形
```python
py.draw.rect(bg, (255, 0, 0), (100, 100, 100, 100), 0)
```
- 紅色方形，(x, y, 寬, 高)，線寬為 `0` 表示填滿。

### 圓形
```python
py.draw.circle(bg, (0, 255, 0), (300, 150), 50, 0)
```
- 綠色圓形，圓心 (300, 150)，半徑 `50`。

### 橢圓形
```python
py.draw.ellipse(bg, (0, 0, 255), (400, 100, 100, 200), 0)
```
- 藍色橢圓形，矩形範圍 (x, y, 寬, 高)。

### 直線
```python
py.draw.line(bg, (255, 0, 255), (0, 0), (width, height), 5)
```
- 紫色線條，起點 (0, 0)，終點 (640, 320)，線寬為 `5`。

### 多邊形
```python
py.draw.polygon(bg, (0, 255, 255), [[100, 100], [0, 200], [200, 200]], 0)
```
- 青色三角形，頂點座標為三個點。

### 圓弧
```python
py.draw.arc(bg, (255, 255, 0), [100, 100, 100, 100], math.radians(180), math.radians(0), 2)
```
- 黃色圓弧，從 180 度到 0 度。

## 6. 事件循環
Pygame 程式需要持續監測事件來回應操作：
```python
while True:
    x, y = py.mouse.get_pos()
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()
        if event.type == py.MOUSEBUTTONDOWN:
            print("click")
            print(f"mouse position: {x},{y}")
    screen.blit(bg, (0, 0))
    py.display.update()
```
- `QUIT`：偵測視窗關閉事件。
- `MOUSEBUTTONDOWN`：偵測滑鼠按鍵按下事件。
- `get_pos()`：取得滑鼠座標。
- `blit()`：將畫布繪製到視窗上。
- `update()`：更新畫面內容。

## 7. 程式結束
當偵測到離開事件時，透過 `sys.exit()` 來結束程式。

