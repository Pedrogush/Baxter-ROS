foo = [12, 12.1, 12.2, 12.3, 12.4, 12.5, 12.51, 12.52, 12.53, 12.54, 12.6, 12.7, 12.8, 12.9, 13, 200, 19, 0, 8, 9.1, 0, 0 ,0 ,0 ,0 ,0 ,0, 0 ,0, 0 ,0, 0,0,0]
acc= float(1)

def rep_filter(listf, acc):
	print sum(listf)/len(listf)
	l = filter(lambda x: (sum(listf)/len(listf))-acc<x<(sum(listf)/len(listf))+acc, listf)
	return l
foo = rep_filter(foo, 0.05)
print foo, 
		

#Ef1 is a list of ALL the numbers in the .feel file, we need a way to break the list into all numbers for a given joint, then update the list by removing anything that is too out of hand of the current mean value, we start with nofiltermeanvalue and work our way from there. accuracy can vary, initial formula is of the form accuracy = 100/(step*steps+100)
#variables: accuracy, currentmeanvalue, nofiltermeanvalue, filteredmeanvalue, list, filteredlist

#def class nonlinear_torque_filter(object):
#	def __init__(self):
#		self.accuracy = 1
#		self.steps = 0
#		self.currentmeanvalue = 0
#		self.nofiltermeanvalue = 0
#		self.filteredmeanvalue = 0
#		self.list = 0
#		self.filteredlist = 0
		