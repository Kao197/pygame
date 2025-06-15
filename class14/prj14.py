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
        # === 步驟14: 新增無敵相關屬性 ===
        self.invincible = False  # 是否處於無敵狀態
        self.invincible_time = 0  # 無敵剩餘幀數

    def draw(self, screen):
        """
        在螢幕上繪製太空船與火焰推進效果
        根據目前方向狀態顯示對應圖片
        無敵期間太空船會閃爍顯示（每4幀隱藏一次）
        """
        # === 步驟14: 無敵時閃爍顯示 ===
        if self.invincible and (self.invincible_time // 4) % 2 == 0:
            # 無敵狀態下，每4幀隱藏一次，產生閃爍效果
            return

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
            self.burn_shift = (self.burn_shift + 1) % 12  # 0~11循環
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

    # === 步驟14: 新增無敵相關方法 ===
    def take_damage(self, invincible_duration=60):
        """
        觸發太空船受傷進入無敵狀態
        invincible_duration: 無敵持續幀數（預設60，約1秒）
        """
        if not self.invincible:
            self.invincible = True
            self.invincible_time = invincible_duration
            # 這裡可加入受傷音效或特效

    def update(self):
        """
        每幀自動遞減無敵剩餘時間，歸零時解除無敵狀態
        """
        if self.invincible:
            self.invincible_time -= 1
            if self.invincible_time <= 0:
                self.invincible = False


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
    def __init__(self, x, y, width, height, speed, burner_img=None):
        """
        初始化敵機
        x, y: 敵機左上角座標
        width, height: 敵機尺寸
        speed: 垂直下落速度
        burner_img: 火焰推進圖片(可選)
        不需傳入圖片參數，直接使用全域 enemy_images
        """
        self.rect = py.Rect(x, y, width, height)  # 使用 Rect 方便碰撞與移動
        self.width = width
        self.height = height
        self.speed = speed
        # 直接使用全域變數 enemy_images
        self.img = random.choice(enemy_images)  # 初始化時隨機選一張敵機圖片
        self.burner_img = burner_img  # 火焰推進圖片
        self.burn_shift = 0  # 火焰動畫的上下位移
        # --- 步驟13: 新增爆炸相關屬性 ---
        self.is_exploded = False  # 是否正在爆炸
        self.exp_count = 0  # 爆炸動畫目前幀數
        self.exp_max = 25  # 爆炸動畫總幀數(5張圖*5幀)

    def move(self, bg_h, bg_w):
        """
        敵機往下移動，超出畫面底部則重生
        爆炸時不移動
        """
        if self.is_exploded:
            return  # 爆炸時不移動
        self.rect.y += self.speed  # 垂直下落
        if self.rect.top > bg_h:
            self.reset(bg_w)

    def reset(self, bg_w):
        """
        敵機重生到畫面上方隨機位置，並隨機換一種外觀
        同時重置爆炸狀態
        """
        self.rect.x = random.randint(0, bg_w - self.width)
        self.rect.y = -self.height  # 從畫面上方外出現
        # 直接使用全域變數 enemy_images
        self.img = random.choice(enemy_images)  # 重生時隨機換圖片
        # --- 步驟13: 重置爆炸狀態 ---
        self.is_exploded = False
        self.exp_count = 0

    def explode(self):
        """
        觸發敵機爆炸動畫
        """
        self.is_exploded = True
        self.exp_count = 0

    def draw_explosion(self, screen):
        """
        繪製爆炸動畫
        根據exp_count顯示對應爆炸圖片
        """
        # 每張爆炸圖顯示5幀，共5張圖
        idx = min(self.exp_count // 5, len(explosion_imgs) - 1)
        exp_img = explosion_imgs[idx]
        exp_img_scaled = py.transform.scale(
            exp_img, (self.width * 1.2, self.height * 1.2)
        )
        screen.blit(exp_img_scaled, self.rect.topleft)
        self.exp_count += 1
        # 爆炸動畫結束後自動重生
        if self.exp_count >= self.exp_max:
            self.reset(bg_w)

    def draw(self, screen):
        """
        繪製敵機與火焰推進效果或爆炸動畫
        """
        if self.is_exploded:
            self.draw_explosion(screen)
            return
        # --- 火焰推進效果 ---
        if self.burner_img is not None:
            # 火焰寬度為敵機寬度的1/4，高度等比例縮放
            burner_w = self.width // 4
            orig_burner_w, orig_burner_h = self.burner_img.get_size()
            burner_h = int(orig_burner_h * (burner_w / orig_burner_w))
            # 火焰動畫上下晃動，讓火焰有動態感
            self.burn_shift = (self.burn_shift + 1) % 12  # 0~11循環
            # 火焰繪製位置：置中在敵機頂部，並加上晃動位移
            burner_x = self.rect.x + self.width // 2 - burner_w // 2
            burner_y = self.rect.y - burner_h // 2 - (self.burn_shift // 2) + 5
            # 將火焰圖片旋轉180度，讓火焰朝上
            burner_img_rotated = py.transform.rotate(self.burner_img, 180)
            # 縮放火焰圖片
            burner_img_scaled = py.transform.scale(
                burner_img_rotated, (burner_w, burner_h)
            )
            # 畫出火焰
            screen.blit(burner_img_scaled, (burner_x, burner_y))
        # --- 再繪製敵機 ---
        if self.img:
            img_scaled = py.transform.scale(self.img, (self.width, self.height))
            screen.blit(img_scaled, self.rect.topleft)
        else:
            # 若無圖片則以紅色矩形顯示
            py.draw.rect(screen, (255, 0, 0), self.rect)


# 新增：碰撞管理類別，專門負責處理遊戲中的碰撞檢查
class CollisionManager:
    def __init__(
        self, enemy_list, missile_list, score_mgr=None, sound_mgr=None, player=None
    ):
        """
        初始化碰撞管理器
        enemy_list: 敵機物件列表
        missile_list: 飛彈物件列表
        score_mgr: 分數管理器
        sound_mgr: 音效管理器
        player: 玩家物件（步驟14新增，檢查玩家與敵機碰撞）
        """
        self.enemy_list = enemy_list
        self.missile_list = missile_list
        self.score_mgr = score_mgr
        self.sound_mgr = sound_mgr
        self.player = player  # 步驟14: 新增玩家參考

    def is_hit(self, obj1, obj2, r):
        """
        判斷兩個物件是否碰撞，使用圓心距離公式
        obj1, obj2: 必須有 x, y, width, height 屬性
        r: 判斷半徑
        回傳: True=碰撞, False=未碰撞
        """
        # 計算兩物件中心點座標
        x1 = obj1.x + obj1.width // 2
        y1 = obj1.y + obj1.height // 2
        x2 = obj2.rect.x + obj2.width // 2
        y2 = obj2.rect.y + obj2.height // 2
        # 計算距離平方
        dist2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return dist2 < r**2

    def check_collision(self):
        """
        檢查所有飛彈與敵機的碰撞
        若有碰撞，敵機爆炸，飛彈設為不活躍，分數加分並播放音效
        同時檢查玩家與敵機碰撞，觸發無敵效果
        """
        # === 步驟14: 檢查玩家與敵機碰撞 ===
        if self.player:
            for emy in self.enemy_list:
                # 只檢查未爆炸的敵機
                if not emy.is_exploded:
                    # 計算玩家與敵機的中心點距離
                    px = self.player.x + self.player.width // 2
                    py_ = self.player.y + self.player.height // 2
                    ex = emy.rect.x + emy.width // 2
                    ey = emy.rect.y + emy.height // 2
                    r = 64
                    dist2 = (px - ex) ** 2 + (py_ - ey) ** 2
                    if dist2 < r**2:
                        if not self.player.invincible:
                            self.player.take_damage()
                            emy.explode()  # 玩家被撞敵機也爆炸
                        # 玩家無敵時不會重複觸發

        # ...existing code for missile-enemy collision...
        for msl in self.missile_list:
            if not msl.active:
                continue
            for emy in self.enemy_list:
                # 設定碰撞半徑，這裡取敵機寬度的一半
                r = emy.width // 2
                if not emy.is_exploded and self.is_hit(msl, emy, r):
                    emy.explode()  # 步驟13: 觸發爆炸動畫
                    msl.active = False  # 飛彈消失
                    # 新增：擊中敵機時加分與播放音效
                    if self.score_mgr:
                        self.score_mgr.add_score(100)
                    if self.sound_mgr:
                        self.sound_mgr.play_hit()
                    break  # 一顆飛彈只擊中一台敵機


# 新增：分數管理類別，負責分數計算與顯示
class ScoreManager:
    def __init__(
        self,
        font_path="C:/Windows/Fonts/msjh.ttc",
        font_size=32,
        pos=(20, 20),
        color=(255, 255, 0),
    ):
        """
        初始化分數管理器
        font_path: 字型檔案路徑
        font_size: 字型大小
        pos: 分數顯示位置
        color: 分數顯示顏色
        """
        self.score = 0  # 分數初始值
        self.font = py.font.Font(font_path, font_size)  # 載入字型
        self.pos = pos
        self.color = color

    def add_score(self, points):
        """增加分數"""
        self.score += points

    def deduct_score(self, points):
        """扣除分數"""
        self.score -= points
        if self.score < 0:
            self.score = 0

    def score_reset(self):
        """重設分數"""
        self.score = 0

    def draw_score(self, screen):
        """在螢幕上繪製分數"""
        score_surf = self.font.render(f"Score: {self.score}", True, self.color)
        screen.blit(score_surf, self.pos)


# 新增：音效管理類別，負責音效播放
class SoundManager:
    def __init__(self, hit_sound_path="image/hit.mp3"):
        """
        初始化音效管理器
        hit_sound_path: 擊中敵機音效檔案路徑
        """
        # 載入擊中敵機音效
        try:
            self.sound_explosion = py.mixer.Sound(hit_sound_path)
        except Exception as e:
            self.sound_explosion = None  # 若載入失敗則設為None

    def play_hit(self):
        """播放擊中敵機音效"""
        if self.sound_explosion:
            self.sound_explosion.play()


###################### 初始化設定區塊 ######################
# 切換工作目錄到程式所在位置，避免路徑問題
os.chdir(sys.path[0])
py.init()  # 初始化pygame
# py.mixer.init()  # 新增：初始化音效系統
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

# 步驟8：載入多種敵機圖片，並建立敵機圖片列表
img_enemy1 = py.image.load("image/enemy1.png")  # 載入敵機圖片1
img_enemy2 = py.image.load("image/enemy2.png")  # 載入敵機圖片2
# 可繼續擴充更多敵機圖片
enemy_images = [img_enemy1, img_enemy2]  # 敵機圖片列表

# --- 步驟13: 載入爆炸動畫圖片 ---
explosion_imgs = [
    py.image.load(f"image/explosion{i}.png") for i in range(1, 6)
]  # 載入爆炸動畫圖片1~5

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
# 步驟9：建立敵機群系統
EMY_NUM = 5  # 敵機數量，可依需求調整
enemy_w, enemy_h = 64, 64  # 敵機尺寸

# 建立敵機物件列表
emy_list = []
for i in range(EMY_NUM):
    # 每台敵機的 x 座標隨機，y 座標分布於畫面上方外不同位置
    enemy_x = random.randint(0, bg_w - enemy_w)
    # y座標設為 -enemy_h - 隨機值，讓敵機分布於畫面上方外不同高度
    enemy_y = -enemy_h - random.randint(0, bg_h)
    # 敵機速度改為5~15隨機
    enemy_speed = random.randint(7, 12)
    # --- 步驟12: 傳入火焰推進圖片 ---
    emy = Enemy(enemy_x, enemy_y, enemy_w, enemy_h, enemy_speed, burner_img=img_burner)
    emy_list.append(emy)


###################### 分數與音效管理設定區塊 ######################
# 新增：建立分數管理器與音效管理器
score_mgr = ScoreManager()
sound_mgr = SoundManager(hit_sound_path="image/hit.mp3")


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

    # --- 步驟9: 處理敵機群的移動與繪製 ---
    # 遍歷每台敵機，讓每台敵機自動下落、重生與繪製
    for emy in emy_list:
        emy.move(bg_h, bg_w)  # 敵機自動下落與重生
        emy.draw(screen)  # 畫出敵機(含爆炸動畫)

    # === 步驟14: 每幀更新玩家無敵狀態 ===
    player.update()

    # 新增：建立碰撞管理器物件，傳入敵機、飛彈、分數與音效管理器與玩家
    collision_mgr = CollisionManager(
        emy_list, missiles, score_mgr=score_mgr, sound_mgr=sound_mgr, player=player
    )
    collision_mgr.check_collision()

    # 畫出玩家太空船
    player.draw(screen)
    # 新增：畫出分數
    score_mgr.draw_score(screen)
    # 更新畫面
    py.display.update()
