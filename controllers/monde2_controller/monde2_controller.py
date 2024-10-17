"""monde2_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, RangeFinder

class RosBot(Robot):
    front_left_wheel = None
    front_right_wheel = None
    rear_left_wheel = None
    rear_right_wheel = None

    def __init__(self):
        super().__init__()
        self.front_left_wheel:Motor = self.getDevice('fl_wheel_joint')
        self.front_right_wheel:Motor = self.getDevice('fr_wheel_joint')

        self.rear_left_wheel:Motor = self.getDevice('rl_wheel_joint')
        self.rear_right_wheel:Motor = self.getDevice('rr_wheel_joint')

        self.front_left_wheel.setPosition(float('inf'))
        self.front_right_wheel.setPosition(float('inf'))

        self.rear_left_wheel.setPosition(float('inf'))
        self.rear_right_wheel.setPosition(float('inf'))

        self.front_left_wheel.setVelocity(0.0)
        self.front_right_wheel.setVelocity(0.0)

        self.rear_left_wheel.setVelocity(0.0)
        self.rear_right_wheel.setVelocity(0.0)

        self.camera:RangeFinder = self.getDevice('camera depth')
        self.camera.enable(int(self.getBasicTimeStep()))

    def count_black_pixels(self, zone):
        black_pixel = 0
        seuil = 1  

        for row in zone:
            for pixel in row:
                if pixel < seuil:
                    black_pixel += 1

        return black_pixel
    
    def image(self):
        matrice = self.camera.getRangeImageArray()
        matrice = matrice[0:240]
        height = len(matrice)
        width = len(matrice[0])

        left_zone = [row[:width // 3] for row in matrice]
        center_zone = [row[width // 3 : 2 * width // 3] for row in matrice]
        right_zone = [row[2 * width // 3:] for row in matrice]

        # print(f"zone_gauche:{left_zone}\n")
        # print(f"zone_centre:{center_zone}\n")
        # print(f"zone_droite:{right_zone}\n")

        left_pixels = self.count_black_pixels(left_zone)
        center_pixels = self.count_black_pixels(center_zone)
        right_pixels = self.count_black_pixels(right_zone)


        print(f"pixels_gauche:{left_pixels}\n")
        print(f"pixels_centre:{center_pixels}\n")
        print(f"pixels_droit:{right_pixels}\n")
        
        return left_pixels, center_pixels, right_pixels

    def run(self):
        
        left_pixels, center_pixels, right_pixels = self.image()

        
        if center_pixels > 100:
            if left_pixels < right_pixels:
                self.front_left_wheel.setVelocity(-5.0)
                self.front_right_wheel.setVelocity(5.0)
                self.rear_left_wheel.setVelocity(-5.0)
                self.rear_right_wheel.setVelocity(5.0)
            else:
                self.front_left_wheel.setVelocity(5.0)
                self.front_right_wheel.setVelocity(-5.0)
                self.rear_left_wheel.setVelocity(5.0)
                self.rear_right_wheel.setVelocity(-5.0)
        elif left_pixels > 100:
            if center_pixels < right_pixels:
                self.front_left_wheel.setVelocity(10.0)
                self.front_right_wheel.setVelocity(10.0)
                self.rear_left_wheel.setVelocity(10.0)
                self.rear_right_wheel.setVelocity(10.0)
            else:
                self.front_left_wheel.setVelocity(5.0)
                self.front_right_wheel.setVelocity(-5.0)
                self.rear_left_wheel.setVelocity(5.0)
                self.rear_right_wheel.setVelocity(-5.0)
        elif right_pixels > 100:  
            if center_pixels < left_pixels:
                self.front_left_wheel.setVelocity(10.0)
                self.front_right_wheel.setVelocity(10.0)
                self.rear_left_wheel.setVelocity(10.0)
                self.rear_right_wheel.setVelocity(10.0)
            else:
                self.front_left_wheel.setVelocity(-5.0)
                self.front_right_wheel.setVelocity(5.0)
                self.rear_left_wheel.setVelocity(-5.0)
                self.rear_right_wheel.setVelocity(5.0)
        else:
            self.front_left_wheel.setVelocity(10.0)
            self.front_right_wheel.setVelocity(10.0)
            self.rear_left_wheel.setVelocity(10.0)
            self.rear_right_wheel.setVelocity(10.0)

# create the Robot instance.
robot = RosBot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:

#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    robot.run()
    pass

# Enter here exit cleanup code.












        


   

    


