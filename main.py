import pygame
import random
import sys
import os


pygame.init()
SIZE = WIDTH, HEIGHT = 1200, 800
FPS = 60
TILE = 50
GRAVITY = 0.3
maps = ['map1.txt', 'map2.txt']
map_count = 0
f = False
floor_img = 0
red_win = 0
blue_win = 0
the_end = 0
screen_rect = (50, 50, WIDTH - 90, HEIGHT - 90)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
font = pygame.font.Font(None, 30)
is_paused = False

DIRECTIONS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image1 = pygame.transform.scale(image, (50, 50))
    return image1


floor = [load_image('green.png'), 
         load_image('blue.png'),
         load_image('lava.png')]

tanks_img = [pygame.transform.scale(load_image('tank1.png'), (45, 45)),
             pygame.transform.scale(load_image('tank2.png'), (45, 45))]

boom_img = [load_image('boom1.png'),
            load_image('boom2.png'),
            load_image('boom3.png'),
            load_image('boom4.png'),
            load_image('boom5.png'),
            load_image('boom6.png'),
            load_image('boom7.png'),
            load_image('boom8.png')]


ending_img = load_image('ending.jpg')

result_img = load_image('result.jpg')


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = "Нажмите любую клавишу чтобы продолжить"

    fullname = os.path.join('data', 'intro.jpeg')
    fon = pygame.image.load(fullname)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text = font.render(intro_text, 1, (255, 255, 255))
    screen.blit(text, (300, 750))  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def rules():
    fullname = os.path.join('data', 'rules.jpeg')
    fon = pygame.image.load(fullname)
    screen.blit(fon, (0, 0))
    f1 = pygame.font.Font(None, 80)
    text1 = f1.render('УПРАВЛЕНИЕ', 1, (0, 0, 0))
    screen.blit(text1, (410, 100))
    f2 = pygame.font.Font(None, 50)
    text2 = f2.render('красный', 1, (200, 0, 0))
    screen.blit(text2, (100, 300))
    f3 = pygame.font.Font(None, 50)
    text3 = f3.render('синий', 1, (0, 0, 200))
    screen.blit(text3, (850, 300))
    f4 = pygame.font.Font(None, 40)
    text4 = f4.render('Left Shift - выстрел', 1, (0, 0, 0))
    screen.blit(text4, (100, 750))
    f5 = pygame.font.Font(None, 40)
    text5 = f5.render('Right Shift - выстрел', 1, (0, 0, 0))
    screen.blit(text5, (850, 750))                           

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
rules()


class Interface:
    def __init__(self):
        pass

    def update(self):
        pass

    def render(self):
        count = 0
        for i in obj:
            if i.ttype == 'tank':
                pygame.draw.rect(screen, i.color, (10 + count * 70, 5, 22, 22))
                text = font.render(str(i.hp), 1, (255, 255, 255))
                rect = text.get_rect(center=(10 + count * 70 + 32, 5 + 11))
                screen.blit(text, rect)
                count += 1


class Tank:
    def __init__(self, color, x, y, direction, keys):
        obj.append(self)
        self.ttype = 'tank'
        self.color = color
        self.rect = pygame.Rect(x, y, TILE, TILE)
        self.direction = direction
        self.speed = 3
        self.bul_dam = 1
        self.bul_speed = 5
        self.shot_timer = 0
        self.shot_delay = 60
        self.hp = 5

        self.key_left = keys[0]
        self.key_right = keys[1]
        self.key_up = keys[2]
        self.key_down = keys[3]
        self.key_shot = keys[4]

        self.tank_level = 1
        self.img = pygame.transform.rotate(tanks_img[self.tank_level], self.direction * 90)
        self.rect = self.img.get_rect(center=self.rect.center)
        if self.color == (255, 0, 0):
            self.img = tanks_img[0]
        else:
            self.img = tanks_img[1]
            self.img1 = pygame.transform.rotate(self.img, self.direction * 90)
            self.img1 = pygame.transform.scale(self.img, 
                                         (self.img.get_width() - 5, self.img.get_height() - 5))
            self.rect = self.img1.get_rect(center=self.rect.center)


    def update(self):
        if self.color == (255, 0, 0):
            self.img = tanks_img[0]
        else:
            self.img = tanks_img[1]
        self.img1 = pygame.transform.rotate(self.img, self.direction * 90)
        self.img1 = pygame.transform.scale(self.img, 
                                         (self.img.get_width() - 5, self.img.get_height() - 5))
        self.rect = self.img1.get_rect(center=self.rect.center)

        prev_x, prev_y = self.rect.topleft
        if keys[self.key_left]:
            self.rect.x -= self.speed
            self.direction = 3
        elif keys[self.key_right]:
            self.rect.x += self.speed
            self.direction = 1
        elif keys[self.key_up]:
            self.rect.y -= self.speed
            self.direction = 0
        elif keys[self.key_down]:
            self.rect.y += self.speed
            self.direction = 2

        for i in obj:
            if i.ttype != 'boom':
                if i != self and self.rect.colliderect(i.rect) or not self.rect.colliderect(screen_rect):                      
                    self.rect.topleft = prev_x, prev_y

        if keys[self.key_shot] and self.shot_timer == 0:
            dx = DIRECTIONS[self.direction][0] * self.bul_speed
            dy = DIRECTIONS[self.direction][1] * self.bul_speed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bul_dam)
            self.shot_timer = self.shot_delay
        if self.shot_timer > 0:
            self.shot_timer -= 1

    def render(self):
        screen.blit(self.img, self.rect)
        #pygame.draw.rect(screen, self.color, self.rect)
        x = self.rect.centerx + DIRECTIONS[self.direction][0] * 30
        y = self.rect.centery + DIRECTIONS[self.direction][1] * 30
        pygame.draw.line(screen, (255, 255, 255), self.rect.center, (x, y), 4)


    def damage(self, value):
        global f
        global red_win
        global blue_win
        self.hp -= value
        if self.hp <= 0:
            obj.remove(self)
            f = True
        a = []
        for i in obj:
            if i.ttype == 'tank':
                a.append(i)
        if len(a) == 1:
            if a[0].color == (255, 0, 0):
                k = 'Победил красный'
                red_win += 1
                results_screen(k)
            else:
                k = 'Победил синий'
                blue_win += 1
                results_screen(k)


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


all_sprites = pygame.sprite.Group()


def results_screen(k):
    global the_end
    intro_text = k

    if intro_text == 'Победил красный':
        color = (255, 0, 0)
    else:
        color = (0, 0, 255)
    the_end += 1
    fullname = os.path.join('data', 'result.jpg')
    res1 = pygame.image.load(fullname)
    res = pygame.transform.scale(res1, (1200, 800))
    screen.blit(res, (0, 0))
    font = pygame.font.Font(None, 80)
    text = font.render(intro_text, 1, color)
    screen.blit(text, (410, 300))
    r_text = 'Нажмите любую клавишу чтобы играть еще раз'
    font_r = pygame.font.Font(None, 40)
    text_r = font_r.render(r_text, 1, (255, 255, 255))
    screen.blit(text_r, (300, 750))
    particle_count = 80

    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle((600, 250), random.choice(numbers), random.choice(numbers))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                f = True
                return
        all_sprites.update()
        screen.blit(res, (0, 0))
        screen.blit(text, (410, 300)) 
        screen.blit(text_r, (300, 750))
        all_sprites.draw(screen)    
        pygame.display.flip()
        clock.tick(40)


class Bullet:
    def __init__(self, ttank, bx, by, dx, dy, dam):
        bullets.append(self)
        self.ttank = ttank
        self.bx = bx
        self.by = by
        self.dx = dx
        self.dy = dy
        self.dam = dam

    def update(self):
        self.bx += self.dx
        self.by += self.dy

        if self.bx < 0 or self.bx > WIDTH or self.by < 0 or self.by > HEIGHT:
            bullets.remove(self)
        else:
            for i in obj:
                if i != self.ttank and i.ttype != 'boom' and i.rect.collidepoint(self.bx, self.by):
                    i.damage(self.dam)
                    bullets.remove(self)
                    Boom(self.bx, self.by)
                    break

    def render(self):
        pygame.draw.circle(screen, (200, 100, 0), (self.bx, self.by), 5)


class Block:
    def __init__(self, bx, by, size):
        obj.append(self)
        self.ttype = 'block'
        self.rect = pygame.Rect(bx, by, size, size)
        self.hp = 1

    def update(self):
        pass

    def render(self):
        screen.blit(floor[floor_img], self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            obj.remove(self)
 


class Boom:
    def __init__(self, bx, by):
        obj.append(self)
        self.ttype = 'boom'
        self.bx = bx
        self.by = by
        self.s_fps = 0

    def update(self):
        self.s_fps += 0.2
        if self.s_fps >= 3:
            obj.remove(self)

    def render(self):
        img = boom_img[int(self.s_fps)]
        rect = img.get_rect(center=(self.bx, self.by))
        screen.blit(img, rect)



def load_level(filename):
    filename = "data/" + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
  
    max_width = max(map(len, level_map))
 
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


obj = []
bullets = []
Tank((255, 0, 0), 100, 200, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT))

Tank((0, 0, 255), 1100, 700, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT))

ui = Interface()

level = load_level("map.txt")
            

def ending():
    if red_win > blue_win:
        intro_text = 'Победил красный'
        color = (255, 0, 0)
    else:
        intro_text =  'Победил синий'
        color = (0, 0, 255)

    fullname = os.path.join('data', 'ending.jpg')
    fon = pygame.image.load(fullname)
    screen.blit(fon, (0, 0))
    ttext = 'Конец игры'
    font1 = pygame.font.Font(None, 100)
    text1 = font1.render(ttext, 1, (255, 192, 203))
    screen.blit(text1, (410, 300))
    font = pygame.font.Font(None, 80)
    text = font.render(intro_text, 1, color)
    screen.blit(text, (410, 550))
    r_text = 'Нажмите любую клавишу чтобы начать новую игру'
    font_r = pygame.font.Font(None, 25)
    text_r = font_r.render(r_text, 1, (255, 255, 255))
    screen.blit(text_r, (300, 750))
    particle_count = 80

    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle((600, 250), random.choice(numbers), random.choice(numbers))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                f = True
                return
        all_sprites.update()
        screen.blit(fon, (0, 0))
        screen.blit(text1, (410, 300))
        screen.blit(text, (410, 550)) 
        screen.blit(text_r, (300, 750))
        all_sprites.draw(screen)    
        pygame.display.flip()
        clock.tick(40)

def create_level(level):
    for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    pass
                elif level[y][x] == '#':
                    Block(x * TILE, y * TILE, TILE)

create_level(level)

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                switch_pause()

    keys = pygame.key.get_pressed()

    if f:
        obj = []
        bullets = []
        Tank((255, 0, 0), 100, 200, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT))

        Tank((0, 0, 255), 1150, 750, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT))
        ui = Interface()
        if map_count < 2:
            level = load_level(maps[map_count])
            create_level(level)
            f = False
        if map_count < 2:
            map_count += 1
        else:
            map_count = 0
        if floor_img < 2:
            floor_img += 1
        else:
            floor_img = 0
        if the_end == 3:
            ending() 

        
    for i in bullets:
        i.update()

    for i in obj:
        i.update()

    ui.update()
    screen.fill((0, 0, 0))
    for i in bullets:
        i.render()

    for i in obj:
        i.render()
    ui.render()
    

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()