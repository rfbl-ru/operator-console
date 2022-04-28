# /
# Консоль оператора для управления луноходами.
# Возможности:
# Отображения роботов и мяча на поле
# Просмотрел камер с поля/робота
# Управление роботом путём нажатия на клавиши клавиатуры
# Программирование клавиш
#
# #


from functions import *
import pyautogui
import vars

# robotsArray = {}
# robotsImageArray = {}
# robotsTextArray = {}

app = Window(language['titleMainWindow'], width, height)

app.getRoot().bind("<KeyPress>", keyPressed)
app.getRoot().bind("<KeyRelease>", keyReleased)
app.getRoot().resizable(True, True)

if __name__ == '__main__':
    createMQTTConnection()

    # CREATE WINDOW
    width_, height_ = pyautogui.size()
    if width_ < 1300 or height_ < 800:
        width = width_ - 100
        height = height_ - 100
        app.getRoot().geometry("{}x{}".format(width, height))
    vars.statusVariable = StringVar()
    statusFrame = app.createFrame(0, 0, 100, 20)
    statusLabel = app.createLabel(statusFrame, foreground='#000', font="Arial 8")
    app.placeLabel(statusLabel, 1, 0, 0)
    statusLabel.configure(textvariable=vars.statusVariable)

    pitchFrame_1 = app.createFrame(0, 20, width / 2, height / 2)
    pitchFrame_2 = app.createFrame(width / 2, 20, width, height / 2)
    camera1Frame = app.createFrame(0, height / 2, width / 2, height / 2, rwidth=0.5)
    camera2Frame = app.createFrame(width / 2, height / 2, width / 2, height / 2, rwidth=0.5)

    sc1 = app.createButton(camera1Frame, lambda: stopCameraStream(0, cc1, sc1), text=language['stopCamera'])
    cc1 = app.createButton(camera1Frame, lambda: chooseCamera(app.getFrame(camera1Frame), cc1, sc1, 0),
                           text=language['ChooseCamera0'])
    app.placeButton(cc1, 2, 0.5, 0.5, CENTER)
    cc1.winfo_screenwidth()

    sc2 = app.createButton(camera2Frame, lambda: stopCameraStream(1, cc2, sc2), text=language['stopCamera'])
    cc2 = app.createButton(camera2Frame, text=language['ChooseCamera1'],
                           command=lambda: chooseCamera(app.getFrame(camera2Frame), cc2, sc2, 1))
    app.placeButton(cc2, 2, 0.5, 0.5, CENTER)

    mainMenu = app.createMenu()
    app.addCommand(mainMenu, language['settings'], openSettingsWindow)
    app.addCommand(mainMenu, language['reloadConnections'], reloadMQTTConnection)
    app.configRoot(mainMenu)

    pitchCanvas_1 = app.createCanvas(pitchFrame_1)
    pitchCanvas_2 = app.createCanvas(pitchFrame_2)

    pitchCanvas_1.config(width=pitchSize[1], height=pitchSize[0])
    pitchCanvas_2.config(width=pitchSize[1], height=pitchSize[0])

    # app.placeCanvas(pitchCanvas, 2, 0.5, 0.5, CENTER)
    app.placeCanvas(pitchCanvas_1, 1, width / 4, 0, CENTER)
    app.placeCanvas(pitchCanvas_2, 1, width / 10, 0, CENTER)

    pitchImage = ImageTk.PhotoImage(Image.open("images/pitch_2.png").rotate(90, expand=True), Image.ANTIALIAS)

    pitchCanvas_1.background = pitchImage
    pitchCanvas_2.background = pitchImage
    bg_1 = pitchCanvas_1.create_image(pitchSize[1] // 2, pitchSize[0] // 2, image=pitchImage, anchor=CENTER)
    bg_2 = pitchCanvas_2.create_image(pitchSize[1] // 2, pitchSize[0] // 2, image=pitchImage, anchor=CENTER)
    markerCalculator_1.setMainRobotId(settings['robot_name'])
    markerCalculator_2.setMainRobotId(settings['robot_name'])

    markerCalculator_1.setCanvas(pitchCanvas_1)  # Create marker drawer on canvas pitchCanvas
    markerCalculator_2.setCanvas(pitchCanvas_2)  # Create marker drawer on canvas pitchCanvas

    client.loop_start()
    try:
        app.loop()
    except KeyboardInterrupt:
        print("KI")
        stopCameraStream(2, cc1, sc1)
        stopCameraStream(3, cc2, sc2)
    # /CREATE WINDOW
