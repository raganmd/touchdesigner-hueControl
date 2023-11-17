'''
Matthew Ragan | matthewragan.com
Zoe Sandoval | zoesandoval.com
'''


from TDHueControllerEXT import TDHueController


class TDHueInterface:
    '''
    The TDHueInterface is the primary mechanism that TouchDesigner
    uses to interact with Phillips Hue Lights. This interface
    is designed to gather and route control messages from TouchDesigner
    Custom Parameters to Hue Lights. 

    The separation of TD Interface from lighting controller allows 
    for a specialized set of operational foci based on the intended 
    target for the code being written. 

    Notes
    ---------------
    To see all debug messages change the DEBUG member to True
    '''

    DEBUG = False
    Version = '1.1.0'

    def __init__(self, my_op: callable) -> None:

        self.My_op = my_op
        self.Controller = TDHueController(my_op)
        print("💡 TDHue Interface Init")

    def Parse_par_exec(self, par: callable) -> None:
        try:
            if "Light" in par.name:
                func = getattr(self.My_op, tdu.base(par.name))
                func(par)

            else:

                func = getattr(self.My_op, par.name)
                func(par)

        except Exception as e:
            if TDHueInterface.DEBUG:
                debug(f"💡 TDHue Interface Error | {e}")
            else:
                pass

    # NOTE Pars
    def Initializelights(self, par: callable) -> None:
        # Pulse par
        self.Controller.Clear_and_setup_lights()
        print(f"running {par.name}")

    def Linktobridge(self, par: callable) -> None:
        # Pulse par
        title = "Link to Bridge"
        message = """You are about to link TouchDesigner
to your Hue Bridge. Before proceeding
please click the link button on your Bridge
then click okay
"""
        buttons = ["Cancel", "Okay"]
        proceed_to_link = ui.messageBox(title, message, buttons=buttons)

        if proceed_to_link:
            print(f"running {par.name}")
            self.Controller._bridge_setup()

        else:
            pass

    def Allcolor(self, par: callable) -> None:
        # par group rgb
        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Allbrightness(self, par: callable) -> None:
        # float par
        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Alltranstimes(self, par: callable) -> None:
        # float par
        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Allpower(self, par: callable) -> None:
        # toggle par
        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Updateall(self, par: callable) -> None:
        # pulse par
        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    # NOTE individual lights
    def Updatebysettings(self, par: callable) -> None:
        # pulse par
        self.Controller.Clear_and_setup_lights()

        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Lightcolor(self, par: callable) -> None:
        # par group rgb
        self._update_hue_light(par)

        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Lightbri(self, par: callable) -> None:
        # float par
        self._update_hue_light(par)

        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Lighttrans(self, par: callable) -> None:
        # float par
        self._update_hue_light(par)

        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Lightpwr(self, par: callable) -> None:
        # toggle par
        self._update_hue_light(par)

        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def Updatelight(self, par: callable) -> None:
        # pulse par
        if TDHueInterface.DEBUG:
            debug(f"running {par.name}")
        else:
            pass

    def _update_hue_light(self, par: callable) -> None:
        light_digit = tdu.digits(par.name)
        light_id = self.My_op.par[f'Lightid{light_digit}'].eval()
        rgb = [
            self.My_op.par[f'Lightcolor{light_digit}r'].eval(),
            self.My_op.par[f'Lightcolor{light_digit}g'].eval(),
            self.My_op.par[f'Lightcolor{light_digit}b'].eval()
        ]
        on_state = self.My_op.par[f'Lightpwr{light_digit}'].eval()
        brightness = self.My_op.par[f'Lightbri{light_digit}'].eval()
        self.Controller.Update_light(light_id, rgb, on_state, brightness)
