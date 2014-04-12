from __future__ import division
import mk_sense
from pylab import *
import numpy

def filter_rule(x,freq, band):
    if abs(freq)>0+band or abs(freq)<0-band:
        return 0
    else:
        return x
def filter_rule_band_reject(x, freq, band):
	if band>abs(freq)>-band:
		return 0
	else:
		return x

def fft_filter(ListA, dt, band):
	F = fft(ListA)
	f = fftfreq(len(F),dt)
	F_filtered = array([filter_rule(x,freq, band) for x,freq in zip(F,f)])
	F_filtered = ifft(F_filtered)
	return F_filtered		

def show_fig(F_filtered, dt, l):
	s_time = [k*dt for k in range(len(F_filtered))]
	figure()
	subplot(1,1,1)
	plot(s_time,F_filtered,'r')
	number = {'i': l}
	xlabel('{i}, time [s]'.format(**number))
	show()
def get_high_signal(F_filtered, b):
	hs = 0.0
	for i in range(b):
		if F_filtered[i]>hs:
			hs = F_filtered[i]
	return hs 
def get_low_signal(F_filtered, b):
	ls = 0.0
	for i in range(b):
		if F_filtered[i]<ls:
			ls = F_filtered[i]
	return ls 

def moving_average(ListA, window, dt, l):
#	np = hanning(len(ListA)-window)
	internal_window = 0
	average = [0.0 for i in range(len(ListA))]
	average_rec = [0.0 for i in range(len(ListA)-window)]
	s_time = [k*dt for k in range(len(ListA)-window)]
	for i in range(len(ListA)-window):
		for k in range(window):
			try:
				internal_window = internal_window+ListA[i+k]
			except IndexError:
				internal_window = internal_window
		average[i] = internal_window/window
		internal_window = 0 
	for i in range(window):
		average.pop()
	return average

		

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


A = [0]*2
B = [[1],[2],[3]]
C = [[0, 0], [0,0],[1], [1, 3]]
break_list_and_append_to(C, A)
break_list_and_append_to(B, A)
print A

		
	
