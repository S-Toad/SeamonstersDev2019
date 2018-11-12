import math
import remi.gui as gui
import seamonsters as sea

class SwerveBotDashboard(sea.Dashboard):

    def main(self, robot, appCallback):
        self.robot = robot

        root = gui.VBox(width=600)

        self.fieldWidth = 500
        self.fieldHeight = 450
        self.fieldSvg = gui.Svg(self.fieldWidth, self.fieldHeight)
        root.append(self.fieldSvg)
        self.arrow = gui.SvgPolyline()
        self.fieldSvg.append(self.arrow)
        self.arrow.add_coord(0, 0)
        self.arrow.add_coord(30, 30)
        self.arrow.add_coord(-30, 30)
        self.arrow.style['fill'] = 'gray'

        self._c_resetPosition(None)

        resetButton = gui.Button("Reset")
        resetButton.set_on_click_listener(self._c_resetPosition)
        root.append(resetButton)

        appCallback(self)
        return root

    def moveRobot(self, magnitude, direction, turn):
        self.robotX += magnitude * math.cos(direction + self.robotAngle) * 50.0
        self.robotY -= magnitude * math.sin(direction + self.robotAngle) * 50.0
        self.robotAngle += turn
        self.updateRobotPosition()

    def _c_resetPosition(self, button):
        self.robotX = self.fieldWidth / 2
        self.robotY = self.fieldHeight / 2
        self.robotAngle = 0
        self.updateRobotPosition()

    def updateRobotPosition(self):
        self.arrow.attributes['transform'] = "translate(%s,%s) rotate(%s)" \
            % (self.robotX, self.robotY, -math.degrees(self.robotAngle))
