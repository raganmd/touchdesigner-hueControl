'''
Matthew Ragan | matthewragan.com
'''

import sys
from phue import Bridge

class Hue:
	'''
		This is a sample class.
		
		This sample class has several important features that can be described here.
		
		
		Notes
		---------------
		Your notes about the class go here
 	'''

	def __init__(self, myOp):

		self.My_op 				= myOp
		self.Dep_path 			= '{}/dependencies/python/'.format(project.folder)
		self.Bridge_ip 			= parent().par.Bridgeip.val

		self.Brightness_from 	= (0, 1)
		self.Brightness_to 		= (0, 255)

		self.Gamma 				= .75

		self.X_vals		 		= (0.664511, 0.154324, 0.162028)
		self.Y_vals		 		= (0.283881, 0.668433, 0.047685)
		self.Z_vals				= (0.000088, 0.072310, 0.986039)

		self.Lights_page_name  	= "Individual Lights"
		self.Trans_time_scaler 	= 10

		print("Hue Control Init")
		return

	def Check_dep(self):
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

		if self.Dep_path in sys.path:
			pass

		else:
			sys.path.append(self.Dep_path)

		for each in sys.path:
			print(each)

		return


	def Hue_lights(self):
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

		My_bridge 			= Bridge(self.Bridge_ip)
		lights 				= My_bridge.lights
		return lights

	def Remap_brightness(self, brightness):
		'''
			Remap values from 0-1 to 0-255.
			
			This is a helper function used to convert normalized values to 0-255.
			                
			Notes
			---------------
			'self' does not need to be included in the Args section.
			
			Args
			---------------
			brightness (float)
			> A normalized float value to be converted to 0-255 
						
			Examples
			---------------
			self.Remap_brightness(1)
			
			Returns
			---------------
			new_brightness (int)
			> An interger value of 0 - 255
		'''

		new_brightness 		= int(tdu.remap(brightness, 
											self.Brightness_from[0], 
											self.Brightness_from[1], 
											self.Brightness_to[0], 
											self.Brightness_to[1]))

		return new_brightness


	def Convert_color(self, rgb):
		'''
			A hue color conversion method.
			
			This method is used to transform color from rgb values to hue xy 
			values. This follows the hue API for color space conversion.
			                
			Notes
			---------------

			
			Args
			---------------
			rgb (list)
			> A list of rgb values to be convereted into the xy color space for the hue
			
			Examples
			---------------
			color 		= [1.0, 0.0, 0.0]
			self.Convert_color(color)

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

		color_X 			= g_correction[0] * self.X_vals[0] + g_correction[1] * self.X_vals[1] + g_correction[2] * self.X_vals[2]
		color_Y 			= g_correction[0] * self.Y_vals[0] + g_correction[1] * self.Y_vals[1] + g_correction[2] * self.Y_vals[2]
		color_Z 			= g_correction[0] * self.Z_vals[0] + g_correction[1] * self.Z_vals[1] + g_correction[2] * self.Z_vals[2]

		color_x 			= color_X / (color_X + color_Y + color_Z)
		color_y 			= color_Y / (color_X + color_Y + color_Z)

		color_xy 			= [color_x, color_y]

		return color_xy


	def Add_pars_for_lights(self):
		'''
			Set-up funciton for getting the lihghting parameters ready with a new device.
			
			This method loops through the lights that are reported by a given hue Bridge
			and creates custom paramaters on the parent() compoent.
			                
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

		lights_page 				= parent().appendCustomPage("Individual Lights")

		# add update all pulse:
		lights_page.appendPulse('Updatebysettings', label='Update by Settings')

		# build custom pars for all lights
		for each_light in enumerate(self.Hue_lights()):

			# add the string name of the light
			str_name 		= 'Lightname{}'.format(each_light[0])
			str_label 		= 'Light {} Name'.format(each_light[0])
			lights_page.appendStr(str_name, label=str_label)

			# add a color control par
			rgb_name 		= 'Lightcolor{}'.format(each_light[0])
			rbg_label 		= 'Light {} Color'.format(each_light[0])
			lights_page.appendRGB(rgb_name, label=rbg_label)

			# add a brightness control par
			bri_name 		= 'Lightbri{}'.format(each_light[0])
			bri_label 		= 'Light {} Brightness'.format(each_light[0])
			lights_page.appendFloat(bri_name, label=bri_label)

			# add a transition time control par
			tri_name 		= 'Lighttrans{}'.format(each_light[0])
			tri_label 		= 'Light {} Trans Time'.format(each_light[0])
			lights_page.appendInt(tri_name, label=tri_label)

			# add a power control par
			pwr_name 		='Lightpwr{}'.format(each_light[0])
			pwr_label 		='Light {} Power'.format(each_light[0])
			lights_page.appendToggle(pwr_name, label=pwr_label)

			# add an update pulse button
			update_name 	= 'Updatelight{}'.format(each_light[0])
			update_label 	= 'Update {} Light'.format(each_light[0])
			lights_page.appendPulse(update_name, label=update_label)

			# set string name for lights based on Hue
			parent().pars('Lightname{}'.format(each_light[0]))[0].val = each_light[1].name

			# set par to be readonly
			parent().pars('Lightname{}'.format(each_light[0]))[0].readOnly = True

			# add section divider
			parent().pars('Lightname{}'.format(each_light[0]))[0].startSection = True

		return

	def Clear_hue_lights(self):
		'''
			A helper function for setting-up the custom parameters.
			
			This function is used to clear out all of the custom parameters
			on the "Individual Lights" page.
			                
			Notes
			---------------
			None.
			
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

		return

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
		return

	def Build_command_dict(self, light_index):
		'''
			A helper function for building a command dictionary for lights.
			
			In the phue library there's a function available for setting lights
			based on their name. This function looks to the index of the parmeter
			that's been pulsed, and retrieves all of the reivant information to build
			a command list.
			                
			Notes
			---------------
			None
			
			Args
			---------------
			light_index (int)
			> The integer value assocaited with the custom parameter index for a light
						
			Examples
			---------------
			self.Build_command_dict(1)

			Returns
			---------------
			command_dict (dict)
			> A dictionary with all appropriate keys for using the set_light() command
		'''

		on_cmd 				= parent().pars('Lightpwr{}'.format(light_index))[0].val
		bri_cmd 			= parent().pars('Lightbri{}'.format(light_index))[0].val
		trans_cmd 			= 1 if parent().pars('Lighttrans{}'.format(light_index))[0].val == 0 else parent().pars('Lighttrans{}'.format(light_index))[0].val
		xy_cmd 				= self.Convert_color([chan.val for chan in parent().pars('Lightcolor{}*'.format(light_index))])

		command_dict 		= {
			'on'				: bool(on_cmd),
			'bri'				: self.Remap_brightness(bri_cmd),
			'transitiontime'	: trans_cmd * self.Trans_time_scaler,
			'xy'				: xy_cmd
		}
		return command_dict

	def Update_light_by_par_index(self, par_index, debug=False):
		'''
			This is helper method for sending a set_light() command to a specific hue light.
			
			This method fetches the approprite light name, constructs a command list, and then
			sends a command to the hue bridge to set the specified light appropriately.
			                
			Notes
			---------------
			None
			
			Args
			---------------
			par_index (int)
			> The integer value assocaited with the custom parameter index for a light
			
			debug (bool)
			> A boolean value for toggling logged output
			
			Examples
			---------------
			self.Update_light_by_par_index(1)

			Returns
			---------------
			None
		'''

		My_bridge 			= Bridge(self.Bridge_ip)

		command_dict 		= self.Build_command_dict(par_index)
		light_name 			= parent().pars('Lightname{}'.format(par_index))[0].val	

		My_bridge.set_light(light_name, command_dict)

		if debug:
			print("light name | ", light_name)
			print("command dict | ", command_dict)
		else:
			pass

		return

	def Update_all_by_settings(self):
		'''
			Loops through all lights and uses the settings on the Individual Lights page.
			
			This method uses the settings on the "Individual Lights page to set the pars for
			all lights. This allows for a single pulse update rather than individual lighting
			calls per light. This convience function takes advantage of other helper methods.
			                
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

		My_bridge 			= Bridge(self.Bridge_ip)
		num_lights 			= len(My_bridge.lights)

		for each in range(num_lights):
			self.Update_light_by_par_index(each)

		print("Update all by Settings")
		return

	def Set_all_lights(self):
		'''
			Set all Lights to uniform pars.
			
			This method uses the parameters set on the "All Lights" page to send commands to all 
			hue lights at the same time. This assumes you would like to control all lights in the
			same fashion - as a single group.
			                
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
		My_bridge 			= Bridge(self.Bridge_ip)
		
		transition 			= parent().par.Alltranstime.val * self.Trans_time_scaler
		brightness 			= self.Remap_brightness(parent().par.Allbrightness.val)
		rgb 				= self.Convert_color([chan.val for chan in parent().pars('Allcolor*')])

		for each in My_bridge.lights:
			print(each)
			each.on 				= parent().par.Allpower.val
			each.transitiontime 	= transition
			each.xy 				= rgb
			each.brightness 		= brightness

		return