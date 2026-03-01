from turtle import Turtle

STARTING_POSITIONS=[(0,0), (-20,0), (-40,0)]
MOVE_POSITIONS=20
UP=90
DOWN=270
LEFT=180
RIGHT=0

class Snake:
    def __init__(self):
        self.body=[]
        self.createsnake()

    def createsnake(self):
        for position in STARTING_POSITIONS:
            self.add_body(position)
        

    def add_body(self, position):
        sq=Turtle("square")
        sq.color("green")
        sq.penup()
        sq.goto(position)
        self.body.append(sq)

    def extend(self):
        self.add_body(self.body[-1].position())
    
    def move(self):
        for sq_num in range(len(self.body)-1,0,-1):
            new_x=self.body[sq_num-1].xcor()
            new_y=self.body[sq_num-1].ycor()
            self.body[sq_num].goto(new_x,new_y)

        self.body[0].forward(MOVE_POSITIONS)

    def up(self):
        if self.body[0].heading()!=DOWN:
            self.body[0].setheading(UP)

    def down(self):
        if self.body[0].heading()!=UP:
            self.body[0].setheading(DOWN)

    def left(self):
        if self.body[0].heading()!=RIGHT:
            self.body[0].setheading(LEFT)

    def right(self):
        if self.body[0].heading()!=LEFT:
            self.body[0].setheading(RIGHT)
