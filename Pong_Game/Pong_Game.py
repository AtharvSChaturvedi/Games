import pygame

pygame.init()

#game variables
WIDTH=600
HEIGHT=600

fps=30
clock=pygame.time.Clock()
font=pygame.font.SysFont(None,55)

#colors
white=(255,255,255)
black=(0,0,0)

#window

window=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

def scores(scorel, scorer):
    left_score_surface=font.render(f"{scorel}", True, white)
    right_score_surface=font.render(f"{scorer}",True,white)

    left_score_rect=left_score_surface.get_rect(center=(WIDTH//4, 50))
    right_score_rect=right_score_surface.get_rect(center=(3*WIDTH//4, 50))

    window.blit(left_score_surface, left_score_rect)
    window.blit(right_score_surface, right_score_rect)


def home_screen():
    exit_game=False
    while not exit_game:
        window.fill(black)

        font = pygame.font.Font(None, 55)
        text_surface = font.render("PONG", True, white)
        text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2-25))
        window.blit(text_surface, text_rect)


        font2 = pygame.font.Font(None, 45)
        text_surface2 = font2.render("press c to continue", True, white)
        text_rect2 = text_surface2.get_rect(center=(WIDTH//2, HEIGHT//2+25))
        window.blit(text_surface2, text_rect2)

        font3 = pygame.font.Font(None, 25)
        text_surface3 = font3.render("Left Paddle:-", True, white)
        text_rect3 = text_surface3.get_rect(center=(150, 450))
        window.blit(text_surface3, text_rect3)

        font5 = pygame.font.Font(None, 25)
        text_surface5 = font5.render("W=UP S=DOWN", True, white)
        text_rect5 = text_surface5.get_rect(center=(150, 466))
        window.blit(text_surface5, text_rect5)

        font4 = pygame.font.Font(None, 25)
        text_surface4 = font4.render("Right Paddle:-", True, white)
        text_rect4 = text_surface4.get_rect(center=(450,450))
        window.blit(text_surface4, text_rect4)

        font6 = pygame.font.Font(None, 25)
        text_surface6 = font6.render("Up=UP Down=DOWN", True, white)
        text_rect6 = text_surface6.get_rect(center=(450, 466))
        window.blit(text_surface6, text_rect6)


        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c:
                    pass
                    gameloop()

        pygame.display.update()
        clock.tick(fps)


def gameloop():
    global fps
    new_fps=fps

    #right paddle bar
    r_paddle_bar_x=560
    r_paddle_bar_y=250
    r_paddle_bar_len=100
    r_paddle_bar_wdth=20
    r_paddle_velocity=10
    score_r=0

    #left paddle bar
    l_paddle_bar_x=30
    l_paddle_bar_y=250
    l_paddle_bar_len=100
    l_paddle_bar_wdth=20
    l_paddle_velocity=10
    score_l=0

    #ball
    ball_x=WIDTH//2
    ball_y=HEIGHT//2
    ball_r=10
    ball_velocity_x=5
    ball_velocity_y=5

    new_vel_x=5
    new_vel_y=5

    exit_game=False
    game_over=False
    while not exit_game:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit_game=True

        if game_over:
            if score_l>=5:
                window.fill(black)
                font = pygame.font.Font(None, 55)
                text_surface = font.render("LEFT WON!", True, white)
                text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2-25))
                window.blit(text_surface, text_rect)
            if score_r>=5:
                window.fill(black)
                font = pygame.font.Font(None, 55)
                text_surface = font.render("RIGHT WON!", True, white)
                text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2-25))
                window.blit(text_surface, text_rect)

            font2 = pygame.font.Font(None, 45)
            text_surface2 = font2.render("press enter to restart", True, white)
            text_rect2 = text_surface2.get_rect(center=(WIDTH//2, HEIGHT//2+25))
            window.blit(text_surface2, text_rect2)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game=True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and r_paddle_bar_y > 0:
                r_paddle_bar_y -= r_paddle_velocity
            if keys[pygame.K_DOWN] and r_paddle_bar_y < HEIGHT - r_paddle_bar_len:
                r_paddle_bar_y += r_paddle_velocity
            if keys[pygame.K_w] and l_paddle_bar_y > 0:
                l_paddle_bar_y -= l_paddle_velocity
            if keys[pygame.K_s] and l_paddle_bar_y < HEIGHT - l_paddle_bar_len:
                l_paddle_bar_y += l_paddle_velocity

            ball_x+=ball_velocity_x
            ball_y+=ball_velocity_y

            #ball collision with side upper walls
            if ball_y-ball_r<=0 or ball_y+ball_r>=HEIGHT:
                ball_velocity_y*=-1
                new_vel_y=ball_velocity_y

            #ball collision with paddle bars
            if (ball_x - ball_r <= l_paddle_bar_x + l_paddle_bar_wdth and
                l_paddle_bar_y <= ball_y <= l_paddle_bar_y + l_paddle_bar_len):
                ball_velocity_x *= -1
                new_vel_x=ball_velocity_x
                new_fps+=fps*(0.05)

            if (ball_x + ball_r >= r_paddle_bar_x and
                r_paddle_bar_y <= ball_y <= r_paddle_bar_y + r_paddle_bar_len):
                ball_velocity_x *= -1 
                new_vel_x=ball_velocity_x
                new_fps+=fps*(0.05)

            #going the other side
            if ball_x<0:
                ball_x, ball_y=WIDTH//2, HEIGHT//2
                ball_velocity_x, ball_velocity_y = -1*(new_vel_x),-1*(new_vel_y)
                score_r+=1
                new_fps=fps
            if ball_x>WIDTH:
                ball_x, ball_y=WIDTH//2, HEIGHT//2
                ball_velocity_x, ball_velocity_y = -1*(new_vel_x),-1*(new_vel_y)
                score_l+=1
                new_fps=fps

            if score_l>=5 or score_r>=5:
                game_over=True       
            
            
            window.fill(black)
            pygame.draw.rect(window, white, [r_paddle_bar_x,r_paddle_bar_y,r_paddle_bar_wdth,r_paddle_bar_len])
            pygame.draw.rect(window, white, [l_paddle_bar_x,l_paddle_bar_y,l_paddle_bar_wdth,l_paddle_bar_len])
            pygame.draw.circle(window,white,[ball_x,ball_y], ball_r)

        scores(score_l,score_r)
        pygame.display.update()
        clock.tick(new_fps)
    

home_screen()
pygame.quit()
quit()
