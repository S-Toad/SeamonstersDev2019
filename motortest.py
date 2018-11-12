import wpilib
import ctre
import seamonsters as sea
import motortest_app

class MotorTestBot(sea.GeneratorBot):

    def robotInit(self):
        self.talons = { } # dictionary, maps talon number to WPI_TalonSRX object

        self.joy = wpilib.Joystick(0)
        self.app = None
        sea.startDashboard(self, motortest_app.MotorTester)

    def teleop(self):
        while self.app is None:
            yield
        self.app.clearEvents()
        self._setTalonNumber(int(self.app.talonBox.get_value()))
        while True:
            yield
            self.app.doEvents()
            self.updateTalonLog()

    def _setTalonNumber(self, n):
        if n in self.talons:
            self.talon = self.talons[n]
        else:
            self.talon = ctre.WPI_TalonSRX(n)
            self.talon.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, 0)
            self.talons[n] = self.talon

    def c_setTalon(self, widget, value):
        self.talon.disable()
        self._setTalonNumber(int(value))

    def c_updateDisabled(self):
        self.talon.disable()

    def c_updatePercentOutput(self, widget, value=None):
        value = float(widget.get_value()) / 100.0
        self.talon.set(ctre.ControlMode.PercentOutput, value)

    def c_updateVelocity(self, widget, value, slider, scaleBox):
        value = float(slider.get_value()) * float(scaleBox.get_value()) / 100.0
        self.talon.set(ctre.ControlMode.Velocity, value)

    def c_updatePosition(self, button, spinBox):
        value = self.talon.getSelectedSensorPosition(0) + \
                int(spinBox.get_value())
        self.talon.set(ctre.ControlMode.Position, value)

    def updateTalonLog(self):
        talon = self.talon
        try:
            self.app.selectedTalonLbl.set_text(
                str(talon.getDeviceID()))
            self.app.outputVoltageLbl.set_text(
                str(talon.getMotorOutputVoltage()))
            self.app.outputCurrentLbl.set_text(
                str(talon.getOutputCurrent()))
            self.app.encoderPositionLbl.set_text(
                str(talon.getSelectedSensorPosition(0)))
            self.app.encoderVelocityLbl.set_text(
                str(talon.getSelectedSensorVelocity(0)))
        except AssertionError:
            pass

if __name__ == "__main__":
    wpilib.run(MotorTestBot)
