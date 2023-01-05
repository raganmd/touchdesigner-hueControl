# me - this DAT
# cur - the Par object that has changed
# prev - the previous value (or a list of previous values)
# 
# NOTE: If Callback Mode is set to 'Combine ParGroup Changes as List', both cur and prev are instead lists.
# NOTE: Make sure the corresponding toggle is enabled in the ParGroup Execute DAT.

def onValueChange(cur, prev):
	# use cur.eval() to get current
	parent().Parse_par_exec(cur)
	return

def onPulse(cur):
	parent().Parse_par_exec(cur)
	return
