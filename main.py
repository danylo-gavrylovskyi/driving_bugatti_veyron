import pgzrun
import pygame
from pgzero.actor import Actor

class Car():
    def __init__(self, width, height, actor: Actor):
        self.width = width
        self.height = height
        self.actor = actor
        self.velocity_y = 0

    def draw(self):
        self.actor.draw()

    def move(self, dt):
        self.actor.y += (self.velocity_y * dt)

    def update(self, dt):
        self.move(dt)

class Obstacle():
    def __init__(self, width, height, actor:Actor):
        self.width = width
        self.height = height
        self.actor = actor
    
    def draw(self):
        self.actor.draw()

    def hit(self, car:Car):
        if ((self.actor.x - (self.width/2))  <= car.actor.x <= (self.actor.x + (self.width/2))) and ((self.actor.y - (self.height/2)) <= car.actor.y <= (self.actor.y + (self.height/2))):
            return True

class CarAsObstacle():
    def __init__(self, width, height, actor:Actor, velocity):
        self.width = width
        self.height = height
        self.actor = actor
        self.velocity_y = velocity
    
    def draw(self):
        self.actor.draw()

    def hit(self, car:Car):
        if ((self.actor.x - (self.width/2))  <= car.actor.x <= (self.actor.x + (self.width/2))) and ((self.actor.y - (self.height/2)) <= car.actor.y <= (self.actor.y + (self.height/2))):
            return True

    def move(self, dt):
        self.actor.y += (self.velocity_y * dt)

    def update(self, dt):
        self.move(dt)

def current_stage(stage:int):
    global obstacles, car_obstacles
    match stage:
        case 1:
            screen.blit(stage_1_bg, (0,0))
            screen.draw.text('STAGE 1', (20, 10), color='white', fontsize=30)
            bugatti.draw()
            obstacles.clear()
            obstacles = [Obstacle(120, 68, Actor('conus', ( 50, 150))),
                            Obstacle(120, 68, Actor('conus', ( 120, 150))),
                            Obstacle(120, 68, Actor('conus', ( 220, 360))),
                            Obstacle(120, 68, Actor('conus', ( 290, 360))),
                            Obstacle(120, 68, Actor('conus', ( 50, 520))),
                            Obstacle(120, 68, Actor('conus', ( 120, 520))),
                            Obstacle(120, 68, Actor('conus', ( 380, 150))),
                            Obstacle(120, 68, Actor('conus', ( 450, 150))),
                            Obstacle(120, 68, Actor('conus', ( 380, 520))),
                            Obstacle(120, 68, Actor('conus', ( 450, 520)))]
            for obstacle in obstacles:
                obstacle.draw()
        case 2:
            screen.blit(stage_2_bg, (0,0))
            screen.draw.text('STAGE 2', (20, 10), color='black', fontsize=30)
            bugatti.draw()
            obstacles.clear()
            obstacles = [Obstacle(120, 68, Actor('barrier', (150, 200))),
                            Obstacle(120, 68, Actor('barrier', (250, 200))),
                            Obstacle(120, 68, Actor('barrier', (290, 400))),
                            Obstacle(120, 68, Actor('barrier', (390, 400))),
                            Obstacle(120, 68, Actor('barrier', (50, 600))),
                            Obstacle(120, 68, Actor('barrier', (150, 600))),
                            Obstacle(120, 68, Actor('barrier', (250, 600))),
                ]
            for obstacle in obstacles:
                obstacle.draw()
        case 3:
            screen.blit(stage_3_bg, (0,0))
            screen.draw.text('STAGE 3', (20, 10), color='white', fontsize=30)
            bugatti.draw()
            obstacles.clear()
            for car in car_obstacles:
                car.draw()
        case 4:
            screen.blit(stage_4_bg, (0,0))
            screen.draw.text('FINAL STAGE', (20, 10), color='white', fontsize=30)
            bugatti.draw()
            obstacles.clear()
            obstacles = [Obstacle(120, 5, Actor('tree', (120, 370))),
                            Obstacle(120, 5, Actor('tree', (360, 350))),
                            Obstacle(120, 5, Actor('tree', (450, 250))),
                            Obstacle(120, 5, Actor('tree', (40, 250))),
                            Obstacle(220, 84, Actor('crashed_car', (260, 200))),
                ]
            for obstacle in obstacles:
                obstacle.draw()

def draw():
    screen.clear()
    if stage < 5 and not is_car_crashed:
        current_stage(stage)
    elif is_car_crashed:
        current_stage(stage)
        screen.draw.text('YOU LOSE(', (150, 250), color='white', fontsize=50)
        screen.draw.text('PRESS "F" TO START AGAIN', (5, 290), color='white', fontsize=50)
    else:
        screen.blit(stage_4_bg, (0,0))
        screen.draw.text('YOU ARE THE WINNER!!!', (40, 250), color='white', fontsize=50)
        obstacles.clear()

def update(dt):
    global stage, is_car_crashed, start_again, acceleration, car_obstacles                      
    if not is_car_crashed:
        bugatti.update(dt)
        if stage == 3:
            for obstacle in car_obstacles:
                obstacle.update(dt)
                if obstacle.hit(bugatti):
                    is_car_crashed = True
        
        if is_right_pressed:
            if not (bugatti.actor.x + 70) > WIDTH:
                bugatti.actor.x += 1+acceleration
        if is_left_pressed:
            if not (bugatti.actor.x - 70) < 0:
                bugatti.actor.x -= 1+acceleration
        if is_acceleration_on:
            bugatti.velocity_y += acceleration
            acceleration *= 1.02
        if not is_acceleration_on:
            if (bugatti.velocity_y - acceleration) >= 0:
                bugatti.velocity_y -= acceleration
                acceleration /= 1.02
            else:
                bugatti.velocity_y = 10
                acceleration = 1

        
    if bugatti.actor.y > HEIGHT:
        stage+=1
        bugatti.actor.y = 10

    for obstacle in obstacles:
        if obstacle.hit(bugatti):
            is_car_crashed = True

    if start_again:
        is_car_crashed = False
        stage = 1
        bugatti.actor.x = WIDTH // 2
        bugatti.actor.y = 0
        bugatti.velocity_y = 100
        current_stage(stage)
        start_again = False

def on_key_down(key):
    global is_right_pressed, is_left_pressed, start_again, is_acceleration_on
    if key == keys.RIGHT:
        is_right_pressed = True
    if key == keys.LEFT:
        is_left_pressed = True
    if key == keys.SPACE:
        is_acceleration_on = True
    if key == keys.F:
        start_again = True

def on_key_up(key):
    global is_right_pressed, is_left_pressed, is_acceleration_on
    if key == keys.RIGHT:
        is_right_pressed = False
    if key == keys.LEFT:
        is_left_pressed = False
    if key == keys.SPACE:
        is_acceleration_on = False


HEIGHT = 650
WIDTH = 500

stage_1_bg = pygame.image.load('first_stage.png')
stage_2_bg = pygame.image.load('second_stage.png')
stage_3_bg = pygame.image.load('third_stage.png')
stage_4_bg = pygame.image.load('fourth_stage.png')
bugatti = Car(280, 250, Actor('bugatti2', (WIDTH//2, 0)))

is_right_pressed = False
is_left_pressed = False
is_car_crashed = False
start_again = False
is_acceleration_on = False

stage = 1
acceleration = 1

obstacles = []
car_obstacles = [CarAsObstacle(100, 73, Actor('car', (100, 0)), 100),
                CarAsObstacle(100, 73, Actor('car', (200, 250)), 50),
                CarAsObstacle(100, 73, Actor('car', (400, 100)), 100),
                CarAsObstacle(100, 73, Actor('car', (200, 400)), 100)]


pgzrun.go()
