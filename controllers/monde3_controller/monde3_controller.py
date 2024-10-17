from controller import Robot, Motor, Gyro, GPS, InertialUnit
from robot import Mavic2Pro

# Créer l'instance du robot (drone)
robot = Mavic2Pro()

# Boucle principale
robot.run()