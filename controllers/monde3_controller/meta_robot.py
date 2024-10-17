from controller import Robot, Gyro, GPS, InertialUnit

class Mavic2ProMeta(Robot):

    imu:InertialUnit = None
    gps:GPS = None
    gyro:Gyro = None