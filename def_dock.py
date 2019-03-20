import cozmo
import asyncio
import time
from cozmo.util import distance_mm, speed_mmps, degrees
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

def dock_with_cube(robot: cozmo.robot.Robot):
    robot.say_text("All right kids. Who's thirsty").wait_for_completed()
    robot.play_anim_trigger(cozmo.anim.Triggers.CubePounceLoseSession, ignore_body_track=True).wait_for_completed()
'''
    robot.move_lift(1)
    time.sleep(1)
    robot.move_lift(-1)
    time.sleep(3)

    cube1 = robot.world.get_light_cube(LightCube1Id)
    robot.set_head_angle(degrees(-5.0)).wait_for_completed()

    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    print("Cozmo is waiting until he sees a cube.")
    robot.world.wait_for_observed_light_cube()
    look_around.stop()

    print("Cozmo found a cube, and will now attempt to dock with it:")
    robot.dock_with_cube(cube1, approach_angle=cozmo.util.degrees(0), num_retries=3).wait_for_completed()
    




def cozmo_program(robot: cozmo.robot.Robot):
    look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)

    # try to find a block
    cube = None

    try:
        cube = robot.world.wait_for_observed_light_cube(timeout=30)
        print("Found cube", cube)

    except asyncio.TimeoutError:
        print("Didn't find a cube :-(")

    finally:
        # whether we find it or not, we want to stop the behavior
        look_around.stop()

    if cube is None:
        robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail)
        return

    print("Yay, found cube")

    cube.set_lights(cozmo.lights.green_light.flash())

    anim = robot.play_anim_trigger(cozmo.anim.Triggers.BlockReact)
    anim.wait_for_completed()


    action = robot.pickup_object(cube)
    print("got action", action)
    result = action.wait_for_completed(timeout=30)
    print("got action result", result)

    robot.turn_in_place(degrees(90)).wait_for_completed()

    action = robot.place_object_on_ground_here(cube)
    print("got action", action)
    result = action.wait_for_completed(timeout=30)
    print("got action result", result)

    anim = robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin)
    cube.set_light_corners(None, None, None, None)
    anim.wait_for_completed()

'''
cozmo.run_program(dock_with_cube)

