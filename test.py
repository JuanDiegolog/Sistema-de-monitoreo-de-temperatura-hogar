import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox
import threading

# Supongo que 'data' y 'df' ya están definidos en el código anterior
data = {'timestamp': [], 'value': []}
df = pd.DataFrame(data)

# Función para actualizar el gráfico con nuevos datos
def actualizar_grafico():
    global line
    # Convertir las nuevas fechas a objetos datetime
    data['timestamp'] = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') if isinstance(date, str) else date for date in data['timestamp']]
    # Actualizar los datos de la línea del gráfico
    line.set_data(data['timestamp'], data['value'])
    # Ajustar los límites del gráfico
    plt.gca().relim()
    plt.gca().autoscale_view()
    # Redibujar el gráfico
    plt.draw()

# Función para mostrar una alerta y cerrarla automáticamente
def mostrar_alerta(mensaje, duracion=2000):
    def cerrar_alerta():
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    messagebox.showwarning("Alerta", mensaje)
    root.after(duracion, cerrar_alerta)
    root.mainloop()

# Crear el gráfico inicial
tiempo_final = datetime.now() + timedelta(minutes=2)
plt.figure(figsize=(10, 5))
(line,) = plt.plot_date(data['timestamp'], data['value'], linestyle='solid', label='Temperatura sala')

# Formatear el eje de las fechas y horas
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

# Rotar las etiquetas de las fechas para que no se superpongan
plt.gcf().autofmt_xdate()

# Añadir título y etiquetas
plt.title('Gráfico de valores con fechas y horas')
plt.xlabel('Fecha y Hora')
plt.ylabel('Valor')

# Añadir la leyenda
plt.legend()

# Inicializar la temperatura inicial
temperatura_inicial = 20

# Bucle que se ejecuta hasta que se cumplan las 2 horas
pendiente = 1
while datetime.now() < tiempo_final:
    # Generar una nueva marca de tiempo en el formato 'YYYY-MM-DD HH:MM:SS'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generar un nuevo valor de temperatura aleatorio en función de la temperatura inicial
    temperatura_inicial = temperatura_inicial + pendiente * random.uniform(0, 3.14)

    # Añadir el nuevo punto de datos a la variable 'data'
    data['timestamp'].append(timestamp)
    data['value'].append(temperatura_inicial)
    # print(data)

    # Actualizar el gráfico con los nuevos datos
    actualizar_grafico()

    # Pausar la ejecución durante 2 segundos antes de generar el próximo punto de datos
    plt.pause(2)

    # Ajustar la pendiente según la temperatura
    if temperatura_inicial > 25:
        print("ALERTA: Se superó la temperatura de 25 grados.")
        threading.Thread(target=mostrar_alerta, args=("Se superó la temperatura de 25 grados.",)).start()
        pendiente = -1
    elif temperatura_inicial < 18:
        print("ALERTA: La temperatura es demasiado baja.")
        threading.Thread(target=mostrar_alerta, args=("La temperatura es demasiado baja.",)).start()
        pendiente = 1

# Desactivar el modo interactivo
plt.ioff()

# Mostrar el gráfico final
plt.show()

# Guardar los datos en un archivo CSV
df.to_csv('datos.csv', index=False)

# Imprimir un mensaje indicando que la gráfica y los datos han sido guardados
print('Gráfica generada y datos guardados en "datos.csv"')

# Guardar el gráfico actualizado
plt.savefig('grafico_actualizado.png')