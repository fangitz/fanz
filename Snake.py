from graphics import Canvas
import time
import random
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SIZE = 20
SNAKE_COLOR = "green"
HEAD_OUTLINE_COLOR = "black"
TAIL_OUTLINE_COLOR = "white"
GOAL_COLOR = "pink"
OBSTACLE_COLOR = "black"

# if you make this larger, the game will go slower
DELAY = 0.2 

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    #goal = canvas.create_rectangle(360, 360, 360 + SIZE, 360 + SIZE, "pink")
    goal = None
    goal = set_goal(canvas, goal)
    
    obstacles =[]
    obstacle = None
    
    snakes = []
    snake = canvas.create_rectangle(0, 0, SIZE, SIZE, SNAKE_COLOR)
    snakes.append(snake)
    canvas.set_outline_color(snake, HEAD_OUTLINE_COLOR)
    
    move_snake(canvas, snakes, goal, obstacle, obstacles)

def move_snake(canvas, snakes, goal, obstacle, obstacles):
    #move snake by a key press, 'this library is buggy with continuous key pressing'
    snake = snakes[0]   #initialize it
    snake_x = canvas.get_left_x(snake)
    snake_y = canvas.get_top_y(snake)
    count = 0
    delay = DELAY
    last_key = "ArrowRight"
    text = canvas.create_text(10, CANVAS_HEIGHT-15, font=('Arial', 12), anchor = "w",text="Score: "+ str(count), color = "blue")
       
    while True:
        key = canvas.get_last_key_press()

        if count != 0 and ( ( key == "ArrowLeft" and last_key == "ArrowRight" ) or ( key == "ArrowRight" and last_key == "ArrowLeft" ) or ( key == "ArrowUp" and last_key == "ArrowDown" ) or ( key == "ArrowDown" and last_key == "ArrowUp" ) ):
            key = None  #disable reverse move
            
        if key == None: #if no key pressed, follow the last key's direction
            key = last_key
        
        if key == "ArrowLeft":
            last_key = "ArrowLeft"
            snake_x -= SIZE
        elif key == "ArrowRight":
            last_key = "ArrowRight"
            snake_x += SIZE
        elif key == "ArrowUp":
            last_key = "ArrowUp"
            snake_y -= SIZE
        elif key == "ArrowDown":
            last_key = "ArrowDown"
            snake_y += SIZE
        
        '''
        #snake_position = {}
        #snake_position = {shape_0: [snake_x0, snake_y0, snake_x, snake_y]}
        #snake head's original poistion become the tailing snake's target position
        for snake in snakes:
            canvas.moveto(snake, snake_x, snake_y)
            snake_x = snake_x_0
            snake_y = snake_y_0
        #snake_position[snake] = [snake_x0, snake_y0, snake_x, snake_y]
        '''
        
        
        #delete the original and create a new snake head in the 'moveto' position (function same as moveto)
        #set the old head's outline white
        canvas.set_outline_color(snakes[-1], TAIL_OUTLINE_COLOR)
        #delete the snake tail which is snakes[0] and remove it from the snakes list
        canvas.delete(snakes[0])
        snakes.remove(snakes[0])
        
        #create a new snake head and set its outline black and append it to the snakes list
        snake = canvas.create_rectangle(snake_x, snake_y, snake_x+SIZE, snake_y+SIZE, SNAKE_COLOR)
        canvas.set_outline_color(snake, HEAD_OUTLINE_COLOR)
        snakes.append(snake)
        

        collision_result = check_collision(canvas, snake, snakes, goal, obstacle, obstacles)
        #if the goal is hit, score 1, set a new goal and create a new snake head
        if (collision_result =="hit_goal"): 
            #if the last snake goes up, x_new=snake_x, y_new=snake_y+SIZE
            #if the last snake goes down, x_new=snake_x, y_new=snake_y-SIZE
            #if the last snake goes left, x_new=snake_x+SIZE, y_new=snake_y
            #if the last snake goes right, x_new=snake_x-SIZE, y_new=snake_y
            
            #if hit the goal, create a new snake head and put it in snakes list
            snake = canvas.create_rectangle(snake_x, snake_y, snake_x+SIZE, snake_y+SIZE, SNAKE_COLOR)
            canvas.set_outline_color(snake, HEAD_OUTLINE_COLOR)
            snakes.append(snake)
            print("after collision: ", snakes, snake[0], snake)

            goal = set_goal(canvas, goal)
            count += 1
            if (count % 5 == 0):
                delay -= 0.01
                #set an obstacle after hit the goal
                obstacle = set_obstacle(canvas, obstacle)
                obstacles.append(obstacle)
                
                obstacle_x = canvas.get_left_x(obstacle)
                obstacle_y = canvas.get_top_y(obstacle)
                goal_x = canvas.get_left_x(goal)
                goal_y = canvas.get_top_y(goal)
                
                #(exclude the existing obstacles or )if obstacle is in same position as goal, reset it
                while (obstacle_x == goal_x and obstacle_y == goal_y):   
                    canvas.delete(obstacle) #delete newly added obstacle
                    obstacles.remove(obstacles[-1])
                    obstacle = set_obstacle(canvas, obstacle)
                    obstacles.append(obstacle)
            
            canvas.change_text(text, "Score: "+ str(count))
        
        #if hit the boundary or hit itslef or the obstacle, game over    
        elif collision_result == "hit_bound" or collision_result== "hit_self_obs":
            canvas.create_text(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, font='Arial', font_size = 18, text="Game Over", color = "blue", anchor = "center")
            break

        '''
        else:
            #set the old head's outline white
            canvas.set_outline_color(snakes[-1], 'white')
            #delete the snake tail which is snakes[0]
            canvas.delete(snakes[0])
            snakes.remove(snakes[0])
            #create a new snake head and set its outline black
            snake = canvas.create_rectangle(snake_x, snake_y, snake_x+SIZE, snake_y+SIZE, SNAKE_COLOR)
            canvas.set_outline_color(snake, 'black')
            snakes.append(snake)
        '''
        #canvas.update()  #need to call it for local machines at the bottom of the while loop before the sleep function
        time.sleep(delay)
        
def check_collision(canvas, snake, snakes, goal, obstacle, obstacles):
    #check if snake goes beyond the bound
    #check if snake hits the goal - in same position
    snake_x = canvas.get_left_x(snake)
    snake_y = canvas.get_top_y(snake)
    snake_box = (snake_x, snake_y, snake_x + SIZE, snake_y + SIZE)
    goal_x = canvas.get_left_x(goal)
    goal_y = canvas.get_top_y(goal)
    
    overlapping_objects = canvas.find_overlapping(*snake_box)
    
    #if the object in overlapping tuple isn't snake head itself and it is in the snakes list
    #or it is in obstacles list, true to hit itself or obstacle
    for object in overlapping_objects:
        if (object != snake and object in snakes) or object in obstacles:
            print("overlapping: ",snakes)
            return "hit_self_obs"
    
    if (snake_x < 0 or snake_x > CANVAS_WIDTH -SIZE or snake_y < 0 or snake_y > CANVAS_HEIGHT -SIZE):
        return "hit_bound"
        
    if (snake_x == goal_x and snake_y == goal_y):
        canvas.delete(goal)
        return "hit_goal"
    
def set_goal(canvas, goal):
    #position goal to the random position in mulitiplies of 20 pixcel
    goal_x = random.randint (0, CANVAS_WIDTH / 20 - 1) * 20
    goal_y = random.randint (0, CANVAS_HEIGHT / 20 - 1) * 20
    goal = canvas.create_rectangle(goal_x, goal_y, goal_x+SIZE, goal_y+SIZE, GOAL_COLOR)
    return goal

def set_obstacle(canvas, obstacle):
    #set an obstacle to a random position
    obstacle_x = random.randint (0, CANVAS_WIDTH / 20 - 1) * 20
    obstacle_y = random.randint (0, CANVAS_HEIGHT / 20 - 1) * 20
    obstacle = canvas.create_rectangle(obstacle_x, obstacle_y, obstacle_x+SIZE, obstacle_y+SIZE, OBSTACLE_COLOR)
    return obstacle

if __name__ == '__main__':
    main()
    