import pygame
import random

class Settings():
    """存储《外星人入侵》的所有设置的类"""
    
    def __init__(self):
        """初始化游戏的设置"""
        
        # 加载音频文件
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.6) # 音量

        self.screen_width = 1200
        self.screen_height = 950
        self.bg_color = (40, 40, 140)
        self.once = True
        
        # 保存最高分数据文件的路径
        self.file_path = 'data/high_score.txt'
        
        # 星星背景
        number = 30
        all_stars = {}
        pic = [3]
        while number:
            star_x = random.randint(0, self.screen_width)
            star_y = random.randint(0, self.screen_height)
            all_stars[number] = [star_x, star_y]
            pic.append(random.randint(0, 2))
            number -= 1
        self.stars = all_stars
        self.pictures = pic
        
        # 飞船的设置
        self.ship_speed_factor = 5
        self.ship_limit = 3
        
        # 子弹的设置
        self.bullets_allowed = 20
        
        # 外星人的设置
        self.fleet_drop_speed = 20
        
        # 记分
        self.alien_points = 50
        
        # 每个外星人分数的提高速度
        self.score_scale = 1.2
        
        # 游戏节奏按比例增长
        self.speedup_scale = 1.2
        self.initialize_dynamic_settings()
        
        
        
    def initialize_dynamic_settings(self):
        """初始化随游戏进度而变化的设置"""
        
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 2
        
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        
    def increase_speed(self):
        """提高速度设置"""
        
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)