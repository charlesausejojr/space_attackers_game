import pygame
import random
import math
from pygame import mixer

#initializing the pygame package
pygame.init()

#making a window              (width, height)
screen = pygame.display.set_mode((800,600))


#background image
background = pygame.image.load('space_bg.png')

#backgroun music
mixer.music.load('bg_music.mp3')
mixer.music.play(-1)

#change title and icon - preferrably 32x32
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space_inv.png')
pygame.display.set_icon(icon)

#player spaceship
player_ship = pygame.image.load('ship.png')
#starting coordinates
player_x = 370
player_y = 480
player_x_change = 0

#enemy alien
enemy_speed = 0.2
enemy_alien = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_population = 6

for i in range(enemy_population):
    enemy_alien.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(40,800))
    enemy_y.append(random.randint(20,160))
    enemy_x_change.append(enemy_speed)
    enemy_y_change.append(40)

#player bullet
#ready - you cannot see bullet on the screen
#fire - fires bullet, moves bullet
bullet = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_y_change = 0.7
bullet_state = "ready"

#score system
score_value = 0

font = pygame.font.Font('cruiser.ttf',32)

text_x = 20
text_y = 10

def show_score(x,y):
    #render your font variable
    score = font.render("Score: " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    #blit - to draw
    screen.blit(player_ship,(x,y)) 

def enemy(x,y,i):
    #blit - to draw
    screen.blit(enemy_alien[i],(x,y)) 

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x + 16 ,y + 10))

#calculates if there is collission between bullet and enemy
def isColliding(enemy_x,enemy_y,bullet_x,bullet_y):
    distance = math.sqrt( math.pow((enemy_x - bullet_x),2) + math.pow((enemy_y - bullet_y),2))
    if (distance < 27): 
        explosion_sound = mixer.Sound('explode.mp3')
        explosion_sound.play()
        return True
    else: 
        return False



#loops the game to persistence
running = True
while running:
    #change background color
    screen.fill((0,0,0))
    #background image
    screen.blit(background,(0,0))
    for event in pygame.event.get(): #event - anything happens in the window. Similar to javascript.
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_LEFT):
                # if you render the player += 1 here
                # it will only increment once when a key is pressed
                player_x_change = -0.5
            if(event.key == pygame.K_RIGHT):
                player_x_change = 0.5
            if(event.key == pygame.K_SPACE):
                if(bullet_y > 0 and bullet_state is "ready"):
                    bullet_sound = mixer.Sound('laser.mp3')
                    bullet_sound.play()
                    bullet_x = player_x
                    bullet_state = "fire"
                    
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                player_x_change = 0
    #to keep changing the position
    #if you want something to change or update, do it inside the while loop
    player_x += player_x_change

    #the change could not be seen because it resumes to the given coordinate
    #setting player boundary
    if (player_x <= 0):
        player_x = 0
    if(player_x >= 736):
        player_x = 736
    
    for i in range(enemy_population):
        enemy_x[i] += enemy_x_change[i]
        #setting enemy movement
        if (enemy_x[i] <= 0):
            enemy_y[i] += enemy_y_change[i]
            enemy_x_change[i] = enemy_speed
        if (enemy_x[i] >= 736):
            enemy_x_change[i] = -enemy_speed
            enemy_y[i] += enemy_y_change[i]

        collission = isColliding(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if (collission):
            bullet_y = 480
            bullet_state = "ready"
            score_value += 5
            enemy_speed += 0.02
            enemy_x[i] = random.randint(40,800)
            enemy_y[i] = random.randint(20,160)

        if (enemy_y[i] >= 448):
            if(score_value <= -5):
                score_value = 0
            score_value = score_value - 5
            enemy_x[i] = random.randint(40,800)
            enemy_y[i] = random.randint(20,160)    
        
        enemy(enemy_x[i],enemy_y[i],i)
    
    #setting bullet mobvement
    if bullet_state is "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_y_change
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    player(player_x,player_y)
    show_score(text_x,text_y)
    pygame.display.update() 