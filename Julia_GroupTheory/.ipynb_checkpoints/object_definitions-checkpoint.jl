
mutable struct actor
    id::Int
    ability::Int
end

mutable struct task
    id::Int
    status
    difficulty::Int
end

mutable struct stage
    id::Int
    rows::Int
    columns::Int
    function createBoard(rows, columns)
        tasks::Array{task}(undef, rows, columns)
    end
end

