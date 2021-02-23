include("object_definitions.jl")
include("group_theory_functions.jl")

num_workers = 2
board_rows = 3
board_columns = 3

board = create_board(board_rows, board_columns)

# Initalize workers
workers = Array{worker}(undef, num_workers)
default_ability = 1
default_start = [-1,-1]
for i=1:num_workers
    id = i
    workers[i] = worker(id,
    default_ability,
    default_start)
end

# Play game
rounds = play_game(board, workers)
println("Game Over")
println("Took: ", rounds, " rounds")
println("Final Board")
print_board(board, workers)
