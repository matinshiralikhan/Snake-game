import turtle
import time
import random

delay = 0.1

# Score and level
score = 0
high_score = 0
level = 1  # Starting level
score_to_next_level = 50  # Score needed to level up
obstacle_flag = 1  # Flag: 1 = obstacles active, 0 = obstacles inactive

# Set up the screen with a gradient-like background
wn = turtle.Screen()
wn.title("Snake Game by Matin Shiralikhan")
wn.bgcolor("#87CEEB")  # Sky blue background for better visuals
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Panel for the score and level at the top
panel = turtle.Turtle()
panel.speed(0)
panel.shape("square")
panel.color("black")
panel.penup()
panel.goto(0, 275)
panel.shapesize(stretch_wid=1, stretch_len=30)  # Create the rectangular panel
panel.hideturtle()

# Snake head (using built-in shape)
head = turtle.Turtle()
head.speed(0)
head.shape("square")  # Using built-in square shape for the snake head
head.color("darkgreen")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Snake food (using built-in shape)
food = turtle.Turtle()
food.speed(0)
food.shape("circle")  # Using built-in circle shape for the food
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# Pen for score and level display inside the panel
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("#FFFFFF")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0  Level: 1", align="center", font=("Courier", 14, "normal"))

# Obstacles setup with built-in shapes
obstacles = []
num_obstacles = 5  # Number of obstacles

# Function to create obstacles
def create_obstacles():
    global obstacles
    if obstacle_flag == 1:  # Only create obstacles if the flag is set to 1
        for _ in range(num_obstacles):
            obstacle = turtle.Turtle()
            obstacle.shape("triangle")  # Using built-in triangle shape for obstacles
            obstacle.color("purple")
            obstacle.penup()
            x = random.randint(-290, 290)
            y = random.randint(-240, 240)
            obstacle.goto(x, y)
            obstacles.append(obstacle)

# Function to reset obstacles
def reset_obstacles():
    global obstacles
    if obstacle_flag == 1:  # Only reset obstacles if the flag is set to 1
        for obstacle in obstacles:
            obstacle.goto(random.randint(-290, 290), random.randint(-240, 240))

# Functions to control the snake's movement
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

# Function to move the snake based on its direction
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Function to update the level
def check_level_up():
    global level, delay, score_to_next_level
    if score >= score_to_next_level:
        level += 1
        score_to_next_level += 50  # Increase the threshold for the next level
        delay -= 0.005  # Increase speed
        pen.clear()
        pen.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level), align="center", font=("Courier", 14, "normal"))
        print(f"Level up! Now at level {level}!")

# Check for collision with obstacles
def check_obstacle_collision():
    if obstacle_flag == 1:  # Only check for obstacle collision if the flag is set to 1
        for obstacle in obstacles:
            if head.distance(obstacle) < 20:
                return True
    return False

# Listen for keypresses and map them to functions
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Main game loop
if obstacle_flag == 1:
    create_obstacles()  # Create obstacles only if the flag is set to 1

while True:
    wn.update()  # Update the screen

    # Check for a collision with the border or obstacles
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 250 or head.ycor() < -290 or check_obstacle_collision():
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)

        # Clear the segments list
        segments.clear()

        # Reset the score and level
        score = 0
        level = 1
        score_to_next_level = 50  # Reset the level-up threshold
        delay = 0.1

        # Reset obstacles if they are active
        if obstacle_flag == 1:
            reset_obstacles()

        # Update the score display
        pen.clear()
        pen.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level), align="center", font=("Courier", 14, "normal"))

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot
        x = random.randint(-290, 290)
        y = random.randint(-240, 240)  # Adjust so food doesn't overlap with the panel
        food.goto(x, y)

        # Add a segment to the snake's body
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#808080")
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay (increases the snake's speed)
        delay -= 0.001

        # Increase the score
        score += 10

        # Update the high score if necessary
        if score > high_score:
            high_score = score

        # Update the score display
        pen.clear()
        pen.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level), align="center", font=("Courier", 14, "normal"))

        # Check for level-up
        check_level_up()

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for collisions between the head and the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)

            # Clear the segments list
            segments.clear()

            # Reset the score and level
            score = 0
            level = 1
            score_to_next_level = 50  # Reset the level-up threshold
            delay = 0.1

            # Reset obstacles if they are active
            if obstacle_flag == 1:
                reset_obstacles()

            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}  Level: {}".format(score, high_score, level), align="center", font=("Courier", 14, "normal"))

    time.sleep(delay)

wn.mainloop()
