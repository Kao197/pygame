######################載入套件######################
import pygame as py
import sys
import random as r


######################物件類別######################
class Brick:  # 因為是物件因此用大寫字母開頭
    def __init__(self, x, y, width, height, color):
        """
        初始化磚塊\n
        x,y:磚塊的左上角座標\n
        width,height:磚塊的寬度和高度\n
        color:磚塊的顏色\n
        """
        self.rect = py.Rect(x, y, width, height)  # 磚塊的矩形區域
        self.color = color  # 磚塊的顏色
        self.hit = False  # 磚塊是否被擊中

    def draw(self, display_area):
        """
        繪製磚塊\n
        display_area:繪製磚塊的區域\n
        """
        if not self.hit:
            py.draw.rect(display_area, self.color, self.rect)


######################定義函式區######################

######################初始化設定######################
py.init()  # 初始化pygame
######################載入圖片######################

######################遊戲視窗設定######################
bg_x = 800
bg_y = 600
bg_size = (bg_x, bg_y)  # 設定視窗大小
py.display.set_caption("打磚塊")  # 設定視窗標題
screen = py.display.set_mode((bg_size))  # 設定視窗大小
######################磚塊######################
bricks_row = 9  # 磚塊有幾個橫排
bricks_col = 11  # 磚塊有幾個直排
bricks_w = 58  # 磚塊的寬度
bricks_h = 26  # 磚塊的高度
bricks_gap = 2  # 磚塊的間距
bricks = []  # 用來存放磚塊物件的List
for col in range(bricks_col):
    for row in range(bricks_row):
        x = col * (bricks_w + bricks_gap) + 70  # 70是磚塊的起始x座標
        y = row * (bricks_h + bricks_gap) + 60  # 60是磚塊的起始y座標
        color = (r.randint(0, 255), r.randint(0, 255), r.randint(0, 255))  # 隨機顏色
        brick = Brick(x, y, bricks_w, bricks_h, color)  # 建立磚塊物件
        bricks.append(brick)  # 將磚塊物件加入List
######################顯示文字設定######################

######################底板設定######################

######################球設定######################

######################遊戲結束設定######################

######################主程式######################
while True:
    for event in py.event.get():  # 事件處理
        if event.type == py.QUIT:
            sys.exit()
    for brick in bricks:
        brick.draw(screen)
    py.display.update()  # 更新畫面
