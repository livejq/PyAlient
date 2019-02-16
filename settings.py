import random

class Settings():
    """存储《外星人入侵》的所有设置的类"""
    
    def __init__(self):
        """初始化游戏的设置"""
        
        self.screen_width = 1200
        self.screen_height = 900
        self.bg_color = (230, 230, 230)
        
        # 星星背景
        number = 30
        all_stars = {}
        while number:
            star_x = random.randint(0, self.screen_width)
            star_y = random.randint(0, self.screen_height)
            all_stars[number] = [star_x, star_y]
            number -= 1
        self.stars = all_stars
        
        # 飞船的设置
        self.ship_speed_factor = 6
        self.ship_limit = 2
        
        # 子弹的设置
        self.bullet_width = 800
        self.bullet_height = 25
        self.bullet_color = 234, 45, 68
        self.bullets_allowed = 20
        
        # 外星人的设置
        self.fleet_drop_speed = 100
        
        # 记分
        self.alien_points = 50
        
        # 每个外星人分数的提高速度
        self.score_scale = 1.5
        
        # 游戏节奏按比例增长
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        
        
        
    def initialize_dynamic_settings(self):
        """初始化随游戏进度而变化的设置"""
        
        self.bullet_speed_factor = 6
        self.alien_speed_factor = 1
        
        # fleet_direction为1表示向右移，为-1表示向左移
        self.fleet_direction = 1
        
    def increase_speed(self):
        """提高速度设置"""
        
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)