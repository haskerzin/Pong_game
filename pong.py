import pygame
from pygame.locals import *

from sys import exit
import random

class Pong:

    def __init__(self):

        # Screen specs
        self.width = 1000
        self.height = 600
        self.screen = pygame.display.set_mode([self.width, self.height])
        
        # Colors
        self.green = (124,252,0)
        self.white = (255, 255, 255)
        self.blue = (0,0,255)
        self.red = (128,0,0)
        self.black = (0,0,0)
        
        self.speed_1 = 0
        self.speed_2 = 0
        self.player_speed = 10
        self.player_size_x = 10
        self.player_size_y = 100
        self.p1_pos = [0, self.height/2 - self.player_size_y/2]
        self.p2_pos = [self.width - 10, self.height/2 - self.player_size_y/2]
        self.score_1 = 0
        self.score_2 = 0
        
        self.ball_size = 10
        self.ball_pos = [self.width/2, self.height/2]
        self.ball_speed = 3
        self.ball_velocity = [(-1)**random.randint(0,1)*self.ball_speed, (-1)**random.randint(0,1)*self.ball_speed]

        self.score = 0

        self.pressed = False



    def hit_sound(self):
        pygame.mixer.Sound.play(self.pong_sound)

    def scoring_sound(self):
        pygame.mixer.Sound.play(self.score_sound)

    
    def restart_game(self):
        pass

    def update_score(self):
        pass

    


    def move_player(self):
        
        self.p1_pos[1] += self.speed_1
        self.p2_pos[1] += self.speed_2
        
        if self.p1_pos[1] < 0 or self.p1_pos[1] > self.height - self.player_size_y:
            self.p1_pos[1] -= self.speed_1
            self.speed_1 = 0
        
        if self.p2_pos[1] < 0 or self.p2_pos[1] > self.height - self.player_size_y:
            self.p2_pos[1] -= self.speed_2
            self.speed_2 = 0


    # Method that moves the ball
    def move_ball(self):
        self.ball_pos[0] += self.ball_velocity[0]
        self.ball_pos[1] += self.ball_velocity[1]

        # Ball crossed the right side of the screen
        if self.ball_pos[0] >= self.width - self.ball_size:
            self.scoring_sound()
            self.score_1 += 1
            self.ball_pos = [self.width/2, self.height/2]
            pygame.time.wait(3000)
            self.ball_velocity = [(-1)**random.randint(0,1)*self.ball_speed, (-1)**random.randint(0,1)*self.ball_speed]

        # Ball crossed the left side of the screen
        if self.ball_pos[0] <= self.ball_size:
            self.scoring_sound()
            self.score_2 += 1
            self.ball_pos = [self.width/2, self.height/2]
            pygame.time.wait(3000)
            self.ball_velocity = [(-1)**random.randint(0,1)*self.ball_speed, (-1)**random.randint(0,1)*self.ball_speed]

        
        # Ball bounces of the upper side and the bottom of the screen
        if self.ball_pos[1] <= self.ball_size or self.ball_pos[1] >= self.height - self.ball_size:
            self.ball_velocity[1] *= -1
            self.hit_sound()

        # Ball bounces of the player 1 platform
        if (self.ball_pos[0] == self.ball_size + self.player_size_x) and (self.ball_pos[1] >= self.p1_pos[1] - self.ball_size and self.ball_pos[1] <= self.p1_pos[1]+self.player_size_y+self.ball_size):
            self.ball_velocity[0] *= -1
            self.hit_sound()
        
        # Ball bounces of the player 2 platform
        if (self.ball_pos[0] == self.width - self.ball_size - self.player_size_x) and (self.ball_pos[1] >= self.p2_pos[1] - self.ball_size and self.ball_pos[1] <= self.p2_pos[1] + self.player_size_y + self.ball_size):
            self.ball_velocity[0] *= -1
            self.hit_sound()
        
    
    def draw_ball(self):
        pygame.draw.circle(self.screen, self.black, self.ball_pos, self.ball_size)


    def draw_player(self):
        pygame.draw.rect(self.screen, self.blue, [self.p1_pos[0], self.p1_pos[1], 10, 100])
        pygame.draw.rect(self.screen, self.red, [self.p2_pos[0], self.p2_pos[1], 10, 100])


    def draw_middle(self):
        for i in range(0,self.height, 25):
            if (i/25)%2 == 0:
                pygame.draw.rect(self.screen, self.white, [self.width/2-5, i, 10, 25])
            else:
                pygame.draw.rect(self.screen, self.green, [self.width/2-5, i, 10, 25])

    def get_input(self, event):
        
        if event.key == pygame.K_w:
            self.speed_1 = -self.player_speed
        
        elif event.key == pygame.K_s:
            self.speed_1 = self.player_speed

        if event.key == pygame.K_UP:
            self.speed_2 = -self.player_speed
        
        if event.key == pygame.K_DOWN:
            self.speed_2 = self.player_speed


    def get_pressed(self):
        
        if pygame.key.get_pressed()[pygame.K_w]:
            self.speed_1 = -self.player_speed
            self.pressed = True
        
        if pygame.key.get_pressed()[pygame.K_s]:
            self.speed_1 = self.player_speed
            self.pressed = True
      
        if pygame.key.get_pressed()[pygame.K_i]:
            self.speed_2 = -self.player_speed
            self.pressed = True
        if pygame.key.get_pressed()[pygame.K_k]:
            self.speed_2 = self.player_speed
            self.pressed = True

    
    def update_player_speed(self):
        self.speed_1 *= 0.1
        self.speed_2 *= 0.1

        if self.speed_1 <= 1:
            self.speed_1 = 0

        if self.speed_2 <= 1:
            self.speed_2 = 0

    def play_again(self):
        self.play()


    
    def play(self):

        pygame.init()

        pygame.display.set_caption('Pong Game - By Gabs')
        self.pong_sound = pygame.mixer.Sound("PongSoundEdited.wav")
        self.score_sound = pygame.mixer.Sound("FailSound.wav")

        
        font = pygame.font.Font('freesansbold.ttf', 20)
        # score_1 = font.render(f'Score: {self.score_1}', True, self.white, self.green)
        # textRect_1 = score_1.get_rect()
        # textRect_1.center = (self.width/4, 20)

        # score_2 = font.render(f'Score: {self.score_2}', True, self.white, self.green)
        # textRect_2 = score_2.get_rect()
        # textRect_2.center = (self.width - self.width/4, 20)
        

        self.screen

        running = True

        pygame.time.wait(300)

        while running:

            score_1 = font.render(f'Score: {self.score_1}', True, self.white, self.green)
            textRect_1 = score_1.get_rect()
            textRect_1.center = (self.width/4, 20)

            score_2 = font.render(f'Score: {self.score_2}', True, self.white, self.green)
            textRect_2 = score_2.get_rect()
            textRect_2.center = (self.width - self.width/4, 20)



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # if event.type == pygame.KEYDOWN:
                #     self.get_input(event)
                self.get_pressed()

                if self.pressed == False:
                    self.update_player_speed()

                self.pressed = False                   

            
            self.screen.fill(self.green)
            self.draw_middle()
            self.move_ball()
            self.draw_ball()
            self.move_player()
            self.draw_player()
            self.screen.blit(score_1, textRect_1)
            self.screen.blit(score_2, textRect_2)

            

            pygame.time.wait(10)

            pygame.display.flip()

        
        pygame.quit()
        exit()