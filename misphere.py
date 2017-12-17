import json
import socket
import os

from homura import download

from msgids import *


class MiSphereConn:
    ms_ip = '192.168.42.1'
    ms_tcp_port = 7878
    ms_fs_port = 50422
    token = 0

    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect((self.ms_ip, self.ms_tcp_port))

    def __del__(self):
        self.socket.close()

    def send_recv(self, msg_id, params=None, token=None):
        if token is None:
            token = self.token
        payload = self.create_payload(msg_id, token, params)
        data = json.dumps(payload).encode()
        self.socket.send(data)
        response = self.socket.recv(1024)
        response = json.loads(response.decode())
        return response

    def create_payload(self, msg_id, token, params=None):
        payload = dict()
        payload['msg_id'] = msg_id
        if params is not None:
            for k, v in params.items():
                payload[k] = str(v)
        payload['token'] = token
        return payload

    def recv(self):
        response = self.socket.recv(1024)
        response = json.loads(response.decode())
        return response

    def get_mode(self):
        resp = self.send_recv(GET_CAMERA)
        return resp

    def connect(self):
        resp = self.send_recv(CONNECT, token=0)
        self.token = resp['param']

    def switch_to_photo(self):
        return self.send_recv(SWITCH_MODE, {'param': 1})

    def get_camera_details(self):
        return self.send_recv(GET_CAMERA)

    def get_device_details(self):
        return self.send_recv(GET_DEVICE)

    def set_photo_EV(self, value):
        return self.send_recv(PHOTO_EV, {'param': int(2 * value)})

    def set_photo_ISO(self, value):
        return self.send_recv(PHOTO_ISO, {'param': value})

    def set_photo_WB(self, value):
        return self.send_recv(PHOTO_WB, {'param': value})

    def click_picture(self, is_timer=False, print_url=False):
        if self.get_mode()['mode'] != 1:
            self.switch_to_photo()
        resp = self.send_recv(PHOTO_LONGPRESS if is_timer else PHOTO_PRESS)
        assert(resp['rval'] == 0)
        resp = self.recv()
        assert(resp['msg_id'] == 8193)
        path = resp['param']
        unix_path = path.replace('\\', '/').replace('C:/DCIM', '')
        download_link = 'http://{}:{}{}'.format(self.ms_ip, self.ms_fs_port, unix_path)
        if print_url:
            print(download_link)
        else:
            print('Saving at {}'.format(os.path.basename(unix_path)))
            download(download_link)

    def disconnect(self):
        self.send_recv(DISCONNECT)


if __name__ == '__main__':
    cam = MiSphereConn()
    cam.connect()
    cam.click_picture()
    cam.disconnect()
