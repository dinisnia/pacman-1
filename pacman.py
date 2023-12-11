#build pac-man from strach in python with paygame
from boards import board
import pygame
import math

pygame.init()

width = 700
height = 750 
screen = pygame.display.set_mode([width, height])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = board
color = 'red'
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/Player_images/{i}.png'), (35, 35))) 
player_x = 330
player_y = 495
direction = 0
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [ False, False, False, False]
direction_command = 0



def draw_boards():
    num1 = ((height - 50) // 32)
    num2 = (width // 30)
    for i in range(len(level)):
        for j in range (len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1 ),
                                 (j * num2 + (0.5 * num2), i * num1 + num1 ), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2*0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, 
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3*PI/2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, 
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3* PI / 2, 2* PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                (j * num2 + num2, i * num1 + (0.5 * num1)),3 )


def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN 
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))        
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5],270), (player_x, player_y))


def check_position(center_x, center_y):
    turns = [False, False, False, False]
    num1 = ((height - 50) // 32)
    num2 = (width // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if center_x //30 < 29:
        if direction == 0:
            if level[center_y//num1][(center_x - num3)// num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[center_y//num1][(center_x + num3)// num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(center_y + num3)//num1][center_x// num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(center_y - num3)//num1][center_x// num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num3)//num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num3)//num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y//num1][(center_x - num2) // num2] < 3:
                    turns[1] = True
                if level[center_y//num1][(center_x - num2) // num2] < 3:
                    turns[0] = True
                
        if direction == 0 or direction == 1:
            if 12 <= center_x % num2 <= 18:
                if level[(center_y + num1)//num1][center_x // num2] < 3:
                    turns[3] = True
                if level[(center_y - num1)//num1][center_x // num2] < 3:
                    turns[2] = True
            if 12 <= center_y % num1 <= 18:
                if level[center_y//num1][(center_x - num3) // num2] < 3:
                    turns[1] = True
                if level[center_y//num1][(center_x - num2) // num3] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True

    return turns



run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else :
        counter = 0
        flicker = True

    screen.fill('black')
    draw_boards()
    draw_player()
    center_x = player_x + 23
    center_y = player_y + 24
    # pygame.draw.circle(screen, 'white', (center_x, center_y), 2)
    turns_allowed = check_position( center_x, center_y)

    for event in pygame.event.get():
        if event.type == pygame.quit:
            run = False
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3  

        if event.type ==pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

        for i in range(4):
            if direction_command == i and turns_allowed[i]:
                direction = i

        if player_x > 900:
            player_x = -47
        elif player_x < -50:
            player_x = 897
    
    pygame.display.flip()
pygame.quit()