
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time


#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 48000 #taxa de amostragem
    sd.default.channels = 2 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration =  5 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = sd.default.samplerate * duration

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("A captura começará em 3 segundos")
    time.sleep(3)
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print('A captura foi inicializada')

    #para gravar, utilize
    audio = sd.rec(int(numAmostras), sd.default.samplerate, channels=1)
    sd.wait()
    print("...     FIM")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    print(audio.shape)
    dados = audio[:,0]
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0, duration, numAmostras)
  
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas) .
    # para isso, plote apenas um ponto a cada 1000 pontos.
    plt.figure()
    plt.plot(tempo[::1000], dados[::1000])
    plt.show()
     
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(dados, 48000)
    signal.plotFFT(dados, 48000)
    plt.axis([0, 1500, 0, 13000])
    plt.show()
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(yf, thres=0.35, min_dist=50)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    print(f'Picos encontrados :{[xf[i] for i in index]}')
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    freq = [xf[i] for i in index]
    freq1 = list(filter(lambda x: x < 1200, freq))
    freq2 = list(filter(lambda x: x > 1200 and x < 1700, freq))

    val_1 = (1e10,0)
    val_2 = (1e10,0)

    for el in freq1:
        opt1 = abs(el - 697)
        opt2 = abs(el - 770)
        opt3 = abs(el - 852)
        opt4 = abs(el - 941)
        opts = {opt1: 697, opt2: 770, opt3: 852, opt4: 941}
        mini = min([opt1, opt2, opt3, opt4])
        if mini < val_1[0]:
            val_1 = (mini, opts[mini])

    for el in freq2:
        opt1 = abs(el - 1209)
        opt2 = abs(el - 1336)
        opt3 = abs(el - 1477)
        opt4 = abs(el - 1633)
        opts = {opt1: 1209, opt2: 1336, opt3: 1477, opt4: 1633}
        mini = min(opts.keys())
        if mini < val_2[0]:
            val_2 = (mini, opts[mini])

    #print o valor tecla!!!
    print(f'{val_1[1]}Hz ;{val_2[1]}Hz')
    freqs_achadas=(val_1[1], val_2[1])
    
    freqs={ '1':(697,1209),'2':(697,1336),'3':(697,1477),'A':(697,1633),
        '4':(770,1209),'5':(770,1336),'6':(770,1477),'B':(770,1633),
        '7':(852,1209),'8':(852,1336),'9':(852,1477),'C':(852,1633),
        'X':(941,1209),'0':(941,1336),'#':(941,1477),'D':(941,1633)}
    
    for k in freqs.keys():
        if freqs_achadas==freqs[k]:
            print(f'Tecla {k} foi pressionada')
            break
    
    
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
