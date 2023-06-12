from graphics import Canvas
import time
import math
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
CENTER_RADIUS = CANVAS_WIDTH / 15    #center hole size
GAP_NUMBERS = 22
GAP_SIZE = 4
INCLINE_DEGREE =25 #inclining degree of four outside lines in upper and lower sides
LENGTH = GAP_NUMBERS * GAP_SIZE
A_RADIANS = math.radians(INCLINE_DEGREE)
COLOR1 = "#48ABAB" #greenish
COLOR2 = "#CCABAB" #pinkish

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    line_color = "red"
    
    # draw background grey square
    draw_background(canvas)
    
    #draw background black diamond
    draw_diamond(canvas)
    

    #line 1 coordinates. 
    x0_l1 = CANVAS_WIDTH / 4
    y0_l1 = CANVAS_HEIGHT / 4
    x1_l1 = CANVAS_WIDTH / 4 + LENGTH * math.cos(A_RADIANS)
    y1_l1 = CANVAS_HEIGHT /4 - LENGTH * math.sin(A_RADIANS)
    
    #line 2 coodinates. indexing counterclock wise
    x0_l2 = CANVAS_WIDTH /6
    y0_l2 = CANVAS_WIDTH / 2 - LENGTH/2
    x1_l2 = CANVAS_WIDTH /6
    y1_l2 = CANVAS_WIDTH / 2 +LENGTH /2
    
    #radial line 1 coordinates
    x0_r1 = CANVAS_WIDTH / 2
    y0_r1 = CANVAS_HEIGHT /2 - CENTER_RADIUS - LENGTH
    x1_r1 = CANVAS_WIDTH /2
    y1_r1 = CANVAS_HEIGHT /2 - CENTER_RADIUS

    #radial line 2 coodinates
    x0_r2 = CANVAS_WIDTH /2 - (LENGTH+CENTER_RADIUS) * math.cos(math.radians(30))
    y0_r2 = CANVAS_HEIGHT /2 - (LENGTH+CENTER_RADIUS) * math.sin(math.radians(30))
    x1_r2 = CANVAS_WIDTH /2 - CENTER_RADIUS * math.cos(math.radians(30))
    y1_r2 = CANVAS_HEIGHT /2 - CENTER_RADIUS * math.sin(math.radians(30))    
    
    #radial line 3 coodinates
    x0_r3 = CANVAS_WIDTH /2 - (LENGTH+CENTER_RADIUS) * math.cos(math.radians(30))
    y0_r3 = CANVAS_HEIGHT /2 + (LENGTH+CENTER_RADIUS) * math.sin(math.radians(30))
    x1_r3 = CANVAS_WIDTH /2 - CENTER_RADIUS * math.cos(math.radians(30))
    y1_r3 = CANVAS_HEIGHT /2 + CENTER_RADIUS * math.sin(math.radians(30)) 
    
    #line 3 coordinates. 
    x0_l3 = CANVAS_WIDTH / 4
    y0_l3 = CANVAS_HEIGHT *3 / 4
    x1_l3 = CANVAS_WIDTH / 4 + LENGTH * math.cos(A_RADIANS)
    y1_l3 = CANVAS_HEIGHT *3 /4 + LENGTH * math.sin(A_RADIANS)
    
    #radial line 4 coordinates
    x0_r4 = CANVAS_WIDTH / 2
    y0_r4 = CANVAS_HEIGHT /2 + CENTER_RADIUS
    x1_r4 = CANVAS_WIDTH / 2
    y1_r4 = CANVAS_HEIGHT /2 + CENTER_RADIUS + LENGTH
    
    #line 4 coordinates
    x0_l4 = CANVAS_WIDTH *3 / 4 - LENGTH * math.cos(A_RADIANS)
    y0_l4 = CANVAS_HEIGHT *3 / 4 + LENGTH * math.sin(A_RADIANS)
    x1_l4 = CANVAS_WIDTH *3 /4
    y1_l4 = CANVAS_HEIGHT *3 /4
    
    #radial line 5 coodinates
    x0_r5 = CANVAS_WIDTH /2 + (LENGTH+CENTER_RADIUS) * math.cos(math.radians(30))
    y0_r5 = CANVAS_HEIGHT /2 + (LENGTH+CENTER_RADIUS) * math.sin(math.radians(30))
    x1_r5 = CANVAS_WIDTH /2 + CENTER_RADIUS * math.cos(math.radians(30))
    y1_r5 = CANVAS_HEIGHT /2 + CENTER_RADIUS * math.sin(math.radians(30)) 
    
    #line 5 coodinates
    x0_l5 = CANVAS_WIDTH *5 /6
    y0_l5 = CANVAS_WIDTH / 2 + LENGTH/2
    x1_l5 = CANVAS_WIDTH *5 /6
    y1_l5 = CANVAS_WIDTH / 2 - LENGTH /2    
    
    #radial line 6 coodinates
    x0_r6 = CANVAS_WIDTH /2 + (LENGTH+CENTER_RADIUS) * math.cos(math.radians(30))
    y0_r6 = CANVAS_HEIGHT /2 - (LENGTH+CENTER_RADIUS) * math.sin(math.radians(30))
    x1_r6 = CANVAS_WIDTH /2 + CENTER_RADIUS * math.cos(math.radians(30))
    y1_r6 = CANVAS_HEIGHT /2 - CENTER_RADIUS * math.sin(math.radians(30)) 
    
    #line 6 coordinates. 
    x0_l6 = CANVAS_WIDTH *3 / 4
    y0_l6 = CANVAS_HEIGHT / 4
    x1_l6 = CANVAS_WIDTH *3 / 4 - LENGTH * math.cos(A_RADIANS)
    y1_l6 = CANVAS_HEIGHT /4 - LENGTH * math.sin(A_RADIANS)
 
   
    #draw strings connecting outside lines (line1 x0 -- radial1 x0)
    canvas.create_line(x0_l1,y0_l1,x1_l1,y1_l1,line_color)
    canvas.create_line(x0_r1,y0_r1,x1_r1,y1_r1,line_color)
    draw_strings_outside(canvas,x0_l1,y0_l1,x1_l1,y1_l1,x0_r1,y0_r1,x1_r1,y1_r1,COLOR2)
    
    #draw strings connecting outside lines (line1 x0 -- radial2 x1)
    #draw_strings_outside2(canvas,x0_l1,y0_l1,x1_l1,y1_l1,x0_r2,y0_r2,x1_r2,y1_r2)
    canvas.create_line(x0_r2,y0_r2,x1_r2,y1_r2,line_color)
    draw_strings_outside(canvas,x0_l1,y0_l1,x1_l1,y1_l1,x1_r2,y1_r2,x0_r2,y0_r2,COLOR1)
    
    #draw strings connecting radial lines (radial1 x0 -- radial2 x1), 
    #the end of r1_x0 color is COLOR1
    draw_strings_inside(canvas,x0_r1,y0_r1,x1_r1,y1_r1,x1_r2,y1_r2,x0_r2,y0_r2,COLOR1)

    #draw strings connecting outside lines (line2 x0 -- radial2 x1)
    canvas.create_line(x0_l2,y0_l2,x1_l2,y1_l2,line_color)
    draw_strings_outside(canvas,x0_l2,y0_l2,x1_l2,y1_l2,x1_r2,y1_r2,x0_r2,y0_r2,COLOR1)
    
    #draw strings connecting outside lines (line2 x0 -- radial3 x0)
    canvas.create_line(x0_r3,y0_r3,x1_r3,y1_r3,line_color)
    draw_strings_outside(canvas,x0_l2,y0_l2,x1_l2,y1_l2,x0_r3,y0_r3,x1_r3,y1_r3,COLOR2)

    #draw strings connecting radial lines (radial2 x0 -- radial3 x1)
    draw_strings_inside(canvas,x0_r2,y0_r2,x1_r2,y1_r2,x1_r3,y1_r3,x0_r3,y0_r3,COLOR2)

    #draw strings connecting outside lines (line3 x0 -- radial3 x1)
    canvas.create_line(x0_l3,y0_l3,x1_l3,y1_l3,line_color)
    draw_strings_outside(canvas,x0_l3,y0_l3,x1_l3,y1_l3,x1_r3,y1_r3,x0_r3,y0_r3,COLOR2)
    
    #draw strings connecting outside lines (line3 x0 -- radial4 x0)
    canvas.create_line(x0_r4,y0_r4,x1_r4,y1_r4,line_color)
    draw_strings_outside(canvas,x0_l3,y0_l3,x1_l3,y1_l3,x1_r4,y1_r4,x0_r4,y0_r4,COLOR1)

    #draw strings connecting radial lines (radial3 x0 -- radial4 x1)
    draw_strings_inside(canvas,x0_r3,y0_r3,x1_r3,y1_r3,x0_r4,y0_r4,x1_r4,y1_r4,COLOR1)

    #draw strings connecting outside lines (line4 x0 -- radial4 x1)
    canvas.create_line(x0_l4,y0_l4,x1_l4,y1_l4,line_color)    
    draw_strings_outside(canvas,x0_l4,y0_l4,x1_l4,y1_l4,x0_r4,y0_r4,x1_r4,y1_r4,COLOR1)

    #draw strings connecting outside lines (line4 x0 -- radial5 x0)
    canvas.create_line(x0_r5,y0_r5,x1_r5,y1_r5,line_color)
    draw_strings_outside(canvas,x0_l4,y0_l4,x1_l4,y1_l4,x0_r5,y0_r5,x1_r5,y1_r5,COLOR2)
    
    #draw strings connecting radial lines (radial4 x0 -- radial5 x1)
    draw_strings_inside(canvas,x0_r4,y0_r4,x1_r4,y1_r4,x0_r5,y0_r5,x1_r5,y1_r5,COLOR1)

    #draw strings connecting outside lines (line5 x0 -- radial5 x1)
    canvas.create_line(x0_l5,y0_l5,x1_l5,y1_l5,line_color)
    draw_strings_outside(canvas,x0_l5,y0_l5,x1_l5,y1_l5,x1_r5,y1_r5,x0_r5,y0_r5,COLOR2)
    
    #draw strings connecting outside lines (line5 x0 -- radial6 x0)
    canvas.create_line(x0_r6,y0_r6,x1_r6,y1_r6,line_color)
    draw_strings_outside(canvas,x0_l5,y0_l5,x1_l5,y1_l5,x0_r6,y0_r6,x1_r6,y1_r6,COLOR1)

    #draw strings connecting radial lines (radial5 x0 -- radial6 x1)
    draw_strings_inside(canvas,x0_r5,y0_r5,x1_r5,y1_r5,x1_r6,y1_r6,x0_r6,y0_r6,COLOR1)
    
    #draw strings connecting outside lines (line6 x0 -- radial6 x1)
    canvas.create_line(x0_l6,y0_l6,x1_l6,y1_l6,line_color)
    draw_strings_outside(canvas,x0_l6,y0_l6,x1_l6,y1_l6,x1_r6,y1_r6,x0_r6,y0_r6,COLOR1)
    
    #draw strings connecting outside lines (line6 x0 -- radial1 x0)
    draw_strings_outside(canvas,x0_l6,y0_l6,x1_l6,y1_l6,x0_r1,y0_r1,x1_r1,y1_r1,COLOR2)

    #draw strings connecting radial lines (radial6 x0 -- radial1 x1)
    draw_strings_inside(canvas,x0_r6,y0_r6,x1_r6,y1_r6,x1_r1,y1_r1,x0_r1,y0_r1,COLOR2)
    
    '''
    #canvas.create_line(x0_l1,y0_l1,x1_l1,y1_l1,line_color)
    canvas.create_line(x0_r1,y0_r1,x1_r1,y1_r1,line_color)
    #canvas.create_line(x0_l2,y0_l2,x1_l2,y1_l2,line_color)
    canvas.create_line(x0_r2,y0_r2,x1_r2,y1_r2,line_color)
    #canvas.create_line(x0_l3,y0_l3,x1_l3,y1_l3,line_color)
    canvas.create_line(x0_r3,y0_r3,x1_r3,y1_r3,line_color) 
    #canvas.create_line(x0_l4,y0_l4,x1_l4,y1_l4,line_color)
    canvas.create_line(x0_r4,y0_r4,x1_r4,y1_r4,line_color)
    #canvas.create_line(x0_l5,y0_l5,x1_l5,y1_l5,line_color)
    canvas.create_line(x0_r5,y0_r5,x1_r5,y1_r5,line_color)
    #canvas.create_line(x0_l6,y0_l6,x1_l6,y1_l6,line_color)  
    canvas.create_line(x0_r6,y0_r6,x1_r6,y1_r6,line_color)
    '''
    canvas.mainloop()

    
def draw_background(canvas):
    x0 =0
    y0 =0
    x1 = CANVAS_WIDTH
    y1 = CANVAS_HEIGHT
    canvas.create_rectangle(x0,y0,x1,y1,"grey")

def draw_diamond(canvas):
    #draw balck diamond by continuous lines
    x0 =0
    y0 = CANVAS_HEIGHT /2
    x1 = CANVAS_WIDTH /2
    y1 = 0
    
    while (y0 <= CANVAS_HEIGHT or x0 <= CANVAS_WIDTH/2):
        canvas.create_line(x0,y0,x1,y1,"black")
        x0 +=1
        y0 +=1
        x1 +=1
        y1 +=1
        #time.sleep(0.001)

def draw_strings_outside(canvas,x0_l,y0_l,x1_l,y1_l,x0_r,y0_r,x1_r,y1_r,color):
    #draw strings between outside line and radial line
    #same one color in full length at one side
    x_l_diff = x1_l - x0_l #avoid putting in the for loop
    y_l_diff = y1_l - y0_l
    x_r_diff = x1_r - x0_r
    y_r_diff = y1_r - y0_r

    for i in range(GAP_NUMBERS+1):
        canvas.create_line(x0_l,y0_l, x0_r,y0_r,color)
        '''
        x0_l += GAP_SIZE * math.cos(A_RADIANS)
        y0_l -= GAP_SIZE * math.sin(A_RADIANS)
        x0_r = x0_r
        y0_r += GAP_SIZE
        '''
        x0_l += x_l_diff / GAP_NUMBERS
        y0_l += y_l_diff / GAP_NUMBERS
        x0_r += x_r_diff / GAP_NUMBERS
        y0_r += y_r_diff / GAP_NUMBERS
        
        time.sleep(0.0001)

'''
def draw_strings_outside2(canvas,x0_l,y0_l,x1_l,y1_l,x0_r,y0_r,x1_r,y1_r):    
    #draw between outside line and radial line
    for i in range(GAP_NUMBERS+1):
        canvas.create_line(x0_l,y0_l, x1_r,y1_r,COLOR1)
        x0_l += GAP_SIZE * math.cos(A_RADIANS)
        y0_l -= GAP_SIZE * math.sin(A_RADIANS)
        x1_r -= GAP_SIZE * math.cos(math.radians(30))
        y1_r -= GAP_SIZE * math.sin(math.radians(30))
        time.sleep(0.05)
'''

def draw_strings_inside(canvas,x0_r1,y0_r1,x1_r1,y1_r1,x1_r2,y1_r2,x0_r2,y0_r2, color):    
    #draw strings between two radial lines
    #two colors in full length at one side, each color for half
    
    x_r1_diff = x1_r1 - x0_r1    #avoid putting in the for loop
    y_r1_diff = y1_r1 - y0_r1
    x_r2_diff = x1_r2 - x0_r2
    y_r2_diff = y1_r2 - y0_r2    
    
    if (color == COLOR1):
        color1 = COLOR1
        color2 = COLOR2
    else:
        color1 = COLOR2
        color2 = COLOR1
    
    for i in range(GAP_NUMBERS+1):
        if(i < GAP_NUMBERS/2):
            #color = COLOR1
            canvas.create_line(x0_r1,y0_r1, x1_r2,y1_r2,color1)
        else:
            #color = COLOR2
            canvas.create_line(x0_r1,y0_r1, x1_r2,y1_r2,color2)
        '''
        y0_r1 += GAP_SIZE
        x1_r2 -= GAP_SIZE * math.cos(math.radians(30))
        y1_r2 -= GAP_SIZE * math.sin(math.radians(30))
        '''
        x0_r1 += x_r1_diff / GAP_NUMBERS
        y0_r1 += y_r1_diff / GAP_NUMBERS
        x1_r2 -= x_r2_diff / GAP_NUMBERS
        y1_r2 -= y_r2_diff / GAP_NUMBERS
        time.sleep(0.0001)


if __name__ == '__main__':
    main()