from controller import Robot, Motor, Gyro, GPS, InertialUnit
from motors import Motors
from meta_robot import Mavic2ProMeta

 

class Mavic2Pro(Robot):

    def __init__(self):
        super().__init__()

        # Temps de simulation
        self.timestep = int(self.getBasicTimeStep())

        # Initialiser les capteurs
        self.gyro = self.getDevice('gyro')
        self.gyro.enable(self.timestep)

        self.gps = self.getDevice('gps')
        self.gps.enable(self.timestep)

        self.imu = self.getDevice('inertial unit')  
        self.imu.enable(self.timestep)

        # Initialisation des moteurs
        self.motors = Motors(self)

    def run(self):
        """Boucle principale pour piloter le drone."""
        while self.step(self.timestep) != -1:
            # Appeler la méthode de décollage
            self.motors.take_off()
            self.motors.up()