import turtle
import math
import colorsys

t = turtle.Turtle()
turtle.bgcolor("black")
turtle.tracer(0)
t.speed(0)
h = 0
a = 0

def draw():
    global h,a
    t.clear()
    for i in range(120):
        c = colorsys.hsv_to_rgb(h %1,1,1)
        t.color(c)
        t.penup()
        t.goto(0,0)
        t.pendown()
        x = math.sin(a+i)*200
        y = math.cos(a+i*2)*200
        t.goto(x,y)
        t.dot(15)
        h += 0.0001
    turtle.update()
    a += 0.05
    turtle.ontimer(draw,10)
draw()
turtle.done

