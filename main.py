import os
import random
import math
import pygame
import time
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Py_game")

WIDTH, HEIGHT = 800,600
FPS = 60
PLAYER_VEL = 5 
window = pygame.display.set_mode((WIDTH, HEIGHT))
COLOR = (255,0,0)

def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def get_trap(width, height):
    path = join("assets","Traps", "Spikes", "Idle.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, width, height)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

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

def quit_game():
    time.sleep(3)
    pygame.quit()
    quit()


class Player(pygame.sprite.Sprite):
    
    GRAVITY = 1 #начална гравитация
    SPRITES = load_sprite_sheets("MainCharacters", "VirtualGuy", 32, 32, True)
    ANIMATION_DELAY = 5


    def __init__(self, x,y,width,height, max_hp):
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
        self.hp = max_hp
        self.max_hp = max_hp

    def check(self):
        if self.rect.y > 1000:
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render('GeeksForGeeks', True,(255, 0, 0))
            textRect = text.get_rect()
            textRect.center = (WIDTH // 2, HEIGHT // 2)
            font = pygame.font.SysFont("Arial", 72)
            txtsurf = font.render("You are dead!", True, (255,0,0))
            window.blit(txtsurf,(400 - txtsurf.get_width() // 2, 50 - txtsurf.get_height() // 2))
            #quit_game()
           
            
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
            self.hp -= 10
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



 #---------------------------------------------------------------------------------------------

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

 
#-------------------------------------------------------------------------------------------------


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

#------------------------------------------------------------------------------------

class HealthBar(Player):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(window, "red", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(window, "green", (self.x, self.y, self.width * ratio, self.height))

#------------------------------------------------------------------------------------
class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    
    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0

#--------------------------------------------------------------------------------------------
class Trap(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        path = join("assets","Traps", "Spikes", "Idle.png")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 0, width, height)
        surface.blit(image, (0, 0), rect)
        self.image.blit(image, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        pygame.transform.scale2x(surface)

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

#--------------------------------------------------------------------------------------------

def get_background(name):
    image = pygame.image.load(join("assets","Background",name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH// width +1):
        for j in range(HEIGHT // height +1):
            pos = (i* width, j*height)
            tiles.append(pos)

    return tiles,image

def draw(window, background, bg_image, player, objects,offset_x,bar):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window,offset_x)
 
        player.draw(window,offset_x)
        player.check()
        bar.draw()
       
        
    


    pygame.display.update()

def handle_move(player,objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)


    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object

def main(window):
    clock = pygame.time.Clock()
    background, bg_color= get_background("Yellow.png")

    block_size = 94

    #spike =Trap(100,HEIGHT - block_size,16,8)

    player = Player(100,100,50,50)

    fire = Fire(1000,HEIGHT -block_size - 64,16,32)
    fire2 = Fire(1032,HEIGHT -block_size - 64,16,32)
    fire3 = Fire(2264,HEIGHT -4*block_size - 64,16,32)
    fire4 = Fire(2232,HEIGHT -4*block_size - 64,16,32)
    fire5 = Fire(2200,HEIGHT -4*block_size - 64,16,32)
    fire6 = Fire(5100,HEIGHT -block_size - 64,16,32)
    fire7 = Fire(5132,HEIGHT -block_size - 64,16,32)
    trap = Trap(300,HEIGHT - 110,1000,1000)


   

    bar = HealthBar(0,0,100,20,100)

    fire.on()
    fire2.on()
    fire3.on()
    fire4.on()
    fire5.on()
    fire6.on()
    fire7.on()
   
    
    
    
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(4)]
    floor2 = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(10,18)]
    
    floor3 = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(33,36)]
    
    floor4 = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(46,47)]
    
    floor5 = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(49,50)]
    
    floor6 = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(54,55)]
    
    floor7 = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range( 58,100)]
    

    objects = [*floor,*floor2,*floor3, *floor4,*floor5, *floor6,*floor7, Block(0, HEIGHT - block_size * 2, block_size),
                       Block(0, HEIGHT - block_size * 3, block_size),
                       Block(0, HEIGHT - block_size * 4, block_size),
                       Block(0, HEIGHT - block_size * 5, block_size),
                       Block(0, HEIGHT - block_size * 6, block_size),


                       Block(block_size * 4, HEIGHT - block_size * 3, block_size),
                       Block(block_size * 5, HEIGHT - block_size * 4, block_size),
                       Block(block_size * 6, HEIGHT - block_size * 5, block_size), 
                       Block(block_size * 7, HEIGHT - block_size * 4, block_size),
                       Block(block_size * 8, HEIGHT - block_size * 4, block_size),
                       Block(block_size * 9, HEIGHT - block_size * 4, block_size),

                     
                       Block(block_size * 11.60, HEIGHT- block_size * 7, block_size),
                       Block(block_size * 11.60, HEIGHT- block_size * 6, block_size),
                       Block(block_size * 11.60, HEIGHT- block_size * 5, block_size),
                       
                       Block(block_size * 14, HEIGHT- block_size * 3, block_size),
                       Block(block_size * 16, HEIGHT- block_size * 4, block_size),
                       Block(block_size * 17, HEIGHT- block_size * 4, block_size),
                       
                       Block(block_size * 22, HEIGHT- block_size * 4, block_size),
                       Block(block_size * 23, HEIGHT- block_size * 4, block_size),
                       Block(block_size * 24, HEIGHT- block_size * 4, block_size),
                       
                       Block(block_size * 28, HEIGHT- block_size * 4.5, block_size),

                       Block(block_size * 35, HEIGHT- block_size * 4.0, block_size),
                       Block(block_size * 37, HEIGHT- block_size * 2.5, block_size),
                       Block(block_size * 40, HEIGHT- block_size * 5.0, block_size),
                       Block(block_size * 41, HEIGHT- block_size * 5.0, block_size),


                       Block(block_size * 35, HEIGHT- block_size * 4.0, block_size),
                       Block(block_size * 37, HEIGHT- block_size * 2.5, block_size),
                       Block(block_size * 39, HEIGHT- block_size * 5.0, block_size),
                       Block(block_size * 40, HEIGHT- block_size * 5.0, block_size),

                       Block(block_size * 46, HEIGHT- block_size, block_size),

                       Block(block_size * 46, HEIGHT- block_size*2, block_size),
                       Block(block_size * 46, HEIGHT- block_size*3, block_size),
                       Block(block_size * 46, HEIGHT- block_size*5, block_size),
                       Block(block_size * 46, HEIGHT- block_size*6, block_size),
                       Block(block_size * 46, HEIGHT- block_size*7, block_size),
                       Block(block_size * 46, HEIGHT- block_size*8, block_size),


                       Block(block_size * 49, HEIGHT- block_size*1, block_size),
                       Block(block_size * 49, HEIGHT- block_size*2, block_size),
                       Block(block_size * 49, HEIGHT- block_size*3, block_size),
                       Block(block_size * 49, HEIGHT- block_size*4, block_size),
                       Block(block_size * 49, HEIGHT- block_size*6, block_size),
                       Block(block_size * 49, HEIGHT- block_size*7, block_size),
                       Block(block_size * 49, HEIGHT- block_size*8, block_size),


                       Block(block_size * 52, HEIGHT- block_size*1, block_size),
                       Block(block_size * 52, HEIGHT- block_size*2, block_size),
                       Block(block_size * 52, HEIGHT- block_size*3, block_size),
                       Block(block_size * 52, HEIGHT- block_size*4, block_size),
                       Block(block_size * 52, HEIGHT- block_size*5, block_size),
                       Block(block_size * 52, HEIGHT- block_size*7, block_size),
                       Block(block_size * 52, HEIGHT- block_size*8, block_size),


                       Block(block_size * 55, HEIGHT- block_size*1, block_size),
                       Block(block_size * 55, HEIGHT- block_size*2, block_size),
                       Block(block_size * 55, HEIGHT- block_size*4, block_size),
                       Block(block_size * 55, HEIGHT- block_size*5, block_size),
                       Block(block_size * 55, HEIGHT- block_size*6, block_size),
                       Block(block_size * 55, HEIGHT- block_size*7, block_size),
                       Block(block_size * 55, HEIGHT- block_size*8, block_size),
                       
                       
                       
                       
                       Block(block_size * 100, HEIGHT - block_size * 1, block_size),
                       Block(block_size * 100, HEIGHT - block_size * 2, block_size),
                       Block(block_size * 100, HEIGHT - block_size * 3, block_size), 
                       Block(block_size * 100, HEIGHT - block_size * 4, block_size),
                       Block(block_size * 100, HEIGHT  - block_size * 5, block_size),
                       Block(block_size * 100, HEIGHT  - block_size * 6, block_size),

                       fire,fire2,fire3,fire4,fire5,fire6,fire7,trap]

    
    offset_x = 0
    scroll_area_width = 200
    run = True
    while run:  
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE  and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        fire2.loop()
        fire3.loop()
        fire4.loop()
        fire5.loop()
        fire6.loop()
        fire7.loop()
        trap.draw(window,offset_x)
        
       
        handle_move(player,objects)
        draw(window, background, bg_color,player,objects,offset_x,bar)
        


    
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)