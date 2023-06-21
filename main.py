import os
from trap import Trap
from object import Object
from block import Block
from player import Player
from fire import Fire
from healthbar import HealthBar
from start import Start
from end import End
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

def draw_start_menu():
    window.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Enter space to', True, (255, 255, 255))
    start_button = font.render('start', True, (255, 255, 255))
    window.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2 - title.get_height()/2))
    window.blit(start_button, (WIDTH/2 - start_button.get_width()/2, HEIGHT/2 + start_button.get_height()/2))
    pygame.display.update()

def draw_game_over_screen():
   window.fill((0, 0, 0))
   font = pygame.font.SysFont('arial', 40)
   title = font.render('Game Over', True, (255, 255, 255))
   restart_button = font.render('R - Restart', True, (255, 255, 255))
   quit_button = font.render('Q - Quit', True, (255, 255, 255))
   window.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2 - title.get_height()/3))
   window.blit(restart_button, (WIDTH/2 - restart_button.get_width()/2, HEIGHT/1.9 + restart_button.get_height()))
   window.blit(quit_button, (WIDTH/2 - quit_button.get_width()/2, HEIGHT/2 + quit_button.get_height()/2))
   pygame.display.update()


def draw_game_win_screen():
   window.fill((0, 0, 0))
   font = pygame.font.SysFont('arial', 40)
   title = font.render('Congrats, you won!', True, (255, 255, 255))
   restart_button = font.render('R - Restart', True, (255, 255, 255))
   quit_button = font.render('Q - Quit', True, (255, 255, 255))
   window.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT/2 - title.get_height()/3))
   window.blit(restart_button, (WIDTH/2 - restart_button.get_width()/2, HEIGHT/1.9 + restart_button.get_height()))
   window.blit(quit_button, (WIDTH/2 - quit_button.get_width()/2, HEIGHT/2 + quit_button.get_height()/2))
   pygame.display.update()



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
        
       
        bar.draw(window)


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
    background, bg_color=  get_background("Yellow.png")
    block_size = 94

    #spike =Trap(100,HEIGHT - block_size,16,8)

    player = Player(100,100,50,50,100)

    fire = Fire(1000,HEIGHT -block_size - 64,16,32)
    fire14 = Fire(968,HEIGHT -block_size - 64,16,32)
    fire2 = Fire(1032,HEIGHT -block_size - 64,16,32)
    fire3 = Fire(2264,HEIGHT -4*block_size - 64,16,32)
    fire4 = Fire(2232,HEIGHT -4*block_size - 64,16,32)
    fire5 = Fire(2200,HEIGHT -4*block_size - 64,16,32)
    fire6 = Fire(5100,HEIGHT -block_size - 64,16,32)
    fire7 = Fire(5132,HEIGHT -block_size - 64,16,32)
    fire8 = Fire(6400,HEIGHT -block_size - 64,16,32)
    fire9 = Fire(435,HEIGHT -3*block_size - 64,16,32)
    fire10 = Fire(530,HEIGHT -4*block_size - 64,16,32)
    fire11 = Fire(625,HEIGHT -5*block_size - 64,16,32)
    fire12 = Fire(6432,HEIGHT -block_size - 64,16,32)
    fire13 = Fire(6464,HEIGHT -block_size - 64,16,32)
    fire15 = Fire(1500,HEIGHT -4*block_size - 64,16,32)
    end = End(6900,HEIGHT - 155,100,100)
    start = Start(20,HEIGHT - 4*block_size - 155,100,100)
    
    trap = Trap(300,HEIGHT - 110,1000,1000)


    bar = HealthBar(0,0,200,20,100)

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
    fire12.on()
    fire13.on()
    fire14.on()
    fire15.on()
 
   
    
    
    
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
             


    
    objects = [*floor,*floor2,*floor3, *floor4,*floor5, *floor6,*floor7,*floor8, Block(0, HEIGHT - block_size * 2, block_size),
                       Block(0, HEIGHT - block_size * 3, block_size),
                       Block(0, HEIGHT - block_size * 4, block_size),
                       Block(0, HEIGHT - block_size * 5, block_size),


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
                       fire,fire2,fire3,fire4,fire5,fire6,fire7,fire8,fire9,fire10,fire11,fire12,fire13,fire14,fire15,end,start]
    

    def restart_game():
        player.rect.x = 100  # Възстановяване на позицията по X на играча
        player.rect.y = 100  # Възстановяване на позицията по Y на играча
        main(window)

        
        
    
    offset_x = 0
    scroll_area_width = 200
    run = True
    game_state = 1
    check = 0
    while run:  
        clock.tick(FPS)    

        if player.check_check():

            result = bar.take_damage(0.175)
            bar.update(result)

            if result == 0:
                game_state = 3
                check = 1
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        

        if game_state == 1:
            keys = pygame.key.get_pressed()
            draw_start_menu()
       
            if keys[pygame.K_SPACE]:
                game_state = 2
                game_over = False

        elif game_state == 3:
            if player.check_status_dead() or check == 1:
                draw_game_over_screen()

            else:
                draw_game_win_screen()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                restart_game()
                game_state = 1
            if keys[pygame.K_q]:
                pygame.quit()
                quit()

        

        if game_state == 2:
            
            bar.draw(window)
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
            fire12.loop()
            fire13.loop()
            fire14.loop()
            fire15.loop()
            
            

            trap.draw(window,offset_x)

        
    
            handle_move(player,objects)
            draw(window, background, bg_color,player,objects,offset_x,bar)

            if player.check_status_dead() or player.check_status_won():
                game_over = True
                game_state = 3

        

            if ((player.rect.right - offset_x + 300>= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                    (player.rect.left - offset_x -300 <= scroll_area_width) and player.x_vel < 0):
                        offset_x += player.x_vel

                        

        
    
if __name__ == "__main__":
    main(window)
    