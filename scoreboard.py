import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """显示得分信息的类"""
    
    def __init__(self, ai_settings, screen, status):
        """初始化显示得分所涉及的属性"""
        
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.status = status
        
        # 显示得分信息所使用的字体
        self.text_color = (64, 128, 128)
        self.font = pygame.font.Font('font/STKAITI.TTF', 32) #pygame.font.Font()使用文件夹中自定义的字体/pygame.font.SysFont()使用本机字体
        
        # 准备初始得分图像和最高分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        
    def prep_score(self):
        """将得分转换成一幅渲染的图像"""
        
        rounded_score = int(round(self.status.score, -1)) # 第二个参数指定精确到小数点后几位，-1则表示将
        # 表示圆整到最近的10、100等的整数倍(python2.7中round()总是返回一个小数，所以加个int)
        # 实测：2775 -> 2780 9214 -> 9210
        
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("总分: "+score_str, True,
                                            self.text_color, self.ai_settings.bg_color)
        
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 25
        self.score_rect.top = 10
        
    def prep_high_score(self):
        """将最高分转换成一幅渲染的图像"""
        
        high_score = int(round(self.status.high_score, -1))
        
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("最高分: "+high_score_str, True,
                                                 self.text_color, self.ai_settings.bg_color)
        
        # 将得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def prep_level(self):
        """将等级转换成一幅渲染的图像"""
    
        self.level_image = self.font.render("等级: "+str(self.status.level), True,
                                            self.text_color, self.ai_settings.bg_color)
    
        # 将得分放在屏幕顶部中央
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 5
        
    def prep_ships(self):
        """显示还剩余多少飞船"""
        self.ships = Group()
        for ship_number in range(self.status.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
    
    def show_score(self):
        """在屏幕上显示得分"""
        
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        
        # 绘制飞船
        self.ships.draw(self.screen)