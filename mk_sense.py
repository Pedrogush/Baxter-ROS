#!/usr/bin/env python
# should output a file that gives the difference between two different .feel files, the intention is to build a database, from 0 to 1000 grams load, each file being compared to the 0 load file, that allows us to develop linear approximations for the joints, which in turn will let us guess the weight. Next step will be, if weight is accurate enough, to work with different geometries.
import os

class torque_acumulator(object):
	def __init__(self):
		self.TorqueListMean = [0]*16
		self.TorqueListLow = [0]*16
		self.TorqueListHigh = [0]*16
		self.Den = 0
	def acum(self, effort_reader):
		self.Den = self.Den+1
		for i in range(16):
			self.TorqueListMean[i] = self.TorqueListMean[i] + effort_reader.Harm_NR[i] 
			self.TorqueListLow[i] = self.TorqueListLow[i] + effort_reader.Harm_NLest[i] 
			self.TorqueListHigh[i] = self.TorqueListHigh[i] + effort_reader.Harm_NHest[i]
	def get_div(self):
		for i in range(16):
			self.TorqueListMean[i] = self.TorqueListMean[i]/self.Den 
			self.TorqueListLow[i] = self.TorqueListLow[i]/self.Den 
			self.TorqueListHigh[i] = self.TorqueListHigh[i]/self.Den
	def print_torques(self):
		print 'The mean torque across the joints is:'
		print  self.TorqueListMean
		print 'The lowest for each joint is:'
		print  self.TorqueListLow
		print 'The highest for each joint is:'
		print  self.TorqueListHigh
def rootname_minus_n(rootname):
	p = ''
	rootname.split()
	for i in range(len(rootname)):
		try:
			int(rootname[i])
		except ValueError:
			p = p + rootname[i]
	return p
			


class impression_taker(object):
	def __init__(self,a,b, rootname):
		self.p = rootname_minus_n(rootname)
		self.numbers= {'p': self.p,'rootname': rootname, 'number1': repr(a), 'number2':repr(b)}
		self.S = open('./resources/{p}/{rootname}{number1}-{number2}.impr'.format(**self.numbers), 'w')

class effort_reader(object):
	def __init__(self, a, nb, rootname):
		self.p = rootname_minus_n(rootname)
		self.Harm_N1 = [0]*17
		self.Harm_NLest1 = [0]*17
		self.Harm_NHest1 = [0]*17
		self.Harm_NR = [0]*17
		self.Harm_N = [0]*17
		self.Harm_D = [0]*17
		self.Harm_NLest = [100]*17
		self.Harm_NHest = [0]*17
		self.size = os.path.getsize('./resources/%s/%s-%s.feel' %(self.p,nb,a))
		self.F = open('./resources/%s/%s-%s.feel' %(self.p,nb,a) , 'r')
		self.V = memoryview(repr(self.F.readlines()))
		self.numbercount = 0
		self.decimals = 1
		self.N_num = 0
		self.allocation = 0
		self.x=0
                self.i=0
		self.inverter = 1
		self.interpretV=0
		self.iEMode = 0
		self.Ef_Filter = 0
		self.Ef_Filter_Clone = 0
		self.j=0
		self.l=0
	def rep_filter(self,listf, acc):
		self.l = filter(lambda x: (sum(listf)/len(listf))-acc<x<(sum(listf)/len(listf))+acc, listf)
		return self.l
	def self_filter_Ef(self):
		for i in range(16):
			self.Ef_Filter[i] = filter(lambda x: x!=0, self.Ef_Filter[i])
		self.Ef_Filter = filter(lambda x: x!=[], self.Ef_Filter)
	def clear(self):
		self.numbercount = 0
		self.decimals = 1
		self.N_num = 0
		self.allocation = 0
		self.x=0
                self.i=0		
	def allocation_def(self):
		while self.i<self.size+1:
			self.i = self.i+1
                	if self.V[self.i]== '.':
				self.allocation = self.allocation + 1
                self.Ef1 = [0]*self.allocation
		self.Ef_Filter = [[0 for i in range(self.allocation)] for j in range(17)]
		self.Ef_Filter_Clone =  [[0 for i in range(self.allocation)] for j in range(17)]
		self.i=0
        def interpret(self, string):
	 if self.iEMode==0:
	    if string =='e':
	       self.iEMode=1
	    if string =='-':
	       self.inverter = -self.inverter
            if string == '(':
               startline=1
	    if string == ',':
	       self.decimals = 1
	       self.numberpass = 1
               self.Ef1[self.N_num] = self.Ef1[self.N_num] *self.inverter
	       self.N_num = self.N_num + 1
 	       self.inverter = 1 
	    if string == '0':
	       self.c = float(string)
	       self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c
	       self.decimals = self.decimals*0.1 
	       self.numbercount = self.numbercount+1
	    if string == '1':
	       self.c = float(string)
	       self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c
	       self.decimals = self.decimals*0.1  
	       self.numbercount = self.numbercount+1 
	    if string == '2':
	       self.c = float(string)
	       self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c
	       self.decimals = self.decimals*0.1 
	       self.numbercount = self.numbercount+1
	    if string == '3':
	       self.c = float(string)
	       self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c
	       self.decimals = self.decimals*0.1 
	    if string == '4':
	       self.c = float(string)
	       self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c  
	       self.decimals = self.decimals*0.1 
	       self.numbercount = self.numbercount+1
	    if string == '5':
	     self.c = float(string)
	     self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c  
	     self.decimals = self.decimals*0.1 
	     self.numbercount = self.numbercount+1
	    if string == '6':
	     self.c = float(string)
	     self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c  
	     self.decimals = self.decimals*0.1 
	     self.numbercount = self.numbercount+1
	    if string == '7':
	     self.c = float(string)
	     self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c  
	     self.decimals = self.decimals*0.1 
	     self.numbercount = self.numbercount+1
	    if string == '8':
	     self.c = float(string)
	     self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c  
	     self.numbercount = self.numbercount+1
	    if string == '9':
	     self.c = float(string)
	     self.Ef1[self.N_num] = self.Ef1[self.N_num] + self.decimals*self.c 
	     self.decimals = self.decimals*0.1   
	     self.numbercount = self.numbercount+1
	    if string == '.':
	     if self.numbercount > 1:
		self.Ef1[self.N_num] = 10*self.Ef1[self.N_num]  
		self.decimals = 10*self.decimals 
	    if string == ' ':
	     self.numbercount = 0
	    if string == ')':
	     self.Ef1[self.N_num] = self.Ef1[self.N_num] *self.inverter
	     self.N_num = self.N_num + 1
	     self.inverter = 1 
	 if self.iEMode==1:
	     try:
		self.interpretV = int(string)
	     except ValueError:
		self.interpretV = self.interpretV
	     if self.interpretV > 0:
		for i in range(self.interpretV):
 	           self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]] = self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]]/10 
	        self.iEMode = 0; self.interpretV = 0

# run get least and maximum effort before getting mean effort, CODE NEEDS HEAVY CLEANUP
	def calc_values_per_joint(self):
		for i in range(self.N_num):
		        self.Ef_Filter[self.j][i] = self.Ef1[i]
			self.j = self.j +1
			if self.j>16:
				self.j = 0
		while self.i<self.N_num:
		     self.Harm_N[self.x] = self.Harm_N[self.x] + self.Ef1[self.i]
		     self.Harm_D[self.x] = self.Harm_D[self.x] + 1
		     if self.Harm_NLest[self.x]>self.Ef1[self.i]:
			self.Harm_NLest[self.x] = self.Ef1[self.i]
		     if self.Harm_NHest[self.x]<self.Ef1[self.i]:
			self.Harm_NHest[self.x] = self.Ef1[self.i]
		     self.i=self.i+1
		     self.x=self.x+1
		     if self.x>16:
			self.x=0
		self.i=0
		while self.i <16:
		      self.i = self.i+1
		      self.Harm_NR[self.i] = self.Harm_N[self.i]/self.Harm_D[self.i]
		self.i = 0           
# NEEDS HEAVY CLEANUP
	def print_mean_effort_per_joint(self, a, impression_taker):
		impression_taker.S.write('The mean torque for each joint in file %s.feel is: uMl \n' %a)
		while self.i < 16:
		      impression_taker.S.write(repr(self.Harm_NR[self.i]))
		      impression_taker.S.write('uM')
                      self.i = self.i+1
                self.i = 0

# This looks good for now...
	def print_lowest_recorded_torque(self, a, impression_taker):	
		impression_taker.S.write('The lowest recorded torque for each joint in file %s.feel is: uMl \n' %a)
		while self.i <16:
		      impression_taker.S.write(repr(self.Harm_NLest[self.i]))
		      impression_taker.S.write('uM')
		      self.i = self.i+1
		self.i = 0
	def print_highest_recorded_torque(self,a, impression_taker):
		impression_taker.S.write('The highest recorded torque for each joint in file %s.feel is: uMl \n' %a)
		while self.i <16:
		      impression_taker.S.write(repr(self.Harm_NHest[self.i]))
		      impression_taker.S.write('uM')
		      self.i = self.i+1
		self.i = 0

	def get_differences_in_torque(self , effort_reader2):
		while self.i<16:
		      self.Harm_N1[self.i] = self.Harm_NR[self.i]-effort_reader2.Harm_NR[self.i]
		      self.Harm_NLest1[self.i] = self.Harm_NLest[self.i]- effort_reader2.Harm_NLest[self.i]
		      self.Harm_NHest1[self.i] = self.Harm_NHest[self.i]- effort_reader2.Harm_NHest[self.i] 
		      self.i = self.i+1 
		self.i=0

# Print difference AND clear the object's memory about that specific comparison
	def print_difference_between_mean_torques(self, impression_taker):
		impression_taker.S.write('The difference between the mean torques in file 1 and file 2 is: uMl\n')
		while self.i<16:  
		      impression_taker.S.write(repr(self.Harm_N1[self.i]))
		      impression_taker.S.write('uM')
		      self.i = self.i+1
		self.i=0
	def print_difference_between_lowest_torques(self, impression_taker):
		impression_taker.S.write('The difference between the lowest recorded torques in file 1 and file 2 is: uMl\n')
		while self.i<16: 
	              impression_taker.S.write(repr(self.Harm_NLest1[self.i]))
                      impression_taker.S.write('uM')
		      self.i = self.i+1
		self.i=0
	def print_difference_between_highest_torques(self, impression_taker):
		impression_taker.S.write('The difference between the highest recorded torques in file 1 and file 2 is: uMl\n')
		while self.i<16:      
	              impression_taker.S.write(repr(self.Harm_NHest1[self.i]))
	              impression_taker.S.write('uM')
		      self.i = self.i+1
		self.i=0
        def read_file(self):
		while self.i<self.size+1:
		  self.interpret(self.V[self.i])
		  self.i = self.i+1
                self.i=0

# CODE NEEDS VERY HEAVY CLEANUP, IF NOT DONE BY FRIDAY SHOW AS IS
def main():
        T = [0]*3
        c1 = 0
	while c1<2:
		T[c1] = effort_reader(1, 'NoWeight')
		T[c1].allocation_def()
		T[c1].read_file()
		T[c1].print_lowest_recorded_torque()
		T[c1].print_highest_recorded_torque()
                if c1>0:
                	T[c1].get_differences_in_torque(T[c1-1])
                        T[c1].print_difference_between_mean_torques()
                        T[c1].print_difference_between_lowest_torques()
                        T[c1].print_difference_between_highest_torques()
                c1=c1+1
		print self.Ef_Filter

if __name__ == "__main__":
    main()
