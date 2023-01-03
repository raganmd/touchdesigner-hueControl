'''
Matthew Ragan | matthewragan.com
Zoe Sandoval | zoesandoval.com
'''

import sys
import threading
import json
import requests

class Hue:
    '''
        This is a sample class.

        This sample class has several important features that can be described here.


        Notes
        ---------------
        Your notes about the class go here
     '''

    def __init__(self, myOp:OP) -> None:

        self.My_op 				= myOp
        self.Dep_path 			= '{}/dep/python/'.format(project.folder)
        self.Bridge_ip 			= parent().par.Bridgeip

        self.Brightness_from 	= (0, 1)
        self.Brightness_to 		= (0, 255)

        self.Gamma 				= .75

        self.X_vals		 		= (0.664511, 0.154324, 0.162028)
        self.Y_vals		 		= (0.283881, 0.668433, 0.047685)
        self.Z_vals				= (0.000088, 0.072310, 0.986039)

        self.Lights_page_name  	= "Individual Lights"
        self.Trans_time_scaler 	= 10

        self.My_bridge 			= None

        self.Use_threads 		= parent().par.Usethreads

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
        return f"{self._bridge_address}/resource/light"

    @property
    def _hue_headers(self) -> dict:
        hue_headers = {
            "hue-application-key":self.My_op.par.Deviceusername.eval(), 
            "Accept": "*/*",
            "Host" : "https://10.0.1.60/api"}
        return hue_headers

    def _bytes_to_json(self, message:bytes) -> json:
        str_message = message.decode("utf-8")
        msg_json = json.loads(str_message)
        return msg_json

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
            json_blob = self._bytes_to_json(set_up_msg.content)
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
        print(self._hue_headers)
        all_lights = requests.get(self._lights_address, headers=self._hue_headers, verify=False)
        print(all_lights)
        print(all_lights.content)




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

