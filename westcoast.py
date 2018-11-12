import math
import wpilib
import ctre
import seamonsters as sea

# rotate motor: 3138 ticks per rotation

class SwerveBot(sea.GeneratorBot):

    def robotInit(self):
        self.joystick = wpilib.Joystick(0)

        wheelATalon = ctre.WPI_TalonSRX(21)
        wheelBTalon = ctre.WPI_TalonSRX(22)

        for talon in [wheelATalon, wheelBTalon]:
            talon.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, 0)

        wheelA = sea.AngledWheel(wheelATalon, 1.0, 0.0, math.pi/2,
                                 encoderCountsPerFoot=31291.1352,
                                 maxVoltageVelocity=16)
        wheelB = sea.AngledWheel(wheelBTalon, -1.0, 0.0, math.pi/2,
                                 encoderCountsPerFoot=31291.1352,
                                 maxVoltageVelocity=16)

        self.superDrive = sea.SuperHolonomicDrive()
        self.superDrive.addWheel(wheelA)
        self.superDrive.addWheel(wheelB)

        for wheel in self.superDrive.wheels:
            wheel.driveMode = ctre.ControlMode.PercentOutput

    def teleop(self):
        # reset joystick buttons
        self.joystick.getRawButtonPressed(3)
        self.joystick.getRawButtonPressed(4)
        self.joystick.getRawButtonPressed(5)
        while True:
            mag = sea.deadZone(self.joystick.getY())
            mag *= 5 # maximum feet per second
            turn = sea.deadZone(self.joystick.getX())
            turn *= math.radians(300) # maximum radians per second

            self.superDrive.drive(mag, math.pi/2, turn)

            if self.joystick.getRawButtonPressed(4):
                print("PercentOutput mode")
                for wheel in self.superDrive.wheels:
                    if isinstance(wheel, sea.AngledWheel):
                        wheel.driveMode = ctre.ControlMode.PercentOutput
            if self.joystick.getRawButtonPressed(3):
                print("Velocity mode")
                for wheel in self.superDrive.wheels:
                    if isinstance(wheel, sea.AngledWheel):
                        wheel.driveMode = ctre.ControlMode.Velocity
            if self.joystick.getRawButtonPressed(5):
                print("Position mode")
                for wheel in self.superDrive.wheels:
                    if isinstance(wheel, sea.AngledWheel):
                        wheel.driveMode = ctre.ControlMode.Position

            yield

if __name__ == "__main__":
    wpilib.run(SwerveBot)
