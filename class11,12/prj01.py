###################### 載入套件區塊 ######################
import pygame as py
import sys
import os
from pygame.locals import *


###################### 定義函式區塊 ######################
def roll_bg(screen, bg_img, roll_y):
    """
    實現背景捲動效果
    :param screen: 遊戲視窗
    :param bg_img: 背景圖片
    :param roll_y: 當前捲動的y座標
    """
    bg_height = bg_img.get_height()
    # 先畫出上半部
    screen.blit(bg_img, (0, roll_y - bg_height))
    # 再畫出下半部
    screen.blit(bg_img, (0, roll_y))


###################### 初始化設定區塊 ######################
# 切換工作目錄到程式所在位置，避免路徑問題
os.chdir(sys.path[0])
py.init()  # 初始化pygame
clock = py.time.Clock()  # 建立時鐘物件控制遊戲速度

###################### 載入圖片區塊 ######################
bg_img = py.image.load("image/space.png")  # 載入太空背景圖片

###################### 遊戲視窗設定區塊 ######################
py.display.set_caption("Galaxy Lancer")  # 設定視窗標題
bg_w, bg_h = bg_img.get_size()  # 取得背景圖片尺寸
screen = py.display.set_mode((bg_w, bg_h))  # 設定視窗大小
roll_y = 0  # 捲動背景的y座標初始值

###################### 玩家設定區塊 ######################
# 步驟1暫不處理玩家物件

###################### 主程式區塊 ######################
while True:
    clock.tick(60)  # 設定每秒60幀
    # 處理事件
    for event in py.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_F1:
                # 切換全螢幕
                screen = py.display.set_mode((bg_w, bg_h), FULLSCREEN)
            elif event.key == K_ESCAPE:
                # 返回視窗模式
                screen = py.display.set_mode((bg_w, bg_h))
    # 更新捲動背景座標
    roll_y = (roll_y + 10) % bg_h
    # 畫出捲動背景
    roll_bg(screen, bg_img, roll_y)
    # 更新畫面
    py.display.update()
