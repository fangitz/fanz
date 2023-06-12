import time
import tkinter as tk

BALL_SIZE = 50
CANVAS_WIDTH = 550
CANVAS_HEIGHT = 450
DELAY = 0.001        # seconds to wait between each update
START_X = 0
START_Y = 0

def main():
    # setup
    window = tk.Tk()
    canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()
    #canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    ball = canvas.create_oval(START_X, START_Y, BALL_SIZE, BALL_SIZE, fill="blue")
    change_x = 1
    change_y = 1
    cur_x = START_X
    cur_y = START_Y

    # animation loop
    while True: 
        # change direction if ball reaches an edge
        if cur_x < 0 or cur_x + BALL_SIZE >= CANVAS_WIDTH:
            change_x = -change_x
            
        if cur_y < 0 or cur_y + BALL_SIZE >= CANVAS_HEIGHT:
            change_y = -change_y
            
        # update the ball
        canvas.move(ball, change_x, change_y)
        cur_x += change_x
        cur_y += change_y
        # update the window
        window.update()    
        # pause
        time.sleep(DELAY)
    
main()
'''If the window.mainloop() call is greyed out in your code editor (such as in VS Code), 
it typically indicates that the line is unreachable or unnecessary in the current context.
In this updated version, the window.mainloop() call is placed after the main() function. 
The main() function is executed first to set up the animation loop, and then the Tkinter 
event loop is started using tk.mainloop(). This allows the window to remain open and 
respond to user events until it is manually closed.'''
tk.mainloop()

