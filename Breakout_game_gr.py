from graphics import Canvas
import time
import random

BRICK_WIDTH = 40
BRICK_THICKNESS = 10
GAP = 4
BRICK_NUMBER = 10
PADDLE_WIDTH = 1.8 * BRICK_WIDTH
PADDLE_THICKNESS  = 1.2 * BRICK_THICKNESS
CANVAS_WIDTH = BRICK_WIDTH * BRICK_NUMBER + GAP * (BRICK_NUMBER-1)
CANVAS_HEIGHT = 400
BALL_DIAMETER = 20 # must set <=20, otherwise won't fall to ground
INITIAL_VELOCITY = 5
#START_X = CANVAS_WIDTH / 2
#START_Y = CANVAS_HEIGHT /2
START_X = CANVAS_WIDTH / 2 - BALL_DIAMETER / 2
START_Y = CANVAS_HEIGHT - 2* PADDLE_THICKNESS - BALL_DIAMETER
DELAY = 0.01

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    paddle = draw_paddle(canvas, CANVAS_WIDTH /2 - PADDLE_WIDTH / 2, CANVAS_HEIGHT - 2* PADDLE_THICKNESS,"black")

    bricks = draw_wall(canvas)
    
    x_velocity = INITIAL_VELOCITY
    y_velocity = INITIAL_VELOCITY
    ball_x = START_X
    ball_y = START_Y
    ball = canvas.create_oval(ball_x, ball_y,
                              ball_x + BALL_DIAMETER,
                              ball_y + BALL_DIAMETER,
                              'blue')

    prompt = canvas.create_text(CANVAS_WIDTH/2-30, CANVAS_HEIGHT /2, "Click to start...", "c", "#0000FF")
    canvas.wait_for_click()
    canvas.delete(prompt)
    count = 1

    while True: #define bounce behaviour
        mouse_x = canvas.get_mouse_x()
        paddle_x = mouse_x
        paddle_y = CANVAS_HEIGHT - 2* BRICK_THICKNESS
        canvas.moveto(paddle, paddle_x, paddle_y)
        
        touch_side = check_collision(canvas, ball, bricks) 
        
        if (ball_x < 0) or (ball_x + BALL_DIAMETER >= CANVAS_WIDTH) or (touch_side =="left_touch") or \
            (touch_side =="right_touch"):
            x_velocity = -x_velocity
        if (ball_y < 0) or (ball_y + BALL_DIAMETER >= CANVAS_HEIGHT) or (touch_side =="bottom_touch") or \
            (touch_side == "top_touch"):
            y_velocity = -y_velocity
        if (touch_side == "paddle_touch"):
            y_velocity = abs(y_velocity)
        ball_x -= x_velocity
        ball_y -= y_velocity
        #print(ball_x,ball_y,touch_side)
        canvas.moveto(ball, ball_x, ball_y)
        canvas.update()
        time.sleep(DELAY)

        #if ball fall below the paddle
        if (ball_y > CANVAS_HEIGHT - 2* BRICK_THICKNESS):
            count += 1
            prompt = canvas.create_text(CANVAS_WIDTH/2-30, CANVAS_HEIGHT /2, "Click to continue...","c", "#0000FF")
            canvas.wait_for_click()
            canvas.delete(prompt)
            canvas.delete(ball)
            x_velocity = INITIAL_VELOCITY
            y_velocity = INITIAL_VELOCITY            
            ball_x =START_X
            ball_y =START_Y
            ball = canvas.create_oval(ball_x, ball_y, ball_x + \
                    BALL_DIAMETER, ball_y + BALL_DIAMETER,'blue')
            
        #when bricks list is empty    
        if len(bricks) == 0: 
            prompt = canvas.create_text(CANVAS_WIDTH/2-100, CANVAS_HEIGHT /2, "You won with "+ str(count) +" attempts", "c", "#FF0000")
            canvas.delete(ball)
            canvas.delete(paddle)
            break
        #canvas.update()
    canvas.mainloop()
	
def check_collision(canvas, ball, bricks):  #finding touching rectangles
    ball_left_x = canvas.get_left_x(ball)
    ball_top_y = canvas.get_top_y(ball)
    ball_right_x = canvas.get_left_x(ball) + BALL_DIAMETER
    ball_bottom_y = canvas.get_top_y(ball) + BALL_DIAMETER
    ball_center_x = canvas.get_left_x(ball) + BALL_DIAMETER / 2
    ball_center_y = canvas.get_top_y(ball) + BALL_DIAMETER / 2
    # Calculate the bounding box around the ball
    ball_bbox = (ball_left_x, ball_top_y, ball_right_x, ball_bottom_y)
    
    # Find all the objects (rectangles) that overlap with the ball's bounding box
    overlapping_objects = canvas.find_overlapping(*ball_bbox)
    
    for brick in overlapping_objects: 
        #print (brick)
        if brick != ball and brick in bricks: #overlappig object is in bricks list and not the ball itself
            brick_left_x = canvas.get_left_x(brick)
            brick_top_y = canvas.get_top_y(brick)
            brick_right_x = canvas.get_left_x(brick) + BRICK_WIDTH
            brick_bottom_y = canvas.get_top_y(brick) + BRICK_THICKNESS
            if ball_center_x >= brick_left_x and ball_center_x <= brick_right_x and \
               ball_center_y >= brick_top_y and ball_center_y <= brick_bottom_y:
                #print("Ball and rectangle are touching!")
                canvas.delete(brick)
                bricks.remove(brick)      
      
                # Compare the distances between the ball and the rectangle's sides
                dist_left = ball_center_x - brick_left_x
                dist_right = brick_right_x - ball_center_x
                dist_top = ball_center_y - brick_top_y
                dist_bottom = brick_bottom_y - ball_center_y
            
                min_dist = min(dist_left, dist_right, dist_top, dist_bottom)
            
                if min_dist == dist_left:
                    return "left_touch"
                    #print("Ball touched left side of the rectangle.")
                elif min_dist == dist_right:
                    return "right_touch"
                    #print("Ball touched right side of the rectangle.")
                elif min_dist == dist_top:
                    return "top_touch"
                    #print("Ball touched top side of the rectangle.")
                else:
                    return "bottom_touch"
                    #print("Ball touched bottom side of the rectangle.")
        elif(brick == ball): #only ball is present in the ball box, no need to handle
            return "no_touch"
        else:
            return "paddle_touch"   #not determine which sides to touch for paddle

    
'''
    #this full iteration code has very low performance!
    for brick in bricks:
        brick_left_x = canvas.get_left_x(brick)
        brick_top_y = canvas.get_top_y(brick)
        
        # Calculate the closest x-coordinate to the ball's center within the rectangle
        closest_x = max(brick_left_x, min(ball_center_x, brick_left_x+BRICK_WIDTH))
        
        # Calculate the closest y-coordinate to the ball's center within the rectangle
        closest_y = max(brick_top_y, min(ball_center_y, brick_top_y+BRICK_THICKNESS))
        
        # Calculate the distance between the ball's center and the closest point within the rectangle
        distance = ((closest_x - ball_center_x) ** 2 + (closest_y - ball_center_y) ** 2) ** 0.5
        
        # Check if the distance is less than or equal to the sum of the ball's radius and half the rectangle's width
        if distance <= BALL_DIAMETER/2:
            canvas.delete(brick)
            bricks.remove(brick)
'''
'''
def draw_ball(canvas,x0,y0):
    ball = canvas.create_oval(x0, y0, x0+BALL_DIAMETER, y0+BALL_DIAMETER,"blue")
    return ball
'''

def draw_wall(canvas):
    bricks = []
    for i in range(4):
        start_x = 0
        start_y = i * 2* (BRICK_THICKNESS+ GAP)
        color = generate_random_color()
        #print(color)
        #color = "blue"
        for i in range(BRICK_NUMBER):
            start_x = i * (BRICK_WIDTH + GAP)
            brick = draw_brick(canvas, start_x, start_y, color)
            bricks.append(brick)
            brick = draw_brick(canvas, start_x, start_y + BRICK_THICKNESS + GAP,color)
            bricks.append(brick)
    return bricks

    
def draw_brick(canvas,start_x,start_y,color):
    brick = canvas.create_rectangle(start_x,start_y,start_x+BRICK_WIDTH,start_y+BRICK_THICKNESS,color)
    return brick


def draw_paddle(canvas,start_x,start_y,color):
    paddle = canvas.create_rectangle(start_x,start_y,start_x+PADDLE_WIDTH,start_y+ PADDLE_THICKNESS,color)
    return paddle


def generate_random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color_string = f"RGB({red}, {green}, {blue})"
    color_hex = f"#{red:02x}{green:02x}{blue:02x}"
    return color_hex
    # Generate a random color
    #random_color = generate_random_color()

main()

#if __name__ == '__main__':
#    main()
