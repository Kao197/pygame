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
        # 根據顏色決定分數
        r, g, b = color
        if r > max(g, b):  # 紅色系
            self.score = 30
        elif g > max(r, b):  # 綠色系
            self.score = 20
        else:  # 藍色系
            self.score = 10

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
            global lives
            lives -= 1  # 扣除生命值

        # 檢查與底板的碰撞
        if (
            self.y + self.radius >= pad.rect.y
            and self.y - self.radius <= pad.rect.y + pad.rect.height
            and self.x + self.radius >= pad.rect.x
            and self.x - self.radius <= pad.rect.x + pad.rect.width
        ):
            # 確保球從底板上方反彈
            if self.y <= pad.rect.y + pad.rect.height / 2:
                self.y = pad.rect.y - self.radius
                self.speed_y = -abs(self.speed_y)

        # 檢查與磚塊的碰撞
        for brick in bricks:
            if not brick.hit:
                # 計算球和磚塊的相對位置
                closest_x = max(brick.rect.left, min(self.x, brick.rect.right))
                closest_y = max(brick.rect.top, min(self.y, brick.rect.bottom))

                # 計算球心到磚塊最近點的距離
                distance_x = self.x - closest_x
                distance_y = self.y - closest_y
                distance = (distance_x**2 + distance_y**2) ** 0.5

                # 如果距離小於球的半徑，發生碰撞
                if distance <= self.radius:
                    brick.hit = True
                    global score
                    score += brick.score

                    # 根據碰撞點位置決定反彈方向
                    if abs(distance_x) > abs(distance_y):
                        self.speed_x = -self.speed_x
                    else:
                        self.speed_y = -self.speed_y

                    # 避免球卡在磚塊內
                    overlap = self.radius - distance
                    if overlap > 0:
                        if abs(distance_x) > abs(distance_y):
                            self.x += overlap * (1 if distance_x < 0 else -1)
                        else:
                            self.y += overlap * (1 if distance_y < 0 else -1)


######################定義函式區######################

######################初始化設定######################
py.init()  # 初始化pygame
FPS = py.time.Clock()  # 設定FPS
score = 0  # 新增分數變數
lives = 5  # 新增生命值
py.font.init()  # 初始化字型
font = py.font.SysFont("microsoft jhengHei", 32)  # 建立字型物件
game_over_font = py.font.SysFont("microsoft jhengHei", 64)  # 遊戲結束字型


def reset_game():
    """重置遊戲"""
    global score, lives, bricks
    score = 0
    lives = 5
    # 重新生成磚塊
    bricks.clear()
    for col in range(bricks_col):
        for row in range(bricks_row):
            x = col * (bricks_w + bricks_gap) + 70
            y = row * (bricks_h + bricks_gap) + 60
            color = (r.randint(128, 255), r.randint(128, 255), r.randint(128, 255))
            brick = Brick(x, y, bricks_w, bricks_h, color)
            bricks.append(brick)
    ball.is_moving = False


######################載入圖片######################

######################遊戲視窗設定######################
bg_x = 800
bg_y = 600
bg_size = (bg_x, bg_y)
py.display.set_caption("打磚塊遊戲")  # 修改遊戲標題
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
        color = (
            r.randint(128, 255),
            r.randint(128, 255),
            r.randint(128, 255),
        )  # 修改顏色範圍
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

    # 處理所有事件
    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()
        if event.type == py.MOUSEBUTTONDOWN and not ball.is_moving and lives > 0:
            ball.is_moving = True
        if event.type == py.KEYDOWN:
            if event.key == py.K_SPACE and lives <= 0:
                reset_game()

    if lives > 0:
        mos_x, mos_y = py.mouse.get_pos()  # 取得滑鼠座標
        pad.rect.x = mos_x - bricks_w // 2  # 設定底板的x座標

        if pad.rect.x < 0:  # 如果底板的x座標小於0
            pad.rect.x = 0  # 設定底板的x座標為0
        if pad.rect.x + bricks_w > bg_x:  # 如果底板的x座標大於視窗的寬度
            pad.rect.x = (
                bg_x - pad.rect.width
            )  # 設定底板的x座標為視窗的寬度減去底板的寬度

        if not ball.is_moving:  # 如果球沒有在移動
            ball.x = pad.rect.x + pad.rect.width // 2
            # 設定球的x座標為底板的x座標加上底板的寬度除以2減去球的半徑
            ball.y = pad.rect.y - ball_radius  # 設定球的y座標為底板的y座標減去球的半徑
        else:
            # 如果球在移動，進行移動和碰撞檢查
            ball.move()  # 移動球
            ball.check_collision(bg_x, bg_y, bricks, pad)  # 檢查與底板的碰撞

        for brick in bricks:
            brick.draw(screen)
        pad.draw(screen)  # 繪製底板
        ball.draw(screen)  # 繪製球

        # 顯示分數與生命值
        score_text = font.render(f"目前分數：{score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        lives_text = font.render(f"剩餘生命：{lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))
    else:
        # 顯示遊戲結束
        game_over_text = game_over_font.render("遊戲結束", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(bg_x / 2, bg_y / 2 - 50))
        screen.blit(game_over_text, text_rect)

        # 顯示最終分數
        final_score_text = font.render(f"最終分數：{score}", True, (255, 255, 255))
        score_rect = final_score_text.get_rect(center=(bg_x / 2, bg_y / 2))
        screen.blit(final_score_text, score_rect)

        # 顯示重新開始提示
        restart_text = font.render("按空白鍵重新開始", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(bg_x / 2, bg_y / 2 + 50))
        screen.blit(restart_text, restart_rect)

    py.display.update()  # 更新畫面
