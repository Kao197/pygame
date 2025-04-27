######################載入套件######################
import pygame  # 載入 pygame 套件，用於遊戲開發
import sys  # 載入 sys 套件，用於系統相關操作
import random  # 載入 random 套件，用於生成隨機數


######################物件類別######################
class Player:
    def reset(self, x, y):
        """重設主角狀態"""
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.is_jumping = True
        self.highest_y = y
        self.score = 0
        self.highest_platform = float("inf")  # 設為無限大，確保第一次踩到平台時會計分
        self.game_over = False

    def __init__(self, x, y, width, height, color):
        """
        初始化主角\n
        x, y: 主角的左上角座標\n
        width, height: 主角的寬度和高度\n
        color: 主角的顏色 (RGB格式)\n
        """
        self.rect = pygame.Rect(x, y, width, height)  # 建立主角的矩形區域
        self.color = color  # 設定主角顏色
        self.speed = 5  # 設定主角的水平移動速度
        self.velocity_y = 0  # 垂直速度初始值
        self.jump_speed = -12  # 跳躍初始速度（負值表示向上）
        self.gravity = 0.5  # 重力加速度
        self.is_jumping = True  # 是否正在跳躍
        self.highest_y = y  # 記錄主角到達的最高點
        self.score = 0  # 初始分數為0
        self.highest_platform = float("inf")  # 設為無限大，確保第一次踩到平台時會計分
        self.game_over = False  # 遊戲是否結束

    def draw(self, display_area, camera_y):
        """
        繪製主角\n
        display_area: 繪製主角的目標視窗\n
        camera_y: 攝影機的Y座標位置\n
        """
        # 根據攝影機位置調整繪製位置
        draw_rect = pygame.Rect(self.rect.x, self.rect.y - camera_y, self.rect.width, self.rect.height)
        pygame.draw.rect(display_area, self.color, draw_rect)

    def move(self, direction, bg_x):
        """
        移動主角並處理穿牆效果\n
        direction: 移動方向 (1為右移, -1為左移)\n
        bg_x: 遊戲視窗寬度，用於計算穿牆位置\n
        """
        # 根據方向和速度移動主角
        self.rect.x += direction * self.speed
        # 穿牆功能處理
        if self.rect.right < 0:  # 當主角完全移出左邊界時
            self.rect.left = bg_x  # 從右側重新出現
        elif self.rect.left > bg_x:  # 當主角完全移出右邊界時
            self.rect.right = 0  # 從左側重新出現

    def update(self, platform_list, camera_y, bg_y):
        """
        更新主角狀態（包含重力效果和碰撞檢測）\n
        platform_list: 平台列表\n
        camera_y: 攝影機的Y座標位置\n
        bg_y: 遊戲視窗高度\n
        """
        # 套用重力效果
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # 更新最高點記錄
        if self.rect.y < self.highest_y:
            self.highest_y = self.rect.y

        # 檢測與平台的碰撞
        for platform in platform_list:
            # 只有在往下掉的時候才檢測碰撞
            if self.velocity_y > 0:
                # 檢查是否與平台發生碰撞
                if (
                    self.rect.bottom >= platform.rect.top
                    and self.rect.bottom <= platform.rect.bottom
                    and self.rect.right >= platform.rect.left
                    and self.rect.left <= platform.rect.right
                ):
                    # 確保主角是從上方碰撞到平台
                    if self.rect.bottom - self.velocity_y <= platform.rect.top:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = self.jump_speed  # 觸發自動跳躍
                        # 計算分數：如果踩到更高的平台就加分
                        if platform.rect.y < self.highest_platform:
                            self.score += 10
                            self.highest_platform = platform.rect.y

        # 檢查遊戲結束條件
        if self.rect.top - camera_y > bg_y:
            self.game_over = True


class Platform:
    def __init__(self, x, y, width, height, color):
        """
        初始化平台\n
        x, y: 平台的左上角座標\n
        width, height: 平台的寬度和高度\n
        color: 平台的顏色 (RGB格式)\n
        """
        self.rect = pygame.Rect(x, y, width, height)  # 建立平台的矩形區域
        self.color = color  # 設定平台顏色

    def draw(self, display_area, camera_y):
        """
        繪製平台\n
        display_area: 繪製平台的目標視窗\n
        camera_y: 攝影機的Y座標位置\n
        """
        # 根據攝影機位置調整繪製位置
        draw_rect = pygame.Rect(self.rect.x, self.rect.y - camera_y, self.rect.width, self.rect.height)
        pygame.draw.rect(display_area, self.color, draw_rect)


def generate_platform(bg_x, y, platform_w, platform_h):
    """
    生成單個平台\n
    bg_x: 遊戲視窗寬度\n
    y: 平台的Y座標\n
    platform_w: 平台寬度\n
    platform_h: 平台高度\n
    return: 新的平台物件\n
    """
    x = random.randint(0, bg_x - platform_w)
    return Platform(x, y, platform_w, platform_h, (255, 255, 255))


def generate_platforms(bg_x, platform_count, platform_w, platform_h, start_y=50):
    """
    隨機生成平台\n
    bg_x: 遊戲視窗寬度\n
    platform_count: 要生成的平台數量\n
    platform_w: 平台寬度\n
    platform_h: 平台高度\n
    start_y: 起始Y座標\n
    return: 平台列表\n
    """
    platforms = []
    min_gap_y = 80  # 平台之間的最小垂直間距
    max_gap_y = 120  # 平台之間的最大垂直間距
    current_y = start_y  # 起始Y座標

    for _ in range(platform_count):
        platform = generate_platform(bg_x, current_y, platform_w, platform_h)
        platforms.append(platform)  # 更新下一個平台的Y座標
        current_y += random.randint(min_gap_y, max_gap_y)  # 向上生成平台

    return platforms


######################初始化設定######################
pygame.init()  # 初始化 pygame
FPS = pygame.time.Clock()  # 創建時鐘物件，用於控制遊戲更新速率

######################遊戲視窗設定######################
bg_x = 400  # 設定視窗寬度
bg_y = 600  # 設定視窗高度
bg_size = (bg_x, bg_y)  # 視窗尺寸元組
pygame.display.set_caption("Doodle Jump")  # 設定視窗標題
screen = pygame.display.set_mode(bg_size)  # 創建遊戲視窗

######################字體設定######################
font = pygame.font.Font("C:/Windows/Fonts/msjh.ttc", 24)  # 設定字體和大小

######################主角設定######################
player_w = 30  # 主角寬度
player_h = 30  # 主角高度
player_x = (bg_x - player_w) // 2  # 計算主角的初始X座標（置中）
player_y = bg_y - player_h - 50  # 計算主角的初始Y座標（底部上方50像素）
player = Player(player_x, player_y, player_w, player_h, (0, 255, 0))  # 創建主角物件，設定為綠色

######################平台設定######################
platform_w = 60  # 平台寬度
platform_h = 10  # 平台高度
platform_count = 6  # 初始平台數量

# 生成初始平台
platform_list = generate_platforms(bg_x, platform_count, platform_w, platform_h)

# 確保在主角底下有一個平台
first_platform = Platform((bg_x - platform_w) // 2, player_y + player_h + 10, platform_w, platform_h, (255, 255, 255))
platform_list.append(first_platform)

######################攝影機設定######################
camera_y = 0  # 攝影機Y軸位置
target_camera_y = 0  # 目標攝影機Y軸位置

######################主程式######################
while True:
    FPS.tick(60)  # 限制遊戲更新率為每秒60幀
    screen.fill((0, 0, 0))  # 用黑色填充畫面背景

    # 獲取當前按下的按鍵狀態並處理移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  # 當按下左方向鍵
        player.move(-1, bg_x)  # 向左移動
    if keys[pygame.K_RIGHT]:  # 當按下右方向鍵
        player.move(1, bg_x)  # 向右移動

    # 更新遊戲狀態
    player.update(platform_list, camera_y, bg_y)  # 更新主角狀態

    # 更新攝影機位置
    target_camera_y = min(camera_y, player.rect.y - (bg_y * 0.6))  # 保持玩家在畫面偏下方，且只能向上移動
    camera_y += (target_camera_y - camera_y) * 0.1  # 平滑移動攝影機

    # 生成新平台
    highest_platform = min(platform.rect.y for platform in platform_list)  # 找出最高的平台
    if highest_platform > camera_y - bg_y:  # 如果最高的平台太低
        # 在上方生成新的平台
        new_platforms = generate_platforms(bg_x, 3, platform_w, platform_h, start_y=highest_platform - 200)
        platform_list.extend(new_platforms)  # 移除離開畫面的平台
    new_platform_list = []
    for p in platform_list:
        if p.rect.y < camera_y + bg_y:  # 只保留在視窗範圍內的平台
            new_platform_list.append(p)
    platform_list = new_platform_list

    # 事件處理迴圈
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 當使用者點擊關閉視窗
            sys.exit()  # 結束程式
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and player.game_over:  # 按下R鍵重新開始遊戲
                player.reset(player_x, player_y)
                platform_list = generate_platforms(bg_x, platform_count, platform_w, platform_h)
                first_platform = Platform(
                    (bg_x - platform_w) // 2, player_y + player_h + 10, platform_w, platform_h, (255, 255, 255)
                )
                platform_list.append(first_platform)
                camera_y = 0
                target_camera_y = 0

    # 繪製遊戲畫面
    for platform in platform_list:  # 繪製所有平台
        platform.draw(screen, camera_y)
    player.draw(screen, camera_y)  # 繪製主角

    # 顯示分數
    score_text = font.render(f"分數: {player.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # 遊戲結束處理
    if player.game_over:
        game_over_text = font.render("遊戲結束！", True, (255, 0, 0))
        final_score_text = font.render(f"最終分數: {player.score}", True, (255, 255, 255))
        restart_text = font.render("按 R 鍵重新開始", True, (255, 255, 255))
        screen.blit(game_over_text, (bg_x // 2 - 60, bg_y // 2 - 30))
        screen.blit(final_score_text, (bg_x // 2 - 70, bg_y // 2 + 10))
        screen.blit(restart_text, (bg_x // 2 - 90, bg_y // 2 + 50))

    pygame.display.update()  # 更新畫面顯示
