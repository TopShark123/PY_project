from healthbar import HealthBar
from trap import Trap
from object import Object
from block import Block
from player import Player
from fire import Fire
from button import Button
import pygame
import time
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Py_game")

WIDTH, HEIGHT = 800,600
FPS = 60
PLAYER_VEL = 5 
game_paused = False
window = pygame.display.set_mode((WIDTH, HEIGHT))
COLOR = (255,0,0)




def quit_game():
    time.sleep(3)
    pygame.quit()
    quit()
    

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
        player.check_down()
        player.check_final()
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
    fire3 = Fire(2214,HEIGHT -4*block_size - 64,16,32)
    fire4 = Fire(2182,HEIGHT -4*block_size - 64,16,32)
    fire5 = Fire(2150,HEIGHT -4*block_size - 64,16,32)
    fire6 = Fire(5100,HEIGHT -block_size - 64,16,32)
    fire7 = Fire(5132,HEIGHT -block_size - 64,16,32)
    fire8 = Fire(6400,HEIGHT -block_size - 64,16,32)
    fire9 = Fire(435,HEIGHT -3*block_size - 64,16,32)
    fire10 = Fire(530,HEIGHT -4*block_size - 64,16,32)
    fire11 = Fire(625,HEIGHT -5*block_size - 64,16,32)
    trap = Trap(300,HEIGHT - 110,1000,1000)


   

    bar = HealthBar(0,0,100,20,100)

    fire.on()
    fire2.on()
    fire3.on()
    fire4.on()
    fire5.on()
    fire6.on()
    fire7.on()
    fire8.on()
    fire9.on()
    fire10.on()
    fire11.on()
   
    
    
    
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
             for i in range( 58,65)]
    
    floor8 = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range( 68,75)]
    

    objects = [*floor,*floor2,*floor3, *floor4,*floor5, *floor6,*floor7, *floor8, 
               
                       Block(0, HEIGHT - block_size * 2, block_size),
                       Block(0, HEIGHT - block_size * 3, block_size),
                       Block(0, HEIGHT - block_size * 4, block_size),
                       Block(0, HEIGHT - block_size * 5, block_size),
                       Block(0, HEIGHT - block_size * 6, block_size),


                       Block(block_size * 4, HEIGHT - block_size * 3, block_size),
                       Block(block_size * 5, HEIGHT - block_size * 4, block_size),
                       Block(block_size * 6, HEIGHT - block_size * 4, block_size),
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



                       Block(block_size * 58, HEIGHT- block_size*3, block_size),
                       Block(block_size * 59, HEIGHT- block_size*3, block_size),
                       Block(block_size * 60, HEIGHT- block_size*3, block_size),
                       Block(block_size * 61, HEIGHT- block_size*3, block_size),
                       Block(block_size * 62, HEIGHT- block_size*3, block_size),  
                       Block(block_size * 63, HEIGHT- block_size*3, block_size),

                       
                       Block(block_size * 62, HEIGHT- block_size*4, block_size),
                       Block(block_size * 61, HEIGHT- block_size*5, block_size),
                       Block(block_size * 60, HEIGHT- block_size*6, block_size),
                       Block(block_size * 64, HEIGHT- block_size*3, block_size),
                       
                       
                       
                       
                       
                       Block(block_size * 75, HEIGHT - block_size * 1, block_size),
                       Block(block_size * 75, HEIGHT - block_size * 2, block_size),
                       Block(block_size * 75, HEIGHT - block_size * 3, block_size), 
                       Block(block_size * 75, HEIGHT - block_size * 4, block_size),
                       Block(block_size * 75, HEIGHT - block_size * 5, block_size),
                       Block(block_size * 75, HEIGHT - block_size * 6, block_size),

                       fire,fire2,fire3,fire4,fire5,fire6,fire7,fire8,fire9,fire10,fire11,trap]

    
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

  #          if event.type == pygame.KEYDOWN:
  #              if event.key == pygame.K_ESCAPE:
          #          resume_button.draw(window)
    #                
                     


        player.loop(FPS)
        fire.loop()
        fire2.loop()
        fire3.loop()
        fire4.loop()
        fire5.loop()
        fire6.loop()
        fire7.loop()
        fire8.loop()
        fire9.loop()
        fire10.loop()
        fire11.loop()
        
        trap.draw(window,offset_x)
        
       
        handle_move(player,objects)
        draw(window, background, bg_color,player,objects,offset_x,bar)
        


    
        if ((player.rect.right - offset_x + 300>= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x -300 <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)