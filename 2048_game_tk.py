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
    grid_rect = [[] for _ in range(GRID_SIZE)]
    grid_label = [[] for _ in range(GRID_SIZE)]

    # create a list to store all tile values (labels)
    grid_value = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
    ]

    draw_bg(canvas, grid_rect, grid_label)

    initialize(canvas, grid_value, grid_rect, grid_label)

    while True:
        # Bind the key press event to move the rectangle
        # use the lambda function in line, to wrap the move_group function and pass additional parameters 
        window.bind("<Key>", lambda event: move_tiles(event, canvas, grid_value, grid_rect, grid_label))
        # Set the focus to the window so that it can receive key events
        window.focus_set()  

        if check_2048(grid_value):
            break

        if (is_grid_movable_down(grid_value) == False and is_grid_movable_up(grid_value) == False and
            is_grid_movable_left(grid_value) == False and is_grid_movable_right(grid_value) == False):
                messagebox.showinfo(title="2048", message="No Movable Tiles. Game Over!")
                break
                # window.destroy()

        print(grid_value)
        # update the window
        window.update()    
        time.sleep(DELAY)


def get_max_value(grid_value):
    max_value = float('-inf')  # Initialize max_value with negative infinity
    for row in grid_value:
        for value in row:
            if value > max_value:
                max_value = value
    return max_value


# Function to check if 2048 is reached
def check_2048(grid_value):
    for row in grid_value:
        for value in row:
            if value == 2048:
                messagebox.showinfo(title="2048", message="Congratulations! You reached 2048!")
                return True

def move_tiles(event, canvas, grid_value, grid_rect, grid_label):

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
    # Iterate over each tile in the grid
    for row in grid_value:  #iterate over each row
        for col in range(1, len(row)):  #starts from 1 (2nd column) to compare with the left adjacent tile, and iterates towards right
            tile_value = row[col]
            # Check if there is an empty space or a tile with the same value to the left
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

#check if the grip is filled
# def is_grid_full(grid_value):
#     for row in grid_value:
#         for value in row:
#             if value == 0:
#                 return False  # Grid is not full, an empty tile is found
#     return True  # Grid is full, all tiles are filled


# Function to move the tiles to the left
def move_left(grid_value):
    if is_grid_movable_left(grid_value):
        for row in grid_value:    #row is the nested lists inside the grid list
            # Compress the row by merging adjacent tiles
            compress_row(row)

            # Merge the tiles with the same value
            merge_row(row)

            # Compress the row again to fill any gaps created by merging
            compress_row(row)
        return grid_value

# Helper function to compress a row by moving all non-zero tiles to the left
def compress_row(row):
    # Create a new list to store the compressed row
    # tile movement only happens in this compress process
    new_row = [0] * GRID_SIZE
    index = 0
    for tile in row:
        if tile != 0:
            new_row[index] = tile
            index += 1
        # elif row[i+1] != 0 and row[i] == 0: #if compressable, move to (x,y), but the bg tile will be moved in this case
        #     canvas.move(grid_rect[i][j], x, y)
        #     canvas.label(grid_label[i][j], x, y)
                        
    # Update the original row with the compressed row
    row[:] = new_row

# Helper function to merge adjacent tiles with the same value in a row
def merge_row(row):
    for i in range(GRID_SIZE - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0

def move_right(grid_value):
    for row in grid_value:
        # Reverse the row
        row.reverse()
        # Move the reversed row to the left
        move_left([row])
        # Reverse the row again to restore its original order
        row.reverse()
    return grid_value

def move_up(grid_value):
    for col in range(GRID_SIZE):
        # Extract the column values using list comprehension
        column = [row[col] for row in grid_value]
        # Move the column to the left
        move_left([column])
        # Update the grid with the moved column values
        for row_idx, row in enumerate(grid_value):
            row[col] = column[row_idx]
    return grid_value

def move_down(grid_value):
    for col in range(GRID_SIZE):
        # Extract the column values
        column = [row[col] for row in grid_value]
        # Reverse the column values to simulate moving down
        column.reverse()
        # Move the column to the left
        move_left([column])
        # Reverse the column values back to their original order
        column.reverse()
        # Update the grid with the moved column values
        for row_idx, row in enumerate(grid_value):
            row[col] = column[row_idx]
    return grid_value


def initialize(canvas, grid_value, grid_rect, grid_label):
    # randomly put two lables on grid
    for i in range(2):
        place_number(canvas, grid_value, grid_rect, grid_label)

def place_number(canvas, grid_value, grid_rect, grid_label):
    # when max in grid value > 32, put random value 2 or 4
    max_value =get_max_value(grid_value)
    if max_value < 512:
        num = 2
    else:
        num =random.choice([2, 4])

    # create random coords to place a tile in
    while True:
        i = random.randint(0,GRID_SIZE-1)
        j = random.randint(0,GRID_SIZE-1)

        # place a tile if no value found on this random position
        if grid_value[i][j] == 0:
            grid_value[i][j] = num    #assign num to grid_value
            render_grid(canvas, grid_value, grid_rect, grid_label)
            break
    # print(grid_value)


def render_grid(canvas, grid_value, grid_rect, grid_label):
    #render the grid based on the retrieved grid values
    for rowidx, row in enumerate(grid_value):   #enumerate outer list to retrieve both idex and content(inner list)
        i = rowidx
        for j in range(GRID_SIZE):
            if row[j] != 0: #if the current tile has a value
                n = int(math.log2(row[j])-1)
                if n > 11:  #if the value is > 2056, color remain unchanged
                    n = 11
                canvas.itemconfig(grid_rect[i][j], fill=(COLORS[n]))
                if n <= 9:  
                    canvas.itemconfig(grid_label[i][j], font=('Arial', 36, 'bold'),text = row[j])
                else:   #if the value >512, the font changed to smaller one
                    canvas.itemconfig(grid_label[i][j], font=('Arial', 24, 'bold'),text = row[j])
            else:
                canvas.itemconfig(grid_rect[i][j], fill="lightgrey")
                canvas.itemconfig(grid_label[i][j], text = "")


def reset_canvas(canvas, grid_rect, grid_label):
    canvas.delete("all")
    draw_bg(canvas, grid_rect, grid_label)

def draw_bg(canvas, grid_rect, grid_label):
    # draw background grid
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
    #draw one square
    rect_id = canvas.create_rectangle(start_x, start_y, start_x+RECT_SIZE, start_y+RECT_SIZE, fill = color, outline="", width=0)
    return rect_id

def draw_label(canvas, start_x, start_y):
    label_id = canvas.create_text(start_x + RECT_SIZE/2, start_y + RECT_SIZE/2, text='', fill="white", font=("Arial", 36), anchor="center")
    return label_id

main()
tk.mainloop()

