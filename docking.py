#try to get dock to work
import cozmo
import asyncio
import time
from cozmo.util import distance_mm, speed_mmps, degrees, Angle
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

def dock_with_cube(robot: cozmo.robot.Robot):
    robot.say_text("This is dock with cube.").wait_for_completed()
    time.sleep(2)

    #this puts his head in the right position
    robot.move_lift(-1)
    time.sleep(1)
    robot.move_head(-0.1)
    time.sleep(0.1)     
    cube1 = robot.world.get_light_cube(LightCube1Id)

    
    robot.say_text("All right kids. Who's thirsty").wait_for_completed()

    print("Cozmo is waiting until he sees a cube.")
    robot.world.wait_for_observed_light_cube()
    
    print("Cozmo found a cube, and will now attempt to dock with it:")
    cube1 = robot.world.get_light_cube(LightCube1Id)
    robot.dock_with_cube(cube1, approach_angle=cozmo.util.degrees(0), in_parallel=True, num_retries=2).wait_for_completed()        
    time.sleep(3)

def cozmo_program(robot: cozmo.robot.Robot):
    #start with head & lift down
    robot.move_head(-1)
    time.sleep(1)
    robot.move_lift(-1)
    #lift head to look for face
    robot.move_head(0.50)
    time.sleep(3) #3 seconds
    robot.say_text("Starting the program.").wait_for_completed()

    dock_with_cube(robot)    

cozmo.run_program(cozmo_program)    