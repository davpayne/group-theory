
function create_board(rows, columns, use_default=1)
    board = Array{task}(undef, rows, columns)
    if use_default == 1
        default_difficulty = 1
        default_occupancy = 0
        default_complete_flag = 0
        for i in 1:length(board)
            id = i
            iteration_task = task(
            id, default_complete_flag,
            default_occupancy, default_difficulty)
            board[i] = iteration_task
        end
    end
    return board
end

function print_board(board, workers)
    for row in 1:size(board)[1]
        line = ""
        for col in 1:size(board)[2]
            worker_loc = 0
            for i in 1:length(workers)
                if [row, col] == workers[i].current_location
                    worker_loc = workers[i].id
                end
            end
            if worker_loc != 0
                line = string(line, worker_loc, " ")
            elseif board[row,col].complete_flag == 1
                line = string(line, "X ")
            else
                line = string(line, "O ")
            end
        end
        println(line)
    end
    return
end

function calculate_turn(board, worker)
    return
end

function calculate_valid_moves(board, worker)
    possible_moves = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
    ]
    valid_moves = []
    if worker.current_location != [-1,-1]
        for i in 1:length(possible_moves)
            move = worker.current_location + possible_moves[i]
            if move[1] > 0 && move[1] <= size(board)[1] &&
                move[2] > 0 && move[2] <= size(board)[2]
                if board[move[1],move[2]].complete_flag == 0
                    push!(valid_moves, possible_moves[i])
                end
            end
        end
    else
        valid_moves = []
    end
    return valid_moves
end

function play_game(board, workers)
    rounds = 0
    num_workers = length(workers)
    num_tasks_remaining = length(board)
    while num_tasks_remaining > 0
        rounds += 1
        println("Start of round ", rounds)
        print_board(board, workers)
        for i=1:num_workers
            # Determine if worker is done working on current task
            current_worker = workers[i];
            # if current_worker
            println("Num tasks remaining ", num_tasks_remaining)
            if num_tasks_remaining > 0
                valid_moves = calculate_valid_moves(board, current_worker)
                if length(valid_moves)==0
                    valid_random_moves = findall(x->(x.occupancy==0
                    && x.complete_flag==0), board)
                    choice = rand((1:length(valid_random_moves)))
                    chosen_move = valid_random_moves[choice]
                    selected_move = [chosen_move[1],chosen_move[2]]
                else
                    choice = rand((1:length(valid_moves)))
                    selected_move = valid_moves[choice] +
                    current_worker.current_location
                end
                current_worker.current_location = selected_move
                board[selected_move[1],selected_move[2]].complete_flag = 1
                num_tasks_remaining -= 1
                println("Move", current_worker.current_location)
            else
                println("No tasks remaining")
                break
            end
        end
    end
    return rounds
end
