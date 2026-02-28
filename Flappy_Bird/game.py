'''FLAPPY BIRD - THE GAME

1.Press ENTER to start the game.

2.Press ENTER(ik again) to save the bird from falling or colliding.

3.Upon colliding press SPACE to restart.

Enjoy the game ;) '''



import pygame as py
import sys,time
from bird import Bird
from pipe import Pipe
from audio import Audio

py.init()

class Game:
    def __init__(self):
        #Initialiszes the game variables
        self.width=289
        self.height=511
        self.caption=py.display.set_caption("Flappy Bird")
        self.win=py.display.set_mode((self.width,self.height))
        self.bird=Bird(0.5) #0.5 is the scale factor
        self.audio=Audio()
        self.enter_pressed=False
        self.start=True
        self.pipes=[]
        self.pipe_count=-20
        self.message_display=True
        self.sound_played=False
        self.bgm_played=True
        self.setupBGandBase()
        self.move_speed=250
        self.font=py.font.SysFont(None,50)
        self.score_txt=self.font.render("0 ",True,(255,255,255))
        self.score_txt_rect=self.score_txt.get_rect(center=(144.5,30))
        self.start_monitoring=False
        self.score_count=0
        self.clock=py.time.Clock()

        self.gameloop()

    def gameloop(self):
        last_time=time.time()
        while True:
            new_time=time.time()
            dt=new_time-last_time
            last_time=new_time
            for event in py.event.get():
                if event.type==py.QUIT:
                    py.quit()
                    sys.exit()
                if event.type==py.KEYDOWN and self.start:
                    if event.key==py.K_RETURN:
                        self.enter_pressed=True
                        self.bird.update_on=True
                        self.message_display=False
                        self.bgm_played=False
                    if event.key==py.K_RETURN and self.enter_pressed:
                        self.bird.fly(dt)
                if event.type==py.KEYUP:
                        if event.key==py.K_SPACE:
                            self.restartgame()
                
                

            self.draw()
            self.score()
            self.playbgm()
            self.show_message()
            self.update_everything(dt)
            self.check_collisions()
            py.display.update()
            self.clock.tick(60) #fps=30

    def score(self):
        #Checks the score as the bird crosses the pipe
        if len(self.pipes)>0:
            if self.bird.rect.left>self.pipes[0].rect_down.left and self.bird.rect.right<self.pipes[0].rect_down.right and not self.start_monitoring:
                self.start_monitoring=True
            if self.bird.rect.left>self.pipes[0].rect_down.right and self.start_monitoring:
                self.start_monitoring=False
                self.score_count+=1
                self.score_txt=self.font.render(f"{self.score_count}",True,(255,255,255))
                self.audio.point_play()
            

    def restartgame(self):
        #Quite obvious...
        self.enter_pressed=False
        self.start=True
        self.bird.reset()
        self.pipes.clear()
        self.pipe_count=-20
        self.bird.update_on=False
        self.message_display=True
        self.sound_played=False
        self.start_monitoring=False
        self.score_count=0
        self.score_txt=self.font.render(f"{self.score_count}",True,(255,255,255))

    def setupBGandBase(self):
        #Sets up the background and base
        self.background=py.image.load("gallery/images/background.png").convert()
        self.base1=py.image.load("gallery/images/base.png").convert()
        self.base2=py.image.load("gallery/images/base.png").convert()
        self.titlecard=py.image.load("gallery/images/titlecard.png").convert_alpha()

        self.base1_rect=self.base1.get_rect()
        self.base2_rect=self.base2.get_rect()

        self.base1_rect.x=0
        self.base2_rect.x=self.base1_rect.right
        self.base1_rect.y=378
        self.base2_rect.y=378

        self.titlecard_rect=self.titlecard.get_rect()
        self.titlecard_rect.x=-110
        self.titlecard_rect.y=-150

    def draw(self):
        #Draws the pipes, base, bird and score
        self.win.blit(self.background,(0,0))
        for pipe in self.pipes:
            pipe.draw_pipe(self.win)
        self.win.blit(self.base1,self.base1_rect)
        self.win.blit(self.base2,self.base2_rect)
        self.win.blit(self.bird.img,self.bird.rect)
        self.win.blit(self.score_txt,self.score_txt_rect)

    def show_message(self):
        #Shows the title card
        if self.message_display:
            self.win.blit(self.titlecard,self.titlecard_rect)
        

    def check_collisions(self):
        #Checks if the bird collids with the pipes
        if len(self.pipes):
            if self.bird.rect.bottom>380:
                self.bird.update_on=False
                self.enter_pressed=False
                self.start=False
                if not self.sound_played:
                    self.audio.hit_play()
                    self.sound_played=True
            if self.bird.rect.colliderect(self.pipes[0].rect_down) or self.bird.rect.colliderect(self.pipes[0].rect_up):
                self.enter_pressed=False
                self.start=False
                if not self.sound_played:
                    self.audio.hit_play()
                    self.sound_played=True
            
    
    def update_everything(self,dt):
        #Updates the game
        if self.enter_pressed:
            self.base1_rect.x-=int(self.move_speed*dt)
            self.base2_rect.x-=int(self.move_speed*dt)

            if self.base1_rect.right<0:
                self.base1_rect.x=self.base2_rect.right
            if self.base2_rect.right<0:
                self.base2_rect.x=self.base1_rect.right

            if self.pipe_count>70:
                self.pipes.append(Pipe(1.0,self.move_speed))
                self.pipe_count=0
            
            self.pipe_count+=1

            for pipe in self.pipes:
                pipe.update(dt)

            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)
        self.bird.update(dt)
    
    def playbgm(self):
        #Plays the kickass bgm
        if self.bgm_played:
            self.audio.bgm_play()
            self.bgm_played=False         

game=Game()
