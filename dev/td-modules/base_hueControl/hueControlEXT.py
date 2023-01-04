﻿'''
Matthew Ragan | matthewragan.com
Zoe Sandoval | zoesandoval.com
'''

import sys
import threading
import json
import requests
import TDFunctions

class Hue:
    '''
        This is a sample class.

        This sample class has several important features that can be described here.


        Notes
        ---------------
        Your notes about the class go here
     '''

    def __init__(self, myOp:OP) -> None:

        self.My_op = myOp
        self.Dep_path = '{}/dep/python/'.format(project.folder)
        self.Bridge_ip = parent().par.Bridgeip

        self.Brightness_from = (0, 1)
        self.Brightness_to = (0, 255)

        self.Gamma = .75

        self.X_vals	= (0.664511, 0.154324, 0.162028)
        self.Y_vals = (0.283881, 0.668433, 0.047685)
        self.Z_vals	= (0.000088, 0.072310, 0.986039)

        self.Lights_page_name = "Individual Lights"
        self.Trans_time_scaler = 10

        self.My_bridge = None

        self.Use_threads  = parent().par.Usethreads

        self._all_lights = None

        self._get_lights()

        print("Hue Control Init")
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
            "hue-application-key":self.My_op.par.Deviceusername.eval(), 
            "Accept": "*/*",
            "Host" : "10.0.1.60"}
        return hue_headers

    def _setup(self) -> list:
        '''Runs set-up functions to connect with bridge
        '''
        api_address = self._api_address
        payload = {
            "devicetype": "TouchDesigner", 
            "generateclientkey":True
            }
        set_up_msg = requests.post(api_address, json=payload, verify=False)
        
        if set_up_msg.status_code == 200:
            json_blob = set_up_msg.json()
            print(json_blob)
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
        all_lights = requests.get(self._lights_address, data ={}, headers=self._hue_headers, verify=False)
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

        self.Clear_hue_lights()
        self.Add_pars_for_lights()

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
        try:
            parent().customPages[2].destroy()

        except:
            pass

        # add the page back onto the COMP
        parent().appendCustomPage(self.Lights_page_name)			


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

        lights_page = parent().appendCustomPage("Individual Lights")

        # add update all pulse:
        lights_page.appendPulse('Updatebysettings', label='Update by Settings')

        if self._all_lights == None:
            self._get_lights() 
        else:
            pass

        all_lights = self._all_lights

        for each_index, each_light in enumerate(all_lights):
            print(each_light, each_index)
            self._add_light_pars(each_index, each_light)
    
    def _add_light_pars(self, index:int, light_info:dict) -> None:
        metadata = light_info.get("metadata")

        default_color = [1.0, 1.0, 1.0]
        default_bri	= 1
        default_transTime = 3
        default_pwr = True

        lights_page = TDFunctions.getCustomPage(parent(), "Individual Lights")

        # add the string name of the light
        str_name = f'Lightname{index}'
        str_label = f'Light {index} Name'
        lights_page.appendStr(str_name, label=str_label)

        light_id_name = f'Light{index}id'
        light_id_label = f'Light {index} ID'
        par_light_id = lights_page.appendStr(light_id_name, label=light_id_label)
        par_light_id.val = light_info.get("id")
        par_light_id.readOnly = True

        # add a color control par
        rgb_name = f'Lightcolor{index}'
        rbg_label = f'Light {index} Color'
        new_color = lights_page.appendRGB(rgb_name, label=rbg_label)
        
        for each in new_color:
            each.default 	= 1.0

        parent().par[f'Lightcolor{index}r'] = default_color[0]
        parent().par[f'Lightcolor{index}g'] = default_color[1]
        parent().par[f'Lightcolor{index}b'] = default_color[2]

        # add a brightness control par
        bri_name = f'Lightbri{index}'
        bri_label = f'Light {index} Brightness'
        new_bri = lights_page.appendFloat(bri_name, label=bri_label)

        for each in new_bri:
            each.default = default_bri

        parent().par[bri_name] = default_bri

        # add a transition time control par
        tri_name = f'Lighttrans{index}'
        tri_label = f'Light {index} Trans Time'
        new_transTime = lights_page.appendInt(tri_name, label=tri_label)
        
        for each in new_transTime:
            each.default = default_transTime
        
        parent().par[tri_name] = default_transTime

        # add a power control par
        pwr_name =f'Lightpwr{index}'
        pwr_label =f'Light {index} Power'
        new_pwr = lights_page.appendToggle(pwr_name, label=pwr_label)
        
        for each in new_pwr:
            each.default = default_pwr
        
        parent().par[pwr_name] = default_pwr

        # add an update pulse button
        update_name = f'Updatelight{index}'
        update_label = f'Update {index} Light'
        lights_page.appendPulse(update_name, label=update_label)

        # set string name for lights based on Hue
        parent().par[f'Lightname{index}'] = metadata.get("name")

        # set par to be readonly
        parent().par[f'Lightname{index}'].readOnly = True

        # add section divider
        parent().par[f'Lightname{index}'].startSection = True

    def _update_single_light(self, light_id:str, rgb:tuple, brightness:int) -> callable:

        xy_color = self._convert_color(rgb)
        light_on = True if brightness > 0 else False
        light_params = { 
            "color" : {
                "xy" : {
                    "x" : xy_color[0],  
                    "y" : xy_color[1]
                }
            },
            "on" : {
                "on" : light_on
            },
            "dimming" : {
                "brightness" : brightness
            }
        }
        light_url = f"{self._lights_address}/{light_id}"
        payload = json.dumps(light_params)
        light_put_request = requests.put(
            light_url, 
            headers=self._hue_headers, 
            data=payload,
            verify=False)

        return light_put_request

    def _convert_color(self, rgb:tuple) -> list:
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
            rgb 	= [0.001, 0.001, 0.001]
        else:
            pass

        gamma 				= self.Gamma
        g_correction 		= [pow(each_chan, (1/gamma)) for each_chan in rgb]

        color_X = g_correction[0] * self.X_vals[0] + g_correction[1] * self.X_vals[1] + g_correction[2] * self.X_vals[2]
        color_Y = g_correction[0] * self.Y_vals[0] + g_correction[1] * self.Y_vals[1] + g_correction[2] * self.Y_vals[2]
        color_Z = g_correction[0] * self.Z_vals[0] + g_correction[1] * self.Z_vals[1] + g_correction[2] * self.Z_vals[2]

        color_x = color_X / (color_X + color_Y + color_Z)
        color_y = color_Y / (color_X + color_Y + color_Z)

        color_xy = [color_x, color_y]

        return color_xy

    def Hue_lights(self) -> list:
        '''
            This is a sample method.

            This sample method is intended to help illustrate what method docstrings should look like.

            Notes
            ---------------
            'self' does not need to be included in the Args section.

            Args
            ---------------
            None

            Returns
            ---------------
            None
        '''

        My_bridge 			= Bridge(self.Bridge_ip.eval())
        lights 				= My_bridge.lights
        return lights

