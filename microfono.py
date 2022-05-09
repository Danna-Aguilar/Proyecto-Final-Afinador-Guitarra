from gc import callbacks
import sounddevice as sd
import numpy as np

periodo_muestreo = 1.0 / 44100

print(sd.query_devices())
#1 entrada
#3 salida

# indata:  arreglo de numpy con la info recopilada por la tarjeta de sonido 
#          a través del dispositivo de entrada.
# outdata: arreglo de numpy que se le enviará al dispositivo de salida
#          por default es un silencio (puros 0's).
# frames:  el número de muestra que tiene indata.
# time:    el tiempo que se lleva haciendo el Stream.
# status:  si ha habido algun error.

def callback_stream(indata, outdata, frames, time, status):
    global periodo_muestreo
    data = indata[:,0]
    transformada = np.fft.rfft(data)
    frecuencias = np.fft.rfftfreq(len(data), periodo_muestreo)
    # print(data.shape)
    print("Frecuencia fundamental: ", frecuencias[np.argmax(np.abs(transformada))])
    
    #outdata[:] = indata

try:
    with sd.Stream(
        device = (1,3), #Se eligen los dispositivos (entrada, salida)
        blocksize = 11025, #0 es que la tarjeta de sonido decide el mejor tamaño, es posible que sea variable.
        samplerate = 44100, #Frecuencia de muestreo
        channels = 1, #Canales
        dtype = np.int16, #Tipo de dato (profundidad de bits)
        latency = 'low', #Latencia, que tanto tiempo pasa desde entrada hasta salida
        callback = callback_stream
    ):
        print('Presiona tecla Enter para salir')
        input()
except Exception as e:
    print(str(e))