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

robotsArray = {}
robotsImageArray = {}
robotsTextArray = {}

app = Window(language['titleMainWindow'], width, height)

app.getRoot().bind("<KeyPress>", key_pressed)
app.getRoot().bind("<KeyRelease>", key_released)
app.getRoot().resizable(False, False)

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

    pitchFrame = app.createFrame(0, 20, width, height / 2)
    camera1Frame = app.createFrame(0, height / 2, width / 2, height / 2, rwidth=0.5)
    camera2Frame = app.createFrame(width / 2, height / 2, width / 2, height / 2, rwidth=0.5)

    sc1 = app.createButton(camera1Frame, lambda: stopCameraStream(camera1Frame, cc1, sc1), text=language['stopCamera'])
    cc1 = app.createButton(camera1Frame, lambda: chooseCamera(app.getFrame(camera1Frame), cc1, sc1, camera1Frame),
                           text=language['ChooseCamera0'])
    app.placeButton(cc1, 2, 0.5, 0.5, CENTER)
    cc1.winfo_screenwidth()

    sc2 = app.createButton(camera2Frame, lambda: stopCameraStream(camera2Frame, cc2, sc2), text=language['stopCamera'])
    cc2 = app.createButton(camera2Frame, text=language['ChooseCamera1'],
                           command=lambda: chooseCamera(app.getFrame(camera2Frame), cc2, sc2, camera2Frame))
    app.placeButton(cc2, 2, 0.5, 0.5, CENTER)

    mainMenu = app.createMenu()
    app.addCommand(mainMenu, language['settings'], openSettingsWindow)
    app.addCommand(mainMenu, language['reloadConnections'], reloadMQTTConnection)
    app.configRoot(mainMenu)

    pitchCanvas = app.createCanvas(pitchFrame)

    pitchCanvas.config(width=pitchSize[1], height=pitchSize[0])

    app.placeCanvas(pitchCanvas, 2, 0.5, 0.5, CENTER)

    pitchImage = ImageTk.PhotoImage(Image.open("images/pitch_2.png").rotate(90, expand=True), Image.ANTIALIAS)

    pitchCanvas.background = pitchImage
    bg = pitchCanvas.create_image(pitchSize[1] // 2, pitchSize[0] // 2, image=pitchImage, anchor=CENTER)
    markerCalculator.setMainRobotId(settings['robot_name'])

    markerCalculator.setCanvas(pitchCanvas)  # Create marker drawer on canvas pitchCanvas

    client.loop_start()
    try:
        app.loop()
    except KeyboardInterrupt:
        print("KI")
        stopCameraStream(2, cc1, sc1)
        stopCameraStream(3, cc2, sc2)
    # /CREATE WINDOW
