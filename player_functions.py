import random
import threading

from Window import *
from PIL import ImageTk, Image
from vars import *
import cv2
import imutils
from imutils.video import VideoStream
import time

popup_init = False
players = [None, None]
stopEvents = [threading.Event(), threading.Event()]
playerThreading = [None, None]
playersFrame = [None, None]
videoStreams = [None, None]


def on_close(root):
    global popup_init
    popup_init = False
    root.destroy()


def chooseCamera(frame, changeBtn, stopBtn, cameraNum):
    global popup_init
    if not popup_init:
        chooseCameraWindow = Window(language['titleChoosingWindow'], pitchSize[0], pitchSize[1], topLevel=1)
        chooseCameraRoot = chooseCameraWindow.getRoot()
        chooseCameraRoot.protocol("WM_DELETE_WINDOW", lambda: on_close(chooseCameraRoot))
        chooseCameraRoot.resizable(False, False)
        chooseCameraRoot.attributes("-topmost", True)
        chooseCameraFrame = chooseCameraWindow.createFrame(0, 0, pitchSize[0], pitchSize[1], rwidth=0)

        chooseCameraCanvas = chooseCameraWindow.createCanvas(chooseCameraFrame)
        chooseCameraCanvas.config(width=pitchSize[0], height=pitchSize[1])
        chooseCameraWindow.placeCanvas(chooseCameraCanvas, 2, 0.5, 0.5)

        pitchImage = ImageTk.PhotoImage(Image.open("images/pitch_1.png"), Image.ANTIALIAS)

        chooseCameraCanvas.background = pitchImage
        chooseCameraCanvas.create_image(pitchSize[0] / 2, pitchSize[1] / 2, image=pitchImage, anchor=CENTER)

        cameraImage = PhotoImage(file="images/cctv-camera.png")

        with open('data/camsConfig.json', 'r+', encoding='utf-8') as f:
            camConfig_ = json.load(f)

        for camera in camConfig_:
            video_host = zm_pattern.format(settings['zm_host'], camera['address'], random.randint(1000, 100000),
                                           settings['zm_login'], settings['zm_pass'])
            btn = chooseCameraWindow.createButton(chooseCameraFrame,
                                                  lambda address=video_host: onCameraSet(frame, address,
                                                                                         chooseCameraRoot,
                                                                                         changeBtn,
                                                                                         stopBtn, cameraNum),
                                                  image=cameraImage)
            btn.image = cameraImage
            chooseCameraWindow.placeButton(btn, 1, x=camera['x'], y=camera['y'])

        popup_init = True


def reloadCameraData(cameraNum):
    stopEvents[cameraNum].set()
    videoStreams[cameraNum].stop()
    videoStreams[cameraNum] = None
    players[cameraNum].place_forget()
    players[cameraNum] = None
    playersFrame[cameraNum].place_forget()


def stopCameraStream(cameraNum, changeBtn, stopBtn):
    cameraNum -= 2
    reloadCameraData(cameraNum)
    stopBtn.place_forget()
    changeBtn.place_forget()
    changeBtn.place(relx=0.5, rely=0.5)


def onCameraSet(frame, address, root, changeBtn, stopBtn, cameraNum):
    cameraNum -= 2
    global popup_init
    popup_init = False

    if videoStreams[cameraNum] is not None:
        reloadCameraData(cameraNum)
    playersFrame[cameraNum] = Frame(frame, width=width / 2, height=(height / 2) - changeBtn.winfo_height(), bg="black")
    playersFrame[cameraNum].place(x=0, y=30)
    stopEvents[cameraNum] = threading.Event()

    playerThreading[cameraNum] = threading.Thread(target=videoLoop, args=(cameraNum, address,
                                                                          stopEvents[cameraNum],
                                                                          stopBtn, changeBtn))
    playerThreading[cameraNum].start()

    changeBtn.place_forget()
    changeBtn.place(relx=0, rely=0)
    stopBtn.place(relx=0.90, rely=0)
    root.destroy()


def videoLoop(cameraNum, address, stopEvent, stopBtn_, changeBtn_):
    global videoStreams
    videoStreams[cameraNum] = VideoStream(src=address, usePiCamera=False).start()
    try:
        while not stopEvent.is_set():
            frame = videoStreams[cameraNum].read()

            frame = imutils.resize(frame, width=640, height=335)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            if players[cameraNum] is None:
                players[cameraNum] = Label(playersFrame[cameraNum], image=image)
                players[cameraNum].image = image
                players[cameraNum].place(x=0, y=0)

            else:
                players[cameraNum].configure(image=image)
                players[cameraNum].image = image
            time.sleep(0.01)


    except RuntimeError:
        print("[INFO] caught a RuntimeError")
        stopCameraStream(cameraNum, changeBtn_, stopBtn_)
    except Exception as e:
        print("Camera disconnected: " + str(e))
        stopCameraStream(cameraNum, changeBtn_, stopBtn_)
