###################### 載入套件區塊 ######################
import pygame as py
import sys
import os
from pygame.locals import *
import random  # 新增：載入 random 模組


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


# 新增 Player 類別，管理玩家太空船
class Player:
    def __init__(self, x, y, sprites, width, height, speed, burner_img=None):
        """
        初始化玩家太空船
        x, y: 太空船左上角座標
        sprites: 太空船圖片字典
        width, height: 太空船尺寸
        speed: 移動速度
        burner_img: 火焰推進圖片
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprites = sprites  # 圖片字典
        self.speed = speed
        self.rect = py.Rect(self.x, self.y, self.width, self.height)
        self.facing_direction = (
            "M"  # 新增屬性，預設為中間直飛狀態("M"=中間，"L"=左，"R"=右)
        )
        self.burner_img = burner_img  # 火焰推進圖片
        self.burn_shift = 0  # 火焰動畫的上下位移

    def draw(self, screen):
        """
        在螢幕上繪製太空船與火焰推進效果
        根據目前方向狀態顯示對應圖片
        """
        # 只有在沒有按下下鍵時才繪製火焰推進效果
        keys = py.key.get_pressed()
        if self.burner_img is not None and not keys[K_DOWN]:
            # 火焰寬度為太空船寬度的1/4，高度等比例縮放
            burner_w = self.width // 4
            # 取得原始火焰圖片的寬高
            orig_burner_w, orig_burner_h = self.burner_img.get_size()
            # 根據寬度等比例縮放火焰高度
            burner_h = int(orig_burner_h * (burner_w / orig_burner_w))
            # 火焰動畫上下晃動，讓火焰有動態感
            self.burn_shift = (self.burn_shift + 2) % 12  # 0~11循環
            # 火焰繪製位置：置中在太空船底部，並加上晃動位移
            burner_x = self.x + self.width // 2 - burner_w // 2
            burner_y = self.y + self.height - burner_h // 2 + (self.burn_shift // 2)
            # 縮放火焰圖片
            burner_img_scaled = py.transform.scale(
                self.burner_img, (burner_w, burner_h)
            )
            # 畫出火焰
            screen.blit(burner_img_scaled, (burner_x, burner_y))
        # 再繪製太空船
        img = self.sprites["fighter_" + self.facing_direction]
        img = py.transform.scale(img, (self.width, self.height))
        screen.blit(img, (self.x, self.y))

    def handle_input(self, keys, bg_w, bg_h):
        """
        處理鍵盤輸入與移動，並自動邊界檢查
        keys: 按鍵狀態
        bg_w, bg_h: 視窗寬高
        """
        # 根據按鍵設定方向狀態
        if keys[K_LEFT] and not keys[K_RIGHT]:
            self.facing_direction = "L"  # 按左鍵顯示左轉
        elif keys[K_RIGHT] and not keys[K_LEFT]:
            self.facing_direction = "R"  # 按右鍵顯示右轉
        else:
            self.facing_direction = "M"  # 沒有按或同時按左右則顯示直飛

        # 計算新座標
        if keys[K_LEFT]:
            self.x -= self.speed
        if keys[K_RIGHT]:
            self.x += self.speed
        if keys[K_UP]:
            self.y -= self.speed
        if keys[K_DOWN]:
            self.y += self.speed
        # 邊界檢查
        if self.x < 0:
            self.x = 0
        if self.x + self.width > bg_w:
            self.x = bg_w - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > bg_h:
            self.y = bg_h - self.height
        # 更新rect
        self.rect.topleft = (self.x, self.y)


# 新增 Missile 類別，管理飛彈
class Missile:
    def __init__(self, img, width, height, speed):
        """
        初始化飛彈
        img: 飛彈圖片
        width, height: 飛彈尺寸
        speed: 飛彈移動速度
        """
        self.img = img  # 飛彈圖片
        self.width = width
        self.height = height
        self.speed = speed
        self.x = 0
        self.y = 0
        self.active = False  # 飛彈是否正在飛行

    def launch(self, x, y):
        """
        發射飛彈，設定初始位置與狀態
        x, y: 飛彈起始座標（通常為玩家中心）
        """
        self.x = x - self.width // 2  # 讓飛彈置中於玩家
        self.y = y
        self.active = True

    def move(self, bg_h):
        """
        飛彈移動，超出畫面則設為不活躍
        bg_h: 視窗高度
        """
        if self.active:
            self.y -= self.speed  # 飛彈往上移動
            if self.y + self.height < 0:
                self.active = False  # 超出畫面上緣則關閉

    def draw(self, screen):
        """
        繪製飛彈
        """
        if self.active:
            img_scaled = py.transform.scale(self.img, (self.width, self.height))
            screen.blit(img_scaled, (self.x, self.y))


# 新增 Enemy 類別，管理敵機
class Enemy:
    def __init__(self, x, y, width, height, speed, img=None):
        """
        初始化敵機
        x, y: 敵機左上角座標
        width, height: 敵機尺寸
        speed: 垂直下落速度
        img: 敵機圖片
        """
        self.rect = py.Rect(x, y, width, height)  # 使用 Rect 方便碰撞與移動
        self.width = width
        self.height = height
        self.speed = speed
        self.img = img

    def move(self, bg_h, bg_w):
        """
        敵機往下移動，超出畫面底部則重生
        bg_h: 視窗高度
        bg_w: 視窗寬度
        """
        self.rect.y += self.speed  # 垂直下落
        if self.rect.top > bg_h:
            self.reset(bg_w)

    def reset(self, bg_w):
        """
        敵機重生到畫面上方隨機位置
        bg_w: 視窗寬度
        """
        self.rect.x = random.randint(0, bg_w - self.width)
        self.rect.y = -self.height  # 從畫面上方外出現

    def draw(self, screen):
        """
        繪製敵機
        """
        if self.img:
            img_scaled = py.transform.scale(self.img, (self.width, self.height))
            screen.blit(img_scaled, self.rect.topleft)
        else:
            # 若無圖片則以紅色矩形顯示
            py.draw.rect(screen, (255, 0, 0), self.rect)


###################### 初始化設定區塊 ######################
# 切換工作目錄到程式所在位置，避免路徑問題
os.chdir(sys.path[0])
py.init()  # 初始化pygame
clock = py.time.Clock()  # 建立時鐘物件控制遊戲速度

###################### 載入圖片區塊 ######################
bg_img = py.image.load("image/space.png")  # 載入太空背景圖片
# 載入太空船圖片
img_player_m = py.image.load("image/fighter_M.png")  # 載入太空船中間飛行圖片
img_player_l = py.image.load("image/fighter_L.png")  # 載入太空船左轉圖片
img_player_r = py.image.load("image/fighter_R.png")  # 載入太空船右轉圖片
# 載入火焰推進圖片
img_burner = py.image.load("image/starship_burner.png")  # 載入太空船火焰圖片
# 載入飛彈圖片
img_missile = py.image.load("image/bullet.png")  # 載入飛彈圖片
# 新增：載入敵機圖片
img_enemy1 = py.image.load("image/enemy1.png")
# 建立太空船圖片字典，包含三種狀態
player_sprites = {
    "fighter_M": img_player_m,
    "fighter_L": img_player_l,
    "fighter_R": img_player_r,
}

###################### 遊戲視窗設定區塊 ######################
py.display.set_caption("Galaxy Lancer")  # 設定視窗標題
bg_w, bg_h = bg_img.get_size()  # 取得背景圖片尺寸
screen = py.display.set_mode((bg_w, bg_h))  # 設定視窗大小
roll_y = 0  # 捲動背景的y座標初始值

###################### 玩家設定區塊 ######################
# 建立玩家太空船物件，初始位置設為畫面中央，並加入火焰推進圖片
player = Player(
    x=bg_w // 2 - 40,  # 80為太空船寬度
    y=bg_h // 2 - 40,  # 80為太空船高度
    sprites=player_sprites,
    width=80,
    height=80,
    speed=10,
    burner_img=img_burner,  # 傳入火焰推進圖片
)

###################### 飛彈設定區塊 ######################
# --- 步驟6: 飛彈連發功能 ---
MISSILE_MAX = 10  # 飛彈最大同時存在數量
msl_cooldown_max = 8  # 飛彈冷卻最大值(幀數)，數字越小可連發越快
msl_cooldown = 0  # 飛彈冷卻計時器

# 建立飛彈物件列表，預先建立好所有飛彈物件，避免遊戲中頻繁建立/銷毀物件
missiles = [
    Missile(
        img=img_missile,
        width=16,  # 飛彈寬度
        height=32,  # 飛彈高度
        speed=20,  # 飛彈速度
    )
    for _ in range(MISSILE_MAX)
]

###################### 敵機設定區塊 ######################
# 新增：建立敵機物件，初始位置隨機，速度固定
enemy_w, enemy_h = 64, 64  # 敵機尺寸
enemy_speed = 10  # 敵機下落速度
enemy_x = random.randint(0, bg_w - enemy_w)
enemy_y = -enemy_h  # 從畫面上方外出現
enemy = Enemy(enemy_x, enemy_y, enemy_w, enemy_h, enemy_speed, img_enemy1)

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

    # --- 步驟6: 飛彈冷卻計時器自動遞減 ---
    if msl_cooldown > 0:
        msl_cooldown -= 1

    # 取得按鍵狀態
    keys = py.key.get_pressed()
    # --- 新增：按住SPACE自動連發 ---
    if keys[K_SPACE] and msl_cooldown == 0:
        for msl in missiles:
            if not msl.active:
                msl.launch(player.rect.centerx, player.rect.y)
                msl_cooldown = msl_cooldown_max
                break

    # 更新捲動背景座標
    roll_y = (roll_y + 10) % bg_h
    # 畫出捲動背景
    roll_bg(screen, bg_img, roll_y)
    # 取得按鍵狀態並傳給玩家物件處理
    keys = py.key.get_pressed()
    player.handle_input(keys, bg_w, bg_h)

    # --- 步驟6: 處理所有飛彈的移動與繪製 ---
    # 先畫飛彈再畫太空船，讓飛彈從太空船中間發射
    for msl in missiles:
        msl.move(bg_h)
        msl.draw(screen)

    # --- 步驟7: 處理敵機移動與繪製 ---
    enemy.move(bg_h, bg_w)  # 敵機自動下落與重生
    enemy.draw(screen)  # 畫出敵機

    # 畫出玩家太空船
    player.draw(screen)
    # 更新畫面
    py.display.update()
