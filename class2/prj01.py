######################載入套件######################
import pygame as py
import sys


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
brickA = Brick(0, 0, 50, 50, (255, 0, 0))  # 磚塊A
brickB = Brick(100, 0, 100, 50, (0, 255, 0))  # 磚塊B
######################顯示文字設定######################

######################底板設定######################

######################球設定######################

######################遊戲結束設定######################

######################主程式######################
while True:
    for event in py.event.get():  # 事件處理
        if event.type == py.QUIT:
            sys.exit()
    # brickA.rect.x = 100  # 改磚塊A的座標
    # brickA.rect.y = 100  # 改磚塊A的座標
    # brickA.rect.width = 200  # 改磚塊A的寬度
    # brickA.rect.height = 200  # 改磚塊A的高度
    brickA.draw(screen)  # 繪製磚塊A
    brickB.draw(screen)  # 繪製磚塊B
    py.display.update()  # 更新畫面
