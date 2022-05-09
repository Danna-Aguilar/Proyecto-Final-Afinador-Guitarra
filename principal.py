import tkinter as tk
import sounddevice as sd
import numpy as np
from threading import Thread, Event

periodo_muestreo = 1.0 / 44100

class StreamThread(Thread):
    def __init__(self):
        super().__init__()
        self.dispositivo_input = 1
        self.dispositivo_output = 3
        self.tamano_bloque = 3500
        self.canales = 1
        self.tipo_dato = np.int16
        self.latencia = "high"
        self.frecuencia_muestreo = 44100
    
    def callback_stream(self, indata, outdata, frames, time, status):
        global app, periodo_muestreo
        data = indata[:,0]
        transformada = np.fft.rfft(data)
        frecuencias = np.fft.rfftfreq(len(data), periodo_muestreo)
        app.etiqueta_valor_ff["text"] = frecuencias[transformada.argmax()] 
        frecuencia_fundamental = frecuencias[transformada.argmax()] 

        if frecuencia_fundamental > 77.0 and frecuencia_fundamental < 87.0:
            app.cuerda_valor["text"] = "Cuerda - E2 - (6)" 
            if (frecuencia_fundamental < 81.6):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_fundamental > 83.0):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: app.ajuste_valor["text"] = "La cuerda esta bien afinada"
        elif frecuencia_fundamental > 105.0 and frecuencia_fundamental < 115.0:
            app.cuerda_valor["text"] = "Cuerda - A2 - (5) " 
            if (frecuencia_fundamental < 109.4):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_fundamental > 110.6):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: app.ajuste_valor["text"] = "La cuerda esta bien afinada"
        elif frecuencia_fundamental > 141.0 and frecuencia_fundamental < 151.0:
            app.cuerda_valor["text"] = "Cuerda - D3 - (4) " 
            if (frecuencia_fundamental < 146.23):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_fundamental > 147.43):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: app.ajuste_valor["text"] = "La cuerda esta bien afinada"
        elif frecuencia_fundamental > 191.0 and frecuencia_fundamental < 201.0:
            app.cuerda_valor["text"] = "Cuerda - G3 - (3)" 
            if (frecuencia_fundamental < 195.4):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_fundamental > 196.6):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: app.ajuste_valor["text"] = "La cuerda esta bien afinada"
        elif frecuencia_fundamental > 242.0 and frecuencia_fundamental < 252.0:
            app.cuerda_valor["text"] = "Cuerda - B3 - (2)" 
            if (frecuencia_fundamental < 246.34):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_fundamental > 247.54):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: app.ajuste_valor["text"] = "La cuerda esta bien afinada"
        elif frecuencia_fundamental > 324.0 and frecuencia_fundamental < 334.0:
            app.cuerda_valor["text"] = "Cuerda - E4 - (1)" 
            if (frecuencia_fundamental < 329.03):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_fundamental > 330.23):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: app.ajuste_valor["text"] = "La cuerda esta bien afinada"
        else:
                app.ajuste_valor["text"] ="No se identificó ninguna cuerda"

        return
    def run(self):
        try:
            self.event = Event()
            with sd.Stream(
                device = (self.dispositivo_input, self.dispositivo_output),
                blocksize = self.tamano_bloque,
                samplerate = self.frecuencia_muestreo,
                channels = self.canales,
                dtype = self.tipo_dato,
                latency = self.latencia,
                callback = self.callback_stream

            ) as self.stream: 
                self.event.wait()

        except Exception as e:
            print(str(e))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Afinador de Guitarra")
        self.geometry("500x200")
        self.config(bg="light blue")

        #Iniciar Boton
        boton_iniciar = tk.Button(self, 
            width = 20, text = "Iniciar",font=("Calibri", 14), bg=("sky blue"),
            command = lambda: self.click_boton_iniciar())

        boton_iniciar.grid(column = 1, row = 8)
        boton_detener = tk.Button(self, 
            width = 20, text = "Detener",font=("Calibri", 10), bg=("sky blue"),
            command = lambda: self.click_boton_detener())
        boton_detener.grid(column = 1, row = 9)

        etiqueta_decoracion = tk.Label(text = "AFINADOR DE GUITARRA ", font=("Agent Orange", 11),bg=("light blue"))
        etiqueta_decoracion.grid(column=1, row=2)

        etiqueta_frecuencias = tk.Label(text = "Frecuencia fundamental: ", font=("Calibri", 10),bg=("light blue"))
        etiqueta_frecuencias.grid(column=0, row=19)

        self.etiqueta_valor_ff = tk.Label(text = "-", font=("Calibri", 10),bg=("light blue"))
        self.etiqueta_valor_ff.grid(column=1, row=19)

        etiqueta_cuerda = tk.Label(text = "Cuerda: ", font=("Calibri", 10),bg=("light blue"))
        etiqueta_cuerda.grid(column = 0, row = 10)

        self.cuerda_valor = tk.Label(text = "-", font=("Calibri", 10),bg=("light blue"))
        self.cuerda_valor.grid(column=1, row=10)

        etiqueta_ajuste = tk.Label(text = " Estado: ", font=("Calibri", 10),bg=("light blue"))
        etiqueta_ajuste.grid(column = 0, row = 12)

        self.ajuste_valor = tk.Label(text = "-", font=("Calibri", 10),bg=("light blue"))
        self.ajuste_valor.grid(column=1, row=12)

        self.stream_thread = StreamThread()
    
    def click_boton_detener(self):
        if self.stream_thread.is_alive():
            self.stream_thread.stream.abort()
            self.stream_thread.event.set()
            self.stream_thread.join()
            
    def click_boton_iniciar(self):
        if not self.stream_thread.is_alive():
            self.stream_thread.daemon = True
            self.stream_thread.start()
           
app = App()

def main():
    global app
    app.mainloop()

if __name__ == "__main__":
    main()