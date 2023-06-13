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
DELAY = 0.2
FLAG_2048 = False


COLORS = ['GREY', '#CC99FF', 'Light Salmon', 'Light Coral', 'Light Pink', 'Orchid', 'Medium Purple',
          'Dark Orchid', 'Medium Blue', 'Dodger Blue', 'Royal Blue']

def main():
    window = tk.Tk()
    window.title('2048 by jaz')
    canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()

    # create lists for tiles: rects and labels
    grid_rect = [[] for _ in range(GRID_SIZE)]
    grid_label = [[] for _ in range(GRID_SIZE)]

    # create a list to store all tile values (labels)
    grid_value = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]

    # draw background grid
    draw_bg(canvas, grid_rect, grid_label)

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

        print(grid_value)

        # update the window
        window.update()    
        time.sleep(DELAY)


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
    # 'move' tiles by key press return. it is not a physical move. the logic here is:
    # <1> to calculate the target position AFTER a move and its number value by compress/merge/compress-again process
    # <2> to render the canvas
    # <3> to place a number in a random position
    # paras: event to trigger moves, 
           # canvas for graphics op, 
           # grid_value for storing value of numbers, 
           # grid_label for storing numbers, 
           # grid_rect for storing physical tiles
    if event.keysym == "Up":
        if(is_grid_movable_up(grid_value)):
            move_up(grid_value)
            render_grid(canvas, grid_value, grid_rect, grid_label)
            place_number(canvas, grid_value, grid_rect, grid_label)
    elif event.keysym == "Down":
        if(is_grid_movable_down(grid_value)):
            move_down(grid_value)
            render_grid(canvas, grid_value, grid_rect, grid_label)
            place_number(canvas, grid_value, grid_rect, grid_label)
    elif event.keysym == "Left":
        if(is_grid_movable_left(grid_value)):
            move_left(grid_value)
            render_grid(canvas, grid_value, grid_rect, grid_label)
            place_number(canvas, grid_value, grid_rect, grid_label)
    elif event.keysym == "Right":
        if(is_grid_movable_right(grid_value)):
            move_right(grid_value)
            render_grid(canvas, grid_value, grid_rect, grid_label)
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


def move_left(grid_value):
    # move the tiles to the left
    # move_left is the primary function which other movement (right, up, down) based upon
    if is_grid_movable_left(grid_value):
        for row in grid_value:    #row is the nested lists inside the grid list
            # compress the row by merging adjacent tiles
            compress_row(row)
            # merge the tiles with the same value
            merge_row(row)
            # compress the row again to fill any gaps created by merging
            compress_row(row)
        return grid_value

def compress_row(row):
    # helper function to compress a row by moving all non-zero tiles to the left
    # paras: row as grid_value's inner list
    # create a new list to store the compressed row
    new_row = [0] * GRID_SIZE
    index = 0
    for tile in row:
        if tile != 0:
            new_row[index] = tile
            index += 1
        # tile movement only happens in this compress process
        # elif row[i+1] != 0 and row[i] == 0: #if compressable, move to (x,y), but the bg tile will be moved in this case
        #     canvas.move(grid_rect[i][j], x, y)
        #     canvas.label(grid_label[i][j], x, y)
    # update the original row with the compressed row
    row[:] = new_row

def merge_row(row):
    # helper function to merge adjacent tiles with the same value in a row
    for i in range(GRID_SIZE - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0

def move_right(grid_value):
    for row in grid_value:
        # reverse the row
        row.reverse()
        # move the reversed row to the left
        move_left([row])
        # reverse the row again to restore its original order
        row.reverse()
    return grid_value

def move_up(grid_value):
    for col in range(GRID_SIZE):
        # extract the column values using list comprehension
        column = [row[col] for row in grid_value]
        # move the column to the left
        move_left([column])
        # update the grid with the moved column values
        for row_idx, row in enumerate(grid_value):
            row[col] = column[row_idx]
    return grid_value

def move_down(grid_value):
    for col in range(GRID_SIZE):
        # extract the column values
        column = [row[col] for row in grid_value]
        # reverse the column values to simulate moving down
        column.reverse()
        # move the column to the left
        move_left([column])
        # reverse the column values back to their original order
        column.reverse()
        # update the grid with the moved column values
        for row_idx, row in enumerate(grid_value):
            row[col] = column[row_idx]
    return grid_value


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

        # place a tile if no value found on this random position
        if grid_value[i][j] == 0:
            grid_value[i][j] = num    #assign num to grid_value and pass it to render_grid
            render_grid(canvas, grid_value, grid_rect, grid_label)
            break
    # print(grid_value)


def render_grid(canvas, grid_value, grid_rect, grid_label):
    # render the grid based on the retrieved grid values, using itemconfig to fill the color of the tile and set the label value and font
    for rowidx, row in enumerate(grid_value):   #enumerate outer list to retrieve both idex and content(inner list)
        i = rowidx
        for j in range(GRID_SIZE):
            if row[j] != 0: #if the current tile has a value
                n = int(math.log2(row[j])-1)
                if n > 11:  #if the value is > 2056, color remain unchanged
                    n = 11
                canvas.itemconfig(grid_rect[i][j], fill=(COLORS[n]))
                if n <= 9:  #if the value >512, the font changed to smaller one
                    canvas.itemconfig(grid_label[i][j], font=('Arial', 36, 'bold'),text = row[j])
                else:   
                    canvas.itemconfig(grid_label[i][j], font=('Arial', 24, 'bold'),text = row[j])
            else:
                canvas.itemconfig(grid_rect[i][j], fill="lightgrey")
                canvas.itemconfig(grid_label[i][j], text = "")


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


def draw_rect(canvas,start_x,start_y,color):
    # draw one tile
    rect_id = canvas.create_rectangle(start_x, start_y, start_x+RECT_SIZE, start_y+RECT_SIZE, fill = color, outline="", width=0)
    return rect_id


def draw_label(canvas, start_x, start_y):
    # draw a lable (the number) on a tile
    label_id = canvas.create_text(start_x + RECT_SIZE/2, start_y + RECT_SIZE/2, text='', fill="white", font=("Arial", 36), anchor="center")
    return label_id

main()
tk.mainloop()
