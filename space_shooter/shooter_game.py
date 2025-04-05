#Создай собственный Шутер!

from pygame import *
from random import*

win_width = 700 #ширина окна
win_height = 500 #высота
lose = 0
score = 0
#Фон и игрок
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
score = 0
lost = 0
max_score = 11 #Для победы
max_lose = 3 #Для проигрыша
#Классы объектов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)

        self.image =  transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed 

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>5:
            self.rect.x-= self.speed
        if keys[K_d] and self.rect.x< win_width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        #Исчезновение внизу экрана
        if self.rect.y>win_height:
            self.rect.y = randint(80, win_width-80)
            self.rect.y = 0
            lose+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y+= self.speed

        if self.rect.y<0:
            self.kill()
#Создание окна
window = display.set_mode((win_width, win_height))
display.set_caption('Игра из рекламы')

background = transform.scale(image.load(img_back), (win_width, win_height))

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#Игрок
ship = Player(img_hero, 5, win_height-100, 80, 100, 10)
finish = False
run = True
#Группа врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width-80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)
bullets = sprite.Group()
#Текст
font.init()
font2 = font.SysFont("Verdana", 36)

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key==K_SPACE:
                fire_sound.play()
                ship.fire()
    if not finish:
        #Текст
        window.blit(background, (0, 0))
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render("Пропущено: " + str(lose), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(bullets, monsters, True, True)
        for c in collides:
            score+=1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        #Возможный проигрыш
        if sprite.spritecollide(ship, monsters, False) or lost>=max_lose:
            finish = True
            window.blit(text_lose, (200, 200))
        #Победа
        if score>=max_score:
            finish = True
            window.blit(text,(200, 200))
        display.update()

    time.delay(50)