from ursina import *
import time as pytime
import pygame

app=Ursina()

window.title='F1 Game'
window.borderless=False
window.fullscreen=False
window.color=color.black

class Track:
    def __init__(self):
        self.track_segments=[]
        self.layout=[
            (0,0),(0,10),(20,0),(30,0),
            (40,0),(50,0),(30,20),(30,30),
            (30,40),(50,40),(40,40),(20,20),
            (10,20),(0,20),(10,0),(60,0),
            (70,0),(80,0),(90,0),(100,0),
            (100,10),(110,10),(110,20),(110,30),
            (110,40),(110,50),(100,50),(90,50),
            (80,50),(70,50),(60,50),(50,50)
        ]
        self.build_track()

        self.finish_line=Entity(model='cube',texture='white_cube',scale=(10,0.5,1),color=color.azure,position=(0,0.25,0),collider='box')

    def build_track(self):
        for pos in self.layout:
            segment=Entity(model='plane',texture='track.png',scale=(10,1,10),color=color.gray,position=(pos[0],0,pos[1]),collider='box')
            self.track_segments.append(segment)


class Car(Entity):
    def __init__(self, position=(0,0,5),color=color.red):
        super().__init__(model='car.obj',color=color,scale=(1.5,0.5,3),position=position,collider='box')
        self.start_position=position
        self.lap_start_time=pytime.time()
        self.lap_times=[]
        self.max_laps=5
        self.original_speed=40
        self.speed=self.original_speed
        self.turn_speed=150
        self.lap_count=0
        self.crossed_finish=False
        self.scale=0.5
        self.gear = 1
        self.max_gear = 5
        self.min_gear = 1
        self.gear_speeds = {1: 40, 2: 50, 3: 55, 4: 60, 5: 65}
        self.gear_change_cooldown = 0.3
        self.last_gear_change_time = pytime.time()


    def reset_car(self):
        print("Car went off track! Resetting...")
        self.position=self.start_position
        self.rotation=(0,0,0)
        self.crossed_finish=False
        self.lap_start_time=pytime.time()

    def drive(self, finish_line):
        if mouse.left and pytime.time() - self.last_gear_change_time > self.gear_change_cooldown:
            if self.gear < self.max_gear:
                self.gear += 1
                self.speed = self.gear_speeds[self.gear]
                gear_text.text = f"Gear: {self.gear}"
                print(f"Gear shifted up to {self.gear}")
            self.last_gear_change_time = pytime.time()

        if mouse.right and pytime.time() - self.last_gear_change_time > self.gear_change_cooldown:
            if self.gear > self.min_gear:
                self.gear -= 1
                self.speed = self.gear_speeds[self.gear]
                gear_text.text = f"Gear: {self.gear}"
                print(f"Gear shifted down to {self.gear}")
            self.last_gear_change_time = pytime.time()

        on_track=any(self.intersects(segment).hit for segment in game.track.track_segments)

        if not on_track:
            self.reset_car()
            return
        
        if held_keys['w']:
            self.position+=self.forward*time.dt*self.speed
        if held_keys['s']:
            self.position-=self.forward*time.dt*self.speed*0.5
        if held_keys['a']:
            self.rotation_y-=self.turn_speed*time.dt
        if held_keys['d']:
            self.rotation_y+=self.turn_speed*time.dt

        if self.intersects(finish_line).hit:
            if not self.crossed_finish:
                lap_time=pytime.time()-self.lap_start_time
                self.lap_times.append(lap_time)
                self.lap_start_time=pytime.time()
                self.lap_count+=1
                lap_text.text=f"Laps: {self.lap_count}/5"

                if self.lap_times:
                    total_time_text.text=f"Total: {sum(self.lap_times):.2f}s"
                    best_time_text.text=f"Best: {min(self.lap_times):.2f}s"

                print(f"Lap {self.lap_count} completed in {lap_time:.2f} seconds!")
                self.crossed_finish=True

                if self.lap_count==self.max_laps:
                    print("RACE OVER!")
                    print(f"Total Time: {sum(self.lap_times):.2f}s")
                    print(f"Best Lap: {min(self.lap_times):.2f}s")
                    application.quit()
        else:
            self.crossed_finish=False




class GameManager:
    def __init__(self):
        self.track=Track()
        self.car=Car()
        self.setup_camera()
        self.setup_ui()
        self.setup_lighting()

    def setup_camera(self):
        camera.parent=self.car
        camera.position=(0,3,-15)
        camera.rotation_x=10

    def setup_ui(self):
        global lap_text, total_time_text, best_time_text, gear_text
        lap_text=Text(text="Laps: 0",position=(-0.85,0.45),scale=2,background=False)
        total_time_text=Text(text="Total: 0.00s",position=(-0.85, 0.4),scale=2,background=False)
        best_time_text=Text(text="Best: --",position=(-0.85, 0.35),scale=2,background=False)
        gear_text = Text(text="Gear: 1", position=(-0.85, 0.3), scale=1.5, background=False)


    def setup_lighting(self):
        DirectionalLight().look_at(Vec3(1,-1,-1))
        Sky()

    def update(self):
        self.car.drive(self.track.finish_line)


game=GameManager()

def update():
    game.update()

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("bgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

app.run()

app.run()
