
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
    sd.default.samplerate = 44100 #taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas# #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print('Leitura efeituada')

    #para gravar, utilize
    audio = sf.read('audioModulado.wav')
    sd.wait()
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    dados = audio[0]

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0, len(dados)/44100, len(dados))

    # Fourrier
    signal.plotFFT(dados, sd.default.samplerate)
    plt.title('Fourier do sinal modulado')
    plt.axis([0, 22000, 0, 15000])
    plt.show()

    # Demodulação
    # Criação do sinal senoidal
    carrier=myFn(14000,tempo)
    dadoDemodulado = carrier*dados
    
    #filther frequencies past 2200hz
    b, a = scipy.signal.butter(5, 2200, 'low', fs=sd.default.samplerate)
    audio_filtrado = scipy.signal.filtfilt(b, a, dadoDemodulado)


    signal.plotFFT(dadoDemodulado, sd.default.samplerate)
    plt.title('Fourier do sinal demodulado')
    plt.show()
      
    ## Exiba gráficos do fourier do som gravados 
    signal.plotFFT(audio_filtrado, sd.default.samplerate)
    plt.title('Fourier do audio filtrado')
    plt.show()
    
    sd.play(audio_filtrado, sd.default.samplerate)
    sf.write('audioDemodulado.wav', audio_filtrado, 44100)
    sd.wait()

if __name__ == "__main__":
    main()