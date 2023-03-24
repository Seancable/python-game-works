from vector import Vector
from character import *
from healthpack import HealthPack
from keyboard import Keyboard
from bullet import Bullet
from obstacles import Obstacle
from enemy import EnemyT1
import random
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


enemy1_a = simplegui.load_image('https://s3.us-east-2.amazonaws.com/ascensiongamedev/filehost/b28a06ac5850e6556ec12c44f65b3e14.png')
enemy1_b = simplegui.load_image('https://s3.us-east-2.amazonaws.com/ascensiongamedev/filehost/55942801df7a044914b713a281c53c7d.png')
enemy1_c = simplegui.load_image('https://s3.us-east-2.amazonaws.com/ascensiongamedev/filehost/16eeaa1a8b6b77bb7fbbd21284a820eb.png')
bck = simplegui.load_image('https://raw.githubusercontent.com/Seancable/Python-game-project/main/Level1_01.png')

class Background:
    def __init__(self, img, width, height):
        self.image = img
        self.width = width
        self.height = height
        self.center = (1152/2, 648/2)
        self.centerDest = (width/2, height/2)
        self.widthHeight = 1152, 648
        self.dest = width, height

    def draw(self, canvas):
        canvas.draw_image(self.image, self.center, self.widthHeight, self.centerDest, self.dest)
    
class Clock:
    def __init__(self):
        self.time=0
    def tick(self):
        self.time+=1
    def transistion(self,frame_duration):
        if self.time % frame_duration==0:
            return True
        else:
            return False

class Interaction:
    def __init__(self, sheet, keyboard,hp, obstacle,enemy,bullet):
        self.sheet = sheet
        self.keyboard = keyboard
        self.hp=hp
        self.obstacle = obstacle
        self.enemies=enemy
        self.bullet=bullet
    def update(self):
        if self.keyboard.up:
            self.keyUp()
        if self.keyboard.right:
            self.keyRight()

        if self.keyboard.left:
            self.keyLeft()

        if not (self.keyboard.right or self.keyboard.left or self.keyboard.up):
            self.sheet.rows=(self.sheet.height/self.sheet.row)/2
            self.sheet.width=IMAGE.get_width()
        if (self.sheet.pos.get_p()[0]<=self.hp.pos.get_p()[0]+30 or self.sheet.pos.get_p()[0]<=self.hp.pos.get_p()[0]-30) and (self.hp.pos.get_p()[1]-30<=self.sheet.pos.get_p()[1]<=self.hp.pos.get_p()[1]+30) :
            if self.hp.used==False and self.sheet.health!=10:
                self.sheet.health+=2.5
                self.hp.used=True
        #print(self.sheet.pos.get_p(), self.obstacle.getStart())
        # this tracks if the player hits the enemy and if they are dead
        #or the player is invincible
        
    def keyRight(self):
        self.sheet.vel.add(Vector(1, 0))
        self.sheet.rows=(self.sheet.height/self.sheet.row/2)*3
        self.sheet.width=(IMAGE.get_width()/self.sheet.col)*6
        if self.bullet.is_fired():
            self.bullet.direct=True

    def keyLeft(self):
        self.sheet.vel.add(Vector(-1,0))
        self.sheet.rows=(self.sheet.height/self.sheet.row/2)*3
        self.sheet.width=(IMAGE.get_width()/self.sheet.col)*6
        if self.bullet.is_fired():
            self.bullet.direct=False
        
    def keyUp(self):
        if self.sheet.on_ground():
            self.sheet.width=(IMAGE.get_width()/self.sheet.col)*3
        if self.sheet.cols>=self.sheet.width:
            self.sheet.cols=(IMAGE.get_width()/self.sheet.col)/2
            self.sheet.vel.add(Vector(0,-40))
            self.sheet.rows=(self.sheet.height/self.sheet.row/2)*7
        else:
            self.keyboard.up = False

    def keyDown(self):
        pass
'''
y1 = 600
y2 = 450
y3 = 300
y4 = 100
obs = [Obstacle(300, y1, 500, y1, 20, "Orange"),
       Obstacle(200, y2, 550, y2, 20, "Orange"),
       Obstacle(50, y3, 300, y3, 20, "Orange"),
       Obstacle(50, y4, 180, y4, 20, "Orange")]      
sheet=Character(Vector(WIDTH/2,HEIGHT-100), obs)
background = Background(bck, WIDTH, HEIGHT)
clock=Clock()
kbd=Keyboard()
hp=HealthPack(Vector(100,600))
gun=False
bullet=Bullet(sheet)
enemyt1list = [enemy1_a, enemy1_b, enemy1_c]
enemies=[(EnemyT1(enemyt1list[random.randint(0,2)], Vector(400, y1 - 45), 100, 400)), (EnemyT1(enemyt1list[random.randint(0,2)], Vector(550, y2 - 50), 200, 550)), (EnemyT1(enemyt1list[random.randint(0,2)], Vector(300, y3 - 50), 50, 300))]
btime=0
invtime=0
inter=Interaction(sheet,kbd,hp, obs,enemies,bullet)
enemy_counter=0
def draw(canvas):
    global gun,btime,invtime,enemy_counter
    clock.tick()
    inter.update()
    sheet.update()
    background.draw(canvas)
    sheet.draw(canvas)
    for enemy in enemies:
        enemy.obstacle()
        hit=enemy.attack(sheet)
        # this tracks if the player hits the enemy and if they are dead
        #or the player is invincible
        if hit==True:
            if sheet.inv==False:
                sheet.hit()
        if enemy.life==False:
            enemy_counter+=1
            enemy.life=True
        enemy.draw(canvas)
        if clock.transistion(200)==True:
            if enemy.left==True:
                enemy.left=False
            else:
                enemy.left=True
    bullet.draw(canvas)
    hp.draw(canvas)
    if enemy_counter==len(enemies):
        print("all enemies arte dead")
    
    for obstacle in obs:
        obstacle.draw(canvas)
    btime+=1
    if clock.transistion(10)==True:
        for enemy in enemies:
            enemy.next_frame()
        sheet.next_frame()
    if sheet.inv==True:
        invtime+=1
        if invtime%50==0:
            sheet.inv=False
        
# this checks to see if the bullet is fready to be fired and will allow
#the bullets position to chnge to interact with the enviroment
    if kbd.fire and bullet.is_fired():
        bullet.pos=Vector(sheet.pos.get_p()[0],sheet.pos.get_p()[1])
        bullet.draw(canvas)
        gun=True
        btime=0
        
    if gun==True:
        bullet.update()
        for enemy in enemies:
            if enemy.hit(bullet, sheet) == True:
                gun = False
                bullet.pos = Vector(0,0)
        if bullet.pos.x > WIDTH or bullet.pos.x<0:
            gun=False
            bullet.pos=Vector(0,0)
        
frame = simplegui.create_frame('Testing', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()
'''
