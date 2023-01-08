from gcody import *

# creating parameters
layer_height = 0.12
line_width=0.25
cube_height = 1
cube_width = 30
cube_length = 30


# creating gcode object
g = gcode()

def draw_square(cube_width, cube_length, layer_height):
    global g
    ew=cube_width * line_width * layer_height / (3.14*((1.75/2)**2))
    el=cube_length * line_width * layer_height / (3.14*((1.75/2)**2))
    g.move(x=cube_width, extrude=ew ) 
    g.move(y=cube_length, extrude=el )
    g.move(x=-cube_width, extrude=ew )
    g.move(y=-cube_length, extrude=el )



# writes the GCODE command to use relative coordinates
# this changes how position is recorded internally (in gcode object)
# abs_coords is the default setting for gcode and is the default for gcody as well
g.code.append("START_PRINT BED_TEMP=80.0 EXTRUDER_TEMP=235.0\n")

g.move(speed=100)
line_width=0.5

# Move to start position
g.move(x=100, y=100, z=layer_height)

# First layer slow
g.move(speed=10)

g.rel_extrude()
g.rel_move()

# Draw 'skirt'
g.move(x=-5, y=-5)
draw_square(cube_width+10, cube_length+10, layer_height)
g.move(x=line_width, y=line_width)
draw_square(cube_width+10-2*line_width, cube_length+10-2*line_width, layer_height)


# do each layer of the print
for j in range(int(cube_height/layer_height)):
    # Go back to start pos
    g.abs_move()
    g.move(x=100, y=100)
    g.rel_move()

    # draw outline
    inset = 0
    #  outer square
    draw_square(cube_width, cube_length, layer_height)
    g.move(x=line_width, y=line_width)
    inset+=line_width*2
    #  inner square
    draw_square(cube_width-inset, cube_length-inset, layer_height)
    g.move(x=line_width, y=line_width)
    inset+=line_width*2

    # draw zigzag
    # Which direction should we zigzag?
    if j%2==0:
        for i in range(int((cube_length-inset)/line_width)):
            g.move(y=line_width)
            e=(cube_width-inset) * line_width * layer_height / (3.14*((1.75/2)**2))
            e = e * 1.3
            g.move(x=(-1)**i * (cube_width-inset), extrude=e )

    else: # in this direction, we vary the density (e variable)
        for i in range(int((cube_width-inset)/line_width)):
            g.move(x=line_width)
            e=(cube_length-inset) * line_width * layer_height / (3.14*((1.75/2)**2))
            e = e * (i/(cube_width/line_width) * 1.9)
            g.move(y=(-1)**i * (cube_length-inset), extrude=e ) # movement in x

    # Move up a layer
    g.move(z=layer_height)
    # Set speed and width (because we set them differently for the first layer)
    g.move(speed=30)
    line_width=0.25

g.code.append("END_PRINT")

# creates a matplotlib figure matching the path of the printer head
g.view('b')

g.save('screen.gcode')

print(g)