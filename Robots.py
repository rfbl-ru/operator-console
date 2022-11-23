from vars import *
from math import atan, degrees
from PIL import Image, ImageTk

robotImage = Image.open("images/robotIcon.png")
robotMainImage = Image.open("images/robotIconMain.png")
robotTeammateImage = Image.open("images/robotTeammateIcon.png")


def centroid(vertexes):
    _x_list = [vertex[0] for vertex in vertexes]
    _y_list = [vertex[1] for vertex in vertexes]
    _len = len(vertexes)
    _x = sum(_x_list) / _len
    _y = sum(_y_list) / _len
    return (_x, _y)


def mapp(n, a1, a2, b1, b2):
    return (n - a1) * (b2 - b1) / (a2 - a1) + b1


class Robots:
    markerIdList = []

    def __init__(self):
        self.ball = None
        self.canvas = None
        self.oldMarkerIdList = []
        self.pitchCornerIdList = pitchCornerIdList
        self.robotsIdList = robotIdList
        self.camsData = [None] * cameraCount
        self.mainRobotId = -1
        self.opponents = []
        self.teammates = []
        self.pitchSize = pitchSize
        self.cameraResolution = cameraResolution
        self.oldMarkerIdList = []
        self.markerIdList = []
        self.lines = []
        self.balls = []

        self.robotsArray = {}
        self.robotsImageArray = {}
        self.robotsTextArray = {}

        self.pitchMarkersArray = {}
        self.pitchTextArray = {}
        self.pitchMarkerLeftCorner = {}

    def setCanvas(self, canvas):
        self.canvas = canvas
        self.ball = self.canvas.create_oval(0, 0, 10, 10, fill='red')

    def setMainRobotId(self, id_):
        self.mainRobotId = id_

    def setTeams(self, t):
        self.teammates = t

    def updateMarkers(self, topic, data, param_2='aruco'):
        if topic.__contains__(param_2):
            count, markerIdList, markersData = self.calculateMarkers(data)
            camId = int(data['camId'])
            self.drawMarkers(count, markerIdList, markersData, camId)

    def calculateMarkers(self, data):
        markersData = []
        self.markerIdList.clear()
        if data['count'] > 0:
            for marker in data['markers']:
                self.markerIdList.append(marker['marker-id'])
                try:
                    self.oldMarkerIdList.remove(marker['marker-id'])
                except ValueError:
                    pass
                aruco_center = centroid(((marker['corners']['1']['x'], marker['corners']['1']['y']),
                                         (marker['corners']['2']['x'], marker['corners']['2']['y']),
                                         (marker['corners']['3']['x'], marker['corners']['3']['y']),
                                         (marker['corners']['4']['x'], marker['corners']['4']['y'])
                                         ))
                coordsX = mapp(aruco_center[0], 0, self.cameraResolution[0], 0, self.pitchSize[1])
                coordsY = mapp(aruco_center[1], 0, self.cameraResolution[1], 0, self.pitchSize[0])
                leftCornerX = mapp(marker['corners']['1']['x'], 0, self.cameraResolution[0], 0, self.pitchSize[1])
                leftCornerY = mapp(marker['corners']['1']['y'], 0, self.cameraResolution[1], 0, self.pitchSize[0])
                rightCornerX = mapp(marker['corners']['2']['x'], 0, self.cameraResolution[0], 0, self.pitchSize[1])
                rightCornerY = mapp(marker['corners']['2']['y'], 0, self.cameraResolution[1], 0, self.pitchSize[0])
                try:
                    angle = degrees(atan((rightCornerY - leftCornerY) / (rightCornerX - leftCornerX)))
                except ZeroDivisionError:
                    angle = 90
                localCoordinateX1 = leftCornerX - coordsX
                localCoordinateY1 = leftCornerY - coordsY
                localCoordinateX2 = rightCornerX - coordsX
                localCoordinateY2 = rightCornerY - coordsY
                if (localCoordinateX1 < 0 and localCoordinateY1 < 0 and localCoordinateX2 < 0 and localCoordinateY2 > 0 and -45 < angle < 90) or \
                        (localCoordinateX1 < 0 and localCoordinateY1 > 0 and localCoordinateX2 > 0 and localCoordinateY2 > 0) or \
                        (localCoordinateX1 > 0 and localCoordinateY1 > 0 and localCoordinateX2 > 0 and localCoordinateY2 < 0 and -90 < angle < 0):
                    angle = angle - 180
                angle = abs(360 - angle)
                if marker['marker-id'] not in self.pitchCornerIdList:
                    markerData = [marker['marker-id'], angle, [coordsX, coordsY]]
                else:
                    markerData = [marker['marker-id'], [coordsX, coordsY]]
                markersData.append(markerData)
        return data['count'], self.markerIdList, markersData

    def drawMarkers(self, count, markerIdList, markersData, camId):
        if count > 0:
            for marker in markersData:
                if marker[0] in self.pitchCornerIdList:
                    try:
                        self.canvas.coords(self.pitchMarkersArray[marker[0] - 1], marker[1][0] - 10, marker[1][1] - 10,
                                           marker[1][0] + 10, marker[1][1] + 10)
                        self.canvas.coords(self.pitchTextArray[marker[0] - 1], marker[1][0], marker[1][1])
                    except KeyError:
                        self.pitchMarkersArray[marker[0] - 1] = self.canvas.create_rectangle((0, 0, 0, 0))
                        self.pitchTextArray[marker[0] - 1] = self.canvas.create_text(0, 0, text=marker[0])
                else:
                    robotImage_ = robotImage
                    if marker[0] == int(self.mainRobotId):
                        robotImage_ = robotMainImage

                    if str(marker[0]) in self.teammates:
                        robotImage_ = robotTeammateImage

                    try:
                        self.robotsImageArray[marker[0] - 1] = ImageTk.PhotoImage(robotImage_.rotate(-marker[1]))
                        self.robotsArray[marker[0] - 1] = self.canvas.create_image(238 - marker[2][0], marker[2][1],
                                                                                   image=self.robotsImageArray[
                                                                                       marker[0] - 1])
                        self.canvas.coords(self.robotsTextArray[marker[0] - 1], 238 - marker[2][0], marker[2][1])
                    except KeyError:
                        self.robotsArray[marker[0] - 1] = self.canvas.create_image(238 - marker[2][0], marker[2][1],
                                                                                   image=self.robotsImageArray[
                                                                                       marker[0] - 1])
                        self.robotsImageArray[marker[0] - 1] = ImageTk.PhotoImage(robotImage_.rotate(-marker[1]))
                        self.robotsTextArray[marker[0] - 1] = self.canvas.create_text(238 - marker[2][0], marker[2][1],
                                                                                      text=marker[0])

            self.clearOldMarkers(markerIdList, camId)
            if self.camsData[camId - 1] is not None:
                self.camsData[camId - 1].clear()
            self.camsData[camId - 1] = markerIdList.copy()
        else:
            # self.clearOldMarkers(markerIdList, camId)
            pass

    def clearOldMarkers(self, markerIdList, camId):
        if self.camsData[camId - 1] is not None:
            try:
                for marker in markerIdList:
                    self.camsData[camId - 1].remove(marker)
            except ValueError:
                pass
            except AttributeError:
                pass
            except TypeError:
                pass

            for marker in self.camsData[camId - 1]:
                if marker in pitchCornerIdList:
                    self.canvas.coords(self.pitchMarkersArray[marker - 1], 0, 0, 0, 0)
                    self.canvas.coords(self.pitchTextArray[marker - 1], 0, 0)
                else:
                    self.canvas.delete(self.robotsArray[marker - 1], 0, 0)
                    self.canvas.coords(self.robotsTextArray[marker - 1], 0, 0)
        else:
            print(camId, "None")

    def calculateBall(self, data):
        if data['ball'] != 'None':
            ballX = mapp(data['ball']['center']['x'], 0, cameraResolution[0], 0, pitchSize[1])
            ballY = mapp(data['ball']['center']['y'], 0, cameraResolution[1], 0, pitchSize[0])
        else:
            ballX = 0
            ballY = 0

        return ballX, ballY

    def drawBall(self, ballX, ballY):
        if ballX != 0 and ballY != 0:
            self.canvas.coords(self.ball, ballX - 5, ballY - 5, ballX + 5, ballY + 5)
        else:
            self.canvas.coords(self.ball, 0, 0, 0, 0)

    def drawAllBalls(self, data):
        if len(self.balls) > 0:
            for ball in self.balls:
                self.canvas.delete(ball)
        if data['ball'] != 'None':
            for ball in data['ball']:
                ballX = mapp(195 - ball['center']['x'], 0, cameraResolution[0], 0, pitchSize[1])
                ballY = mapp(ball['center']['y'], 0, cameraResolution[1], 0, pitchSize[0])
                # self.ball = self.canvas.create_oval(0, 0, 10, 10, fill='red')
                ball_ = self.canvas.create_oval(ballX, ballY, ballX + 10, ballY + 10, fill='red')
                self.balls.append(ball_)

    def drawLines(self, points):
        if len(self.lines) > 0:
            for line in self.lines:
                self.canvas.delete(line)

        for i_ in range(len(points) - 1):
            line_ = self.canvas.create_line(points[i_][0], points[i_][1], points[i_ + 1][0], points[i_ + 1][1],
                                            width=3, fill="white")
            self.lines.append(line_)
