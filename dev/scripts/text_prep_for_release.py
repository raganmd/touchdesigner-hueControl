base_save 		= op('base_hueControl')
version 		= op('table_version')[0,0].val
reset_color 	= (0.545, 0.545, 0.545)
save_loc 		= '../release/base_hueControl.tox'
ext_file 		= 'hueControlEXT'

# save tox
base_save.par.Version 					= version
base_save.op(ext_file).par.file 		= ''
base_save.op(ext_file).par.loadonstart = False
base_save.par.externaltox 				= ''
base_save.color 						= reset_color
base_save.op('null_icon').lock 			= True
base_save.op('svg_icon').destroy()
base_save.op('transform1').destroy()
base_save.save(save_loc)