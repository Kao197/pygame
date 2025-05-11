######################載入套件######################
import pygame as py
import sys
import random as r
import os  # 新增: 用於處理檔案路徑


def load_doodle_sprites():
    """
    載入遊戲所需的圖片資源\n
    從source圖片切割各種平台和彈簧精靈\n
    載入玩家角色四個方向的圖片\n
    return: 包含所有精靈的字典\n
    """
    try:
        # 載入主要圖片資源，使用os.path確保跨平台路徑正確性
        img_path = os.path.join("image", "src.png")
        source_image = py.image.load(img_path).convert_alpha()

        # 定義各個精靈在原始圖片中的位置和大小(x, y, 寬, 高)
        sprite_data = {
            # 平台相關
            "std_platform": (0, 0, 116, 30),  # 標準平台的位置和大小
            "break_platform": (0, 145, 124, 33),  # 可破壞平台的位置和大小
            "spring_normal": (376, 188, 71, 35),  # 普通彈簧的位置和大小
            # 玩家角色的四個狀態圖片路徑
            "player_left_jumping": os.path.join("image", "l.png"),
            "player_left_falling": os.path.join("image", "ls.png"),
            "player_right_jumping": os.path.join("image", "r.png"),
            "player_right_falling": os.path.join("image", "rs.png"),
            # 新增: 飛行帽子精靈圖片位置和大小
            "hat": (660, 473, 68, 44),  # 飛行帽子精靈的位置和大小
        }

        # 用於存放處理後的精靈圖片
        sprites = {}

        # 分別處理每個精靈
        for name, path in sprite_data.items():
            if name.startswith("player_"):
                # 載入玩家角色的獨立圖片
                sprites[name] = py.image.load(path).convert_alpha()
            else:
                # 從主要精靈圖分割出其他物件的圖片
                x, y, width, height = path
                sprites[name] = source_image.subsurface(py.Rect(x, y, width, height))

        return sprites
    except Exception as e:
        print(f"載入精靈圖片時發生錯誤: {e}")
        return None


######################物件類別######################
class Platform:
    def __init__(self, x, y, width, height, color, sprites=None):
        """
        初始化平台\n
        x,y: 平台的左上角座標\n
        width,height: 平台的寬度和高度\n
        color: 平台的顏色\n
        sprites: 平台的精靈圖片字典\n
        """
        self.rect = py.Rect(x, y, width, height)
        self.color = color
        self.is_special = False
        self.is_vanished = False
        self.sprites = sprites  # 新增: 儲存精靈圖片
        self.image = None  # 新增: 當前顯示的圖片

    def draw(self, display_area, camera_y):
        """
        繪製平台\n
        display_area: 繪製平台的遊戲視窗\n
        camera_y: 攝影機的Y軸位置\n
        """
        if not self.is_vanished:  # 新增: 只繪製未消失的平台
            # 建立新的矩形，考慮攝影機位置進行繪製
            platform_rect = py.Rect(
                self.rect.x,
                self.rect.y - camera_y,  # 扣除攝影機位置來計算顯示位置
                self.rect.width,
                self.rect.height,
            )
            # 使用精靈圖片繪製
            if self.sprites and self.image:
                scaled_image = py.transform.scale(
                    self.image, (self.rect.width, self.rect.height)
                )
                display_area.blit(scaled_image, platform_rect.topleft)
            else:
                py.draw.rect(display_area, self.color, platform_rect)


class Player:
    def __init__(self, x, y, width, height, color, sprites=None):
        """
        初始化主角\n
        x,y: 主角的左上角座標\n
        width,height: 主角的寬度和高度\n
        color: 主角的顏色\n
        sprites: 主角的精靈圖片字典\n
        """
        # 保留原有屬性
        self.rect = py.Rect(x, y, width, height)
        self.color = color

        # 新增精靈相關屬性
        self.sprites = sprites  # 儲存精靈圖片字典
        self.image = None  # 當前顯示的圖片
        self.direction = 1  # 面向方向(1為右，-1為左)

        self.speed_x = 5  # 水平移動速度
        self.speed_y = 0  # 垂直速度(初始為0)
        self.jump_speed = -10  # 跳躍初始速度(負值表示向上)
        self.gravity = 0.5  # 重力加速度
        self.is_jumping = False  # 是否正在跳躍
        self.initial_y = y  # 記錄初始Y座標，用於計算分數
        self.highest_y = y  # 記錄最高到達位置
        self.is_dead = False  # 新增遊戲結束檢查

        # 新增: 飛行帽子相關屬性
        self.has_hat = False  # 是否戴上飛行帽子
        self.flying_time = 0  # 飛行時間計時器
        self.max_flying_time = 60  # 最大飛行時間(5秒 * 60FPS = 300幀)
        self.flying_speed = self.jump_speed * 2  # 飛行時的上升速度是跳躍速度的2倍

    def draw(self, display_area, camera_y):
        """
        繪製主角和帽子\n
        display_area: 繪製主角的遊戲視窗\n
        camera_y: 攝影機的Y軸位置\n
        """
        # 建立新的矩形，考慮攝影機位置進行繪製
        player_rect = py.Rect(
            self.rect.x,
            self.rect.y - camera_y,
            self.rect.width,
            self.rect.height,
        )

        # 如果有戴帽子，先繪製帽子
        if self.has_hat and self.sprites and "hat" in self.sprites:
            hat_width = 35
            hat_height = 25
            hat_x = self.rect.x + (self.rect.width - hat_width) // 2
            hat_y = self.rect.y - hat_height
            hat_rect = py.Rect(
                hat_x,
                hat_y - camera_y,
                hat_width,
                hat_height,
            )
            hat_image = py.transform.scale(self.sprites["hat"], (hat_width, hat_height))
            display_area.blit(hat_image, hat_rect.topleft)

        # 繪製主角圖片
        if self.image and self.sprites:
            # 縮放圖片至主角大小
            scaled_image = py.transform.scale(
                self.image, (self.rect.width, self.rect.height)
            )
            display_area.blit(scaled_image, player_rect.topleft)
        else:
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
        if self.has_hat:  # 新增: 飛行狀態檢查
            self.speed_y = self.flying_speed  # 使用固定的飛行速度
            self.flying_time += 1  # 更新飛行時間
            if self.flying_time >= self.max_flying_time:
                self.has_hat = False  # 飛行時間結束
                self.flying_time = 0
        else:
            self.speed_y += self.gravity  # 速度受重力影響

        self.rect.y += self.speed_y  # 更新垂直位置

    def check_platform_collision(self, platforms):
        """
        檢查與平台和彈簧的碰撞\n
        platforms: 平台的列表\n
        只在往下掉的時候檢查碰撞\n
        return: 當碰到彈簧時返回 True\n
        """
        if self.speed_y > 0:  # 只在下降時檢查
            # 檢查所有彈簧的碰撞
            for spring in spring_list:
                if self.rect.colliderect(spring.rect):
                    # 確保是從彈簧上方碰撞
                    if self.rect.bottom >= spring.rect.top:
                        self.rect.bottom = spring.rect.top
                        # 彈簧提供更強的彈跳力（是原本跳躍力的2.5倍）
                        self.speed_y = self.jump_speed * 2.5
                        return True

            # 檢查所有平台的碰撞（原有邏輯）
            for platform in platforms:
                if not platform.is_vanished and self.rect.colliderect(platform.rect):
                    # 確保是從平台上方碰撞
                    if self.rect.bottom >= platform.rect.top:
                        self.rect.bottom = platform.rect.top
                        self.speed_y = self.jump_speed
                        # 新增: 如果是特殊平台，碰到後立即消失
                        if platform.is_special:
                            platform.is_vanished = True
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

    def update_image(self):
        """
        根據主角狀態更新顯示的圖片\n
        根據移動方向和垂直速度選擇適當的精靈圖片
        """
        if not self.sprites:
            return

        # 根據垂直速度判斷是跳躍還是下落
        if self.speed_y < 0:  # 速度為負=往上跳
            # 根據面向方向選擇對應的跳躍圖片
            if self.direction == 1:  # 面向右
                self.image = self.sprites["player_right_jumping"]
            else:  # 面向左
                self.image = self.sprites["player_left_jumping"]
        else:  # 速度為正=下落中
            # 根據面向方向選擇對應的下落圖片
            if self.direction == 1:  # 面向右
                self.image = self.sprites["player_right_falling"]
            else:  # 面向左
                self.image = self.sprites["player_left_falling"]


class Hat:
    """
    飛行帽子類別，提供玩家飛行能力的道具
    """

    def __init__(self, platform, sprites=None):
        """
        初始化飛行帽子\n
        platform: 帽子所在的平台物件\n
        sprites: 帽子的精靈圖片字典\n
        """
        self.width = 35  # 帽子寬度
        self.height = 25  # 帽子高度
        self.color = (0, 0, 255)  # 帽子顏色(藍色，在無精靈時使用)
        # 將帽子放在平台上方中央
        self.rect = py.Rect(
            platform.rect.x + (platform.rect.width - self.width) // 2,
            platform.rect.y - self.height,
            self.width,
            self.height,
        )
        self.platform = platform  # 記錄帽子所在的平台
        self.sprites = sprites  # 儲存精靈圖片
        self.image = None
        # 如果有精靈圖片，使用帽子的圖片
        if sprites and "hat" in sprites:
            self.image = sprites["hat"]

    def draw(self, display_area, camera_y):
        """
        繪製飛行帽子\n
        display_area: 繪製帽子的遊戲視窗\n
        camera_y: 攝影機的Y軸位置\n
        """
        # 建立新的矩形，考慮攝影機位置進行繪製
        hat_rect = py.Rect(
            self.rect.x,
            self.rect.y - camera_y,
            self.rect.width,
            self.rect.height,
        )
        # 使用精靈圖片或矩形繪製
        if self.image:
            scaled_image = py.transform.scale(
                self.image,
                (self.rect.width, self.rect.height),
            )
            display_area.blit(scaled_image, hat_rect.topleft)
        else:
            py.draw.rect(display_area, self.color, hat_rect)


######################新增平台管理功能######################
def generate_platforms():
    """
    隨機生成平台\n
    確保平台間距固定，讓玩家能夠跳躍到達
    """
    global last_hat_spawn
    platform_list.clear()
    spring_list.clear()  # 清空彈簧列表
    hat_list.clear()  # 清空帽子列表

    # 先生成最下方的平台
    bottom_platform = Platform(
        (bg_x - platform_width) // 2,  # 平台X座標置中
        bg_y - 60,  # 固定在底部上方一點的位置
        platform_width,
        platform_height,
        platform_color,
        sprites,  # 傳入精靈圖片
    )
    if sprites:
        bottom_platform.image = sprites["std_platform"]
    platform_list.append(bottom_platform)

    # 生成其他平台
    current_y = bg_y - 60
    for i in range(1, platform_count):
        plat_x = r.randint(0, bg_x - platform_width)
        current_y -= 60  # 固定間距60
        platform = Platform(
            plat_x,
            current_y,
            platform_width,
            platform_height,
            platform_color,
            sprites,  # 傳入精靈圖片
        )
        if sprites:
            platform.image = sprites["std_platform"]
        platform_list.append(platform)

        # 隨機決定是否在平台上生成彈簧
        if r.random() < spring_chance:
            spring = Spring(platform, sprites)  # 傳入精靈圖片
            spring_list.append(spring)

    # 重置帽子生成計時器
    global last_hat_spawn
    last_hat_spawn = 0  # 重置帽子生成計時器


def manage_platforms(platforms, player, camera_y, bg_x):
    """
    管理平台的生成和移除\n
    platforms: 平台列表\n
    player: 主角物件\n
    camera_y: 攝影機Y軸位置\n
    bg_x: 遊戲視窗寬度\n
    """
    global current_score, last_hat_spawn

    # 修改帽子生成邏輯
    hat_threshold = (current_score // hat_spawn_score) * hat_spawn_score
    if len(hat_list) == 0 and hat_threshold > last_hat_spawn:
        valid_platforms = []
        for p in platforms:
            if not p.is_special and not p.is_vanished:
                valid_platforms.append(p)
        if valid_platforms:
            platform = r.choice(valid_platforms)
            new_hat = Hat(platform, sprites)
            hat_list.append(new_hat)
            last_hat_spawn = hat_threshold

    # 移除離開視窗的帽子（只保留上方的帽子）
    hat_list_temp = []
    for hat in hat_list:
        # 只移除低於視窗底部的帽子，保留上方的帽子
        if hat.rect.y - camera_y < bg_y + 100:
            hat_list_temp.append(hat)
    hat_list[:] = hat_list_temp

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

        new_platform = Platform(new_x, new_y, 60, 10, (0, 0, 0), sprites)

        if sprites:
            # 根據是否為特殊平台選擇不同圖片
            if current_score > 1000 and r.random() < 0.2:
                new_platform.is_special = True
                new_platform.image = sprites["break_platform"]
            else:
                new_platform.image = sprites["std_platform"]

        platforms.append(new_platform)

        # 新增: 只在非特殊平台上生成彈簧
        if not new_platform.is_special and r.random() < spring_chance:
            spring = Spring(new_platform, sprites)
            spring_list.append(spring)

    # 修改帽子生成邏輯：使用當前分數判斷
    if current_score >= last_hat_spawn + hat_spawn_score:
        valid_platforms = []
        for p in platforms:
            if not p.is_special and not p.is_vanished:
                valid_platforms.append(p)
        if valid_platforms:
            platform = r.choice(valid_platforms)
            new_hat = Hat(platform, sprites)
            hat_list.append(new_hat)
            last_hat_spawn = current_score


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
os.chdir(sys.path[0])

######################遊戲視窗設定######################
bg_x = 400  # 視窗寬度
bg_y = 600  # 視窗高度
bg_size = (bg_x, bg_y)  # 設定視窗大小
py.display.set_caption("Doodle Jump")  # 設定視窗標題
screen = py.display.set_mode(bg_size)  # 建立視窗

######################載入精靈圖片######################
sprites = load_doodle_sprites()  # 載入精靈圖片

######################全域變數設定######################
hat_list = []  # 存放所有飛行帽子的列表
last_hat_spawn = 0  # 上次產生帽子時的分數

######################平台設定######################
platform_list = []  # 存放所有平台的列表
platform_width = 60  # 平台寬度
platform_height = 10  # 平台高度
platform_color = (0, 0, 0)  # 平台顏色(改為黑色)
platform_count = r.randint(8, 10) + 10  # 隨機決定要生成的平台數量

######################彈簧設定######################
spring_list = []  # 存放所有彈簧的列表
spring_chance = 0.2  # 彈簧生成機率(20%)


class Spring:
    def __init__(self, platform, sprites=None):
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
        self.sprites = sprites  # 新增: 儲存精靈圖片
        # 如果有精靈圖片，使用彈簧的圖片
        if sprites and "spring_normal" in sprites:
            self.image = sprites["spring_normal"]
        else:
            self.image = None

    def draw(self, display_area, camera_y):
        """
        繪製彈簧\n
        display_area: 繪製彈簧的遊戲視窗\n
        camera_y: 攝影機的Y軸位置\n
        """
        spring_rect = py.Rect(
            self.rect.x, self.rect.y - camera_y, self.rect.width, self.rect.height
        )
        if self.image:
            scaled_image = py.transform.scale(
                self.image, (self.rect.width, self.rect.height)
            )
            display_area.blit(scaled_image, spring_rect.topleft)
        else:
            py.draw.rect(display_area, self.color, spring_rect)


# 定義生成平台的函式
def generate_platforms():
    """
    隨機生成平台\n
    確保平台間距固定，讓玩家能夠跳躍到達
    """
    global last_hat_spawn
    platform_list.clear()
    spring_list.clear()  # 清空彈簧列表
    hat_list.clear()  # 清空帽子列表

    # 先生成最下方的平台
    bottom_platform = Platform(
        (bg_x - platform_width) // 2,  # 平台X座標置中
        bg_y - 60,  # 固定在底部上方一點的位置
        platform_width,
        platform_height,
        platform_color,
        sprites,  # 傳入精靈圖片
    )
    if sprites:
        bottom_platform.image = sprites["std_platform"]
    platform_list.append(bottom_platform)

    # 生成其他平台
    current_y = bg_y - 60
    for i in range(1, platform_count):
        plat_x = r.randint(0, bg_x - platform_width)
        current_y -= 60  # 固定間距60
        platform = Platform(
            plat_x,
            current_y,
            platform_width,
            platform_height,
            platform_color,
            sprites,  # 傳入精靈圖片
        )
        if sprites:
            platform.image = sprites["std_platform"]
        platform_list.append(platform)

        # 隨機決定是否在平台上生成彈簧
        if r.random() < spring_chance:
            spring = Spring(platform, sprites)  # 傳入精靈圖片
            spring_list.append(spring)

    # 重置帽子生成計時器
    global last_hat_spawn
    last_hat_spawn = 0  # 重置帽子生成計時器


# 初始生成平台
generate_platforms()

######################主角設定######################
player_width = 50  # 從30改為50
player_height = 50  # 從30改為50
player_x = (bg_x - player_width) // 2  # 主角X座標置中
player_y = bg_y - 90  # 設定在最下方平台上方
player_color = (0, 255, 0)
player = Player(
    player_x,
    player_y,
    player_width,
    player_height,
    player_color,
    sprites,  # 直接傳入sprites，Player類別會處理None的情況
)  # 建立主角物件，讓主角一開始就有向上的初始速度
player.speed_y = player.jump_speed
player.direction = 1  # 設定初始方向向右
player.image = sprites["player_right_jumping"] if sprites else None  # 設定初始圖片

######################新增攝影機設定######################
camera_y = 0  # 攝影機Y軸位置
target_camera_y = 0  # 目標攝影機Y軸位置

######################主程式######################
game_over = False  # 新增遊戲結束判定變數
high_score = 0  # 新增最高分紀錄
current_score = 0  # 新增: 初始化目前分數

######################帽子設定######################
hat_width = 35  # 飛行帽子寬度
hat_height = 25  # 飛行帽子高度
hat_color = (0, 0, 255)  # 飛行帽子顏色(藍色)
hat_spawn_score = 3000  # 每3000分產生一頂新帽子
hat_list = []  # 存放所有飛行帽子的列表
last_hat_spawn = 0  # 上次產生帽子時的分數


while True:
    FPS.tick(60)  # 設定每秒更新60次
    screen.fill((255, 255, 255))  # 清空畫面(改為白色背景)

    # 處理遊戲事件
    events = py.event.get()
    for event in events:
        # 處理退出遊戲
        if event.type == py.QUIT:
            sys.exit()

        # 處理遊戲結束時的重新開始
        if event.type == py.KEYDOWN:
            if player.is_dead:
                if event.key == py.K_SPACE:
                    # 重置遊戲
                    player.rect.x = player_x
                    player.rect.y = player_y
                    player.highest_y = player_y
                    player.speed_y = player.jump_speed
                    player.is_dead = False
                    current_score = 0
                    last_hat_spawn = 0
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
            player.direction = -1  # 設定面向方向為左

        if keys[py.K_RIGHT]:  # 如果按下右方向鍵
            player.move(1, bg_x)  # 向右移動
            player.direction = 1  # 設定面向方向為右

        player.update_image()  # 更新圖片狀態

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

        # 繪製所有帽子
        for hat in hat_list:
            hat.draw(screen, camera_y)
            # 確保玩家碰到帽子時，帽子會消失
            if not player.has_hat:
                if player.rect.colliderect(hat.rect):
                    player.has_hat = True
                    player.flying_time = 0
                    hat_list.remove(hat)
                    break  # 避免在迴圈中修改列表時出錯

        # 繪製主角
        player.draw(screen, camera_y)

        # 更新玩家狀態和分數
        current_score = player.update_score()
        high_score = max(high_score, current_score)
        player.check_death(camera_y, bg_y)

        if player.is_dead:
            game_over = True

    # 顯示分數和遊戲狀態
    draw_text(screen, f"分數: {current_score}", 30, 10, 10, (0, 0, 0))  # 改為黑色
    draw_text(screen, f"最高分: {high_score}", 30, 10, 50, (0, 0, 0))  # 改為黑色

    if game_over:
        draw_text(
            screen, "遊戲結束！", 48, bg_x // 2 - 100, bg_y // 2 - 50, (255, 0, 0)
        )  # 保持紅色
        draw_text(
            screen,
            "按空白鍵重新開始",
            36,
            bg_x // 2 - 150,
            bg_y // 2 + 50,
            (0, 0, 0),  # 改為黑色
        )

    # 更新畫面
    py.display.update()
