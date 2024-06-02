import turtle

# 큐브 한 면의 크기
CUBE_SIZE = 100

# 큐브 한 면에 있는 작은 조각의 크기
PIECE_SIZE = CUBE_SIZE / 3

# 큐브 한 면의 색상
COLORS = ['red', 'green', 'blue', 'orange', 'yellow', 'white']

def draw_square(color):
    turtle.begin_fill()
    turtle.fillcolor(color)
    for _ in range(4):
        turtle.forward(PIECE_SIZE)
        turtle.right(90)
    turtle.end_fill()

def draw_cube():
    # 시작 위치로 이동
    turtle.penup()
    turtle.goto(-CUBE_SIZE / 2, CUBE_SIZE / 2)
    turtle.pendown()
    
    # 큐브 그리기
    for _ in range(4):
        for _ in range(3):
            draw_square('black')
            turtle.forward(PIECE_SIZE)
        turtle.backward(3 * PIECE_SIZE)
        turtle.right(90)
        turtle.forward(PIECE_SIZE)
        turtle.left(90)
    turtle.hideturtle()

def color_cube(colors):
    # 시작 위치로 이동
    turtle.penup()
    turtle.goto(-CUBE_SIZE / 2, CUBE_SIZE / 2)
    turtle.pendown()
    
    # 큐브에 색상 채우기
    for color in colors:
        draw_square(color)
        turtle.forward(PIECE_SIZE)
        if turtle.xcor() >= CUBE_SIZE / 2:
            turtle.backward(CUBE_SIZE)
            turtle.right(90)
            turtle.forward(PIECE_SIZE)
            turtle.left(90)
        elif turtle.xcor() < -CUBE_SIZE / 2:
            turtle.backward(CUBE_SIZE)
            turtle.left(90)
            turtle.forward(PIECE_SIZE)
            turtle.right(90)

# 루빅스 큐브 그리기
draw_cube()

# 큐브에 색상 채우기
# 아래 예제에서 COLORS 리스트에 원하는 색상을 지정하여 큐브를 색칠할 수 있습니다.
color_cube(COLORS)

# 클릭 시 종료
turtle.exitonclick()