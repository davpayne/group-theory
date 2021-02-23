'''
Created on Oct 24, 2018

@author: dpayn
'''
import random

## How long to allow this to run. If complete, will end before this
max_time_steps = 11

## Initialize stage
stageLength = 6
stageWidth = 4
# Create a stage of the dimensions outlined above
stage = [0] * stageLength
for row in range(stageLength):
    stage[row] = [0] * stageWidth

## Initialize actors
numberOfActors = 3
actorLocations = [0]*numberOfActors
for actor in range(numberOfActors):
    actorLocations[actor] = [0,0]
# Could add attributes for actors here, probably want to create an actor class

#################################################################
# User Defined Functions

# get_random_open_task runs through to find a task/spot not currently taken or done
def get_random_open_task():
    valid_location = 'no'
    # randomizes the location given
    while valid_location == 'no':
        vertical_position = random.randint(0,stageLength-1)
        horizontal_position = random.randint(0,stageWidth-1)
        # checks to make sure no actor is currently there. No overlaps are allowed
        if stage[vertical_position][horizontal_position] == 0:
            valid_location = 'yes'
    return [vertical_position, horizontal_position]

# gets the possible valid moves for the actor - constraints - no wrapping, no overlaps, no diagonal, must be adjacent
def get_valid_possible_moves(current_vert_pos, current_horiz_pos):
    # Determine valid moves - look right, left, down, up
    # initialize move matrix with the four possible options
    moves = [[-1,-1], [-1,-1], [-1,-1], [-1,-1]]
    # initialize a valid move available flag
    valid_move_available = 'no'
    
    # check right
    right = current_horiz_pos+1
    if (right>=0) and (right<stageWidth) and (stage[current_vert_pos][right] == 0):
        moves[0] = [current_vert_pos, right] # updates the list of moves
        valid_move_available = 'yes' # sets the flag to a valid move being available
    # check left
    left = current_horiz_pos-1
    if (left>=0) and (left<stageWidth) and (stage[current_vert_pos][left] == 0):
        moves[1] = [current_vert_pos, left]
        valid_move_available = 'yes'
    # check down
    down = current_vert_pos+1
    if (down>=0) and (down<stageLength) and (stage[down][current_horiz_pos] == 0):
        moves[2] = [down, current_horiz_pos]
        valid_move_available = 'yes'
    # check up
    up = current_vert_pos-1
    if (up>=0) and (up<stageLength) and (stage[up][current_horiz_pos] == 0):
        moves[3] = [up, current_horiz_pos]
        valid_move_available = 'yes'

    if valid_move_available == 'yes':
        # Returns a list of valid positions
        return moves
    else:
        return 'none'

# select intended next move
def intended_next_move(current_vert_pos, current_horiz_pos):
        # Get their valid possible moves based on current position
        valid_moves = get_valid_possible_moves(current_vert_pos,current_horiz_pos)
        
        # if valid moves returns none then randomly select an open spot on the stage
        if valid_moves == 'none':
            chosen_move = get_random_open_task()
        # If the actor has a valid move, randomly select one of the valid ones
        else:
            # initializes the variable for the while statement
            chosen_move = [-1, -1]
            # runs while on the moves until a valid move is chosen from list of moves
            while chosen_move == [-1, -1]:
                chosen_move=random.choice(valid_moves)
        return chosen_move
# End User-Defined Functions
#################################################################



# Assign starting locations for each actor
for actor in range(numberOfActors):
    # Get a random task/spot and udpate the actor locations
    actorLocations[actor] = get_random_open_task()
    # Update the stage to reflect that position
    stage[actorLocations[actor][0]][actorLocations[actor][1]] = actor+1

## Play game
# set a complete flag
complete = 0
# initialize the time via number of steps
step = 0

# Print initial state
    # The * refers to completed spots, 0 for jobs to be done, numbers for actor locations
print("\nTime Step %3i:"  %step )
print('  ', '\n   '.join(' '.join(
    str(stage[row][column]).replace('-1', '*') for column in range(stageWidth)) 
            for row in range(stageLength)))


# Run the game until completion, meaning all tasks/spots covered or until hitting the max time
while (complete == 0) and (step < max_time_steps):
    step += 1
    
    # initialize a matrix of intended moves
    intended_moves = [0]*numberOfActors
    for actor in range(numberOfActors):
        intended_moves[actor] = [-1,-1]

    # Complete once for each actor determining their valid moves and building a table of intended moves
    for actor in range(numberOfActors):
        intended_moves[actor] = intended_next_move(actorLocations[actor][0],actorLocations[actor][1])
    # completes for loop
    
    for mover in range(numberOfActors):
        movers_intending = 0
        
        # checks that a mover has a valid move available to them
        if intended_moves[mover] != [-1, -1]:
            # checks whether that move conflicts with another's intended move
            for others_moves in range(numberOfActors):
                if intended_moves[others_moves] == intended_moves[mover]:
                    movers_intending += 1
            # if the mover is the only one intending to go to that spot, do that
            if movers_intending == 1:
                # gets the mover's location. This assignment done only for readability of rest of code block
                moverVerticalPos = actorLocations[mover][0]
                moverHorizontalPos = actorLocations[mover][1]
                # updates stage with move
                stage[moverVerticalPos][moverHorizontalPos] = -1
                stage[intended_moves[mover][0]][intended_moves[mover][1]] = mover+1
                # update actor location with move
                actorLocations[mover] = intended_moves[mover]
            elif movers_intending > 1:
                print('Conflict! Actor %i was intending the same move as another actor. Actor holding still' % (mover+1))
        else:
            print('no valid move available for actor %i' %(mover+1))    
            

                
    # check completeness
    complete = 1
    for row in range(stageLength):
        for column in range(stageWidth):
            if stage[row][column] == 0:
                complete = 0
    if complete == 1:
        print('\nCompleted in %i steps!' %step)
        
    # Printing the results of each time step
        # The * refers to completed spots, 0 for jobs to be done, numbers for actor locations
    print("\nTime Step %3i:"  %step )
    print('  ', '\n   '.join(' '.join(
        str(stage[row][column]).replace('-1', '*') for column in range(stageWidth)) 
                for row in range(stageLength)))



