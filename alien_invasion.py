import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_status import GameStatus
from button import Button
from scoreboard import Scoreboard

import game_functions as gf

def run_game():
    
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)) # ((width,height),x,y)默认0,0
    pygame.display.set_caption("《外星人入侵》")
    
    # 创建开始按钮
    play_button = Button(ai_settings, screen, "开始游戏")
    # pygame.font.get_fonts(),输出本机自带的字体
    
    # # 创建存储游戏统计信息的实例，并创建记分牌
    status = GameStatus(ai_settings)
    sb = Scoreboard(ai_settings, screen, status)
    
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    
    # 创建一个用于存储子弹的编组
    bullets = Group()
    
    # 创建一个用于存储外星人的编组
    aliens = Group()
    
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    # 创建外星人爆炸帧动画
    explosion = Group()
    
    # 创建飞船爆炸帧动画
    destroyed = Group()
    
    # 随机产生一个背景
    once = True
    # 开始游戏的主循环
    while True:
        gf.check_events(ai_settings, screen, status, sb, play_button, ship, aliens, bullets)
        if status.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, status, sb, ship, aliens, bullets, explosion)
            gf.update_aliens(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed)
        gf.update_screen(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed, play_button, once)
        
if __name__ == "__main__":
    run_game()