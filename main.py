import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty

from settings_panel import panel_dict

from misphere import *


class CustBoxLayout(BoxLayout):
    current_module = StringProperty()

    camera_ev = NumericProperty()
    camera_iso = StringProperty()
    camera_wb = StringProperty()
    camera_res = StringProperty()
    camera_shutter = StringProperty()
    #
    sub_camera = StringProperty()
    timer_value = NumericProperty()
    intervalometer_value = NumericProperty()
    bracketing_value = NumericProperty()

    timer_ar = [3, 4, 5, 6, 7, 8, 9, 10]
    intervalometer_ar = [2, 5, 10, 30, 60, 120, 300]
    bracketing_ar = [0.5, 1, 1.5, 2, 2.5, 3]
    #
    video_ev = NumericProperty()
    video_wb = StringProperty()
    video_res = StringProperty()
    #
    sub_video = StringProperty()
    shortvideo_value = NumericProperty()
    timelapse_value = NumericProperty()
    slowmotion_value = NumericProperty()

    shortvideo_ar = [10, 20, 30]
    timelapse_ar = [0.5, 1, 2, 5, 10, 30, 60]
    slowmotion_ar = [2]

    battery = StringProperty()
    sd_free = StringProperty()
    sd_total = StringProperty()
    remain_jpg = StringProperty()
    remain_video = StringProperty()

    current_module_server = False

    sub_camera_server = False
    sub_video_server = False

    camera_res_server = False
    camera_ev_server = False
    camera_iso_server = False
    camera_wb_server = False
    camera_shutter_server = False

    timer_value_server = False
    intervalometer_value_server = False
    bracketing_value_server = False

    video_res_server = False
    video_wb_server = False
    video_ev_server = False

    shortvideo_value_server = False
    timelapse_value_server = False
    slowmotion_value_server = False

    battery_server = False
    buzzer_server = False
    led_server = False
    poweroff_timer_server = False

    def __init__(self, *args, **kwargs):
        super(CustBoxLayout, self).__init__(*args, **kwargs)
        self.current_module = 'Camera'

        self.camera_ev = 0
        self.camera_iso = 'Auto'
        self.camera_wb = 'Auto'
        self.camera_res = '6912x3456'
        self.camera_shutter = 'Auto'

        self.sub_camera = 'None'
        self.timer_value = 0
        self.intervalometer_value = 0
        self.bracketing_value = 0

        self.video_ev = 0
        self.video_wb = 'Auto'
        self.video_res = '3456x1728|30fps'

        self.sub_video = 'None'
        self.shortvideo_value = 0
        self.timelapse_value = 0
        self.slowmotion_value = 0

        self.camera_control = self.ids.camera_control.__self__
        self.record_control = self.ids.record_control.__self__

        self.timer = self.ids.timer.__self__
        self.intervalometer = self.ids.intervalometer.__self__
        self.bracketing = self.ids.bracketing.__self__

        self.shortvideo = self.ids.shortvideo.__self__
        self.timelapse = self.ids.timelapse.__self__
        self.slowmotion = self.ids.slowmotion.__self__

        self.intervalometer_slider = self.ids.intervalometer_slider.__self__

        self.conn = MiSphereConn()
        self.conn.handle_data(self.update_vals)

    def setup_module(self, spinner, text):
        if text == 'Camera':
            self.ids.controls.clear_widgets()
            self.ids.controls.add_widget(self.ids.camera_control)
            if self.current_module_server:
                self.current_module_server = False
                return
            try:
                self.conn.switch_to_photo()
            except AttributeError:
                pass
        elif text == 'Record':
            self.ids.controls.clear_widgets()
            self.ids.controls.add_widget(self.ids.record_control)
            if self.current_module_server:
                self.current_module_server = False
                return
            try:
                self.conn.switch_to_video()
            except AttributeError:
                pass

    def setup_sub_camera(self, spinner, text):
        try:
            if text == 'None':
                self.ids.sub_camera_control.clear_widgets()
                if self.sub_camera_server:
                    self.sub_camera_server = False
                    return
                self.conn.set_sub_camera(text)
            elif text == 'Timer':
                self.ids.sub_camera_control.clear_widgets()
                self.ids.sub_camera_control.add_widget(self.ids.timer)
                if self.sub_camera_server:
                    self.sub_camera_server = False
                    return
                self.conn.set_sub_camera(text, self.timer_ar[int(self.timer_value)])
            elif text == 'Intervalometer':
                self.ids.sub_camera_control.clear_widgets()
                self.ids.sub_camera_control.add_widget(self.ids.intervalometer)
                if self.sub_camera_server:
                    self.sub_camera_server = False
                    return
                self.conn.set_sub_camera(
                    text, self.intervalometer_ar[int(self.intervalometer_value)])
            elif text == 'Bracketing':
                self.ids.sub_camera_control.clear_widgets()
                self.ids.sub_camera_control.add_widget(self.ids.bracketing)
                if self.sub_camera_server:
                    self.sub_camera_server = False
                    return
                self.conn.set_sub_camera(text, self.bracketing_ar[int(self.bracketing_value)])
        except Exception as e:
            self.print_to_log(e)

    def change_camera_to_timer(self, slider, value):
        if self.timer_value_server:
            self.timer_value_server = False
            return
        try:
            self.conn.set_sub_camera('Timer', self.timer_ar[int(value)])
        except Exception as e:
            self.print_to_log(e)

    def change_camera_to_intervalometer(self, slider, value):
        if self.intervalometer_value_server:
            self.intervalometer_value_server = False
            return
        try:
            self.conn.set_sub_camera('Intervalometer', self.intervalometer_ar[int(value)])
        except Exception as e:
            self.print_to_log(e)

    def change_camera_to_bracketing(self, slider, value):
        if self.bracketing_value_server:
            self.bracketing_value_server = False
            return
        try:
            self.conn.set_sub_camera('Bracketing', self.bracketing_ar[int(value)])
        except Exception as e:
            self.print_to_log(e)

    def setup_sub_video(self, spinner, text):
        try:
            if text == 'None':
                self.ids.sub_video_control.clear_widgets()
                if self.sub_video_server:
                    self.sub_video_server = False
                    return
                self.conn.set_sub_video(text)
            elif text == 'Short video':
                self.ids.sub_video_control.clear_widgets()
                self.ids.sub_video_control.add_widget(self.ids.shortvideo)
                if self.sub_video_server:
                    self.sub_video_server = False
                    return
                self.conn.set_sub_video(text, self.shortvideo_ar[int(self.shortvideo_value)])
            elif text == 'Timelapse':
                self.ids.sub_video_control.clear_widgets()
                self.ids.sub_video_control.add_widget(self.ids.timelapse)
                if self.sub_video_server:
                    self.sub_video_server = False
                    return
                self.conn.set_sub_video(text, self.timelapse_ar[int(self.timelapse_value)])
            elif text == 'Slow motion':
                self.ids.sub_video_control.clear_widgets()
                self.ids.sub_video_control.add_widget(self.ids.slowmotion)
                if self.sub_video_server:
                    self.sub_video_server = False
                    return
                self.conn.set_sub_video(text, self.slowmotion_ar[int(self.slowmotion_value)])
        except Exception as e:
            self.print_to_log(e)

    def change_video_to_shortvideo(self, slider, value):
        if self.shortvideo_value_server:
            self.shortvideo_value_server = False
            return
        try:
            self.conn.set_sub_video('Short video', self.shortvideo_ar[int(value)])
        except Exception as e:
            self.print_to_log(e)

    def change_video_to_timelapse(self, slider, value):
        if self.timelapse_value_server:
            self.timelapse_value_server = False
            return
        try:
            self.conn.set_sub_video('Timelapse', self.timelapse_ar[int(value)])
        except Exception as e:
            self.print_to_log(e)

    def change_video_to_slowmotion(self, slider, value):
        if self.slowmotion_value_server:
            self.slowmotion_value_server = False
            return
        try:
            self.conn.set_sub_video('Slow motion', self.slowmotion_ar[int(value)])
        except Exception as e:
            self.print_to_log(e)

    def print_to_log(self, obj):
        s = (str(obj) + '\n').replace('\n', '\n\n')
        self.ids.log_view.text += s

    def connect(self):
        try:
            self.conn.init()
            self.conn.connect()
            self.print_to_log("connected")
            self.print_to_log(self.conn.session.token)
        except Exception as e:
            self.print_to_log(e)

    def poweroff(self):
        try:
            self.conn.poweroff()
        except Exception as e:
            self.print_to_log(e)

    def update_vals(self, data):
        if data['msg_id'] == GET_DEVICE:
            for k, v in data.items():
                if k == 'p_res':
                    if self.camera_res != self.ids.camera_res_spinner.values[v]:
                        self.camera_res_server = True
                        self.camera_res = self.ids.camera_res_spinner.values[v]
                elif k == 'still_ev':
                    if  self.camera_ev != v / 2:
                        self.camera_ev_server = True
                        self.camera_ev = v / 2
                elif k == 'still_iso':
                    if self.camera_iso != self.ids.camera_iso_spinner.values[v]:
                        self.camera_iso_server = True
                        self.camera_iso = self.ids.camera_iso_spinner.values[v]
                elif k == 'still_wb':
                    if self.camera_wb != self.ids.camera_wb_spinner.values[v]:
                        self.camera_wb_server = True
                        self.camera_wb = self.ids.camera_wb_spinner.values[v]
                elif k == 'still_shutter':
                    if self.camera_shutter != self.ids.camera_shutter_spinner.values[v]:
                        self.camera_shutter_server = True
                        self.camera_shutter = self.ids.camera_shutter_spinner.values[v]
                elif k == 'v_res':
                    if self.video_res != self.ids.video_res_spinner.values[v]:
                        self.video_res_server = True
                        self.video_res = self.ids.video_res_spinner.values[v]
                elif k == 'video_ev':
                    if self.video_ev != v / 2:
                        self.video_ev_server = True
                        self.video_ev = v / 2
                elif k == 'video_wb':
                    if self.video_wb != self.ids.video_wb_spinner.values[v]:
                        self.video_wb_server = True
                        self.video_wb = self.ids.video_wb_spinner.values[v]
                elif k == 'battery':
                    if self.battery != str(v):
                        self.battery_server = True  # does not need
                        self.battery = str(v)
                elif k == 'buzzer':
                    if App.get_running_app().config.get('General', 'buzzer') != str(v):
                        self.buzzer_server = True
                        App.get_running_app().config.set('General', 'buzzer', str(v))
                elif k == 'led':
                    if App.get_running_app().config.get('General', 'led') != (v == 1):
                        self.led_server = True
                        App.get_running_app().config.set('General', 'led', v == 1)
                elif k == 'poweroff_time':
                    if App.get_running_app().config.get('General', 'auto_off') != str(v):
                        self.poweroff_timer_server = True
                        App.get_running_app().config.set('General', 'auto_off', str(v))
        elif data['msg_id'] == GET_CAMERA:
            if self.timer_value != self.timer_ar.index(data['timing']):
                self.timer_value_server = True
                self.timer_value = self.timer_ar.index(data['timing'])


            if self.intervalometer_value != self.intervalometer_ar.index(data['cap_interval']):
                self.intervalometer_value_server = True
                self.intervalometer_value = self.intervalometer_ar.index(data['cap_interval'])


            if self.bracketing_value != self.bracketing_ar.index(data['surroundexp'] / 2):
                self.bracketing_value_server = True
                self.bracketing_value = self.bracketing_ar.index(data['surroundexp'] / 2)

            if self.shortvideo_value != self.shortvideo_ar.index(data['second']):
                self.shortvideo_value_server = True
                self.shortvideo_value = self.shortvideo_ar.index(data['second'])

            if self.timelapse_value != self.timelapse_ar.index(data['lapse']):
                self.timelapse_value_server = True
                self.timelapse_value = self.timelapse_ar.index(data['lapse'])

            if self.slowmotion_value != self.slowmotion_ar.index(data['speedx']):
                self.slowmotion_value_server = True
                self.slowmotion_value = self.slowmotion_ar.index(data['speedx'])

            if data['mode'] == 0:
                if self.current_module != 'Record':
                    self.current_module_server = True
                    self.current_module = 'Record'
                if data['sub_mode'] == 0:
                    if self.sub_video != 'None':
                        self.sub_video_server = True
                        self.sub_video = 'None'
                elif data['sub_mode'] == 1:
                    if self.sub_video != 'Short video':
                        self.sub_video_server = True
                        self.sub_video = 'Short video'
                elif data['sub_mode'] == 2:
                    if self.sub_video != 'Timelapse':
                        self.sub_video_server = True
                        self.sub_video = 'Timelapse'
                elif data['sub_mode'] == 4:
                    if self.sub_video != 'Slow motion':
                        self.sub_video_server = True
                        self.sub_video = 'Slow motion'
            elif data['mode'] == 1:
                if self.current_module != 'Camera':
                    self.current_module_server = True
                    self.current_module = 'Camera'
                if data['sub_mode'] == 0:
                    if self.sub_camera != 'None':
                        self.sub_camera_server = True
                        self.sub_camera = 'None'
                elif data['sub_mode'] == 1:
                    if self.sub_camera != 'Timer':
                        self.sub_camera_server = True
                        self.sub_camera = 'Timer'
                elif data['sub_mode'] == 2:
                    if self.sub_camera != 'Intervalometer':
                        self.sub_camera_server = True
                        self.sub_camera = 'Intervalometer'
                elif data['sub_mode'] == 4:
                    if self.sub_camera != 'Bracketing':
                        self.sub_camera_server = True
                        self.sub_camera = 'Bracketing'
        elif data['msg_id'] == GET_STORAGE:
            for k, v in data.items():
                if k == 'remain_video':
                    self.remain_video = str(v) + 's'
                elif k == 'remain_jpg':
                    self.remain_jpg = str(v)
                elif k == 'sd_total':
                    self.sd_total = str(v)
                elif k == 'sd_free':
                    self.sd_free = str(v)
        elif data['msg_id'] == SWITCH_MODE:
            if data['param'] == 0:
                self.current_module = 'Record'
                if data['sub_mode'] == 0:
                    self.sub_video = 'None'
                elif data['sub_mode'] == 1:
                    self.sub_video = 'Short video'
                    self.shortvideo_value = self.shortvideo_ar.index(data['sub_mode_param'])
                elif data['sub_mode'] == 2:
                    self.sub_video = 'Timelapse'
                    self.timelapse_value = self.timelapse_ar.index(data['sub_mode_param'])
                elif data['sub_mode'] == 4:
                    self.sub_video = 'Slow motion'
                    self.slowmotion_value = self.slowmotion_ar.index(data['sub_mode_param'])
            elif data['param'] == 1:
                self.current_module = 'Camera'
                if data['sub_mode'] == 0:
                    self.sub_camera = 'None'
                elif data['sub_mode'] == 1:
                    self.sub_camera = 'Timer'
                    self.timer_value = self.timer_ar.index(data['sub_mode_param'])
                elif data['sub_mode'] == 2:
                    self.sub_camera = 'Intervalometer'
                    self.intervalometer_value = self.intervalometer_ar.index(data['sub_mode_param'])
                elif data['sub_mode'] == 4:
                    self.sub_camera = 'Bracketing'
                    self.bracketing_value = self.bracketing_ar.index(data['sub_mode_param'] / 2)

    def refresh(self):
        try:
            self.conn.get_details()
        except Exception as e:
            self.print_to_log(e)

    def camera_short_press(self):
        try:
            self.conn.click_picture()
        except Exception as e:
            self.print_to_log(e)

    def camera_long_press(self):
        try:
            self.conn.click_picture(True)
        except Exception as e:
            self.print_to_log(e)

    def video_start_press(self):
        try:
            self.conn.record_video()
        except Exception as e:
            self.print_to_log(e)

    def video_long_press(self):
        try:
            self.conn.record_video(True)
        except Exception as e:
            self.print_to_log(e)

    def video_stop_press(self):
        try:
            self.conn.record_stop()
        except Exception as e:
            self.print_to_log(e)

    def disconnect(self):
        try:
            self.conn.disconnect()
            self.print_to_log("disconnected")
        except Exception as e:
            self.print_to_log(e)

    def change_camera_res(self, spinner, text):
        if self.camera_res_server:
            self.camera_res_server = False
            return
        try:
            self.conn.change_camera_res(text)
        except Exception as e:
            self.print_to_log(e)

    def change_camera_wb(self, spinner, text):
        if self.camera_wb_server:
            self.camera_wb_server = False
            return
        try:
            self.conn.change_camera_wb(text)
        except Exception as e:
            self.print_to_log(e)

    def change_camera_iso(self, spinner, text):
        if self.camera_iso_server:
            self.camera_iso_server = False
            return
        try:
            self.conn.change_camera_iso(text)
        except Exception as e:
            self.print_to_log(e)

    def change_camera_shutter(self, spinner, text):
        if self.camera_shutter_server:
            self.camera_shutter_server = False
            return
        try:
            self.conn.change_camera_shutter(text)
        except Exception as e:
            self.print_to_log(e)

    def change_camera_ev(self, slider, value):
        if self.camera_ev_server:
            self.camera_ev_server = False
            return
        try:
            self.conn.change_camera_ev(value)
        except Exception as e:
            self.print_to_log(e)

    def change_video_res(self, spinner, text):
        if self.video_res_server:
            self.video_res_server = False
            return
        try:
            self.conn.change_video_res(text)
        except Exception as e:
            self.print_to_log(e)

    def change_video_wb(self, spinner, text):
        if self.video_wb_server:
            self.video_wb_server = False
            return
        try:
            self.conn.change_video_wb(text)
        except Exception as e:
            self.print_to_log(e)

    def change_video_ev(self, slider, value):
        if self.video_ev_server:
            self.video_ev_server = False
            return
        try:
            self.conn.change_video_ev(value)
        except Exception as e:
            self.print_to_log(e)


class PySphereApp(App):
    use_kivy_settings = False

    def build(self):
        return CustBoxLayout()

    def build_config(self, config):
        config.setdefaults('General',
                           {'auto_off': '0',
                            'buzzer': '0',
                            'led': 1
                            }
                           )
        config.add_callback(self.on_config_changed)

    def build_settings(self, settings):
        settings.add_json_panel('PySphere Settings', self.config, data=json.dumps(panel_dict))

    def on_config_changed(self, section, key, value):
        if section == 'General':
            if key == 'auto_off':
                if self.root.poweroff_timer_server:
                    self.root.poweroff_timer_server = False
                    return
                self.root.conn.set_auto_off(value)
            elif key == 'buzzer':
                if self.root.buzzer_server:
                    self.root.buzzer_server = False
                    return
                self.root.conn.set_buzzer_volume(value)
            elif key == 'led':
                if self.root.led_server:
                    self.root.led_server = False
                    return
                self.root.conn.set_led(value)


if __name__ == '__main__':
    app = PySphereApp()
    app.run()
