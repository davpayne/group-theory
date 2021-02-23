using Test

@testset "objects defined" begin
    test_actor = actor(1)
    @test test_actor.id == 1
    
    test_stage = stage(1)
    @test test_stage.id == 1
end