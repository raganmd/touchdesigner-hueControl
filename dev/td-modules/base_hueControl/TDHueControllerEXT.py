'''
Matthew Ragan | matthewragan.com
Zoe Sandoval | zoesandoval.com
'''

import sys
import threading
import json
import requests
import TDFunctions
import urllib3


class TDHueController:
    '''
    TDHueController is intended to construct and send web
    requests to a Hue Bridge. This heavily leverages the requests 
    library that ships with a default installation of TouchDesigner
    removing a third party integration requirement. This reduces 
    reliance on outside development and the challenges of managing
    third party libraries with TouchDesigner. 

    Notes
    ---------------
    N/A
    '''

    def __init__(self, myOp: OP) -> None:
        urllib3.disable_warnings()
        self.My_op = myOp

        self.Bridge_ip = myOp.par.Bridgeip
        self._ready_to_connect = False
        self._check_bridge()

        self.Gamma = None
        self.X_vals = None
        self.Y_vals = None
        self.Z_vals = None

        self.Lights_page_name = "Individual Lights"
        self.Trans_time_scaler = 10

        self.My_bridge = None

        # TODO - add threaded support for requests
        # self.Use_threads  = myOp.par.Usethreads

        self._all_lights = None

        # runs additional setup to get par vals
        self._setup()

        if self._ready_to_connect:
            self._get_lights()
            print("💡 TDHue Controller Init")
        else:
            pass
        return

    @property
    def _bridge_address(self) -> str:
        return f"https://{self.Bridge_ip.eval()}"

    @property
    def _api_address(self) -> str:
        return f"{self._bridge_address}/api"

    @property
    def _lights_address(self) -> str:
        return f"{self._bridge_address}/clip/v2/resource/light"

    @property
    def _hue_headers(self) -> dict:
        hue_headers = {
            "hue-application-key": self.My_op.par.Deviceusername.eval(),
            "Accept": "*/*",
            "Host": "10.0.1.60"}
        return hue_headers

    def _setup(self) -> None:
        self.Gamma = ipar.Conversion.Gamma.eval()
        self.X_vals = (
            ipar.Conversion.Xvals1.eval(),
            ipar.Conversion.Xvals2.eval(),
            ipar.Conversion.Xvals3.eval())

        self.Y_vals = (
            ipar.Conversion.Yvals1.eval(),
            ipar.Conversion.Yvals2.eval(),
            ipar.Conversion.Yvals3.eval())

        self.Z_vals = (
            ipar.Conversion.Zvals1.eval(),
            ipar.Conversion.Zvals2.eval(),
            ipar.Conversion.Zvals3.eval())

    def _check_bridge(self) -> None:
        device_user_name = self.My_op.par.Deviceusername.eval()
        client_key = self.My_op.par.Clientkey.eval()
        if device_user_name == '' or client_key == '':
            print('NO BRIDGE CONFIGURED')
            self._ready_to_connect = False
        else:
            self._ready_to_connect = True

    def _bridge_setup(self) -> list:
        '''Runs set-up functions to connect with bridge
        '''
        api_address = self._api_address
        payload = {
            "devicetype": "TouchDesigner",
            "generateclientkey": True
        }

        set_up_msg = requests.post(api_address, json=payload, verify=False)

        if set_up_msg.status_code == 200:
            json_blob = set_up_msg.json()

            try:
                # set username and application key on hue op
                success_blob = json_blob[0].get("success")
                user_name = success_blob.get("username")
                application_key = success_blob.get("clientkey")

                self.My_op.par.Deviceusername = user_name
                self.My_op.par.Clientkey = application_key

            except Exception as e:
                raise Exception(f"💡 Message from Hue | {e}")

        else:
            raise Exception(f"💡 Message from Hue | {set_up_msg}")

    def _get_lights(self) -> dict:
        # print(self._hue_headers)
        all_lights = requests.get(
            self._lights_address, data={}, headers=self._hue_headers, verify=False)
        all_lights_json = all_lights.json().get("data")

        self._all_lights = all_lights_json

        return all_lights_json

    def Clear_and_setup_lights(self):
        '''
            A helper function for setting-up the custom parameters.

            This combines two other helper functions to correctly clear all
            previous custom parameters, and create new pars for all lights
            connected to the current Hue Bridge.

            Notes
            ---------------
            None

            Args
            ---------------
            None

            Returns
            ---------------
            None
        '''

        # clear old lights
        self.Clear_hue_lights()

        # # wait 1 second and add new pars
        delay_add_pars = "args[0].Add_pars_for_lights()"
        run(delay_add_pars, self, delayFrames=60)

    def Clear_hue_lights(self):
        '''
            A helper function for setting-up the custom parameters.

            This function is used to clear out all of the custom parameters
            on the "Individual Lights" page.

            Notes
            ---------------
            None

            Args
            ---------------
            None

            Returns
            ---------------
            None
        '''

        # delete the whole page of custom pars
        light_pars = self.My_op.customPars
        for each_light in light_pars:
            try:
                if each_light.page == self.Lights_page_name and each_light.name != "Updatebysettings":
                    each_light.destroy()
            except Exception as e:
                pass

    def Add_pars_for_lights(self) -> None:
        '''
            Set-up function for getting the lighting parameters ready with a new device.

            This method loops through the lights that are reported by a given hue Bridge
            and creates custom paramaters on the parent() component.

            Notes
            ---------------
            None

            Args
            ---------------
            None

            Returns
            ---------------
            None
        '''

        lights_page = self.My_op.appendCustomPage("Individual Lights")

        # add update all pulse:
        lights_page.appendPulse('Updatebysettings', label='Update by Settings')

        self._get_lights()
        all_lights = self._all_lights

        for each_index, each_light in enumerate(all_lights):
            self._add_light_pars(each_index, each_light)

    def _add_light_pars(self, index: int, light_info: dict) -> None:
        metadata = light_info.get('metadata')
        brightness = light_info.get('dimming').get('brightness') / 100
        color = light_info.get('color').get('xy')
        on_state = light_info.get('on').get('on')

        rgb_color = self._convert_xy_to_rgb(
            color.get('x'), color.get('y'), brightness)

        default_color = [1.0, 1.0, 1.0]
        default_bri = 1
        default_transTime = 3
        default_pwr = False

        lights_page = TDFunctions.getCustomPage(
            self.My_op, "Individual Lights")

        # add the string name of the light
        str_name = f'Lightname{index}'
        str_label = f'Light {index} Name'
        lights_page.appendStr(str_name, label=str_label)

        # add id of light
        light_id_name = f'Lightid{index}'
        light_id_label = f'Light {index} ID'
        par_light_id = lights_page.appendStr(
            light_id_name, label=light_id_label)
        par_light_id.val = light_info.get("id")
        par_light_id.readOnly = True

        # add a color control par
        rgb_name = f'Lightcolor{index}'
        rbg_label = f'Light {index} Color'
        new_color = lights_page.appendRGB(rgb_name, label=rbg_label)

        for each in new_color:
            each.default = 1.0

        self.My_op.par[f'Lightcolor{index}r'] = rgb_color[0]
        self.My_op.par[f'Lightcolor{index}g'] = rgb_color[1]
        self.My_op.par[f'Lightcolor{index}b'] = rgb_color[2]

        # add a brightness control par
        bri_name = f'Lightbri{index}'
        bri_label = f'Light {index} Brightness'
        new_bri = lights_page.appendFloat(bri_name, label=bri_label)
        new_bri.default = default_bri
        # set with current brightness
        self.My_op.par[bri_name] = brightness

        # TODO - thoughtful addition of control with transition time
        # add a transition time control par
        # tri_name = f'Lighttrans{index}'
        # tri_label = f'Light {index} Trans Time'
        # new_transTime = lights_page.appendInt(tri_name, label=tri_label)
        # new_transTime.default = default_transTime
        # self.My_op.par[tri_name] = default_transTime

        # add a power control par
        pwr_name = f'Lightpwr{index}'
        pwr_label = f'Light {index} Power'
        new_pwr = lights_page.appendToggle(pwr_name, label=pwr_label)
        new_pwr.default = default_pwr
        # set with current state
        self.My_op.par[pwr_name] = on_state

        # TODO - thoughtful addition of an update button
        # add an update pulse button
        # update_name = f'Updatelight{index}'
        # update_label = f'Update {index} Light'
        # lights_page.appendPulse(update_name, label=update_label)

        # set string name for lights based on Hue
        self.My_op.par[f'Lightname{index}'] = metadata.get("name")

        # set par to be readonly
        self.My_op.par[f'Lightname{index}'].readOnly = True

        # add section divider
        self.My_op.par[f'Lightname{index}'].startSection = True

    def Update_light(self, light_id: str, rgb: list, on_state: bool, brightness: float) -> None:
        update_request = self._update_single_light(
            light_id,
            rgb,
            on_state,
            brightness * 100)

        return

    def _update_single_light(self, light_id: str, rgb: tuple, on_state: bool, brightness: int) -> None:
        """
        """
        xy_color = self._convert_color(rgb)
        light_params = {
            "color": {
                "xy": {
                    "x": xy_color[0],
                    "y": xy_color[1]
                }
            },
            "on": {
                "on": on_state
            },
            "dimming": {
                "brightness": brightness
            }
        }
        light_url = f"{self._lights_address}/{light_id}"
        payload = json.dumps(light_params)

        # update_thread = threading.Thread(
        #     target=requests.put,
        #     args=(light_url,),
        #     kwargs={
        #         "headers": self._hue_headers,
        #         "data": payload,
        #         "verify": False
        #     }
        # )
        # update_thread.start()

        light_put_request = requests.put(
            light_url,
            headers=self._hue_headers,
            data=payload,
            verify=False)

        return

    def _convert_color(self, rgb: tuple) -> list:
        '''
            A hue color conversion method.

            This method is used to transform color from rgb values to hue xy
            values. This follows the hue API for color space conversion.

            Notes
            ---------------


            Args
            ---------------
            rgb (list)
            > A list of rgb values to be converted into the xy color space for the hue

            Examples
            ---------------
            color 		= [1.0, 0.0, 0.0]
            self._convert_color(color)

            Returns
            ---------------
            color_xy (list)
            > A list of two values of converted color space
        '''

        if sum(rgb) == 0:
            rgb = [0.001, 0.001, 0.001]
        else:
            pass

        gamma = self.Gamma
        g_correction = [pow(each_chan, (1/gamma)) for each_chan in rgb]

        color_X = g_correction[0] * self.X_vals[0] + g_correction[1] * \
            self.X_vals[1] + g_correction[2] * self.X_vals[2]
        color_Y = g_correction[0] * self.Y_vals[0] + g_correction[1] * \
            self.Y_vals[1] + g_correction[2] * self.Y_vals[2]
        color_Z = g_correction[0] * self.Z_vals[0] + g_correction[1] * \
            self.Z_vals[1] + g_correction[2] * self.Z_vals[2]

        color_x = color_X / (color_X + color_Y + color_Z)
        color_y = color_Y / (color_X + color_Y + color_Z)

        color_xy = [color_x, color_y]

        return color_xy

    def _convert_xy_to_rgb(self, x: float, y: float, brightness: float) -> list:

        z = 1.0 - x - y

        Y = 0.75
        X = (Y / y) * x
        Z = (Y / y) * z

        r = X * 1.612 - Y * 0.203 - Z * 0.302
        g = -X * 0.509 + Y * 1.412 + Z * 0.066
        b = X * 0.026 - Y * 0.072 + Z * 0.962

        return [r, g, b]
