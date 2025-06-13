class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, player):
        self.x = player.rect.centerx - 960  
        self.y = player.rect.centery - 540  
