from __future__ import division
import mk_sense
from pylab import *
import numpy as np
import nonlinear_filter
import fourier_filter


# periodogram = spectral.lombscargle(time, scaled_mags, freqs)

# NOW WITH PROPER IMPLEMENTATIONS, PURPOSE IS TO TAKE A SET OF .feel FILES AND CREATE A MUCH LARGER SET OF .impr FILES FROM THE BETWEEN EACH COMPARISON 2 INDIVIDUAL .feel FILES
# Needs to be looked at, comparison looks wobly at best, maybe just a question of having the list shift back one position

class weight_eval_p(object): 
	def __init__(self):
		self.samples = raw_input('input number of samples to be read\n')
		self.samples = int(self.samples)
		self.EReader = [0]*self.samples
		self.a=0
		self.b=0
		self.imp_t = [0]*(self.samples*self.samples)
		self.nb = raw_input('input .feel set root file names\n')
		self.A = 0.0
		self.flag = 0
		self.F = 0
		self.f = 0
		self.F_filtered = 0
		self.acc=0.1
		self.dt = 0.01
		self.s_time = [0]*self.samples
		self.sum_of_Ef = [[] for i in range(14)];
		self.spawn_EReaders()
		self.get_organized_Ef()
		self.f = 0
	def spawn_EReaders(self):
		while self.a<self.samples:
			self.EReader[self.a] = mk_sense.effort_reader(self.a, self.nb, self.nb)
			self.EReader[self.a].allocation_def()
			self.EReader[self.a].read_file()
			self.EReader[self.a].calc_values_per_joint()
			for i in range(17):
				 self.EReader[self.a].Ef_Filter[i] = filter(lambda x: x!=0, self.EReader[self.a].Ef_Filter[i])
			self.EReader[self.a].Ef_Filter = filter(lambda x: x!=[], self.EReader[self.a].Ef_Filter)
			self.b = 0
			self.a = self.a+1
		self.b=0
		self.a=0

	def generate_impr(self):
		while self.a<30:
			while self.b<self.samples:
				if self.b>self.a:
					self.imp_t[self.samples*self.a+self.b] = mk_sense.impression_taker(self.a,self.b, self.nb)
					self.EReader[self.a].print_lowest_recorded_torque(self.a, self.imp_t[self.samples*self.a+self.b])
					self.EReader[self.a].print_highest_recorded_torque(self.a, self.imp_t[self.samples*self.a+self.b])
					self.EReader[self.a].print_mean_effort_per_joint(self.a, self.imp_t[self.samples*self.a+self.b])
					self.EReader[self.a].get_differences_in_torque(self.EReader[self.b])
					self.EReader[self.a].print_difference_between_mean_torques(self.imp_t[self.samples*self.a+self.b])
					self.EReader[self.a].print_difference_between_lowest_torques(self.imp_t[self.samples*self.a+self.b])
					self.EReader[self.a].print_difference_between_highest_torques(self.imp_t[self.samples*self.a+self.b])
					self.EReader[self.a].clear()
					self.imp_t[self.samples*self.a+self.b].S.close()
				self.b=self.b+1
			self.b = 0
			self.a = self.a+1

# acc = 0.02 yields good results most of the time, must write code to iterate and try different values of acc
# need to throw this to one of the classes, most likely effort_reader in module mk_sense
	def acc_incrementer_routine(self):
		for i in range(self.samples):
			for j in range(14):
				self.acc = 0.0
				while self.flag==0:
					self.EReader[i].Ef_Filter_Clone[j] = self.EReader[i].Ef_Filter[j]
					self.EReader[i].Ef_Filter_Clone[j] = fourier_filter.rep_filter(self.EReader[i].Ef_Filter_Clone[j], self.acc)
					if len(self.EReader[i].Ef_Filter_Clone[j])>0:
							self.flag = 1
					if len(self.EReader[i].Ef_Filter_Clone[j])==0:
							self.acc = self.acc+0.01
				self.flag=0
		for m in range(14):
			for i in range(self.samples):
				print sum(self.EReader[i].Ef_Filter_Clone[m])/float(len(self.EReader[i].Ef_Filter_Clone[m]))

#for i in range(samples):
#	s_time[i] = [k*dt for k in range(len(EReader[i].Ef_Filter[1]))]#
#
#	F = fft(EReader[i].Ef_Filter[1])
#	f = fftfreq(len(F),0.01)
#	F_filtered = array([filter_rule(x,freq) for x,freq in zip(F,f)])
#	F_filtered = ifft(F_filtered)
#	F = ifft(F)
#	print f
#	print F_filtered
#	figure()
#	subplot(1,1,1)
#	plot(s_time[0],F_filtered,'r')
#	plot(s_time[0],F,'b')
#	xlabel('time [s]')
#	show()
	def get_organized_Ef(self):
		for i in range(14):
			for j in range(self.samples):
				nonlinear_filter.break_list_and_append_to(self.EReader[j].Ef_Filter[i],self.sum_of_Ef[i])

	def get_sum_of_torque_values(self):
		self.M = fourier_filter.return_average(self.sum_of_Ef[0:6])
	def get_sum_of_torque_values_no_phase(self):
		self.M = fourier_filter.return_average(self.sum_of_Ef[0:6])
		self.M = fourier_filter.filter_phase(self.M, 0.05, 50)

	def show_torque_fig(self): 
		fourier_filter.show_fig(self.M, 0.05, 0)
		fourier_filter.show_power_spectrum(self.M, 0.05, 0)
	def sum_filter_routine_1(self):
		self.M = fourier_filter.fft_filter_find_fundamentals(self.M, 0.05, 100)
		fourier_filter.show_fig(self.M, 0.05, 0)
		fourier_filter.show_power_spectrum(self.M, 0.05, 0)		
#fourier_filter.moving_average(sum_of_Ef[2], 2, 0.01)
#for i in range(14):
#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 50,0.01)
	def filter_routine_1(self, a):
		for i in range(7):
		#	print fourier_filter.return_common_elements(sum_of_Ef[i], sum(sum_of_Ef[i])/len(sum_of_Ef[i]), 20, 0.5)
		#	print len(sum_of_Ef[i])
		#	sum_of_Ef[i] = fourier_filter.fft_filter_find_fundamentals(sum_of_Ef[i], 0.01, (len(sum_of_Ef[i])//100))
		#	sum_of_Ef[i] = fourier_filter.fft_filter_find_last_fundamentals(sum_of_Ef[i], 0.01, (len(sum_of_Ef[i])//30))
		#	sum_of_Ef[i] = fourier_filter.fft_filter_find_fundamentals(sum_of_Ef[i], 0.01, (len(sum_of_Ef[i])//31))

			self.sum_of_Ef[i] = fourier_filter.moving_average(self.sum_of_Ef[i], 10,0.05, i)
			self.sum_of_Ef[i] = fourier_filter.fft_filter(self.sum_of_Ef[i], 0.05, 1)

		#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 100,0.01, i)
		#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 125,0.01, i)
		#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 150,0.01, i)
		#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 175,0.01, i)
		#	sum_of_Ef[i] = fourier_filter.moving_average(sum_of_Ef[i], 1000,0.01, i)
			fourier_filter.show_fig(self.sum_of_Ef[i], a, i)
			fourier_filter.show_power_spectrum(self.sum_of_Ef[i], a, i)
			self.show_mean_max_min_and_range(i)

	def show_mean_max_min_and_range(self, i):	
		print sum(self.sum_of_Ef[i])/len(self.sum_of_Ef[i])
		print max(self.sum_of_Ef[i])
		print min(self.sum_of_Ef[i])
		print (max(self.sum_of_Ef[i]) - min(self.sum_of_Ef[i]))

def spectral_subtraction(WEP1, WEP2, dt):
	WEP1.get_sum_of_torque_values_no_phase()
	WEP2.get_sum_of_torque_values_no_phase()
	kep1 = np.hanning(len(WEP1.M))
	kep2 = np.hanning(len(WEP2.M))
	WEP1.M = fourier_filter.fft_filter(WEP1.M, 0.05, 50)
	WEP2.M = fourier_filter.fft_filter(WEP2.M, 0.05, 50)
	for i in range(len(WEP1.M)):
		WEP1.M[i] = WEP1.M[i]*kep1[i]
	for i in range(len(WEP2.M)):
		WEP2.M[i] = WEP2.M[i]*kep2[i]
	result = [0]*len(WEP1.M)
	for i in range(len(WEP1.M)):
		result[i] = abs(WEP1.M[i]) - abs(WEP2.M[i])
	k = np.hanning(len(result))
	for i in range(len(result)):
		result[i] = k[i]*result[i]
#	result = array([fourier_filter.filter_rule(x,freq, 50) for x,freq in zip(result,WEP1.f)])
	print sum(result)/len(result)
	return result


	
	
#	print 100*((max(sum_of_Ef[i]) - min(sum_of_Ef[i]))/2)/(sum(sum_of_Ef[i])/len(sum_of_Ef[i]))
#fourier_filter.moving_average(sum_of_Ef[0], 99, 0.01)
#for i in range(14):
#	print sum_of_Ef[i][0]		
#	for i in range(len(EReader[i].Ef_Filter[0])-1):
#		A = A + EReader[i].Ef_Filter[i][0]
#	print A
def main():
	WEP = weight_eval_p()
	WEP2 = weight_eval_p()
	SPS = spectral_subtraction(WEP, WEP2, 0.05)
	SPS = fourier_filter.moving_average(SPS, 50,0.01, 0)
        fourier_filter.show_fig(spectral_subtraction(WEP, WEP2, 0.05), 0.05, 0)
	fourier_filter.show_fig((WEP.M), 0.05, 0)	
	fourier_filter.show_fig((WEP2.M), 0.05, 0)
	fourier_filter.show_fig(SPS, 0.05, 0)		
 	K = [0]*len(WEP.M)
	for i in range(len(WEP.M)):
		K[i] = abs(WEP.M[i]) - abs(WEP2.M[i])
	fourier_filter.show_fig(K, 0.05, 0)
	K = fourier_filter.fft_filter_find_fundamentals(K, 0.05, 4)
	fourier_filter.show_fig(K, 0.05, 0)
	print sum(K)/len(K)
	WEP.filter_routine_1(0.01)
	WEP2.filter_routine_1(0.01)
if __name__ == "__main__":
        main()
 
