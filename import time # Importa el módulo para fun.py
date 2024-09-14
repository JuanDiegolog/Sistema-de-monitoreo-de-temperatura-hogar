import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox
import threading

# Supongo que 'data' y 'df' ya están definidos en el código anterior
data_sala = {'timestamp': [], 'value': []}
data_cocina = {'timestamp': [], 'value': []}
df_sala = pd.DataFrame(data_sala)
df_cocina = pd.DataFrame(data_cocina)

# Función para actualizar el gráfico con nuevos datos
def actualizar_grafico():
    global line_sala, line_cocina
    # Convertir las nuevas fechas a objetos datetime
    data_sala['timestamp'] = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') if isinstance(date, str) else date for date in data_sala['timestamp']]
    data_cocina['timestamp'] = [datetime.strptime(date, '%Y-%m-%d %H:%M:%S') if isinstance(date, str) else date for date in data_cocina['timestamp']]
    # Actualizar los datos de las líneas del gráfico
    line_sala.set_data(data_sala['timestamp'], data_sala['value'])
    line_cocina.set_data(data_cocina['timestamp'], data_cocina['value'])
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
(line_sala,) = plt.plot_date(data_sala['timestamp'], data_sala['value'], linestyle='solid', label='Temperatura sala')
(line_cocina,) = plt.plot_date(data_cocina['timestamp'], data_cocina['value'], linestyle='solid', label='Temperatura cocina')

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

# Inicializar las temperaturas iniciales y pendientes
temperatura_sala = 20
pendiente_sala = 1
temperatura_cocina = 22
pendiente_cocina = 1

# Bucle que se ejecuta hasta que se cumplan las 2 horas
while datetime.now() < tiempo_final:
    # Generar una nueva marca de tiempo en el formato 'YYYY-MM-DD HH:MM:SS'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Generar nuevos valores de temperatura aleatorios en función de las temperaturas iniciales
    temperatura_sala = temperatura_sala + pendiente_sala * random.uniform(0, 3.14)
    temperatura_cocina = temperatura_cocina + pendiente_cocina * random.uniform(0, 3.24)

    # Añadir los nuevos puntos de datos a las variables 'data'
    data_sala['timestamp'].append(timestamp)
    data_sala['value'].append(temperatura_sala)
    data_cocina['timestamp'].append(timestamp)
    data_cocina['value'].append(temperatura_cocina)
    # print(data_sala)
    # print(data_cocina)

    # Actualizar el gráfico con los nuevos datos
    actualizar_grafico()

    # Pausar la ejecución durante 2 segundos antes de generar el próximo punto de datos
    plt.pause(2)

    # Ajustar la pendiente según la temperatura para la sala
    if temperatura_sala > 25:
        print("ALERTA: Se superó la temperatura de 25 grados en la sala.")
        # threading.Thread(target=mostrar_alerta, args=("Se superó la temperatura de 25 grados en la sala.",)).start()
        pendiente_sala = -1
    elif temperatura_sala < 18:
        print("ALERTA: La temperatura es demasiado baja en la sala.")
        # threading.Thread(target=mostrar_alerta, args=("La temperatura es demasiado baja en la sala.",)).start()
        pendiente_sala = 1

    # Ajustar la pendiente según la temperatura para la cocina
    if temperatura_cocina > 25:
        print("ALERTA: Se superó la temperatura de 25 grados en la cocina.")
        # threading.Thread(target=mostrar_alerta, args=("Se superó la temperatura de 25 grados en la cocina.",)).start()
        pendiente_cocina = -1
    elif temperatura_cocina < 18:
        print("ALERTA: La temperatura es demasiado baja en la cocina.")
        # threading.Thread(target=mostrar_alerta, args=("La temperatura es demasiado baja en la cocina.",)).start()
        pendiente_cocina = 1

# Desactivar el modo interactivo
plt.ioff()

# Mostrar el gráfico final
plt.show()

# Guardar los datos en archivos CSV
df_sala.to_csv('datos_sala.csv', index=False)
df_cocina.to_csv('datos_cocina.csv', index=False)

# Imprimir un mensaje indicando que la gráfica y los datos han sido guardados
print('Gráfica generada y datos guardados en "datos_sala.csv" y "datos_cocina.csv"')

# Guardar el gráfico actualizado
plt.savefig('grafico_actualizado.png')