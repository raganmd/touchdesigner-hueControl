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

    DEBUG = True

    def __init__(self, my_op:callable) -> None:

        self.My_op = my_op
        self.Controller = TDHueController(my_op)
        print("💡 TDHue Interface Init")
    
    def Parse_par_exec(self, par:callable) -> None:
        try:
            if "Light" in par.name:
                func = getattr(self.My_op, par.name[:-1])
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
    def Initializelights(self, par:callable) -> None:
        # Pulse par
        print(f"running {par.name}")

    def Linktobridge(self, par:callable) -> None:
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


    def Allcolor(self, par:callable) -> None:
        # par group rgb
        print(f"running {par.name}")

    def Allbrightness(self, par:callable) -> None:
        # float par
        print(f"running {par.name}")

    def Alltranstimes(self, par:callable) -> None:
        # float par
        print(f"running {par.name}")

    def Allpower(self, par:callable) -> None:
        # toggle par
        print(f"running {par.name}")

    def Updateall(self, par:callable) -> None:
        # pulse par
        print(f"running {par.name}")

    # NOTE individual lights    
    def Updatebysettings(self, par:callable) -> None:
        # pulse par
        self.Controller.Clear_and_setup_lights()
        print(f"running {par.name}")

    def Lightcolor(self, par:callable) -> None:
        # par group rgb
        print(f"running {par.name}")

    def Lightbri(self, par:callable) -> None:
        # float par
        print(f"running {par.name}")

    def Lighttrans(self, par:callable) -> None:
        # float par
        print(f"running {par.name}")

    def Lightpwr(self, par:callable) -> None:
        # toggle par
        print(f"running {par.name}")

    def Updatelight(self, par:callable) -> None:
        # pulse par
        print(f"running {par.name}")