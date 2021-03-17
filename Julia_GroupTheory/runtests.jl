using Test
include("object_definitions.jl")

@testset "objects defined" begin
    test_worker = worker(1,1,1)
    @test test_worker.id == 1

    test_task = task(1,1,1,1)
    @test test_task.id == 1
end
