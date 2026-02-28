import pygame as py

class Audio:
    def __init__(self):
        self.hit=py.mixer.Sound("gallery/audio/hit.wav")
        self.flap=py.mixer.Sound("gallery/audio/flap.wav")
        self.point=py.mixer.Sound("gallery/audio/point.wav")
        self.bgm=py.mixer.Sound("gallery/audio/bgm.wav")

    def hit_play(self):
        self.hit.play()

    def flap_play(self):
        self.flap.play()

    def point_play(self):
        self.point.play()

    def bgm_play(self):
        self.bgm.play(-1)
