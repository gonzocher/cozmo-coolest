#This is working towards the final project, one step at a time
import cozmo
import asyncio
import time
from cozmo.util import distance_mm, speed_mmps, degrees, Angle
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id


#This works
def get_ready(robot: cozmo.robot.Robot):
    robot.say_text("This is get ready.").wait_for_completed()

    #start with head & lift down
    robot.move_head(-1)
    time.sleep(1)
    robot.move_lift(-1)
    #lift head to look for face
    robot.move_head(0.50)
    time.sleep(3) #3 seconds


#This works
def take_order(robot: cozmo.robot.Robot):
    robot.say_text("This is take order.").wait_for_completed()

    #play happy animation
    robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()    

    #say something
    robot.say_text("Oh goody, Mrs. H.  Let me get you a root beer.").wait_for_completed()

    #light up cube1...with spin?
    cube1 = robot.world.get_light_cube(LightCube1Id)
    for i in range(4):
        cube1.set_light_corners(cozmo.lights.off_light,cozmo.lights.off_light,cozmo.lights.off_light,cozmo.lights.red_light)             
        time.sleep(0.1)
        cube1.set_light_corners(cozmo.lights.off_light,cozmo.lights.off_light,cozmo.lights.red_light,cozmo.lights.off_light)
        time.sleep(0.1)
        cube1.set_light_corners(cozmo.lights.off_light,cozmo.lights.red_light,cozmo.lights.off_light,cozmo.lights.off_light)         
        time.sleep(0.1)
        cube1.set_light_corners(cozmo.lights.red_light,cozmo.lights.off_light,cozmo.lights.off_light,cozmo.lights.off_light)
        time.sleep(0.1)

    #set cube lights to red
    cube1.set_lights(cozmo.lights.blue_light)
    time.sleep(2)

    #get lift out of way. not stopping at 20%
    robot.move_lift(1)
    time.sleep(1)

#Does not dock
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
    robot.dock_with_cube(cube1, approach_angle=cozmo.util.degrees(0), num_retries=2).wait_for_completed()        
    time.sleep(3)

#does dock but does not run in cozmo_program
async def dock_with_cube_async(robot: cozmo.robot.Robot):
    await robot.say_text("Running async").wait_for_completed()

    await robot.set_head_angle(degrees(-5.0)).wait_for_completed()

    print("Cozmo is waiting until he sees a cube.")
    cube = await robot.world.wait_for_observed_light_cube()

    print("Cozmo found a cube, and will now attempt to dock with it:")
    # Cozmo will approach the cube he has seen
    # using a 180 approach angle will cause him to drive past the cube and approach from the opposite side
    # num_retries allows us to specify how many times Cozmo will retry the action in the event of it failing
    action = robot.dock_with_cube(cube, approach_angle=cozmo.util.degrees(0), num_retries=2)
    await action.wait_for_completed()
    print("result:", action.result)


def cozmo_program(robot: cozmo.robot.Robot):
    robot.say_text("Starting the program.").wait_for_completed()

    get_ready(robot)

    #when see face, start 
    face = None
    
    robot.say_text("I'm looking for a face.").wait_for_completed()

    while True:
        #if sees Mrs. H, gets root beer (not working yet for specific person)

        if face and face.is_visible:
            robot.say_text("I see you.").wait_for_completed()

            print("Ctrl-c to quit")
            #happy, say, spin cube, set cube
            take_order(robot)


            #drive to soda
            robot.drive_straight(distance_mm(400), speed_mmps(100)).wait_for_completed()

            #dock with cube
            dock_with_cube(robot)


            #pick up cube
            robot.say_text("Did I pick up the cube?").wait_for_completed()

            robot.move_lift(0.5)
            #bring drink back
            robot.say_text("Now I'll bring you your drink.").wait_for_completed()

            robot.drive_straight(distance_mm(-400), speed_mmps(100)).wait_for_completed()

            #put drink down
            robot.move_lift(-1)   

            #say something
            robot.say_text("Here you go.  Enjoy your soda.").wait_for_completed()

            #after program, move head down
            robot.move_head(1)
            time.sleep(1)
            robot.say_text("Now I'll look for a face again.").wait_for_completed()

            time.sleep(3) #3 seconds            

        else:
            robot.set_backpack_lights_off()

            # Wait until we we can see another face
            try:
                face = robot.world.wait_for_observed_face(timeout=30)
            except asyncio.TimeoutError:
                print("Didn't find a face.")
                return

        time.sleep(.2)



#cozmo.run_program(get_ready)
#cozmo.run_program(take_order)
#cozmo.run_program(dock_with_cube)
#cozmo.run_program(dock_with_cube_async)
cozmo.run_program(cozmo_program)
