from __future__ import division
import mk_sense
from pylab import *

#foo = [12, 12.1, 12.2, 12.3, 12.4, 12.5, 12.51, 12.52, 12.53, 12.54, 12.6, 12.7, 12.8, 12.9, 13, 200, 19, 0, 8, 9.1, 0, #0 ,0 ,0 ,0 ,0 ,0, 0 ,0, 0 ,0, 0,0,0, -92012]
#fua = [0, 0, 0, 1]
#fuda = [[1, 2, 3, 4], [5, 6, 7, 8]]
#flima = [[[0,1],[7,8]],[[0,1], [9,10]]]
#flemba = [[[[256],[127],[64],[12]]]]
#acc= float(1)
#print max(flemba)
#print min(flemba)

def rep_filter(listf, acc):
	l = filter(lambda x: (sum(listf)/len(listf))-acc<x<(sum(listf)/len(listf))+acc, listf)
	return l

def function_a(fua, foo):
	for i in range(len(fua)):
		foo.append(fua[i])
def function_a2(fuda, foo):
	for i in range(len(fuda)):
		for j in range(len(fuda[i])):
			foo.append(fuda[i][j])
def function_a3(flima, foo):
	for i in range(len(flima)):
		for j in range(len(flima[i])):
			for k in range(len(flima[i][j])):
				foo.append(flima[i][j][k])
def function_a4(flemba, foo):
	for i in range(len(flemba)):
		for j in range(len(flemba[i])):
			for k in range(len(flemba[i][j])):
				for m in range(len(flemba[i][j][k])):
					foo.append(flemba[i][j][k][m])

def break_list_and_append_to(listA, foo):
	try:
		function_a4(listA, foo)
	except TypeError:
		try: 
			function_a3(listA, foo)
		except TypeError:
			try:
				function_a2(listA, foo)
			except TypeError:
				function_a(listA, foo)
#break_list_and_append_to(fua, foo)
#break_list_and_append_to(fuda, foo)
#break_list_and_append_to(flima, foo)
#break_list_and_append_to(flemba, foo)

		

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
		
