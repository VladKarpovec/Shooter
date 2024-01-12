from pygame import *
from random import randint, choice  # Add choice from random module

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (50, 50))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self, window):  # Added the window parameter
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self, keys):
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def fire(self, bullets):
        bullet = Bullet("пуля.png", self.rect.centerx, self.rect.top, self.speed)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 520)
            self.rect.y = 0
            lost = lost + 1  # If you want to use global lost, you need to declare it as global in the function

    def set_random_image(self, meteors):
        self.image = transform.scale(image.load(choice(meteors)), (50, 50))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

meteors = ["метеор1.png", "метеор2.png", "метеор3.png", "метеор4.png"]
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("45.jpg"), (700, 650))

player = Player("Літак.png", 350, 420, 8)
bullets = sprite.Group()
monsters = sprite.Group()

for i in range(1, 6):
    monster = Enemy(choice(meteors), randint(0, 650), -50, randint(1, 5))
    monster.set_random_image(meteors)
    monsters.add(monster)

score = 0
game = True
finish = False
goal = 25
max_lost = 3
lost = 0
cbullets = 35

clock = time.Clock()
FPS = 30
font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 36)
win_text = font2.render("YOU WON", True, (0, 200, 0))
lose_text = font2.render("YOU LOSE", True, (255, 0, 0))

while game:
    keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if cbullets > 0:
                    cbullets = cbullets - 1
                    player.fire(bullets)
            if e.key == K_r:
                finish = False
                player = Player("Літак.png", 350, 420, 8)
                score = 0
                lost = 0
                cbullets = 35
                monsters.empty()
                for i in range(1, 6):
                    monster = Enemy(choice(meteors), randint(0, 650), -50, randint(1, 5))
                    monster.set_random_image(meteors)
                    monsters.add(monster)
                bullets.empty()

    if not finish:
        window.blit(background, (0, 0))
        player.reset(window)
        player.update(keys)

        text_lose = font1.render(
            "Пропущено: " + str(lost), 1, (255, 255, 255)
        )
        window.blit(text_lose, (10, 50))

        text_score = font1.render(
            "Рахунок: " + str(score), 1, (255, 255, 255)
        )
        window.blit(text_score, (10, 10))
        text_bullets = font1.render(
            "Патрони: "+ str(cbullets), 1, (255,255,255)
        )
        window.blit(text_bullets, (550,10))

        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)

    if sprite.groupcollide(monsters, bullets, True, True):
        score += 1
        monster = Enemy(choice(meteors), randint(80, 420), -40, randint(1, 5))
        monster.set_random_image(meteors)
        monsters.add(monster)

    if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
        finish = True
        text_rect = lose_text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
        window.blit(lose_text, text_rect)

    if score >= goal:
        finish = True
        text_rect = win_text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
        window.blit(win_text, text_rect)

    clock.tick(FPS)
    display.update()
