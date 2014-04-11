from __future__ import division
import mk_sense
from pylab import *

def filter_rule(x,freq, band):
    if abs(freq)>0+band or abs(freq)<0-band:
        return 0
    else:
        return x

def fft_filter(ListA, dt):
	s_time = [k*dt for k in range(len(ListA))]
	F = fft(ListA)
	f = fftfreq(len(F),dt)
	F_filtered = array([filter_rule(x,freq, 0) for x,freq in zip(F,f)])
	F_filtered = ifft(F_filtered)
	F = ifft(F)
	figure()
	subplot(1,1,1)
	plot(s_time,F_filtered,'r')
	plot(s_time,F,'b')
	xlabel('time [s]')
	show()

def moving_average(ListA, window):
	s_time[i] = [k*dt for k in range(window)]

def sum_of_samples(C, samples):
	ListB = []
	for i in range(samples):
		for j in range(len(C[i])):
			ListB.append(C[i][j])
	print ListB
	return ListB

A = [0]*2
B = [[1],[2],[3]]
C = [[0, 0], [0,0],[1], [1, 3]]
A = sum_of_samples(B, 3)

		
	
