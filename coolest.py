#this shows a working def
import cozmo
import asyncio
import time
from cozmo.util import distance_mm, speed_mmps, degrees
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

def cozmo_program(robot: cozmo.robot.Robot):
    #start with head down
    robot.move_lift(-5)
    #lift head to look for face
    robot.move_head(0.50)
    time.sleep(3) #3 seconds

    #when see face, start 
    face = None

    while True:
        #if sees Mrs. H, gets root beer (not working yet for specific person)
        if face and face.is_visible:

            print("Ctrl-c to quit")
            #play happy animation
            robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()    

            #say something
            robot.say_text("Howdy Mrs. H.  Let me get you a root beer.").wait_for_completed()

            #light up cube1...with spin?
            cube1 = robot.world.get_light_cube(LightCube1Id)
            for i in range(4):
                cube1.set_light_corners(cozmo.lights.red_light,cozmo.lights.off_light,cozmo.lights.off_light,cozmo.lights.off_light)
                time.sleep(0.1)
                cube1.set_light_corners(cozmo.lights.off_light,cozmo.lights.red_light,cozmo.lights.off_light,cozmo.lights.off_light)         
                time.sleep(0.1)
                cube1.set_light_corners(cozmo.lights.off_light,cozmo.lights.off_light,cozmo.lights.red_light,cozmo.lights.off_light)
                time.sleep(0.1)
                cube1.set_light_corners(cozmo.lights.off_light,cozmo.lights.off_light,cozmo.lights.off_light,cozmo.lights.red_light)             
                time.sleep(0.1)

            #set cube lights to red
            cube1.set_lights(cozmo.lights.red_light)

            #get lift out of way. not stopping at 20%
            robot.move_lift(10)
            robot.set_lift_height(0.2, in_parallel=True).wait_for_completed()

            #drive
            robot.drive_straight(distance_mm(400), speed_mmps(100)).wait_for_completed()
            robot.move_lift(-1)
            time.sleep(3)


            #dock with cube...NOT WORKING


            robot.move_lift(3)
            #bring drink back
            robot.drive_straight(distance_mm(-400), speed_mmps(100)).wait_for_completed()

            #put drink down
            robot.move_lift(-1)
            #animation
            robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabBored).wait_for_completed()    

            #say something
            robot.say_text("Here you go.  Enjoy your soda.").wait_for_completed()

            #after program, move head down
            robot.move_head(-100)
            robot.move_head(0.50)
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
    
cozmo.run_program(cozmo_program)

