
mutable struct worker
    id::Int
    ability::Int
    current_location
end

mutable struct task
    id::Int
    complete_flag::Int # 0 or 1
    occupancy::Int
    difficulty::Int
end
