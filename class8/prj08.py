######################載入套件######################
import pygame as py
import sys
import random as r


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

    def draw(self, display_area, camera_y):
        """
        繪製平台\n
        display_area: 繪製平台的遊戲視窗\n
        camera_y: 攝影機的Y軸位置\n
        """
        # 建立新的矩形，考慮攝影機位置進行繪製
        platform_rect = py.Rect(
            self.rect.x,
            self.rect.y - camera_y,  # 扣除攝影機位置來計算顯示位置
            self.rect.width,
            self.rect.height,
        )
        py.draw.rect(display_area, self.color, platform_rect)


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
        self.speed_x = 5  # 水平移動速度
        self.speed_y = 0  # 垂直速度(初始為0)
        self.jump_speed = -10  # 跳躍初始速度(負值表示向上)
        self.gravity = 0.5  # 重力加速度
        self.is_jumping = False  # 是否正在跳躍
        self.initial_y = y  # 記錄初始Y座標，用於計算分數
        self.highest_y = y  # 記錄最高到達位置
        self.is_dead = False  # 新增遊戲結束檢查

    def draw(self, display_area, camera_y):
        """
        繪製主角\n
        display_area: 繪製主角的遊戲視窗\n
        camera_y: 攝影機的Y軸位置\n
        """
        # 建立新的矩形，考慮攝影機位置進行繪製
        player_rect = py.Rect(
            self.rect.x,
            self.rect.y - camera_y,  # 扣除攝影機位置來計算顯示位置
            self.rect.width,
            self.rect.height,
        )
        py.draw.rect(display_area, self.color, player_rect)

    def move(self, direction, bg_x):
        """
        移動主角\n
        direction: 移動方向 (1為右, -1為左)\n
        bg_x: 遊戲視窗寬度，用於檢查邊界\n
        """
        # 更新主角的X座標
        self.rect.x += direction * self.speed_x

        # 檢查是否超出左邊界
        if self.rect.left < 0:
            self.rect.right = bg_x  # 從右邊出現

        # 檢查是否超出右邊界
        elif self.rect.right > bg_x:
            self.rect.left = 0  # 從左邊出現

    def apply_gravity(self):
        """
        套用重力效果\n
        更新主角的垂直速度和位置
        """
        self.speed_y += self.gravity  # 速度受重力影響
        self.rect.y += self.speed_y  # 更新垂直位置

    def check_platform_collision(self, platforms):
        """
        檢查與平台的碰撞\n
        platforms: 平台的列表\n
        只在往下掉的時候檢查碰撞
        """
        if self.speed_y > 0:  # 只在下降時檢查
            for platform in platforms:
                if self.rect.colliderect(platform.rect):  # 使用pygame內建的碰撞檢測
                    # 確保是從平台上方碰撞
                    if self.rect.bottom >= platform.rect.top:
                        self.rect.bottom = platform.rect.top  # 調整位置
                        self.speed_y = self.jump_speed  # 碰到平台後彈跳
                        return True
        return False

    def check_death(self, camera_y, bg_y):
        """
        檢查玩家是否死亡\n
        camera_y: 攝影機Y軸位置\n
        bg_y: 遊戲視窗高度\n
        """
        # 當玩家掉出畫面底部，判定死亡
        if self.rect.y - camera_y > bg_y + 100:
            self.is_dead = True

    def update_score(self):
        """
        更新分數\n
        根據玩家達到的最高位置計算分數
        """
        # 更新最高點紀錄
        if self.rect.y < self.highest_y:
            self.highest_y = self.rect.y
        # 計算分數 (每上升100像素獲得100分)
        return int((self.initial_y - self.highest_y) / 100) * 100


######################新增平台管理功能######################
def generate_platforms():
    """
    隨機生成平台\n
    確保平台間距固定，讓玩家能夠跳躍到達
    """
    platform_list.clear()
    spring_list.clear()  # 清空彈簧列表

    # 先生成最下方的平台
    bottom_platform = Platform(
        (bg_x - platform_width) // 2,  # 平台X座標置中
        bg_y - 60,  # 固定在底部上方一點的位置
        platform_width,
        platform_height,
        platform_color,
    )
    platform_list.append(bottom_platform)

    # 生成其他平台
    current_y = bg_y - 60
    for i in range(1, platform_count):
        plat_x = r.randint(0, bg_x - platform_width)
        current_y -= 60  # 固定間距60
        platform = Platform(
            plat_x, current_y, platform_width, platform_height, platform_color
        )
        platform_list.append(platform)

        # 隨機決定是否在平台上生成彈簧
        if r.random() < spring_chance:
            spring = Spring(platform)
            spring_list.append(spring)


def manage_platforms(platforms, player, camera_y, bg_x):
    """
    管理平台的生成和移除\n
    platforms: 平台列表\n
    player: 主角物件\n
    camera_y: 攝影機Y軸位置\n
    bg_x: 遊戲視窗寬度\n
    """
    # 移除離開視窗太遠的平台
    remaining_platforms = []
    for p in platforms:
        if p.rect.y - camera_y < bg_y:
            remaining_platforms.append(p)
    platforms[:] = remaining_platforms

    # 當平台數量太少時，在上方生成新平台
    while len(platforms) < platform_count:
        # 取得最高的平台Y座標
        highest_y = float("inf")
        for p in platforms:
            if p.rect.y < highest_y:
                highest_y = p.rect.y

        # 在上方生成新平台，固定間距60
        new_x = r.randint(0, bg_x - 60)
        new_y = highest_y - 60  # 固定間距

        new_platform = Platform(new_x, new_y, 60, 10, (255, 255, 255))
        platforms.append(new_platform)

        # 隨機決定是否在新平台上生成彈簧
        if r.random() < spring_chance:
            spring = Spring(new_platform)
            spring_list.append(spring)


######################新增文字顯示功能######################
def draw_text(screen, text, size, x, y, color):
    """
    在畫面上顯示文字\n
    screen: 遊戲視窗\n
    text: 要顯示的文字\n
    size: 文字大小\n
    x,y: 文字位置\n
    color: 文字顏色\n
    """
    font = py.font.Font("C:/Windows/Fonts/msjh.ttc", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    screen.blit(text_surface, text_rect)


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
platform_count = r.randint(8, 10) + 10  # 隨機決定要生成的平台數量

######################彈簧設定######################
spring_list = []  # 存放所有彈簧的列表
spring_chance = 0.2  # 彈簧生成機率(20%)


class Spring:
    def __init__(self, platform):
        """
        初始化彈簧道具\n
        platform: 彈簧所在的平台\n
        """
        self.width = 20  # 彈簧寬度
        self.height = 10  # 彈簧高度
        self.color = (255, 255, 0)  # 彈簧顏色(黃色)
        # 將彈簧放在平台上方中央
        self.rect = py.Rect(
            platform.rect.x + (platform.rect.width - self.width) // 2,
            platform.rect.y - self.height,
            self.width,
            self.height,
        )

    def draw(self, display_area, camera_y):
        """
        繪製彈簧\n
        display_area: 繪製彈簧的遊戲視窗\n
        camera_y: 攝影機的Y軸位置\n
        """
        spring_rect = py.Rect(
            self.rect.x, self.rect.y - camera_y, self.rect.width, self.rect.height
        )
        py.draw.rect(display_area, self.color, spring_rect)


# 定義生成平台的函式
def generate_platforms():
    """
    隨機生成平台\n
    確保平台間距固定，讓玩家能夠跳躍到達
    """
    platform_list.clear()
    spring_list.clear()  # 清空彈簧列表

    # 先生成最下方的平台
    bottom_platform = Platform(
        (bg_x - platform_width) // 2,  # 平台X座標置中
        bg_y - 60,  # 固定在底部上方一點的位置
        platform_width,
        platform_height,
        platform_color,
    )
    platform_list.append(bottom_platform)

    # 生成其他平台
    current_y = bg_y - 60
    for i in range(1, platform_count):
        plat_x = r.randint(0, bg_x - platform_width)
        current_y -= 60  # 固定間距60
        platform = Platform(
            plat_x, current_y, platform_width, platform_height, platform_color
        )
        platform_list.append(platform)

        # 隨機決定是否在平台上生成彈簧
        if r.random() < spring_chance:
            spring = Spring(platform)
            spring_list.append(spring)


# 初始生成平台
generate_platforms()

######################主角設定######################
player_width = 30
player_height = 30
player_x = (bg_x - player_width) // 2  # 主角X座標置中
player_y = bg_y - 90  # 設定在最下方平台上方
player_color = (0, 255, 0)
player = Player(
    player_x, player_y, player_width, player_height, player_color
)  # 建立主角物件，讓主角一開始就有向上的初始速度
player.speed_y = player.jump_speed

######################新增攝影機設定######################
camera_y = 0  # 攝影機Y軸位置
target_camera_y = 0  # 目標攝影機Y軸位置

######################主程式######################
game_over = False  # 新增遊戲結束判定變數
high_score = 0  # 新增最高分紀錄

while True:
    FPS.tick(60)  # 設定每秒更新60次
    screen.fill((0, 0, 0))  # 清空畫面(黑色背景)

    for event in py.event.get():
        if event.type == py.QUIT:
            sys.exit()
        # 新增遊戲結束時的重新開始功能
        if event.type == py.KEYDOWN and player.is_dead:
            if event.key == py.K_SPACE:
                # 重置遊戲
                player.rect.x = player_x
                player.rect.y = player_y
                player.highest_y = player_y
                player.speed_y = player.jump_speed
                player.is_dead = False
                camera_y = 0
                target_camera_y = 0
                platform_list.clear()
                generate_platforms()
                game_over = False

    if not game_over:
        # 取得鍵盤輸入狀態並控制主角移動
        keys = py.key.get_pressed()
        # 檢查左右鍵的按下狀態並移動主角
        if keys[py.K_LEFT]:  # 如果按下左方向鍵
            player.move(-1, bg_x)  # 向左移動
        if keys[py.K_RIGHT]:  # 如果按下右方向鍵
            player.move(1, bg_x)  # 向右移動

        # 更新攝影機位置
        if player.rect.y < bg_y * 0.6 and player.rect.y < target_camera_y + bg_y * 0.6:
            # 只有當玩家位置比目前相機高度更高時才更新目標位置
            target_camera_y = player.rect.y - bg_y * 0.6
        camera_y += (target_camera_y - camera_y) * 0.1  # 降低跟隨速度以減少晃動

        # 套用重力和處理碰撞
        player.apply_gravity()  # 套用重力效果
        player.check_platform_collision(platform_list)  # 檢查平台碰撞

        # 管理平台
        manage_platforms(platform_list, player, camera_y, bg_x)

        # 繪製所有平台
        for platform in platform_list:
            platform.draw(screen, camera_y)

        # 繪製所有彈簧
        for spring in spring_list:
            spring.draw(screen, camera_y)

        # 繪製主角
        player.draw(screen, camera_y)

        # 更新玩家狀態和分數
        current_score = player.update_score()
        high_score = max(high_score, current_score)
        player.check_death(camera_y, bg_y)

        if player.is_dead:
            game_over = True

    # 顯示分數和遊戲狀態
    draw_text(screen, f"分數: {current_score}", 30, 10, 10, (255, 255, 255))
    draw_text(screen, f"最高分: {high_score}", 30, 10, 50, (255, 255, 255))

    if game_over:
        draw_text(
            screen, "遊戲結束！", 48, bg_x // 2 - 100, bg_y // 2 - 50, (255, 0, 0)
        )
        draw_text(
            screen,
            "按空白鍵重新開始",
            36,
            bg_x // 2 - 150,
            bg_y // 2 + 50,
            (255, 255, 255),
        )

    # 更新畫面
    py.display.update()
