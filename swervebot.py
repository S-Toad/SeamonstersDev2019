import math
import wpilib
import ctre
import seamonsters as sea
import swervebot_app

# rotate motor: 3138 ticks per rotation

class SwerveBot(sea.GeneratorBot):

    def robotInit(self):
        self.joystick = wpilib.Joystick(0)

        wheelADriveTalon = ctre.WPI_TalonSRX(1)
        wheelARotateTalon = ctre.WPI_TalonSRX(0)

        wheelBDriveTalon = ctre.WPI_TalonSRX(3)
        wheelBRotateTalon = ctre.WPI_TalonSRX(2)

        wheelCDriveTalon = ctre.WPI_TalonSRX(5)
        wheelCRotateTalon = ctre.WPI_TalonSRX(4)

        for talon in [wheelADriveTalon, wheelARotateTalon,
                      wheelBDriveTalon, wheelBRotateTalon,
                      wheelCDriveTalon, wheelCRotateTalon]:
            talon.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, 0)

        wheelADrive = sea.AngledWheel(wheelADriveTalon, .75, .75, 0,
                                      encoderCountsPerFoot=31291.1352,
                                      maxVoltageVelocity=16)
        wheelBDrive = sea.AngledWheel(wheelBDriveTalon, -.75, .75, 0,
                                      encoderCountsPerFoot=31291.1352,
                                      maxVoltageVelocity=16)        
        wheelCDrive = sea.AngledWheel(wheelCDriveTalon, 0, -.75, 0,
                                      encoderCountsPerFoot=31291.1352,
                                      maxVoltageVelocity=16)

        wheelARotate = sea.SwerveWheel(wheelADrive, wheelARotateTalon,
                                       1612.8, True)
        wheelBRotate = sea.SwerveWheel(wheelBDrive, wheelBRotateTalon,
                                       1612.8, True)
        wheelCRotate = sea.SwerveWheel(wheelCDrive, wheelCRotateTalon,
                                       1680, True) # 1670, 1686, 1680
        self.superDrive = sea.SuperHolonomicDrive()
        sea.setSimulatedDrivetrain(self.superDrive)

        for wheelrotate in [wheelARotate, wheelBRotate, wheelCRotate]:
            self.superDrive.addWheel(wheelrotate)

        for wheel in self.superDrive.wheels:
            wheel.driveMode = ctre.ControlMode.PercentOutput

        self.robotOrigin = None

        self.app = None
        sea.startDashboard(self, swervebot_app.SwerveBotDashboard)

    def teleop(self):
        if self.app is not None:
            self.app.clearEvents()
        # reset joystick buttons
        self.joystick.getRawButtonPressed(3)
        self.joystick.getRawButtonPressed(4)
        self.joystick.getRawButtonPressed(5)
        while True:
            if self.app is not None:
                self.app.doEvents()

            mag = sea.deadZone(self.joystick.getMagnitude())
            mag *= 3 # maximum feet per second
            direction = -self.joystick.getDirectionRadians() - math.pi/2
            turn = sea.deadZone(self.joystick.getRawAxis(3))
            turn *= math.radians(120) # maximum radians per second

            self.superDrive.drive(mag, direction, turn)

            if self.app is not None:
                moveMag, moveDir, moveTurn, self.robotOrigin = \
                    self.superDrive.getRobotPositionOffset(self.robotOrigin)
                self.app.moveRobot(moveMag, moveDir, moveTurn)

            if self.joystick.getRawButtonPressed(4):
                print("PercentOutput mode")
                for wheel in self.superDrive.wheels:
                    if isinstance(wheel, sea.SwerveWheel):
                        wheel.angledWheel.driveMode = ctre.ControlMode.PercentOutput
            if self.joystick.getRawButtonPressed(3):
                print("Velocity mode")
                for wheel in self.superDrive.wheels:
                    if isinstance(wheel, sea.SwerveWheel):
                        wheel.angledWheel.driveMode = ctre.ControlMode.Velocity
            if self.joystick.getRawButtonPressed(5):
                print("Position mode")
                for wheel in self.superDrive.wheels:
                    if isinstance(wheel, sea.SwerveWheel):
                        wheel.angledWheel.driveMode = ctre.ControlMode.Position

            yield

if __name__ == "__main__":
    wpilib.run(SwerveBot)
