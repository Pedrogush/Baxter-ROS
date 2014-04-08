import mk_sense
import os
#A = [[0 for i in range(5)] for j in range(5)]
# purpose is to take a large set of .impr files and return the average variation between differences in them, in this way we can calculate the range in which the measurement for a given variable is likely to be (effort in this case), subsequent development will allow us to gauge weight from torque with a proper treatment to the ''noise'' problem.
# IMPLEMENT IF atB>atA correctly for this class, save some memory, speed and headaches.
class noise_canceller(object):
	def __init__(self, a, b):
		self.a = a; self.b = b; self.F = [[0 for i in range(a)] for j in range(b)]; self.atA = 0
		self.atB = 0; self.V = [[[] for i in range(a)] for j in range(b)]; self.size = [[0 for i in range(a)] for j in range(b)]
                while self.atA < a:
			while self.atB < b-1:
			    self.atB = self.atB + 1
			    if self.atB>self.atA:	
		               self.numbers = {'n1': repr(self.atA),'n2': repr(self.atB)}
			       self.F[self.atA][self.atB] = open('./resources/{n1}-{n2}.impr'.format(**self.numbers), 'r')
			       self.V[self.atA][self.atB] = memoryview(repr(self.F[self.atA][self.atB].read()))
			       self.size[self.atA][self.atB]= os.path.getsize('./resources/{n1}-{n2}.impr'.format(**self.numbers))
			self.atB = 0; self.atA = self.atA + 1
		self.atA = 0; self.atB = 0
		self.Means = [[[0 for i in range(17)] for j in range(a)] for k in range(b)]
		self.Highs = [[[0 for i in range(17)] for j in range(a)] for k in range(b)]
		self.Lows = [[[100 for i in range(17)] for j in range(a)] for k in range(b)]
		self.MeansV = [0]*17; self.MeanDiffDen = [0]*17; self.HighDiffDen = [0]*17;
                self.LowDiffDen = [0]*17; self.MeanDiff = [0]*17; self.HighDiff = [0]*17
		self.LowDiff = [0]*17; self.MeanHigh = [0]*17; self.MeanLow = [100]*17; 
		self.HighHigh = [0]*17; self.HighLow = [100]*17; self.LowHigh = [0]*17; self.LowLow = [100]*17;
                self.Ef1 = []; self.Ef1_listLoc = [[0 for j in range(a)] for k in range(b)]
		self.numbercount = 0; self.decimals = 1; self.N_num = [[0 for i in range(a)] for j in range(b)]
                self.set = [[0 for i in range(a)] for j in range(b)]; self.allocation = [[0 for i in range(a)] for j in range(b)]
		self.allocationmax = 0; self.i=0; self.inverter = 1;
		self.yetanothervariable = 0; self.precedingstring = 0; self.l=-1; self.iEMode = 0; self.interpretV = 0


	def allocation_def(self):
		while self.atA<self.a:
			while self.atB<self.b-1:
				self.atB = self.atB+1	
				if self.atB>self.atA:
					while self.i<self.size[self.atA][self.atB]+1:
						self.i = self.i+1
						if self.V[self.atA][self.atB][self.i]== 'M' and self.V[self.atA][self.atB][self.i-1] == 'u':
							self.allocation[self.atA][self.atB] = self.allocation[self.atA][self.atB] + 1
					self.Ef1_listLoc[self.atA][self.atB] = self.l 
					self.l = self.l+1 		
					self.Ef1.append([0 for m in range(self.allocation[self.atA][self.atB])])
				self.i=0									
			self.atA= self.atA+1
			self.atB=0
		self.atA = 0

        def interpret(self, string, na, nb):
            if string == ':':
               self.set[na][nb]=self.set[na][nb] + 1
	    if self.set[na][nb]>3:
		if self.set[na][nb]<7 and self.iEMode == 0:
	            if string == '-':
		       self.inverter = -self.inverter
		    if string == 'u' and self.precedingstring != ':':
		       self.decimals = 1; self.numberpass = 1; self.N_num[na][nb] = self.N_num[na][nb] + 1; self.numbercount = 0; 			       self.inverter=1
	     	    try:
		       self.c = int(string)
		       self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]] = (self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]] + self.decimals*self.c)*self.inverter
		       self.decimals = self.decimals*0.1; self.numbercount = 2
	            except ValueError:
		       self.decimals = self.decimals
		    if string == 'e':
		       self.iEMode = 1
	            if string == '.' and self.numbercount>1:
				self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]] = 10*self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]]
				self.decimals = 10*self.decimals
	            if string == 'f' and self.precedingstring == '.':
 				self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]] = self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]]/10 
			        self.decimals = self.decimals/10
            if self.iEMode == 1:
		try:
			self.interpretV = int(string)
		except ValueError:
			self.interpretV = self.interpretV
		if self.interpretV > 0:
		   for i in range(self.interpretV):
 				self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]] = self.Ef1[self.Ef1_listLoc[na][nb]][self.N_num[na][nb]]/10 
	           self.iEMode = 0; self.interpretV = 0



        def read_file(self, a, b):
		while self.i<self.size[a][b]+1:
                  try:
                      self.precedingstring = self.V[a][b][self.i-1]
		  except ValueError:
		      self.precedingstring = self.precedingstring
		  self.interpret(self.V[a][b][self.i], a, b)
		  self.i = self.i+1
		self.inverter = 1;
	        self.decimals = 1; self.N_num[a][b] = 0; self.numbercount = 0 
		self.yetanothervariable = 0; self.set[a][b]=0; self.i=0
# highest variation in difference between two files in file matrix
# lowest variation in difference between two files in file matrix
# mean variation in difference between mean values in files in file matrix
# mean variation in difference between highest values in files in file matrix
# mean variation in difference between lowest values in files in file matrix

	def load_variables(self):
		while self.atB< self.b:
			while self.atA< self.a:
				if self.atA>self.atB:
					while self.i<17:
							if -30<self.Ef1[self.Ef1_listLoc[self.atB][self.atA]][self.i]<30:
								self.Means[self.atB][self.atA][self.i] = self.Ef1[self.Ef1_listLoc[self.atB][self.atA]][self.i]
							if -30<self.Ef1[self.Ef1_listLoc[self.atB][self.atA]][17+self.i]<30:
								self.Lows[self.atB][self.atA][self.i] = self.Ef1[self.Ef1_listLoc[self.atB][self.atA]][17+self.i]
							if -30<self.Ef1[self.Ef1_listLoc[self.atB][self.atA]][34+self.i]<30:
								self.Highs[self.atB][self.atA][self.i] = self.Ef1[self.Ef1_listLoc[self.atB][self.atA]][34+self.i]
						        self.i=self.i+1
				self.l=0; self.i=0; self.atA = self.atA+1
			self.atA = 0; self.atB = self.atB +1
		self.atB=0

	def acum_mean(self, listA, listB, listAcumulator):
		for i in range(17):
			listA[i] = listA[i] + listB[i]
			listAcumulator[i] = listAcumulator[i] + 1
	def get_mean(self, listA, listAcumulator):
		for i in range(17):
			listA[i] = listA[i]/listAcumulator[i]

	def sorthigh(self, listA, listB):
		for i in range(17):
			if listA[i]<listB[i]:
				listA[i] = listB[i]

	def sortlow(self, listA,listB):
		for i in range(17):
			if listA[i]>listB[i]:
				listA[i] = listB[i]	
# Highs receives all the high difference variables, means receives all mean difference and lows receives all low difference, we then #proceed to sort those into the mean high differece, low high difference and high high difference and so on, this creates 9 sets of #variables for us to work with, we should now take the mean values across all .feel files and use them as a baseline to characterize #our 'torque resolution' 
	def treat_variables(self):
		while self.atB<self.b:
			while self.atA<self.a:
				if self.atA>self.atB:
						self.acum_mean(self.MeanDiff, self.Means[self.atB][self.atA], self.MeanDiffDen)
						self.acum_mean(self.HighDiff, self.Highs[self.atB][self.atA], self.HighDiffDen)
						self.acum_mean(self.LowDiff, self.Lows[self.atB][self.atA], self.LowDiffDen)
						self.sorthigh(self.MeanHigh, self.Means[self.atB][self.atA])
						self.sorthigh(self.HighHigh, self.Highs[self.atB][self.atA])
						self.sorthigh(self.LowHigh, self.Lows[self.atB][self.atA])
						self.sortlow(self.MeanLow, self.Means[self.atB][self.atA])
						self.sortlow(self.HighLow, self.Highs[self.atB][self.atA])
						self.sortlow(self.LowLow, self.Lows[self.atB][self.atA])
				self.atA = self.atA+1
			self.atA=0; self.atB = self.atB+1
		self.atB = 0
		self.get_mean(self.MeanDiff, self.MeanDiffDen)
		self.get_mean(self.HighDiff, self.HighDiffDen)
		self.get_mean(self.LowDiff, self.LowDiffDen)
		self.i=0

	def readmatrix(self):
		self.allocation_def()
		while self.atA< self.a:
			while self.atB< self.b:
				if self.atB>self.atA:
					self.read_file(self.atA, self.atB)
				self.atB = self.atB+1
			self.atB = 0; self.atA = self.atA+1
		self.atA=0
		self.load_variables()
		self.treat_variables()

def main():
	NC = noise_canceller(30, 30)
	NC.allocation_def()
	NC.readmatrix()
# [4] not N_num and not self set
#	print NC.allocationmax
	print NC.MeanDiff
	
#
if __name__ == "__main__":
    main()
