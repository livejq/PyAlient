import pygame
import sys
from time import sleep
from pygame.locals import *

from bullet import Bullet
from alien import Alien
from decoration import Star
from cartoon import MySprite

def check_keydown_events(event, ai_settings, screen, status, sb, ship, aliens, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        # 向上移动飞船
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        # 向下移动飞船
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        shoot_wav = pygame.mixer.Sound('sound/shoot.wav')
        shoot_wav.set_volume(0.5)
        shoot_wav.play(0)
    elif event.key == pygame.K_q:
        save_data(ai_settings, status)
        sys.exit()
    elif event.key == pygame.K_p and not status.game_active:
        start_game(ai_settings, screen, status, sb, ship, aliens, bullets)
        
def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def save_data(ai_settings, status):
    """保存必要的统计信息"""
    
    with open(ai_settings.file_path, 'w') as file:
        file.write(str(status.high_score))

def check_events(ai_settings, screen, status, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_data(ai_settings, status)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, status, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    if index == 0:
                        # 点击左键隐藏光标,1,2分别是wheel和right
                        pygame.mouse.set_visible(False)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, status, sb, play_button, ship,aliens,bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, status, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击开始游戏按钮时开始新游戏"""
    
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 解决开始游戏按钮透明时单击同样的位置还有响应的Bug
    if button_clicked and not status.game_active:
        start_game(ai_settings, screen, status, sb, ship, aliens, bullets)
    
def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人向下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    # 乘于-1来改变符号（一开始我是没想到的）
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed, alien=None):
    """响应被外星人撞到的飞船或到达屏幕底端"""

    if alien:
        status.score += ai_settings.alien_points
            
        blast_wav = pygame.mixer.Sound('sound/blast.wav')
        blast_wav.set_volume(0.2)
        blast_wav.play(0)
                
        # 加载帧动画
        cartoon = MySprite(screen)
        cartoon.load("images/alien_killed.bmp", alien.rect.x, alien.rect.y, 90, 90, 7)
        explosion.add(cartoon)
                
        sb.prep_score()
            
        # 加载帧动画
        destroy = MySprite(screen)
        destroy.load("images/ship_blast.bmp", ship.rect.x, ship.rect.y, 48, 48, 16)
        destroyed.add(destroy)
            
        check_high_score(status, sb)
            
    if len(aliens) == 0:
        # 删除现有子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
                
        # 提高等级
        status.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
    
    if status.ships_left:
        status.ships_left -= 1
        
        # 更新记分牌
        sb.prep_ships()
        
        print("剩余战舰：%d\n" % status.ships_left)
    else:
        print("游戏结束\n\n")
        status.game_active = False
        pygame.mixer.music.load('sound/fail.mp3')
        pygame.mixer.music.play(-1)
        
        # 显示光标
        pygame.mouse.set_visible(True)
    
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    
    # 重新创建
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def start_game(ai_settings, screen, status, sb, ship, aliens, bullets):
    """开始新游戏"""
    
    # 重置上一次游戏末的设置，使之回到初始值
    ai_settings.initialize_dynamic_settings()
    
    # 重置游戏统计信息
    status.reset_status()
    status.game_active = True
    
    # 重置记分牌图像
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    
    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
    pygame.mixer.music.load('sound/fighting.mp3')
    pygame.mixer.music.play(-1)



def fire_bullet(ai_settings, screen, ship, bullets):
    """如果子弹还有剩余，则发射一颗子弹"""
    
    # 创建一颗子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings, screen, status, sb, ship, aliens, bullets, explosion):
    """更新子弹的位置，并删除已消失的子弹"""
    
    # 更新子弹的位置
    bullets.update()
    
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        
        check_bullet_alien_collisions(ai_settings, screen, status, sb, ship, aliens, bullets, explosion)
        
def check_bullet_alien_collisions(ai_settings, screen, status, sb, ship, aliens, bullets, explosion):
    """响应子弹和外星人的碰撞"""
    
    # 删除发生碰撞的子弹和外星人，下面参数若为False则与之相对应的物体碰撞后不消失
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # collisions 返回值是一个字典，每一个子弹对应于被其打中的外星人，所以值是一个列表，包含所有被打中的外星人
    if collisions:
        # 修复一个子弹打中几个外星人或两个子弹同时打中一个外星人的Bug情况
        for alien in collisions.values():
            killed = len(alien)
            status.score += ai_settings.alien_points * killed
            while killed:
                blast_wav = pygame.mixer.Sound('sound/explosion.wav')
                blast_wav.set_volume(0.2)
                blast_wav.play(0)
                
                for blast in alien:
                    
                    # 加载帧动画
                    cartoon = MySprite(screen)
                    cartoon.load("images/alien_killed.bmp", blast.rect.x, blast.rect.y, 90, 90, 7)
                    explosion.add(cartoon)
                    
                killed -= 1
                
            sb.prep_score()
        check_high_score(status, sb)
        
    if len(aliens) == 0:
        # 删除现有子弹并新建一群外星人
            bullets.empty()
            ai_settings.increase_speed()
            
            # 提高等级
            status.level += 1
            sb.prep_level()
            
            create_fleet(ai_settings, screen, ship, aliens)
 
def check_aliens_bottom(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed):
    """检查是否有外星人到达屏幕底端"""
    
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            print("===== 地球被占领！ =====")
            ship_hit(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed)
            break
 
def update_aliens(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed):
    """更新外星人群中的所有外星人的位置"""

    check_fleet_edges(ai_settings, aliens)
    aliens.update()# Group中的所有alien对象都调用此方法！！！

    # 检测外星人和飞船之间的碰撞,有一对一、一对多和多对一的相关方法
    alien = pygame.sprite.spritecollideany(ship, aliens)
    if alien:
        print("===== 战舰坠毁！=====")
        ship_hit(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed, alien)
        
    check_aliens_bottom(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed)
 
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))    
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (7 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height * 1.5 + 2 * alien.rect.height * row_number
    aliens.add(alien)    

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    
    # 创建一个外星人，并计算每行可容纳多少个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
       
def check_high_score(status, sb):
    """检查是否诞生了新的最高分"""
    
    if status.score > status.high_score:
        status.high_score = status.score
        sb.prep_high_score()



def update_screen(ai_settings, screen, status, sb, ship, aliens, bullets, explosion, destroyed, play_button, once):
    """更新屏幕上的图像，并切换到新屏幕"""
    
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)

    if once:
        # 绘制所有星星
        stars = ai_settings.stars
        pic = ai_settings.pictures
        for num in stars:       
            star = Star(screen, stars[num][0], stars[num][1], pic[num-2])
            star.blitme()
        once = False

    # 显示得分
    sb.show_score()
    
    # 重绘所有子弹
    for bullet in bullets.sprites():
        bullet.blitme()
        
    # 覆盖在背景/子弹上（先后顺序问题）
    ship.blitme()
    aliens.draw(screen) #Group中的方法
    
    # 加载帧动画
    framerate = pygame.time.Clock() #创建一个对象来帮助跟踪时间
    #应该每帧调用一次此方法。
    framerate.tick() #它将计算自上次调用以来经过的毫秒数。(无参数)
    # 其中可选的帧参数，这可以用于帮助限制游戏的运行时速度。通过每帧调用一次，程序将永远不会超过每秒40帧（有参数）
    # 也就是说不会很快地将所有图片全部加载完
    
    ticks = pygame.time.get_ticks() # 以毫秒为单位获取时间
    explosion.update(ticks)
    destroyed.update(ticks)
    
    # 移除已加载完的动画
    for explo in explosion.copy():
        if explo.isLast:
            explosion.remove(explo)
    explosion.draw(screen)
    
    for dest in destroyed.copy():
        if dest.isLast:
            destroyed.remove(dest)
    destroyed.draw(screen)   
    # 如果游戏处于非活动状态， 就绘制开始按钮
    if not status.game_active:
        play_button.draw_button()
    
    # 让最近绘制的屏幕可见
    pygame.display.flip()
    