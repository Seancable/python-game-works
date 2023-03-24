
from vector import Vector
import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
#enemy1_a = simplegui.load_image('https://s3.us-east-2.amazonaws.com/ascensiongamedev/filehost/b28a06ac5850e6556ec12c44f65b3e14.png')
#enemy1_b = simplegui.load_image('https://s3.us-east-2.amazonaws.com/ascensiongamedev/filehost/55942801df7a044914b713a281c53c7d.png')
#enemy1_c = simplegui.load_image('https://s3.us-east-2.amazonaws.com/ascensiongamedev/filehost/16eeaa1a8b6b77bb7fbbd21284a820eb.png')

class EnemyT1:
    def __init__(self, image, pos, x, endX):
        self.pos = pos
        self.image = image
        self.row = 4
        self.col = 4
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rowmid = (self.height/self.row)*1.5
        self.colmid = (self.width/self.row)/2
        self.health = 3
        self.edge = self.pos.get_p()
        self.life = True
        self.x = x
        self.endX = endX
        self.move = Vector(-1, 0)
        #self.left=True
        
    def draw(self,canvas):
        '''
        if self.left==True:
            self.pos.add(Vector(-1,0))
        else:
            self.pos.add(Vector(1,0))
        '''
        self.pos.add(self.move)
        canvas.draw_image(self.image, (self.colmid, self.rowmid), (self.width/self.col, self.height/self.row), self.pos.get_p(), (100,100))

    def next_frame(self):
        self.rowmid = (self.height/self.row)*1.5
        self.colmid += self.width/self.col
        if self.colmid >= self.width:
            self.colmid = (self.width/self.col)/2
            if self.rowmid >= self.height:
                self.rowmid = (self.height/self.row)*1.5

    def hit(self, bullet, character):
        if bullet.pos.x+30 >= self.pos.x >=bullet.pos.x-30 and self.pos.y - 30 <= bullet.pos.y <= self.pos.y + 30:
            if self.health == 1:
                self.health -= 1
                self.life = False
                self.pos = Vector(1000,1000)
            self.health -= 1
            return True
        
    def attack(self, character):
        if  self.pos.x + 30 >= character.pos.x >= self.pos.x - 30  and self.pos.y + 30 >= character.pos.y >= self.pos.y - 30:
            #self.pos = (Vector(self.pos.x + 100, self.pos.y))
            return True
         
        if self.pos.x < self.x:
            self.pos.x = self.x
            self.move = Vector(1, 0)
        if self.pos.x > self.endX:
            self.pos.x = self.endX
            self.move = Vector(-1, 0)      
    def obstacle(self):
        if self.pos.x < self.x:
            self.pos.x = self.x
            self.move = Vector(1, 0)
        if self.pos.x > self.endX:
            self.pos.x = self.endX
            self.move = Vector(-1, 0)          
        
