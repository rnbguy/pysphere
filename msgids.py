CONNECT = 257
DISCONNECT = 258
GET_SERIAL_NO = 4097
GET_WIFI = 1539
GET_TCP = 261  # {"msg_id":261,"param":"192.168.42.2","token":3,"type":"TCP"}
GET_CAMERA = 4365
SET_DATE = 6147  # {"msg_id":6147,"param":"2017-12-16-12-00-04-6","token":3}
GET_SD = 4358
GET_DEVICE = 4364
CHANGE_DIRECTORY = 1283  # {"msg_id":1283,"param":"/tmp/SD0/DCIM/","token":2}
LIST_DIRECTORY = 1282
SET_GPS = 4917  # alt, lat, lon

SWITCH_MODE = 4611  # 1 for camera, 0 for recorder
SET_TIMER = 4866  # 0, 3, 4, 5, 6, 7, 8, 9, 10
SET_INTERVALOMETER = 4929  # 0, 2, 5, 10, 30, 60, 120, 300
SET_BRACKETING = 4918  # if +-x on app, param = 2 * x

SET_BUZZER_VOLUME = 6145  # 0, 1, 2, 3, 4 -> [0, 100]
SET_LED = 6156  # 0, 1
AUTO_TURN_OFF = 6151  # params 0, 5, 10 seconds
TURN_OFF = 6155
DELETE_FILE = 1281
FILE_INFO = 1026
# {"msg_id":1025,"param":"/tmp/SD0/DCIM/20171216/IMG_20171216_030505.JPG","token":3,"type":"thumb"}
FILE_PREVIEW = 1025
CAPTURE_START = 4864  # ( 513 ? )
CAPTURE_TIMER = 4868  # seconds
CAPTURE_STOP = 514  # ?
GYRO_CALIBRATION = 6165

PHOTO_EXPOSER_COMPENSATION = 5169  # if x[-3, 3, .5] on app, param = 2 * x
PHOTO_EXPOSER_TIME = 5171  # if auto; x = 0, if x >= 1; x, if x < 1; (1 << 15) + 1/x
PHOTO_ISO = 5172  # 0, 50, 100, 200, 400, 800, 1600
PHOTO_WHITE_BALANCE = 5168  # Auto: 0, Outdoors: 1, Overcast: 2, Incandescent: 3, Fluorescent: 4
# 6912x3456: 0, 3456x1728(stitched): 1, 6912x3456(stitched): 2, 6912x3456(RAW): 3
PHOTO_RESOLUTION = 4872


VIDEO_EXPOSER_COMPENSATION = 5137  # if x[-3, 3, .5] on app, param = 2 * x
VIDEO_WHITE_BALANCE = 5136  # Auto: 0, Outdoors: 1, Overcast: 2, Incandescent: 3, Fluorescent: 4
# 3456x1728|30fps: 0, 2304x1152|30fps: 1, 2304x1152|60fps: 2, 2048x512|120fps Top: 7, 2048x512|120fps bottom (Bullet time): 9, 3456x1728|30fps HighBitrate: 10
VIDEO_RESOLUTION = 4612

# unknown - 4361, 4362
