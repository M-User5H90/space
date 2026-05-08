from pygame import *
from random import *

#global variable
score = 0
lost = 0

#directory
img_bg = "GalaxyGame/Space.jpg"
img_player = "GalaxyGame/Spaceship.png"
img_enemy = "GalaxyGame/Enemy.png"
img_bullet = "GalaxyGame/Missile.png"
music1 = 'GalaxyGame/BGM.mp3'

#Class GameSprite
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
        
#player n enemy
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < h-80:
            self.rect.y += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < w-80:
            self.rect.x += self.speed  

    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,-15)
        bullet.rect.centerx = self.rect.centerx
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y > h:
            self.rect.x = randint(80, w-80)
            self.rect.y = 0
            missed += 1
            self.speed = randint(1,5)     

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#Game Scene:            
w = 700
h = 500
window = display.set_mode((w, h))
display.set_caption('Catch')
background = transform.scale(image.load(img_bg), (w, h))

finish = False
game = True
FPS = 60
clock = time.Clock()

#music
mixer.init()
mixer.music.load(music1)
mixer.music.play()
mixer.music.set_volume(0.2)

#text
font.init()
font1 = font.Font(None,80)
font2 = font.Font(None, 30)
win = font1.render("YOU WIN!", True, (0,255,0))
lose = font1.render("YOU LOSE", True, (255,0,0))

#scoring
score = 0
missed = 0
win = 50
lose = 10
life = 3

#Game characters
player = Player(img_player, 5, h-80, 5) 
enemies = sprite.Group()
for i in range(1,6):
    enemy = Enemy(img_enemy, randint(80,w-80),-40,randint(1,3))
    enemies.add(enemy)

#bullets
bullets = sprite.Group()

while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_z:
                player.fire()
    if not finish:
        window.blit(background, (0,0))
        player.update()
        enemies.update()
        player.reset()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)

        #player collision
        if sprite.spritecollide(player, enemies, False):
            sprite.spritecollide(player, enemies, True)
            life -= 1

        #bullet collision
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy(img_enemy, randint(80, w-80),-40,randint(1,3))
            enemies.add(enemy)

        #add score
        text = font2.render('Score:  '+str(score),1,(255,255,255))
        window.blit(text,(10,20))

        #enemy missed
        text_missed = font2.render('Missed:  '+ str(missed), 1, (255,255,255))
        window.blit(text_missed,(10,50))

        #total life
        if life == 3:
            life_color = (0,150,0)
        elif life == 2:
            life_color = (150,150,0)
        elif life == 1:
            life_color = (150,0,0)

        text_life = font2.render('Life:  '+ str(life),1,(life_color))
        window.blit(text_life,(630,10))

        #win
        if score >= win:
            finish = True
            text_win = font1.render('YOU WIN!!',True,(0,255,0))
            window.blit(text_win,(200,200))

        #lsoe
        if life == 0 or missed >= lose:
            finish = True
            text_lose = font1.render('You lost..',True,(255,0,0))
            window.blit(text_lose,(200,200))

    display.update()
    clock.tick(FPS)