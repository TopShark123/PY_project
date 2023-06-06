import pygame
from object import Object
from os import listdir
from os.path import isfile, join

WIDTH, HEIGHT = 800,600
window = pygame.display.set_mode((WIDTH, HEIGHT))

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet= pygame.image.load(join(path,image)).convert_alpha()

        sprites = []

        for i in range(sprite_sheet.get_width()//width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)  
            rect = pygame.Rect(i * width, 0, width, height)         
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png","") + "_right"] = sprites
            all_sprites[image.replace(".png","") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png","")] = sprites

    return all_sprites

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

class Player(pygame.sprite.Sprite):
    
    GRAVITY = 1 #начална гравитация
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
    ANIMATION_DELAY = 5


    def __init__(self, x,y,width,height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0 #за да се регулира ускорението при падане (по- голям fall.count-> повече ускорение)
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def check_down(self):
        if self.rect.y > 1000:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('GeeksForGeeks', True,(255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2)
            font = pygame.font.SysFont("Arial", 72)
            txtsurf = font.render("You are dead!", True, (255,0,0))
            window.blit(txtsurf,(400 - txtsurf.get_width() // 2, 50 - txtsurf.get_height() // 2))
            

    def check_final(self):
        if self.rect.x > 6800:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('GeeksForGeeks', True,(255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2)
            font = pygame.font.SysFont("Arial", 72)
            txtsurf = font.render("You won!", True, (255,0,0))
            window.blit(txtsurf,(400 - txtsurf.get_width() // 2, 50 - txtsurf.get_height() // 2))
            
           
            
    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY) #изчисляване на земното ускорение 
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count +=1
        if self.hit_count > fps * 2:
            self.hit = False


        self.fall_count += 1
        self.update_sprite()


    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def make_hit(self):
        self.hit = True
        self.hit_count = 0
    
    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count +=1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
