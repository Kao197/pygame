###################### 匯入模組 ######################
import pygame as py  # pip install pygame -U
import sys

###################### 初始化 ######################
py.init()
width = 640
height = 320

###################### 建立視窗及物件 ######################
screen = py.display.set_mode((width, height))  # 設定視窗大小
py.display.set_caption("Pygame挑戰")  # 設定視窗標題

###################### 建立畫布 ######################
bg = py.Surface((width, height))  # 建立畫布
bg.fill((255, 255, 255))  # 畫布為白色(255,255,255)

###################### 循環偵測 ######################
a = 0
running = True  # 遊戲運行狀態

while running:
    for event in py.event.get():  # 取得事件
        if event.type == py.QUIT:  # 如果按下{X}按鈕就結束
            running = False

        elif event.type == py.MOUSEBUTTONDOWN:  # 如果按下滑鼠按鈕
            a = not a  # 切換 a 的狀態

    if a:
        x, y = py.mouse.get_pos()  # 取得滑鼠座標
        py.draw.circle(bg, (255, 0, 255), (x, y), 5)  # 畫出圓點

    screen.blit(bg, (0, 0))  # 繪製畫布於視窗左上角
    py.display.update()  # 更新畫面

py.quit()  # 退出 Pygame
sys.exit()  # 結束程式
