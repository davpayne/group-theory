
mutable struct worker
    id::Int
    ability::Int
    current_location
    # Want abilities that can be turned on/off
end

mutable struct task
    id::Int
    complete_flag::Int # 0 or 1
    occupancy::Int
    difficulty::Int
end
