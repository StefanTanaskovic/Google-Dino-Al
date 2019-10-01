import os
import time
import pygame
import random
import neat
from random import randrange
pygame.font.init() 

WIN_WIDTH = 700
WIN_HEIGHT = 150

DINO_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs","dinorun0000.png")),(40,40)),
             pygame.transform.scale(pygame.image.load(os.path.join("imgs","dinorun0001.png")),(40,40)),
             pygame.transform.scale(pygame.image.load(os.path.join("imgs","dinoduck0000.png")),(50,30)),
             pygame.transform.scale(pygame.image.load(os.path.join("imgs","dinoduck0001.png")),(50,30)),
             pygame.transform.scale(pygame.image.load(os.path.join("imgs","dinoJump0000.png")),(40,40)),
             pygame.transform.scale(pygame.image.load(os.path.join("imgs","dinoDead0000.png")),(40,40))]

GROUND_IMG = pygame.image.load(os.path.join("imgs","ground.png"))
BIRD_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs","bird1.png")),(40,40)),
             pygame.transform.scale(pygame.image.load(os.path.join("imgs","bird2.png")),(40,40))]
CSMALL_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","cactusSmall0000.png")),(40,40))
CBIG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","cactusBig0000.png")),(40,40))
CMANY_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs","cactusSmallMany0000.png")),(50,40))

STAT_FONT = pygame.font.SysFont("comicsans",40)

class Dino:
    IMGS = DINO_IMGS
    ANIMATION_TIME = 2

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.img_count = 0
        self.img = self.IMGS[0]
        self.vel = 0
        self.height = self.y
        self.isJumping = False
        self.gravity = 1
        self.isDucking = False

    def jump(self):
        self.isJumping = True
        self.vel = -12
        self.tick_count = 0

    def move(self):
        self.tick_count += 1
        if (self.isJumping):
            self.vel += self.gravity * 1
            if self.vel == 12:
                self.y = 87
                self.vel = 0
                self.isJumping = False
        self.y += self.vel

    def draw(self,win):
        self.img_count += 1

        if (self.isJumping):
            self.img = self.IMGS[4]
            self.img_count = 0
        elif(self.isDucking):
            self.y = 96
            if self.img_count < self.ANIMATION_TIME:
                self.img = self.IMGS[2]
            elif self.img_count < self.ANIMATION_TIME*2:
                self.img = self.IMGS[3]
            elif self.img_count < self.ANIMATION_TIME*3:
                self.img = self.IMGS[3]
            elif self.img_count == self.ANIMATION_TIME*3 + 1:
                self.img = self.IMGS[2]
                self.img_count = 0
                self.isDucking = False
        else:
            self.y = 87
            if self.img_count < self.ANIMATION_TIME:
                self.img = self.IMGS[0]
            elif self.img_count < self.ANIMATION_TIME*2:
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME*3:
                self.img = self.IMGS[1]
            elif self.img_count == self.ANIMATION_TIME*3 + 1:
                self.img = self.IMGS[0]
                self.img_count = 0
   
        win.blit(self.img,(self.x,self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)



class Bird:
    BIRD_IMGS = BIRD_IMGS
    VEL = 7
    ANIMATION_TIME = 2
    def __init__(self,x,y):
        self.distance = x
        self.height = y
        self.img = BIRD_IMGS[0]
        self.passed = False
        self.img_count = 0

    def move(self):
        self.distance -= self.VEL

    def draw(self,win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.BIRD_IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.BIRD_IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.BIRD_IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*3 + 1:
            self.img = self.BIRD_IMGS[0]
            self.img_count = 0
        win.blit(self.img,(self.distance,self.height))


    def collide(self, dino):
        dino_mask = dino.get_mask()
        bottom_mask = pygame.mask.from_surface(self.img)

        bottom_offset = (self.distance - dino.x, self.height - round(dino.y))
        b_point = dino_mask.overlap(bottom_mask, bottom_offset)
        if b_point:
            return True

        return False






class Obstacle:
    DISTANCE = 80
    VEL = 7
    
    def __init__(self,x):
        self.distance = x
        self.height = 87
        self.img = self.set_img()

        self.passed = False


    def set_img(self):
        imgs = [CMANY_IMG,CBIG_IMG,CSMALL_IMG]
        self.img = imgs[random.randrange(0,3) ]
        return self.img
    def move(self):
        self.distance -= self.VEL

    def draw(self,win):
        win.blit(self.img,(self.distance,self.height))

    def collide(self, dino):
        dino_mask = dino.get_mask()
        bottom_mask = pygame.mask.from_surface(self.img)

        bottom_offset = (self.distance - dino.x, self.height - round(dino.y))
        b_point = dino_mask.overlap(bottom_mask, bottom_offset)

        if b_point:
            return True

        return False

class Ground:
    VEL = 7
    WIDTH = GROUND_IMG.get_width()
    IMG = GROUND_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 =self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 =self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1, self.y))
        win.blit(self.IMG,(self.x2, self.y))


def draw_window(win, dinos, obstacles,birds,ground,score,popSize):
    win.fill((255,255,255))
    ground.draw(win)
    for dino in dinos:
        dino.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)
    for bird in birds:
        bird.draw(win)

    text1 = STAT_FONT.render("Population: "+ str(popSize),1,(0,0,0))
    text = STAT_FONT.render("Score: "+ str(score),1,(0,0,0))
    win.blit(text, (5,0))
    win.blit(text1, (WIN_WIDTH - 5 - text1.get_width(),0))

    pygame.display.update()

def main(genomes, config):
    random = randrange(1,3) 
    if random == 1:
        random = 82
    else:
        random = 56
    obstacles = [Obstacle(700)]
    birds = [Bird(1000,56)]
    ground = Ground(120)
    nets = []
    dinos = []
    ge = []

    for _, g in genomes:
        g.fitness = 0  
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(20,87))
        ge.append(g)

    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    popSize = 100
    run = True
    birdstate = False
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        obstacle_ind = 0 
        if len(dinos)> 0:
            if len(obstacles)> 1 and dinos[0].x > obstacles[0].distance + obstacles[0].height:
                obstacle_ind =1
                birdstate = True
        else:
            run = False
            break

        bird_ind = 0 
        if len(dinos)> 0:
            if len(birds)> 1 and dinos[0].x > birds[0].distance + birds[0].height:
                bird_ind =1
                birdstate = False
                
        else:
            run = False
            break

        obstacleDistance = abs(dinos[0].x -obstacles[0].distance )

        for x, dino in enumerate(dinos):
            dino.move()
            ge[x].fitness += 0.1

            if birdstate:
                obstacleDistance = abs(dino.x -birds[bird_ind].distance)
            else:
                obstacleDistance = abs(dino.x -obstacles[obstacle_ind].distance )


            output = nets[x].activate((obstacleDistance,birds[bird_ind].height,abs(obstacles[obstacle_ind].distance -birds[bird_ind].distance )))
            

            mx = 0;
            maxIndex = 0;
            for i in range(len(output)):
                if output[i] > mx:
                    mx = output[i]
                    maxIndex = i

            if maxIndex == 0:
                dino.isDucking = True  
            elif maxIndex == 1:
                if dino.isJumping == False:
                    ge[x].fitness -= 0.2
                    dino.jump() 
            elif maxIndex == 2:
                dino.isDucking = False

        add_obstacle = False
        rem = []
        for obstacle in obstacles:
            for x, dino in enumerate(dinos):
                if obstacle.collide(dino):
                    popSize -=1 
                    ge[x].fitness -=1
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not obstacle.passed and obstacle.distance < dino.x:
                
                    obstacle.passed =True
                    add_obstacle = True

            if obstacle.distance + obstacle.height < 0:
                    rem.append(obstacle)

            obstacle.move()

        if add_obstacle:
            for g in ge:
                g.fitness += 5
            score += 1
            obstacles.append(Obstacle(700))

        for r in rem:
            obstacles.remove(r)

        add_bird = False
        rem1 = []
        for bird in birds:
            for x, dino in enumerate(dinos):
                if bird.collide(dino):
                    popSize -=1 
                    ge[x].fitness -=1
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not bird.passed and bird.distance < dino.x:
                    bird.passed =True
                    add_bird = True
                    

            if bird.distance + bird.height < 0:
                rem1.append(bird)

            bird.move()


        if add_bird:
            for g in ge:
                g.fitness += 5
            score += 1

            if birds[0].height == 56:
                y = 82
            else:
                y = 56
        
            birds.append(Bird((obstacles[obstacle_ind].distance+300),y))

        for r in rem1:
            birds.remove(r)

        ground.move()
        draw_window(win,dinos,obstacles,birds,ground,score,popSize)

            
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter())
    p.add_reporter(neat.StatisticsReporter())


    winner = p.run(main,1000)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    run(config_path)
        






