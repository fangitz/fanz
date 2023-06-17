import time
import tkinter as tk
import random
import math
from tkinter import messagebox

GRID_SIZE = 4
RECT_SIZE = 120
GAP = 20
CANVAS_WIDTH = RECT_SIZE * GRID_SIZE + GAP * (GRID_SIZE+1)
CANVAS_HEIGHT = RECT_SIZE * GRID_SIZE + GAP * (GRID_SIZE+1)
FLAG_2048 = False
DELAY = 4  # Delay between consecutive animation steps in milliseconds
# ANIMATION_DURATION = 200  # Duration of each animation step in milliseconds
# DELAY1 = 0.1

COLORS = ['GREY', '#CC99FF', 'Light Salmon', 'Light Coral', 'Light Pink', 'Orchid', 'Medium Purple',
          'Dark Orchid', 'Medium Blue', 'Dodger Blue', 'Royal Blue']
# COLORS = ['Pale Goldenrod','#F2D7AD', '#F4D6A3', '#F8D19B', '#F6CC9E', '#F8C78E', '#F7C075', '#F5B866', '#F9B256', '#FAB442', '#F9A534',
#           '#F8A02E', '#FF9933', '#FF8C00',  '#FF7F50', '#FF7256', '#FF6347', '#FF5733', '#FF4500', '#FF4000', '#FF3300']

def main():
    window = tk.Tk()
    window.title('2048 by jaz')
    canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()

    # Create lists for rects and labels
    # grid_rect = [[] for _ in range(GRID_SIZE)]
    # grid_label = [[] for _ in range(GRID_SIZE)]
    grid_rect = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    grid_label = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # create a list to store all tile values (labels)
    grid_value = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]

    draw_bg(canvas)

    initialize(canvas, grid_value, grid_rect, grid_label)

    while True:
        # bind the key press event to move the rectangle
        # use the lambda function in line, to wrap the move_group function and pass additional parameters 
        window.bind("<Key>", lambda event: move_tiles(event, canvas, grid_value, grid_rect, grid_label))
        # set the focus to the window so that it can receive key events
        window.focus_set()  

        # if there is no movable tiles in the grid, prompt to retry or quit the game
        if (is_grid_movable_down(grid_value) == False and is_grid_movable_up(grid_value) == False and
            is_grid_movable_left(grid_value) == False and is_grid_movable_right(grid_value) == False):
            msg = messagebox.askquestion("2048", "No Movable Tiles! Do you want to play again?", icon= 'warning')
            if msg == "yes":
                window.destroy()
                main()
            elif msg == "no":
                quit()
            break

        print('value: ', grid_value,'\n', 'rect: ', grid_rect,'\n', 'label: ', grid_label)

        # update the window
        window.update()    
        # time.sleep(DELAY1)

'''
The animate_item() function calculates the step size for each animation step based on the desired duration and delay. 
It recursively calls itself with the updated position until the animation is complete.
'''
def animate_move(canvas, item, offset_x_ini, offset_y_ini, offset_x, offset_y, steps=10):
    # calculate every step
    # paras offset_x_ini = offset_x, it is for a passed-in constant only
    step_x = offset_x_ini / steps
    step_y = offset_y_ini / steps
    # move the item by a step towards the target position
    canvas.move(item, step_x, step_y)
    offset_x -= step_x
    offset_y -= step_y
    # check if the item has reached the target position
    if (offset_x, offset_y) != (0, 0):
        # call back animate_move() to schedule the next animation step after a short delay
        canvas.after(DELAY, animate_move, canvas, item, offset_x_ini, offset_y_ini, offset_x, offset_y)


def get_max_value(grid_value):
    # get the max value in the grid
    # check if 2048 is reached
    global FLAG_2048
    max_value = float('-inf')  # initialize max_value with negative infinity
    for row in grid_value:
        for value in row:
            if value > max_value:
                max_value = value
            if max_value == 2048 and not FLAG_2048:
                messagebox.showinfo(title="2048", message="Congratulations. You reached 2048!")
                FLAG_2048 = True
    return max_value


def move_tiles(event, canvas, grid_value, grid_rect, grid_label):
    # 'move' tiles by key press return. the logic is...
    # <1> calculate the target position and its label value AFTER a move by compress/merge/compress the value list, update the list
    # <2> move the tile to target position, update the tile list (rect+label) to keep consistent with value list
    # <3> to place a number in a random position
    # paras: event to trigger moves, 
           # canvas for graphics operation, 
           # grid_value for storing value of numbers, 
           # grid_label for storing numbers, 
           # grid_rect for storing physical tiles
    if event.keysym == "Up":
        if(is_grid_movable_up(grid_value)):
            move_up(canvas, grid_value, grid_rect, grid_label)
            place_number(canvas, grid_value, grid_rect, grid_label)
    elif event.keysym == "Down":
        if(is_grid_movable_down(grid_value)):
            move_down(canvas, grid_value, grid_rect, grid_label)
            place_number(canvas, grid_value, grid_rect, grid_label)
    elif event.keysym == "Left":
        if(is_grid_movable_left(grid_value)):
            move_left(canvas, grid_value, grid_rect, grid_label)
            place_number(canvas, grid_value, grid_rect, grid_label)
    elif event.keysym == "Right":
        if(is_grid_movable_right(grid_value)):
            move_right(canvas, grid_value, grid_rect, grid_label)
            place_number(canvas, grid_value, grid_rect, grid_label)

def is_grid_movable_left(grid_value):
    # iterate over each tile in the grid
    for row in grid_value:  # iterate over each row
        for col in range(1, len(row)):  # starts from 1 (2nd col) to compare with the left adjacent tile, and iterates towards right
            tile_value = row[col]
            # check if there is an empty space or a tile with the same value to the left
            if tile_value != 0 and (row[col-1] == 0 or row[col-1] == tile_value):
                return True
    return False

def is_grid_movable_right(grid_value):
    for row in grid_value:
        for i in range(GRID_SIZE - 1):
            if row[i] != 0 and (row[i+1] == 0 or row[i] == row[i+1]):
                return True
    return False

def is_grid_movable_up(grid_value):
    for col in range(GRID_SIZE):    #iterate over each column
        for i in range(1, GRID_SIZE):   #range start from 1 (second row) and downwards
            if grid_value[i][col] != 0 and (grid_value[i-1][col] == 0 or grid_value[i][col] == grid_value[i-1][col]):
                return True
    return False

def is_grid_movable_down(grid_value):
    for col in range(GRID_SIZE):
        for row in range(GRID_SIZE - 2, -1, -1):    #starting from the second-to-last row and moving upwards
            if grid_value[row][col] != 0:
                if grid_value[row+1][col] == 0 or grid_value[row+1][col] == grid_value[row][col]:
                    return True
    return False


def move_left(canvas, grid_value, grid_rect, grid_label):
    # move the tiles to the left
    # move_left is the primary function which other movement (right, up, down) based upon
    if is_grid_movable_left(grid_value):
        for i, row_value in enumerate(grid_value):    #row is the nested lists inside the grid list
            row_rect = grid_rect[i]
            row_label = grid_label[i]
            # compress the row by merging adjacent tiles
            compress_row_left(canvas, row_value, row_rect, row_label)
            # merge the tiles with the same value
            merge_row_left(canvas, row_value, row_rect, row_label)
            # compress the row again to fill any gaps created by merging
            compress_row_left(canvas, row_value, row_rect, row_label)
        # return grid_value, grid_rect, grid_label

def compress_row_left(canvas, row_value, row_rect, row_label):
    # helper function to compress a row by moving all non-zero tiles to the left
    # paras: row as grid_value's inner list
    # create a new list to store the compressed row
    # move the compressed tile to target position
    new_row_value = [0] * GRID_SIZE
    index = 0
    for j in range(GRID_SIZE):
        if row_value[j] != 0:
            new_row_value[index] = row_value[j]
        # tile move happens in this compress process, move to the empty tile
        # the tile is moved only if its current position (j) is different from the target position (index)
            if j != index:
                x_offset = -(j - index) * (RECT_SIZE + GAP)
                y_offset = 0
                # animate the move
                animate_move(canvas, row_rect[j], x_offset, y_offset, x_offset, y_offset)
                animate_move(canvas, row_label[j], x_offset, y_offset, x_offset, y_offset)
                # canvas.move(row_rect[j], x_offset, y_offset)
                # canvas.move(row_label[j], x_offset, y_offset)
                row_rect[index] = row_rect[j]
                row_label[index] = row_label[j]
                row_rect[j] = None
                row_label[j] = None
                # row_rect[j], row_rect[index] = row_rect[index], row_rect[j]
                # row_label[j], row_label[index] = row_label[index], row_label[j]
            index += 1
    # update the original row with the compressed row
    row_value[:] = new_row_value

def merge_row_left(canvas, row_value, row_rect, row_label):
    # helper function to merge adjacent tiles with the same value in a row
    # tile move also happens here, move to the merged tile position which is to the immeidate left 
    # update the row_rect and row_label lists
    for j in range(GRID_SIZE - 1):  # minus 1 to avoid out-of-range
        if row_value[j] == row_value[j + 1] and row_value[j] != 0:
            row_value[j] *= 2
            row_value[j + 1] = 0

            canvas.delete(row_rect[j], row_label[j])
            x_offset = -(RECT_SIZE+GAP)
            y_offset = 0
            animate_move(canvas, row_rect[j+1], x_offset, y_offset, x_offset, y_offset)
            animate_move(canvas, row_label[j+1], x_offset, y_offset, x_offset, y_offset)
            # canvas.move(row_rect[j+1], -(RECT_SIZE+GAP), 0)
            # canvas.move(row_label[j+1], -(RECT_SIZE+GAP), 0)
            row_rect[j] = row_rect[j+1]
            row_label[j] = row_label[j+1]
            row_rect[j+1] = None
            row_label[j+1] = None
            # row_rect[j], row_rect[j + 1] = row_rect[j + 1], row_rect[j]
            # row_label[j], row_label[j + 1] = row_label[j + 1], row_label[j]
            render_tile(canvas, row_value[j], row_rect[j], row_label[j])
            

def move_right(canvas, grid_value, grid_rect, grid_label):
    if is_grid_movable_right(grid_value):
        for i, row_value in enumerate(grid_value):
            row_rect = grid_rect[i]
            row_label = grid_label[i]
            compress_row_right(canvas, row_value, row_rect, row_label)
            merge_row_right(canvas, row_value, row_rect, row_label)
            compress_row_right(canvas, row_value, row_rect, row_label)

def compress_row_right(canvas, row_value, row_rect, row_label):
    new_row_value = [0] * GRID_SIZE
    index = GRID_SIZE - 1
    for j in range(GRID_SIZE - 1, -1, -1):  #loop from 3 to 0 (-1 exclusive)
        if row_value[j] != 0:
            new_row_value[index] = row_value[j]
            if j != index:
                x_offset = -(j - index) * (RECT_SIZE + GAP)
                y_offset = 0
                animate_move(canvas, row_rect[j], x_offset, y_offset, x_offset, y_offset)
                animate_move(canvas, row_label[j], x_offset, y_offset, x_offset, y_offset)
                # canvas.move(row_rect[j], x_offset, 0)
                # canvas.move(row_label[j], x_offset, 0)
                row_rect[index] = row_rect[j]
                row_label[index] = row_label[j]
                row_rect[j] = None
                row_label[j] = None
            index -= 1
    row_value[:] = new_row_value

def merge_row_right(canvas, row_value, row_rect, row_label):
    for j in range(GRID_SIZE - 1, 0, -1): #loop from 3 to 1 (0 exclusive)
        if row_value[j] == row_value[j - 1] and row_value[j] != 0:
            row_value[j] *= 2
            row_value[j - 1] = 0
            canvas.delete(row_rect[j], row_label[j])
            x_offset = RECT_SIZE+GAP
            y_offset = 0
            animate_move(canvas, row_rect[j-1], x_offset, y_offset, x_offset, y_offset)
            animate_move(canvas, row_label[j-1], x_offset, y_offset, x_offset, y_offset)
            # canvas.move(row_rect[j - 1], RECT_SIZE + GAP, 0)
            # canvas.move(row_label[j - 1], RECT_SIZE + GAP, 0)
            row_rect[j] = row_rect[j - 1]
            row_label[j] = row_label[j - 1]
            row_rect[j - 1] = None
            row_label[j - 1] = None
            render_tile(canvas, row_value[j], row_rect[j], row_label[j])


def move_up(canvas, grid_value, grid_rect, grid_label):
    if is_grid_movable_up(grid_value):
        for j in range(GRID_SIZE):
            column_value = [grid_value[i][j] for i in range(GRID_SIZE)]
            column_rect = [grid_rect[i][j] for i in range(GRID_SIZE)]
            column_label = [grid_label[i][j] for i in range(GRID_SIZE)]
            compress_column_up(canvas, column_value, column_rect, column_label)
            merge_column_up(canvas, column_value, column_rect, column_label)
            compress_column_up(canvas, column_value, column_rect, column_label)
            for i in range(GRID_SIZE):
                grid_value[i][j] = column_value[i]
                grid_rect[i][j] = column_rect[i]
                grid_label[i][j] = column_label[i]

def move_down(canvas, grid_value, grid_rect, grid_label):
    if is_grid_movable_down(grid_value):
        for j in range(GRID_SIZE):
            column_value = [grid_value[i][j] for i in range(GRID_SIZE - 1, -1, -1)]
            column_rect = [grid_rect[i][j] for i in range(GRID_SIZE - 1, -1, -1)]
            column_label = [grid_label[i][j] for i in range(GRID_SIZE - 1, -1, -1)]
            compress_column_down(canvas, column_value, column_rect, column_label)
            merge_column_down(canvas, column_value, column_rect, column_label)
            compress_column_down(canvas, column_value, column_rect, column_label)
            for i in range(GRID_SIZE):
                grid_value[i][j] = column_value[GRID_SIZE - 1 - i]
                grid_rect[i][j] = column_rect[GRID_SIZE - 1 - i]
                grid_label[i][j] = column_label[GRID_SIZE - 1 - i]

def compress_column_up(canvas, column_value, column_rect, column_label):
    new_column_value = [0] * GRID_SIZE
    index = 0
    for i in range(GRID_SIZE):
        if column_value[i] != 0:
            new_column_value[index] = column_value[i]
            if i != index:
                x_offset = 0
                y_offset = -(i - index) * (RECT_SIZE + GAP)
                animate_move(canvas, column_rect[i], x_offset, y_offset, x_offset, y_offset)
                animate_move(canvas, column_label[i], x_offset, y_offset, x_offset, y_offset)
                # canvas.move(column_rect[i], 0, y_offset)
                # canvas.move(column_label[i], 0, y_offset)
                column_rect[index] = column_rect[i]
                column_label[index] = column_label[i]
                column_rect[i] = None
                column_label[i] = None
            index += 1
    column_value[:] = new_column_value

def merge_column_up(canvas, column_value, column_rect, column_label):
    for i in range(GRID_SIZE - 1):
        if column_value[i] == column_value[i + 1] and column_value[i] != 0:
            column_value[i] *= 2
            column_value[i + 1] = 0
            canvas.delete(column_rect[i], column_label[i])
            x_offset = 0
            y_offset = -(RECT_SIZE + GAP)
            animate_move(canvas, column_rect[i+1], x_offset, y_offset, x_offset, y_offset)
            animate_move(canvas, column_label[i+1], x_offset, y_offset, x_offset, y_offset)
            # canvas.move(column_rect[i + 1], 0, -(RECT_SIZE + GAP))
            # canvas.move(column_label[i + 1], 0, -(RECT_SIZE + GAP))
            column_rect[i] = column_rect[i + 1]
            column_label[i] = column_label[i + 1]
            column_rect[i + 1] = None
            column_label[i + 1] = None
            render_tile(canvas, column_value[i], column_rect[i], column_label[i])

def compress_column_down(canvas, column_value, column_rect, column_label):
    new_column_value = [0] * GRID_SIZE
    index = 0
    for i in range(GRID_SIZE):
        if column_value[i] != 0:
            new_column_value[index] = column_value[i]
            if i != index:
                x_offset = 0
                y_offset = (i - index) * (RECT_SIZE + GAP)
                animate_move(canvas, column_rect[i], x_offset, y_offset, x_offset, y_offset)
                animate_move(canvas, column_label[i], x_offset, y_offset, x_offset, y_offset)
                # canvas.move(column_rect[i], 0, y_offset)
                # canvas.move(column_label[i], 0, y_offset)
                column_rect[index] = column_rect[i]
                column_label[index] = column_label[i]
                column_rect[i] = None
                column_label[i] = None
            index += 1
    column_value[:] = new_column_value

def merge_column_down(canvas, column_value, column_rect, column_label):
    for i in range(GRID_SIZE - 1):
        if column_value[i] == column_value[i + 1] and column_value[i] != 0:
            column_value[i] *= 2
            column_value[i + 1] = 0
            canvas.delete(column_rect[i], column_label[i])
            x_offset = 0
            y_offset = RECT_SIZE + GAP
            animate_move(canvas, column_rect[i+1], x_offset, y_offset, x_offset, y_offset)
            animate_move(canvas, column_label[i+1], x_offset, y_offset, x_offset, y_offset)
            # canvas.move(column_rect[i + 1], 0, (RECT_SIZE + GAP))
            # canvas.move(column_label[i + 1], 0, (RECT_SIZE + GAP))
            column_rect[i] = column_rect[i + 1]
            column_label[i] = column_label[i + 1]
            column_rect[i + 1] = None
            column_label[i + 1] = None
            render_tile(canvas, column_value[i], column_rect[i], column_label[i])

def initialize(canvas, grid_value, grid_rect, grid_label):
    # randomly place two lables on grid at the beginning of the game
    for i in range(2):
        place_number(canvas, grid_value, grid_rect, grid_label)


def place_number(canvas, grid_value, grid_rect, grid_label):
    # randomly place a number (label) with a movable key press
    max_value =get_max_value(grid_value)
    if max_value < 512: # when max in grid value > 512, put random value 2 or 4
        num = 2
    else:
        num =random.choice([2, 4])

    # create random indice for the list to place a tile in
    while True:
        i = random.randint(0,GRID_SIZE-1)
        j = random.randint(0,GRID_SIZE-1)

        # place a tile in an empty position
        if grid_value[i][j] == 0 and grid_rect[i][j] == None and grid_label[i][j] == None:
            grid_value[i][j] = num    #assign num to grid_value and pass it to create tile
            create_tile(canvas, i, j, grid_value, grid_rect, grid_label)
            break
    # print(grid_value)

def render_tile(canvas, value, rect, label):
    #render tile when the value changes due to merge
    num = value
    n = int(math.log2(num)-1)
    if n > 10:  #if the value is > 2048, color remain unchanged
        n = 10 
    color = COLORS[n]
    canvas.itemconfig(rect, fill=color)
    canvas.itemconfig(label, text=num)
    if n > 9:  #if the value >512, the font size changed to smaller one
        canvas.itemconfig(label, font=('Arial', 24, 'bold'))


def create_tile(canvas, i, j, grid_value, grid_rect, grid_label):
    # create tiles based on the passed-in grid value
    # THE RECT AND LABEL LISTS i&j ALWAYS KEEP CONSISTENT WITH VALUE LIST
    x = GAP + j * (RECT_SIZE + GAP)
    y = GAP + i * (RECT_SIZE+ GAP)
    num = grid_value[i][j]
    n = int(math.log2(num)-1)
    if n > 10:  #if the value is > 2048, color remain unchanged
        n = 10 
    color = COLORS[n]
    rect_id = draw_rect(canvas, x, y, color)
    label_id = draw_label(canvas, x, y, num)
    grid_rect[i][j] = rect_id
    grid_label[i][j] =label_id
    # canvas.itemconfig(grid_rect[i][j], fill=(COLORS[n]))
    if n > 9:  #if the value >512, the font size changed to smaller one
        canvas.itemconfig(label_id, font=('Arial', 24, 'bold'))


def draw_bg(canvas):
    # draw the background grid with rects and labels
    color = 'lightgrey'
    for i in range(GRID_SIZE):
        start_y = GAP + i * (RECT_SIZE+ GAP)
        for j in range(GRID_SIZE):
            start_x = GAP + j * (RECT_SIZE + GAP)
            draw_rect(canvas, start_x, start_y, color)
            draw_label(canvas, start_x, start_y, "")


def draw_rect(canvas,start_x,start_y,color):
    # draw one tile
    rect_id = canvas.create_rectangle(start_x, start_y, start_x+RECT_SIZE, start_y+RECT_SIZE, fill = color, outline="", width=0)
    return rect_id


def draw_label(canvas, start_x, start_y, num):
    # draw a lable (the number) on a tile
    label_id = canvas.create_text(start_x + RECT_SIZE/2, start_y + RECT_SIZE/2, text=num, fill="white", font=("Arial", 36, 'bold'), anchor="center")
    return label_id


main()
tk.mainloop()


'''
X0 = GAP
Y0 = GAP
X1 = GAP + (RECT_SIZE + GAP)
Y1 = GAP + (RECT_SIZE + GAP)
X2 = GAP + 2 * (RECT_SIZE + GAP)
Y2 = GAP + 2 * (RECT_SIZE + GAP)
X3 = GAP + 3 * (RECT_SIZE + GAP)
Y3 = GAP + 3 * (RECT_SIZE + GAP)
# list of rect coords (tuple)
GRID_COORDS = [
[(X0, Y0), (X1, Y0), (X2, Y0), (X3, Y0)],
[(X0, Y1), (X1, Y1), (X2, Y1), (X3, Y1)],
[(X0, Y2), (X1, Y2), (X2, Y2), (X3, Y2)],
[(X0, Y3), (X1, Y3), (X2, Y3), (X3, Y3)]
    ]

# if check_2048(grid_value): #break the while loop if 2048 is reached
#     break

def check_2048(grid_value):
    # check if 2048 is reached
    max_value = get_max_value(grid_value)
    if max_value == 2048:
        messagebox.showinfo(title="2048", message="Congratulations. You reached 2048!")
        return True

def create_tiles(canvas, grid_value, grid_rect, grid_label):
    # create tiles based on the passed-in grid value
    # THE RECT AND LABEL LISTS i&j ALWAYS KEEP CONSISTENT WITH VALUE LIST
    for rowidx, row in enumerate(grid_value):   #enumerate outer list to retrieve both idex and content(inner list)
        i = rowidx
        row_rect = grid_rect[i]
        row_label = grid_label[i]
        for j in range(GRID_SIZE):
            x = GAP + j * (RECT_SIZE + GAP)
            y = GAP + i * (RECT_SIZE+ GAP)
            if row[j] != 0: #if the current tile has a value
                n = int(math.log2(row[j])-1)
                if n > 10:  #if the value is > 2048, color remain unchanged
                    n = 10 
                color = COLORS[n]
                rect_id = draw_rect(canvas, x, y, color)
                row_rect[j] = rect_id
                label_id = draw_label(canvas, x, y, row[j])
                row_label[j] =label_id
                # canvas.itemconfig(grid_rect[i][j], fill=(COLORS[n]))
                if n > 9:  #if the value >512, the font changed to smaller one
                    canvas.itemconfig(row_label, font=('Arial', 24, 'bold'))
            # else:
            #     canvas.itemconfig(grid_rect[i][j], fill="lightgrey")
            #     canvas.itemconfig(grid_label[i][j], text = "")

def draw_bg(canvas, grid_rect, grid_label):
    # draw the tile grid with rects and labels
    # add the rects and labels to the grid_rect and grid_label lists
    color = 'lightgrey'
    for i in range(GRID_SIZE):
        start_y = GAP + i * (RECT_SIZE+ GAP)
        row_rect = grid_rect[i]
        row_label = grid_label[i]

        for j in range(GRID_SIZE):
            start_x = GAP + j * (RECT_SIZE + GAP)
            rect_id = draw_rect(canvas, start_x, start_y, color)
            label_id = draw_label(canvas, start_x, start_y)
            row_rect.append(rect_id)
            row_label.append(label_id)
    return grid_rect, grid_label

def create_tile(canvas, i, j):
    # create a combination of rect and label based on the grid_value(i,j) list
    x = GAP + j * (RECT_SIZE + GAP)
    y = GAP + i * (RECT_SIZE+ GAP)
    rect = canvas.create_rectangle(x, y, x+RECT_SIZE, y+RECT_SIZE, fill="grey", outline="", width=0)
    label = canvas.create_text(x + RECT_SIZE/2, y + RECT_SIZE/2, text=num, fill="white", font=("Arial", 36), anchor="center")
    return rect, label
'''

'''def move_down(grid): 
    # another way to implement tile movement. This function iterates over each column of the board from bottom to top.
    # It checks if the current tile in a row is equal to the tile above it and merges them if they are. 
    # If a merge occurs, the merged flag is set to True to prevent multiple merges in a single move. 
    # If the current tile is empty (0), it swaps it with the tile above it. This process is repeated for each column, 
    # resulting in a downward movement of tiles.
    for col in range(GRID_SIZE):
        merged = False
        for row in range(GRID_SIZE - 1, 0, -1):
            if grid[row][col] == grid[row-1][col] and not merged:
                grid[row][col] *= 2
                grid[row-1][col] = 0
                merged = True
            elif grid[row][col] == 0:
                grid[row][col] = grid[row-1][col]
                grid[row-1][col] = 0

def move_up(canvas, grid_value, grid_rect, grid_label):
    for j, row_value in enumerate(grid_value):
        row_rect = grid_rect[j]
        row_label = grid_label[j]
        # extract the column items using list comprehension
        row_value = [row_value[j] for row_value in grid_value]
        row_rect = [row_rect[j] for row_rect in grid_rect]
        row_label = [row_label[j] for row_label in grid_label]
        # move the column to the left
        move_left(canvas, grid_value, grid_rect, grid_label)
        # update the grid with the moved column values
        for row_idx, row_value in enumerate(grid_value):
            row_value[j] = row_value[row_idx]
            row_label[j] = row_label[row_idx]
            row_rect[j] = row_rect[row_idx]
    # return grid_value, grid_rect, grid_label

def move_down(canvas, grid_value, grid_rect, grid_label):
    for j, row_value in enumerate(grid_value):
        row_rect = grid_rect[j]
        row_label = grid_label[j]
        # extract the column items using list comprehension
        row_value = [row_value[j] for row_value in grid_value]
        row_rect = [row_rect[j] for row_rect in grid_rect]
        row_label = [row_label[j] for row_label in grid_label]
        # reverse the column values to simulate moving down
        row_value.reverse()
        row_rect.reverse()
        row_label.reverse()
        # move the column to the left
        move_left(canvas, grid_value, grid_rect, grid_label)
        # reverse the column values back to their original order
        row_value.reverse()
        row_rect.reverse()
        row_label.reverse()
        # update the grid with the moved column values
        for row_idx, row_value in enumerate(grid_value):
            row_value[j] = row_value[row_idx]
            row_label[j] = row_label[row_idx]
            row_rect[j] = row_rect[row_idx]
    # return grid_value, grid_rect, grid_label
                                
# def move_right(canvas, grid_value, grid_rect, grid_label):
#     for i, row_value in enumerate(grid_value):
#         row_rect = grid_rect[i]
#         row_label = grid_label[i]
#         # reverse the row
#         row_value.reverse()
#         row_rect.reverse()
#         row_label.reverse()
#         # move the reversed row to the left
#         move_left(canvas, grid_value, grid_rect, grid_label)
#         # reverse the row again to restore its original order
#         row_value.reverse()
#         row_rect.reverse()
#         row_label.reverse()
#     # return grid_value, grid_rect, grid_label

def create_tile(canvas, x, y, num):
    # Create a frame as a container
    # frame = tk.Frame(canvas, width=RECT_SIZE, height=RECT_SIZE)
    # # Create a rectangle inside the frame
    # rect = canvas.create_rectangle(x, y, x+RECT_SIZE, y+RECT_SIZE, fill="grey", outline="", width=0)
    # # Create a text label inside the frame
    # label = tk.Label(frame, text=label, fg="white", font=("Arial", 36), anchor="center", bg="grey")
    # label.pack(fill="both", expand=True)
    # # Place the frame on the canvas
    # group = canvas.create_window(x+RECT_SIZE/2, y+RECT_SIZE/2, anchor="center", window=frame)
    # group = canvas.addtag_withtag("group", rect)
    # canvas.addtag_withtag("group", label)
    rect = canvas.create_rectangle(x, y, x+RECT_SIZE, y+RECT_SIZE, fill="grey", outline="", width=0)
    label = canvas.create_text(x + RECT_SIZE/2, y + RECT_SIZE/2, text=num, fill="white", font=("Arial", 36), anchor="center")
    return rect, label

def reset_canvas(canvas, grid_rect, grid_label):
    canvas.delete("all")
    draw_bg(canvas, grid_rect, grid_label)
'''