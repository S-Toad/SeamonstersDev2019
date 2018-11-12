import wpilib

class Pneumatics(wpilib.IterativeRobot):

    def robotInit(self):
        self.pneu = wpilib.Solenoid(0)
        self.joystick = wpilib.Joystick(0)

    def teleopPeriodic(self):
        if self.joystick.getRawButton(1):
            self.pneu.set(True)
        if self.joystick.getRawButton(2):
            self.pneu.set(False) 

if __name__ == "__main__":
    wpilib.run(Pneumatics, physics_enabled = True)