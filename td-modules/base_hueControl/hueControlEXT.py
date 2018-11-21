'''
Matthew Ragan | matthewragan.com
'''

import sys
from phue import Bridge

class Hue:

	def __init__(self, myOp):

		self.My_op 			= myOp
		self.Dep_path 		= '{}/dependencies/python/'.format(project.folder)
		self.Bridge_ip 		= parent().par.Bridgeip.val

		self.Brightness_from 	= (0, 1)
		self.Brightness_to 		= (0, 255)

		self.X_vals		 	= (0.664511, 0.154324, 0.162028)
		self.Y_vals		 	= (0.283881, 0.668433, 0.047685)
		self.Z_vals			= (0.000088, 0.072310, 0.986039)


		print("Hue Control Init")
		return

	def Check_dep(self):

		if self.Dep_path in sys.path:
			pass

		else:
			sys.path.append(self.Dep_path)

		for each in sys.path:
			print(each)


		return

	def Set_lights(self):

		My_bridge 			= Bridge(self.Bridge_ip)
		transition 			= 10

		brightness 			= 1

		new_brightness 		= self.Remap_brightness(brightness)

		rgb 				= op('constant1').sample(x=0,y=0)

		for each in My_bridge.lights:
			print(each)
			each.on 				= True
			each.transitiontime 	= transition * 10
			each.xy 				= self.Convert_color(rgb)
			each.brightness 		= new_brightness
		
		return


	def Remap_brightness(self, brightness):

		new_brightness 		= int(tdu.remap(brightness, 
											self.Brightness_from[0], 
											self.Brightness_from[1], 
											self.Brightness_to[0], 
											self.Brightness_to[1]))

		return new_brightness


	def Convert_color(self, rgb):
		gamma 				= 1.5
		g_correction 		= [pow(each_chan, (1/gamma)) for each_chan in rgb]

		color_X 			= g_correction[0] * self.X_vals[0] + g_correction[1] * self.X_vals[1] + g_correction[2] * self.X_vals[2]
		color_Y 			= g_correction[0] * self.Y_vals[0] + g_correction[1] * self.Y_vals[1] + g_correction[2] * self.Y_vals[2]
		color_Z 			= g_correction[0] * self.Z_vals[0] + g_correction[1] * self.Z_vals[1] + g_correction[2] * self.Z_vals[2]

		color_x 			= color_X / (color_X + color_Y + color_Z)
		color_y 			= color_Y / (color_X + color_Y + color_Z)

		color_xy 			= [color_x, color_y]

		return color_xy
