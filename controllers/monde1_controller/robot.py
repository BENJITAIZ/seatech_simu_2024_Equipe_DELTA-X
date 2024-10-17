from controller import Robot, Motor

class Motors:
    def __init__(self, robot):
        self.left_wheel: Motor = robot.getDevice('left wheel')
        self.right_wheel: Motor = robot.getDevice('right wheel')

        self.left_wheel.setPosition(float('inf'))
        self.right_wheel.setPosition(float('inf'))

        self.left_wheel.setVelocity(0.0)
        self.right_wheel.setVelocity(0.0)

    def avancer(self): 
        self.left_wheel.setVelocity(10.0)
        self.right_wheel.setVelocity(10.0)

    def tourner_gauche(self, speed=2.0): 
        self.left_wheel.setVelocity(-speed) 
        self.right_wheel.setVelocity(speed) 

    def tourner_droite(self, speed=2.0): 
        self.left_wheel.setVelocity(speed)
        self.right_wheel.setVelocity(-speed) 

    def stop(self):
        self.left_wheel.setVelocity(0.0)
        self.right_wheel.setVelocity(0.0)

class Pioneer3dx(Robot):
    def __init__(self):
        super().__init__()
        self.timestep = int(self.getBasicTimeStep())
        self.motors = Motors(self)

        self.distance_sensors = []
        self.sensor_names = [
        'so0', 'so1', 'so2', 'so3', 'so4', 'so5', 'so6', 'so7'
        ]
 
        for sensor_name in self.sensor_names:
            sensor = self.getDevice(sensor_name)
            sensor.enable(self.timestep)
            self.distance_sensors.append(sensor)

    def get_sensor_values(self):
        return [sensor.getValue() for sensor in self.distance_sensors]

    def run(self):
        while self.step(self.timestep) != -1:
            sensor_values = self.get_sensor_values()

            obstacle_threshold = 875.0 

            front_obstacle = any(value > obstacle_threshold for value in sensor_values)

            if front_obstacle:
                if sensor_values[6] > obstacle_threshold or sensor_values[7] > obstacle_threshold: 
                    self.motors.tourner_gauche()
                else:
                    self.motors.tourner_droite()
            else:
                self.motors.avancer()