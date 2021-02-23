'''
Created on Oct 24, 2018

@author: dpayn
'''
import random
from math import ceil

## How long to allow this to run. If complete, will end before this
max_time_steps = 13

## Initialize stage
stageLength = 5
stageWidth = 5
# Create a stage of the dimensions outlined above
stage = [0] * stageLength
for row in range(stageLength):
    stage[row] = [0] * stageWidth
# Set attributes of tasks on stage
stage_attributes = {
    'adjacency_depedency':'no' # Are actors only allowed to take on tasks adjacent to the one they've just done
    }

## Initialize actors
numberOfActors = 3
actorLocations = [0]*numberOfActors
for actor in range(numberOfActors):
    actorLocations[actor] = [0,0]
# Attributes for actors here, probably want to create an actor class. Could vary them across the actors
actor_attributes = { 
    'percent_stubborness':25, # Sturbborness is defined as willingness to try same task again after a conflict with another actor
    'plan_follower':'no'
}
# Print out initial conditions
print("Total number of tasks: {}\nNumber of Actors: {}\nMax Time Steps: {}\n".format((stageLength*stageWidth), numberOfActors, max_time_steps))
minimum_possible_steps = int(ceil(stageLength*stageWidth/numberOfActors))
print("Minimum Number of Steps to Complete: %i\n" %(minimum_possible_steps))
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

# gets the possible valid adjacent moves for the actor - constraints - no wrapping, no overlaps, no diagonal
def get_valid_possible_moves(current_vert_pos, current_horiz_pos):
    # Determine valid moves - look right, left, down, up
    # initialize move matrix
    moves = []
    
    # check right
    right = current_horiz_pos+1
    if (right>=0) and (right<stageWidth) and (stage[current_vert_pos][right] == 0):
        moves.append([current_vert_pos, right]) # updates the list of moves
    # check left
    left = current_horiz_pos-1
    if (left>=0) and (left<stageWidth) and (stage[current_vert_pos][left] == 0):
        moves.append([current_vert_pos, left])
    # check down
    down = current_vert_pos+1
    if (down>=0) and (down<stageLength) and (stage[down][current_horiz_pos] == 0):
        moves.append([down, current_horiz_pos])
    # check up
    up = current_vert_pos-1
    if (up>=0) and (up<stageLength) and (stage[up][current_horiz_pos] == 0):
        moves.append([up, current_horiz_pos])
        
    # Returns a list of valid positions
    return moves

# plan role, meaning the set of tasks that actor will do
def plan_role(start_vert_pos, start_horiz_pos, number_of_tasks_to_plan):
    # Plans out a role (aka set of tasks) of given length based on current position
    vert_pos = start_vert_pos
    horiz_pos = start_horiz_pos
    planned_role = [[vert_pos, horiz_pos]]
    for task in range (number_of_tasks_to_plan):
        # choose a next task
        valid_next_moves = get_valid_possible_moves(vert_pos, horiz_pos)
        next_task = random.choice(valid_next_moves)
        # add that to the end of the plan
        planned_role.append(next_task)
        # update plan position for next iteration
        vert_pos = next_task[0]
        horiz_pos = next_task[1] 
    return planned_role

# End User-Defined Functions
#################################################################


# Initialize memories
actor_memory = [0] * numberOfActors
actor_plans = [0] * numberOfActors

# Assign starting locations for each actor
for actor in range(numberOfActors):
    # Get a random task/spot and udpate the actor locations
    actorLocations[actor] = get_random_open_task()
    # Update the stage to reflect that position
    stage[actorLocations[actor][0]][actorLocations[actor][1]] = actor+1
    role = plan_role(actorLocations[actor][0], actorLocations[actor][1], int(stageWidth*stageLength/3))
    actor_plans[actor] = role
    print("Planned role for actor %i\n" %(actor+1), role)
                                         
    # Initialize each actor's memory
    # For now - just previous action and was it successful
    actor_memory[actor] = [actorLocations[actor], 'yes']
    
## Play game
# set a complete flag
complete = 0
# initialize the time via number of steps
step = 1

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

    # Complete once for each actor determining their valid moves and building a table of intended moves
    for actor in range(numberOfActors):
        # If the actor is a plan follower, their last step was successful, and they still have a plan - continue on the plan
        if (actor_attributes.get('plan_follower') == 'yes') and (actor_memory[actor][0][1] == 'yes') and (len(actor_plans[actor])>step-2):
            next_move = actor_plans[actor][step-2]
        else:
            # get all valid adjacent moves
            valid_next_moves = get_valid_possible_moves(actorLocations[actor][0],actorLocations[actor][1])
            # If there is a valid adjacent move, do that
            if (len(valid_next_moves) > 0):
                next_move = random.choice(valid_next_moves)
            # Else if the stage is not set to be strictly adjacent dependent, select an open task elsewhere
            elif (stage_attributes.get('adjacency_depedency') == 'no'):
                next_move = get_random_open_task()
            # Or stay where they are
            else:
                next_move = actorLocations[actor]
            
        # If that intended move is the same as most recent action and that was a failure (this is redundant)
        # given current implementation. And checks that the actor is not intending to stay in place
        if (next_move == actor_memory[actor][0][0]) and (actor_memory[actor][0][1] == 'no') and (next_move != actorLocations[actor]):
            # decide whether to try again or hold still
            dice_roll = random.randint(1,101)
            # try the same thing again
            if (dice_roll <= actor_attributes.get('percent_stubborness')):
                intended_moves[actor] = next_move
                print('Actor %i doing the same thing again and expecting a different result' %(actor+1))
            # stay where they are
            else:
                print('Actor %i standing idle, letting others go first after failed last action' %(actor+1))
                intended_moves[actor] = actorLocations[actor]
        else:
            intended_moves[actor] = next_move
    # completes for loop
    
    for mover in range(numberOfActors):
        movers_intending = 0
        
        # checks that a mover has a valid move available to them
        if intended_moves[mover] == actorLocations[mover]:
            print('no valid move available for actor %i, staying in place' %(mover+1))    
            actor_memory[mover].insert(0,[intended_moves[mover], 'no'])
        else:
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
                # update memory to indicate success
                actor_memory[mover].insert(0, [intended_moves[mover], 'yes'])
            elif movers_intending > 1:
                # update memory to indicate failure
                actor_memory[mover].insert(0,[intended_moves[mover], 'no'])
                print('Conflict! Actor %i was intending the same move as another actor. Actor holding still' % (mover+1))

                
    # check completeness
    complete = 1
    for row in range(stageLength):
        for column in range(stageWidth):
            if stage[row][column] == 0:
                complete = 0        
        
    # Printing the results of each time step
        # The * refers to completed spots, 0 for jobs to be done, numbers for actor locations
    print("\nTime Step %3i:"  %step )
    print('  ', '\n   '.join(' '.join(
        str(stage[row][column]).replace('-1', '*') for column in range(stageWidth)) 
                for row in range(stageLength)))

# Determine efficacy
print('Statistics for task:')
if complete == 1:
    print('Completed in %i steps!' %step)
    efficacy = minimum_possible_steps/step*100
    print('The minimum possible number of steps was {}, that is an efficacy of {} percent'.format(minimum_possible_steps,efficacy))
elif complete == 0:
    print('Did not complete. Hit time limit of %i maximum time steps' %max_time_steps)

for actor in range(numberOfActors):
    idle_time = 0
    for action in range(len(actor_memory[actor])):
        if (actor_memory[actor][action][1] == 'no'):
            idle_time += 1
    percent_time_idle = idle_time/(step)*100
    print("Actor {} was idle for {} time steps out of {} total steps or in other words, {} percent of the time".format((actor+1), idle_time, step, percent_time_idle))

