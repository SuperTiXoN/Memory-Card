from pygame import *
import random 


class GameSprite(sprite.Sprite):
    def __init__(self, player_x, player_y, player_speed, player_image, sprite_height, sprite_width):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (sprite_width, sprite_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, player_x, player_y, player_speed, player_image, sprite_height, sprite_width):
        super().__init__(player_x, player_y, player_speed, player_image, sprite_height, sprite_width)
        self.fire_rate = 0
        self.fall_monsters = 0
        self.score_monsters = 0
    def update(self):
        key_click = key.get_pressed()
        self.fire_rate -= 1
        if key_click[K_a]:
            self.rect.x -= self.speed
        if key_click[K_d]:
            self.rect.x += self.speed
        if key_click[K_w]:
            self.rect.y -= self.speed
        if key_click[K_s]:
            self.rect.y += self.speed
        if key_click[K_SPACE]:
            self.faer()
    def faer(self):
        if self.fire_rate <= 0:
            bullets.add(Bullet(self.rect.centerx - 4, self.rect.top, 8, "bullet.png", 15, 10))
            shot = mixer.Sound('fire.ogg')
            shot.play()
            self.fire_rate = 20 


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > win_height:
            self.rect.x = random.randint(65, win_height - 65)
            self.rect.y = random.randint(-80, -60)
            rocket.fall_monsters += 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

bullets = sprite.Group()

window = display.set_mode((700, 700))
display.set_caption("Шутер")

background = transform.scale(image.load('galaxy.jpg'), (700, 700))



fire_rate = 30
FPS = 60
clock = time.Clock()
speed = 2
win_height = 700
lose = 0
win = 0
fall_monsters = 0
score_monsters = 0

rocket = Player(350, 620, 8, 'rocket.png', 65, 65)

monsters = sprite.Group()

for i in range(5):
    monsters.add(Enemy(random.randint(0, 635), random.randint(-100, -60), random.randint(1, 3), "ufo.png", 60, 80))



font.init()
font1 = font.SysFont('Arial', 50)
win_img = font1.render('Попаданий:', 1, (255, 255, 255))
lose_img = font1.render('Пропусков:' + str(lose), 1, (255, 255, 255))
#lives_img = font1.render('Жизней:' + str(3 -= lose), 1, (255, 255, 255))

title_win = font1.render('YOU WIN', True, (255, 0, 0))

title_lose = font1.render('YOU LOSE', True, (255, 0, 0))



#🎵🎵🎵 музыка 🎵🎵🎵
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()




game = True
finish = False
LOSE = False
WIN = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
    window.blit(background, (0, 0))

    sprites_list1 = sprite.spritecollide(rocket, monsters, True)

    if rocket.fall_monsters >= 3 or len(sprites_list1) > 0:
        finish = True
        LOSE = True
        window.blit(title_lose, (300, 300))
    if rocket.score_monsters >= 10:
        finish = True
        WIN = True
        title_win = font1.render('YOU WIN!', 1, (0, 0, 0))
        window.blit(title_win, (300, 300))
    if not finish:
        win_img = font1.render('Убито:' + str(rocket.score_monsters), 1, (255, 255, 255))
        lose_img = font1.render('Пропусков:' + str(rocket.fall_monsters), 1, (255, 255, 255))
        window.blit(win_img, (0, 0))
        window.blit(lose_img, (0, 40))

        fire_rate -= 1

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            i.kill()
            rocket.score_monsters += 1
            monsters.add(Enemy(random.randint(0, 635), random.randint(-100, -60), random.randint(1, 3), "ufo.png", 60, 80))

        rocket.update()
        rocket.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

    if WIN:
        window.blit(title_win, (300, 300))
    if LOSE:
        window.blit(title_lose, (300, 300))
    display.update()
    clock.tick(FPS)

