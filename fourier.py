import numpy as np
import matplotlib.pyplot as plt

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

def sincFunction (arg, time, fs = 44100):
    '''
    '''
    vector_t = np.linspace(-time/2, time/2, round(time*fs))
    sinc = np.sin(arg*vector_t)/(arg*vector_t)
    return sinc

def a_n(signal, period, n_harmonic, fs = 44100):
    '''
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

def fourierSeries(signal, period, stop_at_error = True , max_harmonics = 10, min_error = 0.1, fs = 44100):
    '''
    '''
    time = len(signal)/fs
    vector_t = np.linspace(0, time, round(time*fs))
    fourier_series = 1/2 * a_n(signal, period, 0, fs)
    
    if stop_at_error == True :
        n = 0
        while msError(signal, fourier_series) > min_error:
            n += 1
            fourier_series += (a_n(signal,period,n,fs) * 
                                   np.cos((vector_t*n*2*np.pi)/period)
                            + b_n(signal,period,n,fs) * 
                                   np.sin((vector_t*n*2*np.pi)/period))
        
    elif stop_at_error == False:
        
        for n in range(1, max_harmonics+1):
              fourier_series += (a_n(signal,period,n,fs) * 
                                     np.cos((vector_t*n*2*np.pi)/period)
                                + b_n(signal,period,n,fs) * 
                                     np.sin((vector_t*n*2*np.pi)/period))    
    
    return (fourier_series, n)


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
    
def dirichletCheck (signal, fs):
    pass

#-------------------------------TREN DE PULSOS-------------------------------#

# # Armado de senal y serie.
# freq = 2
# time = 1
# fs = 44100
# max_harmonics = 500
# min_error = 0.8
# stop_at_error = False
# vector_t = np.linspace(0, time, round(time*fs))
# signal = pulseTrain(freq, time, fs)
# fourier_tuple = fourierSeries(signal, 1/freq, stop_at_error, max_harmonics, min_error, fs)
# n_harmonics = fourier_tuple[1]
# fourier_series = fourier_tuple[0]

# # Graficamos
# plt.plot(vector_t, fourier_series,'y')
# plt.plot(vector_t, signal, ',r')
# plt.title('Fourier series of a Train Pulse')
# plt.show()

# # Print del chequeo de Dirichlet, Mean Square Error y chequeo de gibbs.
# ms_error = msError(signal, fourier_series)
# print('El MSE con', n_harmonics, 'armónicos es de: ', round(ms_error, 2), '%')
# gibbs_check = gibbsCheck(signal, fourier_series) 
# print('El error generado por la discontinuidad es de', round(gibbs_check), '%')
# error_continous = msError(signal[:round(fs/(freq*2))], fourier_series[:round(fs/(freq*2))]) 
# print('El error generado por la CONTINUIDAD es de', round(error_continous, 2), '%')

#-------------------------------SENAL CONTINUA-------------------------------#

# # Armado de senal y serie.
arg = 3
time = 10
fs = 44100
max_harmonics = 20
min_error = 1
stop_at_error = True
vector_t = np.linspace(-time/2, time/2, round(time*fs))
signal = sincFunction(arg, time, fs)
fourier_tuple = fourierSeries(signal, time, stop_at_error, max_harmonics, min_error, fs)
n_harmonics = fourier_tuple[1]
fourier_series = fourier_tuple[0]

# Graficamos
plt.plot(vector_t, fourier_series,'b')
plt.plot(vector_t, signal, ',r')
plt.title('Fourier series of a Sinc function')
plt.show()

# Print del chequeo de Dirichlet, Mean Square Error y chequeo de gibbs.
ms_error = msError(signal, fourier_series)
print('El MSE con', n_harmonics, 'armónicos es de: ', round(ms_error, 3), '%')
gibbs_check = gibbsCheck(signal, fourier_series) 
print('El error maximo es de', round(gibbs_check, 2), '%')

