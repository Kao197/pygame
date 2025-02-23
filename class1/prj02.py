######################匯入模組######################
import pygame as py  # pip install pygame -U
import sys
import math

######################初始化######################
py.init()
width = 640
height = 320
######################建立視窗及物件######################
screen = py.display.set_mode((width, height))  # 設定視窗大小
py.display.set_caption("Pygame範例")  # 設定視窗標題
######################建立畫布######################
bg = py.Surface((width, height))  # 建立畫布
bg.fill((255, 255, 255))  # 畫布為白色(255,255,255)
######################繪製圖形######################
# 畫方形(畫布, 顏色, (x,y,寬,高), 線寬)
py.draw.rect(bg, (255, 0, 0), (100, 100, 100, 100), 0)  # 繪製紅色方形
# 畫圓形(畫布, 顏色, 圓心, 半徑, 線寬)
py.draw.circle(bg, (0, 255, 0), (300, 150), 50, 0)  # 繪製綠色圓形
# 畫橢圓形(畫布, 顏色, (x,y,寬,高), 線寬)
py.draw.ellipse(bg, (0, 0, 255), (400, 100, 100, 200), 0)  # 繪製藍色橢圓形
# 畫線(畫布, 顏色, 起點, 終點, 線寬)
py.draw.line(bg, (255, 0, 255), (0, 0), (width, height), 5)  # 繪製紫色線
# 畫多邊形(畫布, 顏色,  [[x1, y1], [x2, y2], [x3, y3]], 線寬)
py.draw.polygon(
    bg, (0, 255, 255), [[100, 100], [0, 200], [200, 200]], 0
)  # 繪製青色三角形
# 畫圓弧(畫布, 顏色, [x,y,寬,高], 起始角度, 結束角度, 線寬)
py.draw.arc(
    bg, (255, 255, 0), [100, 100, 100, 100], math.radians(180), math.radians(0), 2
)  # 繪製黃色圓弧

######################循環偵測######################
while True:
    x, y = py.mouse.get_pos()  # 取得滑鼠座標
    for event in py.event.get():
        if event.type == py.QUIT:  # 如果按下{X}按鈕就結束
            sys.exit()  # 離開遊戲
        if event.type == py.MOUSEBUTTONDOWN:  # 如果按下滑鼠按鈕
            print("click")
            print(f"mouse position: {x},{y}")  # 印出滑鼠座標
    screen.blit(
        bg, (0, 0)
    )  # 繪製畫布於視窗左上角(座標0(x),0(y))(x為橫向座標,y為直向座標)
    py.display.update()  # 更新畫面，並且清除畫面
