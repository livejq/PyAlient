class GameStatus():
    """跟踪游戏的统计信息"""
    
    def __init__(self, ai_settings):
        """初始化统计信息"""
        
        # 无论如何都不能重置
        with open(ai_settings.file_path) as file:
            scores = file.read()
        self.high_score = int(scores)
        
        self.ai_settings = ai_settings
        self.reset_status()
        
        # 一开始处于非活动状态
        self.game_active = False
        
    def reset_status(self):
        """初始化随游戏进行而可能变化的统计信息"""
        
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1