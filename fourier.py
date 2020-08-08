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
    vectorT = np.arange(0, len(signal))/fs
    signal = signal * np.cos((2*n_harmonic*np.pi*vectorT)/period)
    coeff_a = (2/period) * np.trapz(signal, vectorT)
    
    return coeff_a

def b_n(signal, period, n_harmonic, fs = 44100):
    '''
    '''
    
    signal = signal[:round(period*fs)]
    vectorT = np.arange(0, len(signal))/fs
    signal = signal * np.sin((2*n_harmonic*np.pi*vectorT)/period)
    coeff_b = (2/period) * np.trapz(signal, vectorT)
    
    return coeff_b

def fourierSeries(signal, period, n_harmonics, min_error = 0.1, fs = 44100):
    '''
    '''
    time = len(signal)/fs
    vector_t = np.linspace(0, time, round(time*fs))
    fourier_series = 1/2 * a_n(signal, period, 0, fs)
    for n in range(1, n_harmonics+1):
          fourier_series += (a_n(signal,period,n,fs) * 
                                 np.cos((vector_t*n*2*np.pi)/period)
                            + b_n(signal,period,n,fs) * 
                                 np.sin((vector_t*n*2*np.pi)/period))
          if msError(signal, fourier_series) < min_error:
              break  
         
    return fourier_series


def msError(signal, fourier_series):
    '''
    '''
    ms_error = ((signal - fourier_series)**2).mean()
    return ms_error*100

def gibbsCheck(signal, fourier_series):
    '''
    '''
    norm_signal = signal/max(abs(signal))
    norm_fourier = fourier_series/max(abs(signal))
    max_error = abs(max(norm_signal)-max(norm_fourier))
    min_error = abs(min(norm_signal)-min(norm_fourier))
    if abs(min_error-max_error) < 0.001:
        return (max_error+min_error)*100
    elif min_error < max_error:
        return max_error*100
    else:
        return min_error*100
    
    
#-------------------------------TREN DE PULSOS-------------------------------#

# Armado de senal y serie.
freq = 2
time = 1
fs = 44100
n_harmonics = 50
min_error = 0.01
vector_t = np.linspace(0, time, round(time*fs))
signal = pulseTrain(freq, time, fs) -1
fourier_series = fourierSeries(signal, 1/freq, n_harmonics, min_error, fs)

# Graficamos
plt.plot(vector_t, fourier_series,'y')
plt.plot(vector_t, signal, ',r')
plt.title('Fourier series of a Train Pulse')
plt.show()

# Print del Mean Square Error y chequeo de gibbs.
ms_error = msError(signal, fourier_series)
print('El MSE con', n_harmonics, 'armónicos es de: ', round(ms_error, 3), '%')
gibbs_check = gibbsCheck(signal, fourier_series) 
print('El error generado por la discontinuidad es de', round(gibbs_check, 2), '%')

#-------------------------------SENAL CONTINUA-------------------------------#

# Armado de senal y serie.
time = 20
fs = 44100
n_harmonics = 9
min_error = 0.1
vector_t = np.linspace(-time/2, time/2, round(time*fs))
signal = np.sinc(vector_t)
fourier_series = fourierSeries(signal, time, n_harmonics, min_error, fs)

# Graficamos
plt.plot(vector_t, fourier_series,'y')
plt.plot(vector_t, signal, ',r')
plt.title('Fourier series of a Sinc function')
plt.show()

# Print del Mean Square Error y chequeo de gibbs.
ms_error = msError(signal, fourier_series)
print('El MSE con', n_harmonics, 'armónicos es de: ', round(ms_error, 3), '%')
gibbs_check = gibbsCheck(signal, fourier_series) 
print('El error maximo es de', round(gibbs_check, 2), '%')

