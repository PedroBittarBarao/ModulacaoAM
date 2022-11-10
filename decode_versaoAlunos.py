
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import time
from math import pi, sin
import scipy



#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def build_senoide(freq,time_array):
    A=1
    return A*sin(2*pi*freq*time_array)

def normaliza(s):
    return s/np.max(np.abs(s))

myFn = np.vectorize(build_senoide, excluded=['freq'])


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 48000 #taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  1 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = sd.default.samplerate * duration

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("A captura começará em 3 segundos")
    time.sleep(3)
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print('A captura foi inicializada')

    #para gravar, utilize
    audio = sf.read('audioModulado.wav')
    sd.wait()
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados = audio[0]

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0, duration, numAmostras)

    # Fourrier
    signal.plotFFT(dados, sd.default.samplerate)
    plt.axis([0, 17000, 0, 13000])
    plt.show()

    # Demodulação
    # Criação do sinal senoidal
    carrier=myFn(14e3,tempo)
    dadoModulado = dados*carrier

    # filtro passa baixa
    nyq_rate = sd.default.samplerate/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = scipy.signal.kaiserord(ripple_db, width)
    cutoff_hz = 2200.0
    taps = scipy.signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    yFiltrado = scipy.signal.lfilter(taps, 1.0, dadoModulado)

    sd.play(yFiltrado, sd.default.samplerate)
    sd.wait()

    # Plot
      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
