#!/usr/bin/env python
# should output a file that gives the difference between two different .feel files, the intention is to build a database, from 0 to 1000 grams load, each file being compared to the 0 load file, that allows us to develop linear approximations for the joints, which in turn will let us guess the weight. Next step will be, if weight is accurate enough, to work with different geometries.
import os

class impression_taker(object):
	def __init__(self,a,b):
		self.numbers= {'number1': repr(a), 'number2':repr(b)}
		self.S = open('./resources/{number1}-{number2}.impr'.format(**self.numbers), 'w')

class effort_reader(object):
	def __init__(self, a):
		self.Harm_N1 = [0]*17
		self.Harm_NLest1 = [0]*17
		self.Harm_NHest1 = [0]*17
		self.Harm_NR = [0]*17
		self.Harm_N = [0]*17
		self.Harm_D = [0]*17
		self.Harm_NLest = [100]*17
		self.Harm_NHest = [0]*17
		self.size = os.path.getsize('./resources/%s.feel' %a)
		self.F = open('./resources/%s.feel' %a , 'r')
		self.V = memoryview(repr(self.F.readlines()))
		self.numbercount = 0
		self.decimals = 1
		self.N_num = 0
		self.allocation = 0
		self.x=0
                self.i=0
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
		self.i=0
        def interpret(self, string):
            if string == '(':
               startline=1
	    if string == ',':
	       self.decimals = 1
	       self.numberpass = 1
	       self.N_num = self.N_num + 1
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
	     self.N_num = self.N_num + 1
# run get least and maximum effort before getting mean effort, CODE NEEDS HEAVY CLEANUP
	def calc_values_per_joint(self):
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
		impression_taker.S.write('The mean torque for each joint in file %s.feel is: uM \n' %a)
		while self.i < 16:
		      print self.Harm_NR[self.i]
                      print '\n'
		      impression_taker.S.write(repr(self.Harm_NR[self.i]))
		      impression_taker.S.write('uM')
                      self.i = self.i+1
                self.i = 0

# This looks good for now...
	def print_lowest_recorded_torque(self, a, impression_taker):	
		impression_taker.S.write('The lowest recorded torque for each joint in file %s.feel is: uM \n' %a)
		while self.i <16:
		      print self.Harm_NLest[self.i]
                      print '\n'
		      impression_taker.S.write(repr(self.Harm_NLest[self.i]))
		      impression_taker.S.write('uM')
		      self.i = self.i+1
		self.i = 0
	def print_highest_recorded_torque(self,a, impression_taker):
		impression_taker.S.write('The highest recorded torque for each joint in file %s.feel is: uM \n' %a)
		while self.i <16:
		      print self.Harm_NHest[self.i]
                      print '\n'
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
		impression_taker.S.write('The difference between the mean torques in file 1 and file 2 is: uM\n')
		while self.i<16:  
		      print self.Harm_N1[self.i]
		      impression_taker.S.write(repr(self.Harm_N1[self.i]))
		      impression_taker.S.write('uM')
		      self.i = self.i+1
                      print '\n'
		self.i=0
                print '\n'
	def print_difference_between_lowest_torques(self, impression_taker):
		impression_taker.S.write('The difference between the lowest recorded torques in file 1 and file 2 is: uM\n')
		while self.i<16: 
	              print self.Harm_NLest1[self.i]
	              impression_taker.S.write(repr(self.Harm_NLest1[self.i]))
                      impression_taker.S.write('uM')
		      self.i = self.i+1
                      print '\n'
		self.i=0
                print '\n'
	def print_difference_between_highest_torques(self, impression_taker):
		impression_taker.S.write('The difference between the highest recorded torques in file 1 and file 2 is: uM\n')
		while self.i<16:      
		      print self.Harm_NHest1[self.i]
	              impression_taker.S.write(repr(self.Harm_NHest1[self.i]))
	              impression_taker.S.write('uM')
		      self.i = self.i+1
                      print '\n'
		self.i=0
                print '\n'
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
		T[c1] = effort_reader()
		T[c1].get_user_input()
		T[c1].allocation_def()
		T[c1].read_file()
		T[c1].get_least_and_maximum_effort_per_joint()
		T[c1].get_mean_effort_per_joint()
		T[c1].print_lowest_recorded_torque()
		T[c1].print_highest_recorded_torque()
                if c1>0:
                	T[c1].get_differences_in_torque(T[c1-1])
                        T[c1].print_difference_between_mean_torques()
                        T[c1].print_difference_between_lowest_torques()
                        T[c1].print_difference_between_highest_torques()
                c1=c1+1


if __name__ == "__main__":
    main()
