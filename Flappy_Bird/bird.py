import pygame as py
from audio import Audio

class Bird(py.sprite.Sprite):
    def __init__(self,scale_factor):
        super(Bird,self).__init__()
        self.img=py.transform.scale_by(py.image.load("gallery/images/bird.png").convert_alpha(),scale_factor)
        self.rect=self.img.get_rect(center=(50,255))
        self.y_velocity=0
        self.gravity=10
        self.flapseed=250
        self.update_on=False
        self.audio=Audio()

    def update(self,dt):
        if self.update_on:
            self.apply_gravity(dt)
            if self.rect.y<=0 and self.flapseed==250:
                self.rect.y=0
                self.flapseed=0
                self.y_velocity=0
            elif self.rect.y>0 and self.flapseed==0:
                self.flapseed=250
    
    def apply_gravity(self,dt):
        self.y_velocity+=self.gravity*dt
        self.rect.y+=self.y_velocity
    
    def fly(self,dt):
        self.y_velocity=-self.flapseed*dt
        self.audio.flap_play()

    def reset(self):
        self.rect.center=(50,255)
        self.y_velocity=0
