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
py.display.set_caption("Pygame挑戰")  # 設定視窗標題
######################建立畫布######################
bg = py.Surface((width, height))  # 建立畫布
bg.fill((255, 255, 255))  # 畫布為白色(255,255,255)
######################循環偵測######################
a = 0
while True:
    for event in py.event.get():
        if event.type == py.QUIT:  # 如果按下{X}按鈕就結束
            sys.exit()  # 離開遊戲
        if event.type == py.MOUSEBUTTONDOWN:  # 如果按下滑鼠按鈕
            a = 1
        if event.type == py.MOUSEBUTTONUP:
            a = 0

    screen.blit(
        bg, (0, 0)
    )  # 繪製畫布於視窗左上角(座標0(x),0(y))(x為橫向座標,y為直向座標)
    if a == 1:
        x, y = py.mouse.get_pos()  # 取得滑鼠座標
        py.draw.circle(bg, (255, 0, 255), (x, y), 5)  # 畫出圓點
    py.display.update()  # 更新畫面，並且清除畫面
