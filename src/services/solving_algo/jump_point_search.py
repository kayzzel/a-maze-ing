# steps
#
# Create a new array with the same dimentions as the maze filled with None
# to have the cell already expolered and theyre direction
# 0 -> still; 1 -> North; 2 -> South; 3 -> West; 4 East
#
# Start from the start coordinate
# and set it to True
# create new pathfider for each ways possible
#
# calculate the cost to go to the end (heuristic calcul)
# and add the distance from the start
#
# With the one with the less cost go in the same direction will you can
# (open wall in front and cell not explored)
# and create a new pathfinder at each open wall that is open
# set all the cell that has already been explored at theyre direction
# in the new array
#
# Repeate the 2 previous steps utile the end is found
#
# When the end is found go back to the start using the directions in the array
# for each direction add the letter for the opposite direction
# Reverse the string containing the direction and return it
