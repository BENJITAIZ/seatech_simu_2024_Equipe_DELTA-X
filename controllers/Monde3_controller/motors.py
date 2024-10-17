from meta_robot import Mavic2ProMeta
K_VERTICAL_THRUST = 68.5  # with this thrust, the drone lifts.
K_VERTICAL_OFFSET = 0.6   # Vertical offset where the robot actually targets to stabilize itself.
K_VERTICAL_P = 3.0        # P constant of the vertical PID.
K_ROLL_P = 50.0           # P constant of the roll PID.
K_PITCH_P = 30.0          # P constant of the pitch PID.


def clamp(value, value_min, value_max):
    return min(max(value, value_min), value_max)

class Motors:

    def __init__(self, robot:Mavic2ProMeta) -> None:
        self.robot = robot

        # Initialisation des moteurs
        self.front_left_motor = robot.getDevice('front left propeller')
        self.front_right_motor = robot.getDevice('front right propeller')
        self.rear_left_motor = robot.getDevice('rear left propeller')
        self.rear_right_motor = robot.getDevice('rear right propeller')

        # Configuration des moteurs pour le contrôle en vitesse
        self.front_left_motor.setPosition(float('inf'))
        self.front_right_motor.setPosition(float('inf'))
        self.rear_left_motor.setPosition(float('inf'))
        self.rear_right_motor.setPosition(float('inf'))

        # Valeur initiale de la poussée
        self.thrust = 70.0  # Ajustez cette valeur si nécessaire
        self.stabilized_thrust = 60.0  # Poussée stabilisée pour maintenir l'altitude

        self.target_altitude = 1.0

    def take_off(self):
        """Appliquer une poussée aux moteurs pour le décollage."""

        roll = self.robot.imu.getRollPitchYaw()[0]
        pitch = self.robot.imu.getRollPitchYaw()[1]
        altitude = self.robot.gps.getValues()[2]
        roll_velocity = self.robot.gyro.getValues()[0]
        pitch_velocity = self.robot.gyro.getValues()[1]


        roll_disturbance = 0.0
        pitch_disturbance = 0.0
        yaw_disturbance = 0.0

        # Compute the roll, pitch, yaw and vertical inputs.
        roll_input = K_ROLL_P * clamp(roll, -1.0, 1.0) + roll_velocity + roll_disturbance
        pitch_input = K_PITCH_P * clamp(pitch, -1.0, 1.0) + pitch_velocity + pitch_disturbance
        yaw_input = yaw_disturbance
        clamped_difference_altitude = clamp(self.target_altitude - altitude + K_VERTICAL_OFFSET, -1.0, 1.0)
        vertical_input = K_VERTICAL_P * pow(clamped_difference_altitude, 3.0)

        # Actuate the motors taking into consideration all the computed inputs.
        front_left_motor_input = K_VERTICAL_THRUST + vertical_input - roll_input + pitch_input - yaw_input
        front_right_motor_input = K_VERTICAL_THRUST + vertical_input + roll_input + pitch_input + yaw_input
        rear_left_motor_input = K_VERTICAL_THRUST + vertical_input - roll_input - pitch_input + yaw_input
        rear_right_motor_input = K_VERTICAL_THRUST + vertical_input + roll_input - pitch_input - yaw_input

        print(f"Applying thrust: {self.thrust}")  # Log de la valeur de poussée
        self.front_left_motor.setVelocity( front_left_motor_input)
        self.front_right_motor.setVelocity(-front_right_motor_input)
        self.rear_left_motor.setVelocity(-rear_left_motor_input)
        self.rear_right_motor.setVelocity( rear_right_motor_input)

    def up(self):
        self.target_altitude += 0.05

    def stabilize(self):
        """Stabiliser le drone à une altitude donnée."""
        self.front_left_motor.setVelocity(self.stabilized_thrust)
        self.front_right_motor.setVelocity(self.stabilized_thrust)
        self.rear_left_motor.setVelocity(self.stabilized_thrust)
        self.rear_right_motor.setVelocity(self.stabilized_thrust)

    def move(self, direction="forward"):
        """Déplacer le drone doucement dans une direction tout en maintenant l'altitude."""
        move_speed = 2.0  # Vitesse de déplacement, ajustez si nécessaire

        if direction == "forward":
            # Moteurs arrière tournent plus vite pour pousser le drone vers l'avant
            self.front_left_motor.setVelocity(self.stabilized_thrust - move_speed)
            self.front_right_motor.setVelocity(self.stabilized_thrust - move_speed)
            self.rear_left_motor.setVelocity(self.stabilized_thrust + move_speed)
            self.rear_right_motor.setVelocity(self.stabilized_thrust + move_speed)
        elif direction == "backward":
            # Moteurs avant tournent plus vite pour reculer
            self.front_left_motor.setVelocity(self.stabilized_thrust + move_speed)
            self.front_right_motor.setVelocity(self.stabilized_thrust + move_speed)
            self.rear_left_motor.setVelocity(self.stabilized_thrust - move_speed)
            self.rear_right_motor.setVelocity(self.stabilized_thrust - move_speed)
        elif direction == "left":
            # Moteurs droite tournent plus vite pour déplacer le drone vers la gauche
            self.front_left_motor.setVelocity(self.stabilized_thrust + move_speed)
            self.rear_left_motor.setVelocity(self.stabilized_thrust + move_speed)
            self.front_right_motor.setVelocity(self.stabilized_thrust - move_speed)
            self.rear_right_motor.setVelocity(self.stabilized_thrust - move_speed)
        elif direction == "right":
            # Moteurs gauche tournent plus vite pour déplacer le drone vers la droite
            self.front_left_motor.setVelocity(self.stabilized_thrust - move_speed)
            self.rear_left_motor.setVelocity(self.stabilized_thrust - move_speed)
            self.front_right_motor.setVelocity(self.stabilized_thrust + move_speed)
            self.rear_right_motor.setVelocity(self.stabilized_thrust + move_speed)

        print(f"Moving {direction}")
