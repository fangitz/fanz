import tkinter as tk

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 300
current_index = 0 #define global variable outside the canvas.bind on_click loop

def main():
    #create the main window
    window = tk.Tk()

    #create the canvas widget
    canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()

    draw_japan_flag(canvas)
    #canvas.wait_for_click() #this method not in tk library

    #bind the click event to canvas, use lambda function to pass both "event" and "canvas"
    canvas.bind("<Button-1>", lambda event : on_click(event, canvas)) 
    
    '''By adding root.mainloop() at the end of the code, the event loop is started, 
    and the window will stay open until you manually close it. 
    This allows you to see the line displayed within the IDE.'''
    window.mainloop()

def on_click(event, canvas): #get the mouse click event with mouse coords
    #demo for mouse coords
    x = event.x
    y = event.y
    print(x,y)

    global current_index

    functions = [
        lambda: draw_bangladesh_flag(canvas), 
        lambda: draw_pulau_flag(canvas), 
        lambda: draw_georgia_flag(canvas)
        ]

    # Get the current function from the list
    current_function = functions[current_index]
    # Execute the current function
    current_function()
    # Move to the next function in the list
    current_index += 1
    if current_index >= len(functions):
        current_index = 0


def draw_japan_flag(canvas):
    draw_circle(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, 120, 'red')

def draw_bangladesh_flag(canvas):
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill='darkgreen')
    draw_circle(canvas, CANVAS_WIDTH * 0.4, CANVAS_HEIGHT / 2, 150, 'red')

def draw_pulau_flag(canvas):
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill='dodgerblue')
    draw_circle(canvas, CANVAS_WIDTH * 0.4, CANVAS_HEIGHT / 2, 150, 'yellow')

def draw_circle(canvas, center_x, center_y, size, color):
    """
    draw a circle on the given canvas. Centered at the given location, in
    the given color
    """
    left_x = center_x - size / 2
    top_y = center_y - size / 2
    right_x = left_x + size
    bottom_y = top_y + size
    canvas.create_oval(left_x, top_y, right_x, bottom_y, fill=color)

def draw_georgia_flag(canvas):
    canvas.delete("all")
    # some calculations for where the pluses go!
    x_left = CANVAS_WIDTH * 1 / 4
    x_right = CANVAS_WIDTH * 3 / 4
    y_top = CANVAS_HEIGHT * 1 / 4
    y_bottom = CANVAS_HEIGHT * 3 / 4

    # four calls to draw_plus
    draw_plus(canvas, x_left - 20, y_top - 20, x_left + 20, y_top + 20, 10)
    draw_plus(canvas, x_right - 20, y_top - 20, x_right + 20, y_top + 20, 10)
    draw_plus(canvas, x_left - 20, y_bottom - 20, x_left + 20, y_bottom + 20, 10)
    draw_plus(canvas, x_right - 20, y_bottom - 20, x_right + 20, y_bottom + 20, 10)

    # big background plus
    draw_plus(canvas, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 30)

def draw_plus(canvas, x_1, y_1, x_2, y_2, width):
    """
    Draws a plus which is inscribed in the rectangle defined by the two
    points (x_1, y_1) and (x_2, y_2). The thickness of each arm of the plus
    is also passed in as a parameter
    """
    # compute the middle of the plus
    mid_x = x_1 + (x_2 - x_1) / 2
    mid_y = y_1 + (y_2 - y_1) / 2

    # half an arm thickness
    half = width / 2

    # create the two rectangles
    canvas.create_rectangle(x_1, mid_y - half, x_2, mid_y + half, fill='red')
    canvas.create_rectangle(mid_x - half, y_1, mid_x + half, y_2, fill='red')

main()