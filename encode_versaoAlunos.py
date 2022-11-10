
#importe as bibliotecas
from math import pi, sin
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import sys
import scipy

fs=48000


#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)
        
def normaliza(s):
    return s/np.max(np.abs(s))

#converte intensidade em dB, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def build_senoide(freq,time_array):
    A=1
    return A*sin(2*pi*freq*time_array)

myFn = np.vectorize(build_senoide, excluded=['freq'])

""" def build_tone(tecla,t):
    time_array=np.linspace(0,t,(48000*t)+1)
    return myFn(freqs[tecla][0],time_array)+myFn(freqs[tecla][1],time_array)
"""


def main():
    data, fs = sf.read('TacoBell.wav')
    data1=data[:,0]
    data2=data[:,1]
    dataMono=np.array([(data1[i]+data2[i])/2 for i in range(len(data1))])
    time_array=np.linspace(0,len(dataMono)/fs,len(dataMono))
    carrier=myFn(14e3,time_array)

    # Sem filtro
    sd.play(dataMono, fs)
    sd.wait()

    originalNormalizado=normaliza(dataMono)
    
    nyq_rate = fs/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = scipy.signal.kaiserord(ripple_db, width)
    cutoff_hz = 2200.0
    taps = scipy.signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = scipy.signal.lfilter(taps, 1.0, dataMono)

    # Com filtro
    sd.play(yFiltrado, fs)
    sd.wait()

    dataModulado=np.array([(yFiltrado[i]*carrier[i] + carrier[i]) for i in range(len(yFiltrado))])
    yModuladoNormalizado=normaliza(dataModulado)
    

    # Normalizado
    sd.play(yModuladoNormalizado, fs)
    sd.wait()

    sf.write('audioModulado.wav', yModuladoNormalizado, fs)

    # Gráficos

    # Gráfico do sinal original normalizado
    plt.figure(1)
    plt.title("Sinal original normalizado")
    plt.plot(time_array[::500],originalNormalizado[::500])
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()

    # Gráfico do sinal filtrado
    plt.figure(2)
    plt.title("Sinal filtrado")
    plt.plot(time_array[::500],yFiltrado[::500])
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()

    # Gráfico do sinal filtrado fourrier
    signal=signalMeu()
    signal.plotFFT(yFiltrado, fs)
    plt.axis([0, 4000, 0, 4000])
    plt.show()


    # Gráfico do sinal modulado
    plt.figure(4)
    plt.title("Sinal modulado")
    plt.plot(time_array[::500],dataModulado[::500])
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")
    plt.show()

    # Gráfico do sinal modulado fourrier
    signal.plotFFT(dataModulado, fs)
    plt.axis([0, 17000, 0, 13000])
    plt.show()


    # aguarda fim do audio
    sd.wait()
    # Exibe gráficos
    plt.show()
    

if __name__ == "__main__":
    main()
