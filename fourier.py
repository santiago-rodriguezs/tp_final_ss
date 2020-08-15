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

def fourierSeries(signal, period, stop_at_error, value , fs = 44100):
    '''
    '''
    time = len(signal)/fs
    vector_t = np.linspace(0, time, round(time*fs))
    fourier_series = 1/2 * a_n(signal, period, 0, fs)
    
    if stop_at_error == True :
        min_error = value
        n = 0
        while msError(signal, fourier_series) > min_error:
            n += 1
            fourier_series += (a_n(signal,period,n,fs) * 
                                   np.cos((vector_t*n*2*np.pi)/period)
                            + b_n(signal,period,n,fs) * 
                                   np.sin((vector_t*n*2*np.pi)/period))
        
    elif stop_at_error == False:
        max_harmonics = value
        for n in range(1, max_harmonics+1):
            fourier_series += (a_n(signal,period,n,fs) * 
                                     np.cos((vector_t*n*2*np.pi)/period)
                                + b_n(signal,period,n,fs) * 
                                     np.sin((vector_t*n*2*np.pi)/period))    
    
    return (fourier_series, n, msError(signal, fourier_series))


def msError(signal, fourier_series):
    '''
    '''
    ms_error = ((fourier_series - signal)**2).mean()
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

def pulseMainFunction (time, freq, value, stop_at_error, fs = 44100):
    # Building signal and Fourier series
    vector_t = np.linspace(0, time, round(time*fs))
    signal = pulseTrain(freq, time, fs)
    fourier_tuple = fourierSeries(signal, 1/freq, stop_at_error, value, fs)
    fourier_series = fourier_tuple[0]
    n_harmonics = fourier_tuple[1]
    ms_error = fourier_tuple[2]
    # Plotting
    plt.plot(vector_t, fourier_series,'y')
    plt.plot(vector_t, signal, ',r')
    plt.title('Fourier series of a Train Pulse')
    plt.savefig("./static/img/series.png")
    
    if stop_at_error == True:
        return n_harmonics
    elif stop_at_error == False:
        return ms_error
         
def sincMainFunction (time, arg, value, stop_at_error, fs = 44100):
    # Building signal and Fourier series
    vector_t = np.linspace(-time/2, time/2, round(time*fs))    
    signal = sincFunction(arg, time, fs)
    fourier_tuple = fourierSeries(signal, time, stop_at_error, value, fs)
    fourier_series = fourier_tuple[0]
    n_harmonics = fourier_tuple[1]
    ms_error = fourier_tuple[2]
    # Plotting
    plt.plot(vector_t, fourier_series,'y')
    plt.plot(vector_t, signal, ',r')
    plt.title('Fourier series of a Sinc function')
    plt.savefig("./static/img/series.png")
    plt.show()
    
    if stop_at_error == True:
        return n_harmonics
    elif stop_at_error == False:
        return ms_error

#-------------------------------TREN DE PULSOS-------------------------------#

# freq = 2
# time = 2
# value = 3
# stop_at_error = False
# pulseMainFunction(time, freq, value, stop_at_error)

#-------------------------------SENAL CONTINUA-------------------------------#

# arg = 3
# time = 10
# value = 0.8
# stop_at_error = True
# sincMainFunction(time, arg, value, stop_at_error)
