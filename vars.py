import json

with open('data/language.json', 'r+', encoding='utf-8') as f:
    language = json.load(f)

with open('data/camsConfig.json', 'r+', encoding='utf-8') as f:
    camConfig = json.load(f)

with open('data/keyboard.json', 'r+', encoding='utf-8') as f:
    keyboard = json.load(f)

with open('data/settings.json', 'r+', encoding='utf-8') as f:
    settings = json.load(f)


topicRoot = "MIPT-SportRoboticsClub/LunokhodFootball/RawARUCO/#"
topicBall = "MIPT-SportRoboticsClub/LunokhodFootball/Ball"
topicRobot = "MIPT-SportRoboticsClub/LunokhodFootball/Robots/"
topicInternalCommands = "MIPT-SportRoboticsClub/LunokhodFootball/Internal/{0}"
topicInternalData = "MIPT-SportRoboticsClub/LunokhodFootball/Data/{0}"
topicLines = "MIPT-SportRoboticsClub/LunokhodFootball/PitchLines"

pitchCornerIdList = [10, 20, 30, 40]
robotIdList = [11, 12, 13, 14, 15, 16]
pitchSize = (336, 238)
cameraResolution = (195, 293)
width, height = 1280, 720
cameraCount = 2

statusVariable = None

zm_pattern = "http://{0}/zm/cgi-bin/nph-zms?scale=100&width=640px&height=480px&mode=jpeg&maxfps=30&monitor={" \
             "1}&connkey={2}&user={3}&pass={4}"
