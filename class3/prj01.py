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


class Ball:
    def __init__(self, x, y, radius, color):
        """
        初始化球\n
        x,y:球的中心座標\n
        radius:球的半徑\n
        color:球的顏色\n
        """
        self.x = x  # 球的x座標
        self.y = y  # 球的y座標
        self.color = color  # 球的顏色
        self.radius = radius  # 球的半徑
        self.speed_x = 5  #  初始水平速度
        self.speed_y = -5  # 初始垂直速度(負數表示向上移動)
        self.is_moving = False  # 球是否在移動

    def draw(self, display_area):
        """
        繪製球\n
        display_area:繪製球的區域\n
        """
        py.draw.circle(
            display_area, self.color, (int(self.x), int(self.y)), self.radius
        )

    def move(self):
        """
        移動球\n
        """
        if self.is_moving:
            self.x += self.speed_x
            self.y += self.speed_y

    def check_collision(self, bg_x, bg_y, bricks, pad):
        """
        檢查碰撞並處理反彈\n
        bg_x,bg_y:視窗的寬度和高度\n
        bricks:磚塊的List\n
        pad:底板物件\n
        """
        # 檢查與視窗邊緣的碰撞
        if self.x - self.radius <= 0 or self.x + self.radius >= bg_x:
            self.speed_x = -self.speed_x
        if self.y - self.radius <= 0:
            self.speed_y = -self.speed_y
        # 檢查是否掉出底部(遊戲結束)
        if self.y + self.radius >= bg_y:
            self.is_moving = False
        # 檢查與底板的碰撞
        if (
            self.y + self.radius >= pad.rect.y
            and self.y + self.radius <= pad.rect.y + pad.rect.height
            and self.x >= pad.rect.x
            and self.x <= pad.rect.x + pad.rect.width
        ):
            self.speed_y = -abs(self.speed_y)
        # 檢查與磚塊的碰撞
        for brick in bricks:
            if not brick.hit:  # 只檢查未被擊中的磚塊
                # 計算球心到磚塊的距離
                dx = abs(self.x - (brick.rect.x + brick.rect.width // 2))
                dy = abs(self.y - (brick.rect.y + brick.rect.height // 2))
                # 檢查是否碰撞
                if (
                    dx < self.radius + brick.rect.width // 2
                    and dy < self.radius + brick.rect.height // 2
                ):
                    brick.hit = True  # 標記磚塊被擊中
                    # 從磚塊的哪一邊碰撞來決定反彈方向
                    if self.x < brick.rect.x or brick.rect.x + brick.rect.width:
                        self.speed_x = -self.speed_x  # 水平反彈
                    else:
                        self.speed_y = -self.speed_y  # 垂直反彈


######################定義函式區######################

######################初始化設定######################
py.init()  # 初始化pygame
FPS = py.time.Clock()  # 設定FPS
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
pad = Brick(0, bg_y - 48, bricks_w, bricks_h, (255, 255, 255))  # 底板的設定
######################球設定######################
ball_radius = 10  # 球的半徑
ball_color = (255, 215, 0)  # 球的顏色
ball = Ball(
    pad.rect.x + bricks_w // 2, pad.rect.y - ball_radius, ball_radius, ball_color
)  # 球的設定
######################遊戲結束設定######################

######################主程式######################
b = 0
while True:
    FPS.tick(60)  # 設定每秒60FPS
    screen.fill((0, 0, 0))  # 清空畫面
    mos_x, mos_y = py.mouse.get_pos()  # 取得滑鼠座標
    pad.rect.x = mos_x - bricks_w // 2  # 設定底板的x座標

    if pad.rect.x < 0:  # 如果底板的x座標小於0
        pad.rect.x = 0  # 設定底板的x座標為0
    if pad.rect.x + bricks_w > bg_x:  # 如果底板的x座標大於視窗的寬度
        pad.rect.x = bg_x - pad.rect.width  # 設定底板的x座標為視窗的寬度減去底板的寬度

    if not ball.is_moving:  # 如果球沒有在移動
        ball.x = pad.rect.x + pad.rect.width // 2
        # 設定球的x座標為底板的x座標加上底板的寬度除以2減去球的半徑
        ball.y = pad.rect.y - ball_radius  # 設定球的y座標為底板的y座標減去球的半徑
    else:
        # 如果球在移動，進行移動和碰撞檢查
        ball.move()  # 移動球
        ball.check_collision(bg_x, bg_y, bricks, pad)  # 檢查與底板的碰撞

    for event in py.event.get():  # 事件處理
        if event.type == py.QUIT:
            sys.exit()
        if event.type == py.MOUSEBUTTONDOWN:
            if not ball.is_moving:
                ball.is_moving = True
    for brick in bricks:
        brick.draw(screen)
    pad.draw(screen)  # 繪製底板
    ball.draw(screen)  # 繪製球
    py.display.update()  # 更新畫面
