#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: 10766201
#    Student name: Morgan Rory Dideln
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  All files submitted will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Task Description-----------------------------------------------#
#
#  NOT CONNECT-4
#
#  This assignment tests your skills at processing data stored in
#  lists, creating reusable code and following instructions to display
#  a complex visual image.  The incomplete Python program below is
#  missing a crucial function, "play_game".  You are required to
#  complete this function so that when the program is run it fills
#  a grid with various rectangular tokens, using data stored in a
#  list to determine which tokens to place and where.  See the
#  instruction sheet accompanying this file for full details.
#
#  Note that this assignment is in two parts, the second of which
#  will be released only just before the final deadline.  This
#  template file will be used for both parts and you will submit
#  your final solution as a single Python 3 file, whether or not you
#  complete both parts of the assignment.
#
#--------------------------------------------------------------------#  



#-----Preamble-------------------------------------------------------#
#
# This section imports necessary functions and defines constant
# values used for creating the drawing canvas.  You should not change
# any of the code in this section.
#

# Import the functions needed to complete this assignment.  You
# should not need to use any other modules for your solution.  In
# particular, your solution must NOT rely on any non-standard Python
# modules that need to be downloaded and installed separately,
# because the markers will not have access to such modules.
from turtle import *
from math import *
from random import *

# Define constant values for setting up the drawing canvas
cell_size = 100 # pixels (default is 100)
num_columns = 7 # cells (default is 7)
num_rows = 6 # cells (default is 6)
x_margin = cell_size * 2.75 # pixels, the size of the margin left/right of the board
y_margin = cell_size // 2 # pixels, the size of the margin below/above the board
canvas_height = num_rows * cell_size + y_margin * 2
canvas_width = num_columns * cell_size + x_margin * 2

# Validity checks on board size
assert cell_size >= 80, 'Cells must be at least 80x80 pixels in size'
assert num_columns >= 7, 'Board must be at least 7 columns wide'
assert num_rows >= 6, 'Board must be at least 6 rows high'

#
#--------------------------------------------------------------------#



#-----Functions for Creating the Drawing Canvas----------------------#
#
# The functions in this section are called by the main program to
# manage the drawingage.  You should not change
# any of the code in this section.
#

# Set up the canvas and draw the background for the overall image
def create_drawing_canvas(mark_legend_spaces = True, # show text for legend
                          mark_axes = True, # show labels on axes
                          bg_colour = 'light grey', # background colour
                          line_colour = 'slate grey'): # line colour for board
    
    # Set up the drawing canvas with enough space for the board and
    # legend
    setup(canvas_width, canvas_height)
    bgcolor(bg_colour)

    # Draw as quickly as possible
    tracer(False)

    # Get ready to draw the board
    penup()
    color(line_colour)
    width(2)

    # Determine the left-bottom coords of the board
    left_edge = -(num_columns * cell_size) // 2 
    bottom_edge = -(num_rows * cell_size) // 2

    # Draw the horizontal grid lines
    setheading(0) # face east
    for line_no in range(0, num_rows + 1):
        penup()
        goto(left_edge, bottom_edge + line_no * cell_size)
        pendown()
        forward(num_columns * cell_size)
        
    # Draw the vertical grid lines
    setheading(90) # face north
    for line_no in range(0, num_columns + 1):
        penup()
        goto(left_edge + line_no * cell_size, bottom_edge)
        pendown()
        forward(num_rows * cell_size)

    # Mark the centre of the board (coordinate [0, 0])
    penup()
    home()
    dot(10)

    # Optionally label the axes
    if mark_axes:

        # Define the font and position for the labels
        small_font = ('Arial', (18 * cell_size) // 100, 'normal')
        y_offset = (27 * cell_size) // 100 # pixels

        # Draw each of the labels on the x axis
        penup()
        for x_label in range(0, num_columns):
            goto(left_edge + (x_label * cell_size) + (cell_size // 2), bottom_edge - y_offset)
            write(chr(x_label + ord('a')), align = 'center', font = small_font)

        # Draw each of the labels on the y axis
        penup()
        x_offset, y_offset = 7, 10 # pixels
        for y_label in range(0, num_rows):
            goto(left_edge - x_offset, bottom_edge + (y_label * cell_size) + (cell_size // 2) - y_offset)
            write(str(y_label + 1), align = 'right', font = small_font)

    # Optionally mark the spaces for drawing the legend
    if mark_legend_spaces:
        # Font for marking the legend's position
        big_font = ('Arial', (24 * cell_size) // 100, 'normal')
        # Left side
        goto(-(num_columns * cell_size) // 2 - 50, -25)
        write('Put your token\ndescriptions here', align = 'right', font = big_font)    
        # Right side
        goto((num_columns * cell_size) // 2 + 50, -25)
        write('Put your token\ndescriptions here', align = 'left', font = big_font)    

    # Reset everything ready for the student's solution
    pencolor('black')
    width(1)
    penup()
    home()
    tracer(True)


# End the program and release the drawing canvas to the operating
# system.  By default the cursor (turtle) is hidden when the
# program ends.  Call the function with False as the argument to
# prevent this.
def release_drawing_canvas(hide_cursor = True):
    tracer(True) # ensure any drawing still in progress is displayed
    if hide_cursor:
        hideturtle()
    done()
    
#
#--------------------------------------------------------------------#



#-----Test Data for Use During Code Development----------------------#
#
# The "fixed" data sets in this section are provided to help you
# develop and test your code.  You can use them as the argument to
# the "play_game" function while perfecting your solution.  However,
# they will NOT be used to assess your program.  Your solution will
# be assessed using the "random_game" function appearing below.
# Your program must work correctly for any data set that can be
# generated by the "random_game" function.
#
# Each of the data sets is a list of instructions, each specifying
# in which column to drop a particular type of game token.  The
# general form of each instruction is
#
#     [column, token_type]
#
# where the columns range from 'a' to 'g' and the token types
# range from 1 to 4.
#
# Note that the fixed patterns below all assume the board has its
# default dimensions of 7x6 cells.
#

# The following data sets each draw just one token type once
fixed_game_a0 = [['a', 1]]
fixed_game_a1 = [['b', 2]]
fixed_game_a2 = [['c', 3]]
fixed_game_a3 = [['d', 4]]

# The following data sets each draw just one type
# of token multiple times
fixed_game_a4 = [['c', 1], ['f', 1], ['g', 1], ['c', 1]] 
fixed_game_a5 = [['d', 2], ['d', 2], ['a', 2], ['c', 2]] 
fixed_game_a6 = [['c', 3], ['f', 3], ['g', 3], ['c', 3]] 
fixed_game_a7 = [['f', 4], ['f', 4], ['c', 4], ['c', 4]]

# The following small data sets each draw all four kinds
# of token
fixed_game_a8 = [['e', 3], ['e', 4], ['f', 3], ['e', 1],
                 ['c', 2], ['g', 4]]
fixed_game_a9 = [['g', 3], ['d', 4], ['b', 3], ['e', 1],
                 ['f', 2], ['g', 4], ['c', 2], ['g', 4]]
fixed_game_a10 = [['f', 3], ['d', 1], ['c', 3], ['c', 4],
                  ['e', 2], ['b', 1], ['b', 3]]
fixed_game_a11 = [['e', 3], ['c', 3], ['d', 3], ['c', 2],
                  ['c', 3], ['d', 4], ['a', 4], ['f', 1]]
fixed_game_a12 = [['f', 1], ['b', 4], ['f', 1], ['f', 4],
                  ['e', 2], ['a', 3], ['c', 3], ['b', 2],
                  ['a', 2]]
fixed_game_a13 = [['b', 3], ['f', 4], ['d', 4], ['b', 1],
                  ['b', 4], ['f', 4], ['b', 2], ['c', 4],
                  ['d', 3], ['a', 1], ['g', 3]]
fixed_game_a14 = [['c', 1], ['c', 4], ['g', 2], ['d', 4],
                  ['d', 1], ['f', 3], ['f', 4], ['f', 1],
                  ['g', 2], ['c', 2]]
fixed_game_a15 = [['d', 3], ['d', 4], ['a', 1], ['c', 2],
                 ['g', 3], ['d', 3], ['g', 1], ['a', 2],
                 ['a', 2], ['f', 4], ['a', 3], ['c', 2]]

# The following large data sets are each a typical game
# as generated by the "play_game" function.  (They are
# divided into five groups whose significance will be
# revealed in Part B of the assignment.)
fixed_game_b0_0 = [['d', 4], ['e', 1], ['f', 1], ['d', 1],
                   ['e', 2], ['c', 3], ['a', 2], ['e', 4],
                   ['g', 1], ['d', 4], ['a', 2], ['f', 2]]
fixed_game_b0_1 = [['f', 3], ['a', 2], ['d', 2], ['f', 4],
                   ['b', 2], ['a', 2], ['f', 3], ['f', 3],
                   ['e', 1], ['b', 2], ['e', 1], ['c', 1],
                   ['a', 3], ['d', 3], ['f', 1], ['f', 4],
                   ['b', 4], ['b', 1], ['c', 4], ['d', 1],
                   ['a', 3], ['e', 1], ['b', 2], ['c', 3],
                   ['d', 3], ['c', 2], ['c', 1], ['a', 2],
                   ['d', 4], ['b', 4], ['g', 2]]
fixed_game_b0_2 = [['d', 3], ['d', 4], ['a', 4], ['g', 3],
                   ['d', 2], ['g', 2], ['f', 1], ['b', 2],
                   ['a', 1], ['a', 3], ['a', 4], ['c', 3],
                   ['f', 3], ['b', 2], ['c', 3], ['a', 4],
                   ['g', 1]]

fixed_game_b1_0 = [['e', 3], ['a', 4], ['c', 2], ['f', 1],
                   ['a', 1], ['c', 4], ['g', 3], ['d', 1],
                   ['f', 3], ['d', 1], ['f', 1], ['g', 1],
                   ['e', 3], ['f', 3], ['f', 3], ['e', 4],
                   ['b', 2], ['a', 2], ['g', 1], ['d', 1],
                   ['a', 1], ['a', 1]]
fixed_game_b1_1 = [['f', 3], ['g', 1], ['g', 2], ['b', 1],
                   ['c', 2], ['c', 2], ['f', 3], ['g', 3],
                   ['b', 4], ['g', 4], ['d', 4], ['b', 1],
                   ['e', 3], ['e', 3], ['a', 2], ['c', 1],
                   ['f', 4], ['f', 3], ['e', 3], ['a', 2],
                   ['f', 4], ['g', 1], ['f', 4], ['a', 1]]
fixed_game_b1_2 = [['d', 2], ['f', 1], ['f', 1], ['c', 1],
                   ['c', 4], ['c', 4], ['d', 1], ['d', 4],
                   ['b', 2], ['d', 4], ['b', 1], ['d', 3],
                   ['d', 1], ['a', 1], ['f', 2], ['c', 2],
                   ['c', 4], ['c', 1], ['g', 1], ['g', 1],
                   ['g', 4], ['g', 2], ['a', 1], ['g', 1],
                   ['f', 2], ['e', 4], ['b', 1], ['e', 3],
                   ['b', 4], ['a', 4], ['b', 1], ['a', 4],
                   ['f', 2], ['g', 2], ['a', 1], ['f', 4],
                   ['e', 1], ['b', 4], ['a', 4], ['e', 2],
                   ['e', 3], ['e', 1]]

fixed_game_b2_0 = [['g', 2], ['d', 2], ['f', 2], ['f', 2],
                   ['b', 2], ['e', 1], ['d', 1], ['d', 3],
                   ['e', 1], ['e', 1], ['b', 1], ['b', 1],
                   ['d', 3], ['f', 3], ['d', 3]]
fixed_game_b2_1 = [['c', 2], ['g', 3], ['e', 4], ['g', 2],
                   ['a', 2], ['f', 2], ['f', 2], ['c', 1],
                   ['d', 2], ['b', 3], ['f', 2], ['d', 4],
                   ['b', 4], ['e', 2], ['g', 3], ['b', 4],
                   ['a', 1], ['g', 3], ['f', 1], ['e', 4],
                   ['d', 3], ['a', 1], ['a', 1], ['d', 2],
                   ['g', 3], ['d', 2], ['c', 4], ['f', 2],
                   ['g', 1], ['e', 4], ['f', 3], ['e', 3],
                   ['e', 3], ['b', 1], ['d', 2], ['c', 1],
                   ['c', 3]]
fixed_game_b2_2 = [['e', 2], ['b', 2], ['e', 2], ['g', 2],
                   ['f', 3], ['e', 3], ['e', 2], ['g', 2],
                   ['d', 2], ['e', 2], ['a', 1], ['c', 2],
                   ['e', 2], ['a', 3], ['f', 1], ['a', 3],
                   ['d', 2], ['g', 3], ['b', 4], ['b', 2],
                   ['f', 2], ['g', 4], ['d', 3], ['f', 1],
                   ['d', 3], ['a', 1], ['a', 4], ['g', 1],
                   ['f', 3], ['b', 3], ['c', 4], ['a', 3],
                   ['g', 2], ['c', 1], ['f', 3], ['b', 2],
                   ['b', 4], ['c', 3], ['d', 4], ['c', 4],
                   ['d', 1], ['c', 1]]

fixed_game_b3_0 = [['b', 2], ['d', 4], ['g', 2], ['e', 3],
                   ['d', 3], ['f', 4], ['g', 3], ['a', 3],
                   ['g', 2], ['d', 4], ['g', 4], ['f', 4],
                   ['a', 4], ['a', 4], ['f', 2], ['b', 1]]
fixed_game_b3_1 = [['d', 2], ['b', 2], ['e', 4], ['e', 3],
                   ['d', 3], ['c', 2], ['e', 3], ['b', 4],
                   ['b', 4], ['d', 4], ['f', 1], ['c', 2],
                   ['a', 1], ['e', 3], ['b', 4], ['f', 3],
                   ['c', 3], ['b', 3], ['c', 2], ['b', 2],
                   ['d', 3], ['e', 4], ['f', 2], ['g', 3],
                   ['g', 4], ['e', 2], ['c', 1], ['d', 3],
                   ['d', 1], ['f', 3], ['g', 3], ['f', 3],
                   ['c', 3], ['g', 4], ['g', 3], ['g', 3]]
fixed_game_b3_2 = [['a', 2], ['c', 1], ['f', 2], ['d', 2],
                   ['a', 3], ['c', 2], ['b', 3], ['e', 3],
                   ['e', 3], ['f', 4], ['a', 1], ['a', 2],
                   ['b', 1], ['c', 3], ['a', 2], ['c', 2],
                   ['g', 3], ['g', 3], ['d', 3], ['b', 2],
                   ['c', 4], ['g', 3], ['f', 3], ['a', 3],
                   ['f', 2], ['f', 1], ['d', 4], ['d', 4],
                   ['g', 2], ['e', 3], ['e', 4], ['f', 3],
                   ['d', 3], ['e', 4], ['g', 4], ['c', 3],
                   ['d', 1], ['e', 2], ['b', 2], ['b', 1],
                   ['g', 1]]

fixed_game_b4_0 = [['g', 3], ['f', 3], ['e', 4], ['a', 4],
                   ['a', 4], ['c', 4], ['e', 3], ['e', 4],
                   ['a', 4], ['a', 2], ['a', 2], ['c', 4],
                   ['f', 4], ['d', 4], ['c', 4], ['f', 3],
                   ['e', 1], ['b', 2], ['c', 2], ['a', 3],
                   ['g', 4], ['d', 3], ['f', 1], ['f', 2],
                   ['e', 2], ['d', 1], ['c', 4]]
fixed_game_b4_1 = [['a', 3], ['d', 4], ['g', 4], ['b', 3],
                   ['e', 1], ['b', 4], ['e', 3], ['f', 1],
                   ['f', 4], ['b', 4], ['d', 2], ['e', 4],
                   ['g', 4], ['d', 2], ['c', 3], ['b', 2],
                   ['f', 4], ['d', 2], ['b', 2], ['e', 4],
                   ['c', 3], ['d', 2], ['a', 1], ['e', 1],
                   ['d', 2], ['g', 1], ['g', 3]]
fixed_game_b4_2 = [['c', 1], ['c', 4], ['d', 1], ['c', 2],
                   ['d', 3], ['d', 4], ['g', 3], ['e', 1],
                   ['g', 4], ['c', 3], ['f', 1], ['b', 4],
                   ['a', 3], ['c', 4], ['e', 2], ['e', 3],
                   ['b', 3], ['d', 1], ['c', 3], ['f', 4],
                   ['e', 1], ['g', 4], ['b', 4], ['g', 3],
                   ['b', 4], ['b', 3], ['b', 3], ['g', 3],
                   ['e', 3], ['f', 1], ['e', 1], ['a', 1],
                   ['a', 4], ['a', 1], ['f', 4], ['f', 2],
                   ['f', 3], ['d', 1], ['d', 3], ['a', 3],
                   ['a', 1], ['g', 2]]

# If you want to create your own test data sets put them here,
# otherwise call function random_game to obtain data sets.
 
#
#--------------------------------------------------------------------#



#-----Function for Assessing Your Solution---------------------------#
#
# The function in this section will be used to assess your solution.
# Do not change any of the code in this section.

# The following function creates a random data set describing a
# game to draw.  Your program must work for any data set that
# can be returned by this function.  The results returned by calling
# this function will be used as the argument to your "play_game"
# function during marking.  For convenience during code development
# and marking this function also prints each move in the game to the
# shell window.  NB: Your code should not print anything else to
# the shell.  Make sure any debugging calls to the "print" function
# are disabled before you submit your solution.
#
# To maximise the amount of "randomness" the function makes no attempt
# to give each of the four "players" the same number of turns.  (We
# assume some other random mechanism, such as rolling a die, determines
# who gets to drop a token into the board at each turn.)  However the
# function has been designed so that it will never attempt to overfill
# a column of the board.  Also, the function will not necessarily
# generate enough moves to fill every cell in the board.
#
def random_game():
    # Welcoming message
    print('Welcome to the game!')
    print('Here are the randomly-generated moves:')
    # Initialise the list of moves
    game = []
    # Keep track of free spaces
    vacant = [["I'm free!"] * num_rows] * num_columns
    # Decide how many tokens to insert
    num_tokens = randint(0, num_rows * num_columns * 1.5)
    # Drop random tokens into the board, provided they won't
    # overfill a column
    for move in range(num_tokens):
        # Choose a random column and token type
        column_num = randint(0, num_columns - 1)
        column = chr(column_num + ord('a'))
        token = randint(1, 4)
        # Add the move, provided it won't overfill the board
        if vacant[column_num] != []:
            # Display the move
            print([column, token])
            # Remember it
            game.append([column, token])
            vacant[column_num] = vacant[column_num][1:]
    # Print a final message and return the completed game
    print('Game over!')
    if len(game) == 0:
        print('Zero moves were generated')
    elif len(game) == 1:
        print('Only one move was generated')
    else:
        print('There were', len(game), 'moves generated')
    return game

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
#  Complete the assignment by replacing the dummy function below with
#  your own "play_game" function.
#

# Define dummy token to draw tokens per player
def spirals(x_pos, y_pos, player_type):

    # set spiral token variables    

    recenter = ["#006CFF", "#0FB5EE", "#00D3F9", "#FF5251", "#CC1111", "#9F9F9F"]

    sanctuary = ["#5EBD3E", "#5AFF00", "#5AFF00", "#FFF800", "#F20000"]

    calm = ["#FAC699", "#CE8060", "#000400", "#FF9C12", "#D35308"]

    slowdown = ["#C608D1", "#FF00FE", "#FF77FD", "#2900A5", "#FFA9FD"]
##["#C608D1", "#FF00FE", "#FF77FD", "#FFA9FD", "#2900A5"]

    # Get turtle ready to draw
    penup()
    width(3)
    goto(x_pos, y_pos)
    pendown()

    # Draw spirals
    if player_type == 1:
        for i in range(360):
            pencolor(recenter[i%6])
            width(i / 250 +1)
            forward(i)
            left(59)
            if (i / 250 +1) >= 1.19:
                break
    
    elif player_type == 2:
        for i in range(360):
            pencolor(sanctuary[i%5])
            width(i / 250 +1)
            forward(i)
            left(59)
            if (i / 250 +1) >= 1.19:
                break

    elif player_type == 3:
        for i in range(360):
            pencolor(calm[i%5])
            width(i / 250 +1)
            forward(i)
            left(59)
            if (i / 250 +1) >= 1.19:
                break

    elif player_type == 4:
        for i in range(360):
            pencolor(slowdown[i%5])
            width(i / 250 +1)
            forward(i)
            left(59)
            if (i / 250 +1) >= 1.19:
                break
    
# theme description of each spiral placed on the corners of the boardgame
def player_descriptions():
    penup()
    spirals(-500, 200, 1)
    penup()
    goto(-595, 125)
    write("Token 1: Re-Centered Spiral", font=('size= 12'))

    penup()
    spirals(-500, -100, 2)
    penup()
    goto(-585, -175)
    write("Token 2: Sanctuary Spiral", font=('size= 12'))

    penup()
    spirals(500, -100, 3)
    penup()
    goto(410, -175)
    write("Token 3: Calming Spiral", font=('size= 12'))

    penup()
    spirals(500, 200, 4)
    penup()
    goto(390, 125)
    write("Token 4: Slowing-Down Spiral", font=('size= 12'))

# GLOBAL VARIABLES

# Initlise empty list for played moves memory
played_moves = []

# Initialise empty list for move memory
move_memory = []

# Defining played out game movements in the process_move function of tokens and their coordinates.
def process_move(column, player_type):

    if column == "a":
        if player_type == 1:
            if move_memory.count("a") == 0:
                spirals(-300, -250, 1)
            else:
                row_difference = move_memory.count("a") * 100
                row_position = -250 + row_difference
                spirals(-300, row_position, 1)
        elif player_type == 2:
            if move_memory.count("a") == 0:
                spirals(-300, -250, 2)
            else:
                row_difference = move_memory.count("a") * 100
                row_position = -250 + row_difference
                spirals(-300, row_position, 2)
        elif player_type == 3:
            if move_memory.count("a") == 0:
                spirals(-300, -250, 3)
            else:
                row_difference = move_memory.count("a") * 100
                row_position = -250 + row_difference
                spirals(-300, row_position, 3)
        elif player_type == 4:
            if move_memory.count("a") == 0:
                spirals(-300, -250, 4)
            else:
                row_difference = move_memory.count("a") * 100
                row_position = -250 + row_difference
                spirals(-300, row_position, 4)

        move_memory.append("a")
        
    elif column == "b":
        if player_type == 1:
            if move_memory.count("b") == 0:
                spirals(-200, -250, 1)
            else:
                row_difference = move_memory.count("b") * 100
                row_position = -250 + row_difference
                spirals(-200, row_position, 1)
        elif player_type == 2:
            if move_memory.count("b") == 0:
                spirals(-200, -250, 2)
            else:
                row_difference = move_memory.count("b") * 100
                row_position = -250 + row_difference
                spirals(-200, row_position, 2)
        elif player_type == 3:
            if move_memory.count("b") == 0:
                spirals(-200, -250, 3)
            else:
                row_difference = move_memory.count("b") * 100
                row_position = -250 + row_difference
                spirals(-200, row_position, 3)
        elif player_type == 4:
            if move_memory.count("b") == 0:
                spirals(-200, -250, 4)
            else:
                row_difference = move_memory.count("b") * 100
                row_position = -250 + row_difference
                spirals(-200, row_position, 4)

        move_memory.append("b")
        
    elif column == "c":
        if player_type == 1:
            if move_memory.count("c") == 0:
                spirals(-100, -250, 1)
            else:
                row_difference = move_memory.count("c") * 100
                row_position = -250 + row_difference
                spirals(-100, row_position, 1)
        elif player_type == 2:
            if move_memory.count("c") == 0:
                spirals(-100, -250, 2)
            else:
                row_difference = move_memory.count("c") * 100
                row_position = -250 + row_difference
                spirals(-100, row_position, 2)
        elif player_type == 3:
            if move_memory.count("c") == 0:
                spirals(-100, -250, 3)
            else:
                row_difference = move_memory.count("c") * 100
                row_position = -250 + row_difference
                spirals(-100, row_position, 3)
        elif player_type == 4:
            if move_memory.count("c") == 0:
                spirals(-100, -250, 4)
            else:
                row_difference = move_memory.count("c") * 100
                row_position = -250 + row_difference
                spirals(-100, row_position, 4)

        move_memory.append("c")
        
    elif column == "d":
        if player_type == 1:
            if move_memory.count("d") == 0:
                spirals(0, -250, 1)
            else:
                row_difference = move_memory.count("d") * 100
                row_position = -250 + row_difference
                spirals(0, row_position, 1)
        elif player_type == 2:
            if move_memory.count("d") == 0:
                spirals(0, -250, 2)
            else:
                row_difference = move_memory.count("d") * 100
                row_position = -250 + row_difference
                spirals(0, row_position, 2)
        elif player_type == 3:
            if move_memory.count("d") == 0:
                spirals(0, -250, 3)
            else:
                row_difference = move_memory.count("d") * 100
                row_position = -250 + row_difference
                spirals(0, row_position, 3)
        elif player_type == 4:
            if move_memory.count("d") == 0:
                spirals(0, -250, 4)
            else:
                row_difference = move_memory.count("d") * 100
                row_position = -250 + row_difference
                spirals(0, row_position, 4)

        move_memory.append("d")
        
    elif column == "e":
        if player_type == 1:
            if move_memory.count("e") == 0:
                spirals(100, -250, 1)
            else:
                row_difference = move_memory.count("e") * 100
                row_position = -250 + row_difference
                spirals(100, row_position, 1)
        elif player_type == 2:
            if move_memory.count("e") == 0:
                spirals(100, -250, 2)
            else:
                row_difference = move_memory.count("e") * 100
                row_position = -250 + row_difference
                spirals(100, row_position, 2)
        elif player_type == 3:
            if move_memory.count("e") == 0:
                spirals(100, -250, 3)
            else:
                row_difference = move_memory.count("e") * 100
                row_position = -250 + row_difference
                spirals(100, row_position, 3)
        elif player_type == 4:
            if move_memory.count("e") == 0:
                spirals(100, -250, 4)
            else:
                row_difference = move_memory.count("e") * 100
                row_position = -250 + row_difference
                spirals(100, row_position, 4)

        move_memory.append("e")
        
    elif column == "f":
        if player_type == 1:
            if move_memory.count("f") == 0:
                spirals(200, -250, 1)
            else:
                row_difference = move_memory.count("f") * 100
                row_position = -250 + row_difference
                spirals(200, row_position, 1)
        elif player_type == 2:
            if move_memory.count("f") == 0:
                spirals(200, -250, 2)
            else:
                row_difference = move_memory.count("f") * 100
                row_position = -250 + row_difference
                spirals(200, row_position, 2)
        elif player_type == 3:
            if move_memory.count("f") == 0:
                spirals(200, -250, 3)
            else:
                row_difference = move_memory.count("f") * 100
                row_position = -250 + row_difference
                spirals(200, row_position, 3)
        elif player_type == 4:
            if move_memory.count("f") == 0:
                spirals(200, -250, 4)
            else:
                row_difference = move_memory.count("f") * 100
                row_position = -250 + row_difference
                spirals(200, row_position, 4)

        move_memory.append("f")
        
    elif column == "g":
        if player_type == 1:
            if move_memory.count("g") == 0:
                spirals(300, -250, 1)
            else:
                row_difference = move_memory.count("g") * 100
                row_position = -250 + row_difference
                spirals(300, row_position, 1)
        elif player_type == 2:
            if move_memory.count("g") == 0:
                spirals(300, -250, 2)
            else:
                row_difference = move_memory.count("g") * 100
                row_position = -250 + row_difference
                spirals(300, row_position, 2)
        elif player_type == 3:
            if move_memory.count("g") == 0:
                spirals(300, -250, 3)
            else:
                row_difference = move_memory.count("g") * 100
                row_position = -250 + row_difference
                spirals(300, row_position, 3)
        elif player_type == 4:
            if move_memory.count("g") == 0:
                spirals(300, -250, 4)
            else:
                row_difference = move_memory.count("g") * 100
                row_position = -250 + row_difference
                spirals(300, row_position, 4)

        move_memory.append("g")

    played_moves.append([column, player_type])

# defining winning spiral function 
def winning_spiral():   

# local variables set up for future for loop token population
    col_one = "0"
    col_two = "0"
    col_three = "0"
    col_four = "0"
    col_five = "0"
    col_six = "0"
    col_seven = "0"

# converted player_type variable to feed as string data and improve efficiency of loop code
    for column, player_type in played_moves:
        
        converted_player_type = str(player_type)

        if column == 'a':
            col_one = col_one + converted_player_type
        elif column == 'b':
            col_two = col_two + converted_player_type
        elif column == 'c':
            col_three = col_three + converted_player_type
        elif column == 'd':
            col_four = col_four + converted_player_type
        elif column == 'e':
            col_five = col_five + converted_player_type
        elif column == 'f':
            col_six = col_six + converted_player_type
        elif column == 'g':
            col_seven = col_seven + converted_player_type

# innitialise drawn spiral check loop in newly populated variables and return winner
    for player_num in range(1, 5):

        score = 0
        
        if col_one[-1] == str(player_num):
            score += 1
        if col_two[-1] == str(player_num):
            score += 1
        if col_three[-1] == str(player_num):
            score += 1
        if col_four[-1] == str(player_num):
            score += 1
        if col_five[-1] == str(player_num):
            score += 1
        if col_six[-1] == str(player_num):
            score += 1
        if col_seven[-1] == str(player_num):
            score += 1

        if score >= 4:
            winner = player_num
            return winner

    
# Draw tokens on the board as per the provided data set
def play_game(generated_moves):

    # calling spiral description function
    player_descriptions()
 
    winner = None

    # Extract column and player_type data from move list
    for column, player_type in generated_moves:

        process_move(column, player_type)

        if winning_spiral() != None:
            winner = winning_spiral()
            break
# Draw stars for winner and draw illustration

    if winner == None:
        print("It is a Draw")
# Draw the draw star
        penup()
        home()
        goto(-590, 195)
        color("silver")
        begin_fill()
        points = 1
        while points < 5:
            forward(50)
            left(145)
            points = points + 1
        end_fill()

        penup()
        home()
        goto(-590, -115)
        color("silver")
        begin_fill()
        points = 1
        while points < 5:
            forward(50)
            left(145)
            points = points + 1
        end_fill()

        penup()
        home()
        goto(540, 195)
        color("silver")
        begin_fill()
        points = 1
        while points < 5:
            forward(50)
            left(145)
            points = points + 1
        end_fill()

        penup()
        home()
        goto(540, -105)
        color("silver")
        begin_fill()
        points = 1
        while points < 5:
            forward(50)
            left(145)
            points = points + 1
        end_fill()
        
# Draw winning star
    elif winner == 1:
        print("winner is player", winner)
        penup()
        home()
        goto(-590, 195)
        color("gold")
        begin_fill()
        points = 1
        while points < 5:
            forward(50)
            left(145)
            points = points + 1
        end_fill()
        
    elif winner == 2:
        print("winner is player", winner)
        penup()
        home()
        goto(-590, -115)
        color("gold")
        begin_fill()
        points = 1
        while points < 5:
            forward(50)
            left(145)
            points = points + 1
        end_fill()

    elif winner == 4:
        print("winner is player", winner)
        penup()
        home()
        goto(540, 195)
        color("gold")
        begin_fill()
        points = 1
        while points < 5:
            forward(50)
            left(145)
            points = points + 1
        end_fill()

    elif winner == 3:
        print("winner is player", winner)
        penup()
        home()
        goto(540, -105)
        color("gold")
        begin_fill()
        points = 1
        while points < 5:
            forward(50)
            left(145)
            points = points + 1
        end_fill()
        
#--------------------------------------------------------------------#



#-----Main Program---------------------------------------------------#
#
# This main program sets up the background, ready for you to start
# drawing your solution.  Do not change any of this code except
# as indicated by the comments marked '*****'.
#

# Set up the drawing canvas
# ***** You can change the background and line colours, and choose
# ***** whether or not to label the axes and mark the places for the
# ***** legend, by providing arguments to this function call
create_drawing_canvas(mark_legend_spaces = False)

# Control the drawing speed
# ***** Change the following argument if you want to adjust
# ***** the drawing speed
speed('fastest')

# Decide whether or not to show the drawing step-by-step
# ***** Set the following argument to False if you don't want to wait
# ***** forever while the cursor moves slowly around the screen
tracer(False)

# Give the drawing canvas a title
# ***** Replace this title with a description of your solution's
# ***** theme and its tokens
title('Spiraling Out Of Control (Re-Centering, Sanctuary, Calm and Slow-down)')

### Call the student's function to play the game
### ***** While developing your program you can call the "play_game"
### ***** function with one of the "fixed" data sets, but your
### ***** final solution must work with "random_game()" as the
### ***** argument.  Your "play_game" function must work for any data
### ***** set that can be returned by the "random_game" function.
#play_game(fixed_game_b4_2) # <-- use this for code development only
play_game(random_game()) # <-- this will be used for assessment

# Exit gracefully
# ***** Change the default argument to False if you want the
# ***** cursor (turtle) to remain visible at the end of the
# ***** program as a debugging aid
release_drawing_canvas()

#
#--------------------------------------------------------------------#
