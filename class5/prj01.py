######################載入套件######################
import pygame as py
import sys


######################物件類別######################
class Player:
    def __init__(self, x, y, width, height, color):
        """
        初始化主角\n
        x,y: 主角的左上角座標\n
        width,height: 主角的寬度和高度\n
        color: 主角的顏色\n
        """
        self.rect = py.Rect(x, y, width, height)  # 主角的矩形區域
        self.color = color  # 主角的顏色

    def draw(self, display_area):
        """
        繪製主角\n
        display_area: 繪製主角的區域\n
        """
        py.draw.rect(display_area, self.color, self.rect)


######################初始化設定######################
py.init()  # 初始化pygame
FPS = py.time.Clock()  # 設定FPS時鐘物件

######################遊戲視窗設定######################
bg_x = 400  # 視窗寬度
bg_y = 600  # 視窗高度
bg_size = (bg_x, bg_y)  # 設定視窗大小
py.display.set_caption("Doodle Jump")  # 設定視窗標題
screen = py.display.set_mode(bg_size)  # 建立視窗

######################主角設定######################
player_width = 30  # 主角寬度
player_height = 30  # 主角高度
player_x = (bg_x - player_width) // 2  # 主角初始x座標(置中)
player_y = bg_y - player_height - 50  # 主角初始y座標(底部)
player_color = (0, 255, 0)  # 主角顏色(綠色)
player = Player(
    player_x, player_y, player_width, player_height, player_color
)  # 建立主角物件

######################主程式######################
while True:
    FPS.tick(60)  # 設定每秒更新60次
    screen.fill((0, 0, 0))  # 清空畫面(黑色背景)

    # 事件處理
    for event in py.event.get():
        if event.type == py.QUIT:  # 如果按下視窗的關閉按鈕
            sys.exit()  # 退出遊戲

    # 繪製主角
    player.draw(screen)

    # 更新畫面
    py.display.update()
