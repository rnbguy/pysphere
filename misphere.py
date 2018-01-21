import json
import socket
import os
import threading
import time
import io
import select

from msgids import *


class Session():
    pass


class MiSphereConn:
    ms_ip = '192.168.42.1'
    ms_tcp_port = 7878
    ms_uk_port = 8787
    ms_fs_port = 50422

    def init(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.connect((self.ms_ip, self.ms_tcp_port))
        self.socket_1 = socket.socket()
        self.recv_handle_live = True
        self.recv_thread = threading.Thread(target=self.recv_handler)
        self.recv_thread.daemon = True
        self.session = Session()
        self.session.conf = {}
        self.session.locks = {}
        self.last_send = 0

    def handle_data(self, func):
        self.handle_data = func

    def recv_handler(self):
        while self.recv_handle_live:
            r, _, _ = select.select([self.socket], [], [], 0.5)
            if r:
                resps = self.socket.recv(512).decode()
                while True:
                    resp_dict, idx = json.JSONDecoder().raw_decode(resps)
                    self.resp_handler(resp_dict)
                    if idx >= len(resps):
                        break
                    else:
                        resps = resps[idx:]

    def resp_handler(self, data):
        if 'rval' in data:
            print(data)
            # assert(data['rval'] >= 0)
        self.handle_data(data)
        if data['msg_id'] == CONNECT:
            self.session.token = data['param']
        elif data['msg_id'] == DISCONNECT:
            self.recv_handle_live = False
        elif data['msg_id'] in [GET_CAMERA, GET_STORAGE, GET_DEVICE]:
            cdata = {}
            for e in data:
                if e not in ['rval', 'msg_id']:
                    cdata[e] = data[e]
            self.session.conf[data['msg_id']] = cdata
        else:
            print("UNKNOWN", data)
        if data['msg_id'] in self.session.locks:
            self.session.locks[data['msg_id']].release()
            print('[UNLOCK]', data['msg_id'])

    def connect_8787(self):
        self.socket_1.connect((self.ms_ip, self.ms_uk_port))

    def poweroff(self):
        self.send(TURN_OFF)

    def create_payload(self, msg_id, token, params=None):
        payload = dict()
        payload['msg_id'] = msg_id
        if params is not None:
            for k, v in params.items():
                payload[k] = str(v) if k == 'param' else v
        payload['token'] = token
        return payload

    def send(self, msg_id, params=None, token=None):
        if msg_id not in self.session.locks:
            self.session.locks[msg_id] = threading.Lock()
        print("[LOCK] ", msg_id)
        if self.session.locks[msg_id].locked():
            return 0
        else:
            self.session.locks[msg_id].acquire()
        if token is None:
            token = self.session.token
        payload = self.create_payload(msg_id, token, params)
        data = json.dumps(payload).encode()
        print(data)
        timediff = time.time() - self.last_send
        if timediff < 0.5:
            time.sleep(0.5 - timediff)
        self.last_send = time.time()
        return self.socket.send(data)

    def recv(self):
        response = self.socket.recv(1024)
        response = json.loads(response.decode())
        return response

    def send_recv(self, msg_id, params=None, token=None):
        self.send(msg_id, params, token)
        return self.recv()

    def get_mode(self):
        self.send(GET_CAMERA)

    def connect(self):
        self.recv_handle_live = True
        self.recv_thread.start()
        self.send(CONNECT, token=0)
        while self.session.locks[CONNECT].locked():
            time.sleep(.2)
        print('token is {}'.format(self.session.token))
        self.get_details()

    def set_sub_camera(self, sub_cam, value=0):
        if sub_cam == 'Timer':
            self.send(SET_PHOTO_TIMER, {'param': value})
        elif sub_cam == 'Intervalometer':
            self.send(SET_PHOTO_INTERVALOMETER, {'param': value})
        elif sub_cam == 'Bracketing':
            self.send(SET_PHOTO_BRACKETING, {'param': int(2 * value)})
        elif sub_cam == 'None':
            self.send(SET_PHOTO_TIMER, {'param': 0})
            self.send(SET_PHOTO_INTERVALOMETER, {'param': 0})
            self.send(SET_PHOTO_BRACKETING, {'param': 0})

    def set_sub_video(self, sub_vid, value=0):
        if sub_vid == 'Short video':
            self.send(SET_VIDEO_SHORT, {'param': value})
        elif sub_vid == 'Timelapse':
            self.send(SET_VIDEO_TIMELAPSE, {'param': value})
        elif sub_vid == 'Slow motion':
            self.send(SET_VIDEO_SLOWMO, {'param': value})
        elif sub_vid == 'None':
            self.send(SET_VIDEO_SHORT, {'param': 0})
            self.send(SET_VIDEO_TIMELAPSE, {'param': 0})
            self.send(SET_VIDEO_SLOWMO, {'param': 0})

    def get_details(self):
        self.get_camera_details()
        self.get_storage_details()
        self.get_device_details()

    def is_set_to_photo(self):
        return self.send(GET_CAMERA)['mode'] == 1

    def is_set_to_video(self):
        return self.send(GET_CAMERA)['mode'] == 0

    def switch_to_video(self):
        return self.send(SWITCH_MODE, {'param': 0})

    def switch_to_photo(self):
        return self.send(SWITCH_MODE, {'param': 1})

    def switch_mode(self):
        if self.is_set_to_photo():
            return self.switch_to_video()
        elif self.is_set_to_video():
            return self.switch_to_photo()

    def get_camera_details(self):
        return self.send(GET_CAMERA)

    def get_storage_details(self):
        return self.send(GET_STORAGE)

    def get_device_details(self):
        return self.send(GET_DEVICE)

    def set_photo_EV(self, value):
        return self.send(PHOTO_EV, {'param': int(2 * value)})

    def set_photo_ISO(self, value):
        return self.send(PHOTO_ISO, {'param': value})

    def set_photo_WB(self, value):
        return self.send(PHOTO_WB, {'param': value})

    def get_info(self, filepath=''):
        self.send(FILE_INFO,
                  {
                      "param": "/tmp/SD0/DCIM/20171210/f0297728.jpg",
                  }
                  )
        return self.recv()

    def get_thumb(self, filepath=''):
        self.send(FILE_PREVIEW,
                  {
                      "param": "/tmp/SD0/DCIM/20171210/f0297728.jpg",
                      "type": "thumb"
                  }
                  )
        return self.recv()

    def register_tcp(self, params={}):
        params = {"param": "192.168.42.3", "type": "TCP"}
        self.send(REGISTER_TCP, params)
        return self.recv()

    def click_picture(self, long_press=False):
        self.send(PHOTO_LONGPRESS if long_press else PHOTO_PRESS)

    def record_video(self, long_press=False):
        self.send(VIDEO_LONGPRESS if long_press else VIDEO_REC_START)

    def record_stop(self):
        self.send(VIDEO_REC_STOP)

    def change_camera_res(self, value):
        l = {
            '6912x3456': 0,
            '3456x1728 (stitched)': 1,
            '6912x3456 (stitched)': 2,
            '6912x3456 with RAW': 3
        }
        self.send(PHOTO_RES, {'param': l[value]})

    def change_camera_wb(self, value):
        l = {
            'Auto': 0,
            'Outdoors': 1,
            'Overcast': 2,
            'Incandescent': 3,
            'Fluorescent': 4
        }
        self.send(PHOTO_WB, {'param': l[value]})

    def change_camera_iso(self, value):
        l = {
            'Auto': 0,
            '50': 50,
            '100': 100,
            '200': 200,
            '400': 400,
            '800': 800,
            '1600': 1600
        }
        self.send(PHOTO_ISO, {'param': l[value]})

    def change_camera_shutter(self, value):
        print("yo")

        def l(val):
            if val == 'Auto':
                return 0
            else:
                if val.startswith('1/'):
                    val = val[2:]
                    val = int(val)
                    val += 1 << 15
                else:
                    val = int(val)
            return val
        self.send(PHOTO_SHUTTERTIME, {'param': l(value)})

    def change_camera_ev(self, value):
        self.send(PHOTO_EV, {'param': int(2 * value)})

    def change_video_res(self, value):
        l = {
            '3456x1728 | 30fps': 0,
            '2304x1152 | 30fps': 1,
            '2304x1152 | 60fps': 2,
            '2048x512 | 120fps': 3,
            '2048x512 | 120fps bottom (Bullet time)': 4,
            '3456x1728 | 30fps HighBitrate': 5
        }
        self.send(VIDEO_RES, {'param': l[value]})

    def change_video_wb(self, value):
        l = {
            'Auto': 0,
            'Outdoors': 1,
            'Overcast': 2,
            'Incandescent': 3,
            'Fluorescent': 4
        }
        self.send(VIDEO_WB, {'param': l[value]})

    def change_video_ev(self, value):
        self.send(VIDEO_EV, {'param': int(2 * value)})

    def set_auto_off(self, value):
        self.send(AUTO_TURN_OFF, {'param': value})

    def set_buzzer_volume(self, value):
        self.send(SET_BUZZER_VOLUME, {'param': value})

    def set_led(self, value):
        self.send(SET_LED, {'param': int(value)})

    def disconnect(self):
        self.send(DISCONNECT)
        while self.session.locks[DISCONNECT].locked():
            time.sleep(0.5)
        self.recv_handle_live = False
        self.recv_thread.join()

    def test(self, l, h):
        import msgids
        known = set()
        for e in vars(msgids):
            if not e.startswith('__'):
                known.add(msgids.__dict__[e])
        for i in range(l, h + 1):
            self.send(i)

    def __del__(self):
        self.socket.close()
        self.socket_1.close()


if __name__ == '__main__':
    cam = MiSphereConn()
    cam.connect()
    # cam.click_picture()
    # cam.disconnect()
