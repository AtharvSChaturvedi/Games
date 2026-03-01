from turtle import Screen
import time
from snake import Snake
from food import Food
from scoreboard import ScoreBoared

screen=Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)


snake=Snake()
food=Food()
score=ScoreBoared()

screen.listen()
screen.onkey(snake.up, "w")
screen.onkey(snake.down, "s")
screen.onkey(snake.left, "a")
screen.onkey(snake.right, "d")

#moving a snake

game_on=True
while game_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    #detect collision from food
    if snake.body[0].distance(food)<15:
        food.new_location()
        snake.extend()
        score.increase_score()
    
    #collision with wall
    if snake.body[0].xcor()>280 or snake.body[0].xcor()<-280 or snake.body[0].ycor()>280 or snake.body[0].ycor()<-280:
        game_on=False
        score.game_over()

    #detect tail collision
    for i in snake.body[1:]: #everything except heading
        if snake.body[0].distance(i)<10:
            game_on=False
            score.game_over()


screen.exitonclick()
