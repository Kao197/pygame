######################載入套件######################
import pygame as py
import sys
import random as r  # 之後用於隨機產生平台位置


######################物件類別######################
class Platform:
    def __init__(self, x, y, width, height, color):
        """
        初始化平台\n
        x,y: 平台的左上角座標\n
        width,height: 平台的寬度和高度\n
        color: 平台的顏色\n
        """
        self.rect = py.Rect(x, y, width, height)  # 平台的矩形區域
        self.color = color  # 平台的顏色

    def draw(self, display_area):
        """
        繪製平台\n
        display_area: 繪製平台的遊戲視窗\n
        """
        py.draw.rect(display_area, self.color, self.rect)  # 繪製矩形平台


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
        self.speed = 5  # 主角的移動速度

    def draw(self, display_area):
        """
        繪製主角\n
        display_area: 繪製主角的區域\n
        """
        py.draw.rect(display_area, self.color, self.rect)

    def move(self, direction, bg_x):
        """
        移動主角\n
        direction: 移動方向 (1為右, -1為左)\n
        bg_x: 遊戲視窗寬度，用於檢查邊界\n
        """
        # 更新主角的X座標
        self.rect.x += direction * self.speed

        # 檢查是否超出左邊界
        if self.rect.left < 0:
            self.rect.right = bg_x  # 從右邊出現

        # 檢查是否超出右邊界
        elif self.rect.right > bg_x:
            self.rect.left = 0  # 從左邊出現

    def check_platform_collision(self, platforms):
        """
        檢查是否與平台發生碰撞\n
        platforms: 平台的列表\n
        """
        for platform in platforms:
            if self.rect.colliderect(platform.rect):  # 使用pygame內建的碰撞檢測
                return True
        return False


######################初始化設定######################
py.init()  # 初始化pygame
FPS = py.time.Clock()  # 設定FPS時鐘物件

######################遊戲視窗設定######################
bg_x = 400  # 視窗寬度
bg_y = 600  # 視窗高度
bg_size = (bg_x, bg_y)  # 設定視窗大小
py.display.set_caption("Doodle Jump")  # 設定視窗標題
screen = py.display.set_mode(bg_size)  # 建立視窗

######################平台設定######################
platform_list = []  # 存放所有平台的列表
platform_width = 60  # 平台寬度
platform_height = 10  # 平台高度
platform_color = (255, 255, 255)  # 平台顏色(白色)

# 建立一些靜態平台
test_platforms = [
    (100, 400),  # (x, y)座標
    (200, 300),
    (300, 200),
    (150, 500),
]

# 將平台加入列表中
for plat_x, plat_y in test_platforms:
    platform = Platform(plat_x, plat_y, platform_width, platform_height, platform_color)
    platform_list.append(platform)

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

    # 取得鍵盤輸入狀態
    keys = py.key.get_pressed()
    # 檢查左右鍵的按下狀態並移動主角
    if keys[py.K_LEFT]:  # 如果按下左方向鍵
        player.move(-1, bg_x)  # 向左移動
    if keys[py.K_RIGHT]:  # 如果按下右方向鍵
        player.move(1, bg_x)  # 向右移動

    # 繪製所有平台
    for platform in platform_list:
        platform.draw(screen)

    # 繪製主角
    player.draw(screen)

    # 更新畫面
    py.display.update()
