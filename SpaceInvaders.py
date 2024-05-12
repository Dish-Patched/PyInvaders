import turtle
import random
import time

fps = 30
fpsForOne = 1 / fps

#screen
window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor("black")
window.title("Space Invaders Clone")

#coordinates of edges
left = -window.window_width() / 2
right = window.window_width() / 2
top = window.window_height() / 2
bottom = -window.window_height() / 2
floor = bottom * 0.9
edge = 0.055 * window.window_width()

#laser cannon
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("square")
cannon.setpos(0, floor)
cannon.Movement = 0

#move
step = 10
laserSpeed = 20
laserLength = 20
alienSpawn = 1.2 #seconds
alienSpeed = 3.5

#drawing cannon
def drawCannon():
    cannon.clear()

    cannon.turtlesize(1,4)
    cannon.stamp()
    cannon.sety(floor + 10)

    cannon.turtlesize(1,1.5)
    cannon.stamp()
    cannon.sety(floor + 20)

    cannon.turtlesize(0.8,0.3)
    cannon.stamp()
    cannon.sety(floor)

lasers = []

def drawLaser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.hideturtle()
    laser.setpos(cannon.xcor(), cannon.ycor())
    laser.setheading(90)
    laser.forward(20)
    laser.pendown()
    laser.pensize(5)

    lasers.append(laser) 

aliens = []

def drawAlien():
    alien = turtle.Turtle()
    alien.penup()
    alien.setpos(random.randint(int(left + edge), int(right - edge)), top)
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    aliens.append(alien)

def moveLaser(laser):
    laser.clear()
    laser.forward(laserSpeed)
    laser.forward(laserLength)
    laser.forward(-laserLength)

def mvLeft():
    cannon.Movement = -1

def mvRight():
    cannon.Movement = 1

def stop():
    cannon.Movement = 0

def clearSprite(sprite, spriteList):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    spriteList.remove(sprite)
    turtle.turtles().remove(sprite)

#for writing text
text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(left, top * 0.8)
text.color("white")


window.onkeypress(mvLeft, "Left")
window.onkeypress(mvRight, "Right")
window.onkeyrelease(stop, "Left")
window.onkeyrelease(stop, "Right")
window.onkeypress(drawLaser, "space")
window.onkeypress(turtle.bye, "q")
window.listen()

drawCannon()

alienTimer = 0
gameTimer = time.time()
score = 0

#game loop
gameStatus = True

while gameStatus:
    timerCurrFrame = time.time()

    timeElapsed = time.time() - gameTimer
    text.clear()
    text.write(
        f"Time: {timeElapsed:5.1f}s\nScore: {score:5}",
        font=("Courier", 20, "bold"),    
    )

    newpos = cannon.xcor() + step * cannon.Movement
    if left + edge <= newpos <= right - edge:
        cannon.setx(newpos)
        drawCannon()

    for laser in lasers.copy():
        moveLaser(laser)
        if laser.ycor() > top:
            clearSprite(laser, lasers)
            break
        for alien in aliens.copy():
            if laser.distance(alien) < 20:
                clearSprite(laser, lasers)
                clearSprite(alien, aliens)
                score += 1
                break

    if time.time() - alienTimer > alienSpawn:
        drawAlien()
        alienTimer = time.time()
    for alien in aliens:
        alien.forward(alienSpeed)
        if alien.ycor() < bottom:
            gameStatus = False
            break

    timeCurrFrame = time.time() - timerCurrFrame
    if timeCurrFrame < fpsForOne:
        time.sleep(fpsForOne - timeCurrFrame)
    window.update()

endScreen = turtle.Turtle()
endScreen.hideturtle()
endScreen.color("red")
endScreen.write("GAME OVER", font=("Courier", 40, "bold"), align="center")

turtle.done()
