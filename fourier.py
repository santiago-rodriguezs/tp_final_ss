import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square, sawtooth

def pulseTrain (freq, time, fs = 44100):
    '''
    '''
    period = 1/freq
    ones = np.ones(round((period/2)*fs))
    zeros = np.zeros(round((period/2)*fs))
    pulse_train = np.hstack((ones,zeros))
    
    while len(pulse_train) < time*fs:
        pulse_train = np.hstack((pulse_train,pulse_train))
    
    return pulse_train[:round(time*fs)]

def a_n(signal, period, n_harmonic, fs = 44100):
    '''

    Parameters
    ----------
    signal : TYPE
        DESCRIPTION.
    period : TYPE
        DESCRIPTION.
    n_harmonic : TYPE
        DESCRIPTION.
    fs : TYPE, optional
        DESCRIPTION. The default is 44100.

    Returns
    -------
    coeff_a : TYPE
        DESCRIPTION.

    '''
    signal = signal[:round(period*fs)]
    time = len(signal)/fs
    vectorT = np.linspace(0, time, round(time*fs))
    signal = signal * np.cos((2*n_harmonic*np.pi*vectorT)/period)
    coeff_a = (2/period) * np.trapz(signal, vectorT)
    
    return coeff_a

def b_n(signal, period, n_harmonic, fs = 44100):
    '''
    '''
    
    signal = signal[:round(period*fs)]
    time = len(signal)/fs
    vectorT = np.linspace(0, time, round(time*fs))
    signal = signal * np.sin((2*n_harmonic*np.pi*vectorT)/period)
    coeff_b = (2/period) * np.trapz(signal, vectorT)
    
    return coeff_b

def fourierSeries(signal, period, n_harmonics, fs = 44100):
    '''
    '''
    time = len(signal)/fs
    vectorT = np.linspace(0, time, round(time*fs))
    series = np.zeros(len(signal))
    for n in range(1, n_harmonics+1):
          series += (a_n(signal,period,n,fs)*np.cos((vectorT*n*2*np.pi)/period)
                     +b_n(signal,period,n,fs)*np.sin((vectorT*n*2*np.pi)/period))
    fourier_series = 1/2 * a_n(signal, period, 0, fs) + series
         
    return fourier_series
    
#------------------------------------TEST------------------------------------#

freq = 1/(2*np.pi)
time = 18
fs = 44100
vectorT = np.linspace(0, time, round(time*fs))

signal = sawtooth(vectorT)
fourier_series = fourierSeries(signal, 1/freq, n_harmonics = 15, fs = fs)

plt.plot(vectorT, signal)
plt.plot(vectorT, fourier_series)