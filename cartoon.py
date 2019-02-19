import pygame

class MySprite(pygame.sprite.Sprite):
    def __init__(self, target, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
        self.topleft = 0,0
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.isLast = False
        
    def load(self, filename, x, y, width, height, columns):
        self.master_image = pygame.image.load(filename)
        self.frame_width = width
        self.frame_height = height
        self.rect = x,y,width,height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1 # 行列都是从下标0开始

    def update(self, current_time, rate=80):
        if current_time > self.last_time + rate: # 判断是否该更换帧,rate越大则更换得越慢
            self.frame += 1
            if self.frame > self.last_frame: # 判断此更换的帧是否超过最后一张
                self.isLast = True
            self.last_time = current_time

        if self.frame != self.old_frame and not self.isLast: # 判断若更换了帧且并不是最后一张，则替换原来的帧
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = ( frame_x, frame_y, self.frame_width, self.frame_height )
            self.image = self.master_image.subsurface(rect) # 新的Surface将从其父级继承调色板，颜色键和alpha设置
            self.old_frame = self.frame
