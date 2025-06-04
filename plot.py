import matplotlib.pyplot as plt
import datetime

# Inicializar listas para almacenar los datos
local_times = []
ch1_values = []
ch2_values = []
ch3_values = []

# Abrir el archivo y leer los datos
with open('Codigos Finales/20241114T010619_SECOND_SKYGLOW_LABSENS.txt', 'r') as file:
    lines = file.readlines()

    # Encontrar el índice donde termina el encabezado
    data_start_index = 0
    for i, line in enumerate(lines):
        if line.strip() == "# END OF HEADER":
            data_start_index = i + 1  # La línea siguiente al fin del encabezado
            break

    # Procesar las líneas de datos
    for line in lines[data_start_index:]:
        line = line.strip()
        if not line:
            continue  # Saltar líneas vacías

        # Dividir la línea en campos
        fields = line.split(';')
        if len(fields) < 5:
            continue  # Asegurarse de que la línea tenga todos los campos necesarios

        # Extraer y convertir los datos
        utc_datetime_str = fields[0]
        local_datetime_str = fields[1]
        ch1 = int(fields[2])
        ch2 = int(fields[3])
        ch3 = int(fields[4])

        # Convertir la cadena de fecha y hora local a objeto datetime
        local_datetime = datetime.datetime.strptime(local_datetime_str, '%Y-%m-%dT%H:%M:%S.%f')

        # Almacenar los datos en las listas
        local_times.append(local_datetime)
        ch1_values.append(ch1)
        ch2_values.append(ch2)
        ch3_values.append(ch3)

# Crear el gráfico
plt.figure(figsize=(12, 6))
plt.plot(local_times, ch1_values, label='CH1')
plt.plot(local_times, ch2_values, label='CH2')
plt.plot(local_times, ch3_values, label='CH3')

# Formato de la fecha en el eje x
plt.gcf().autofmt_xdate()

# Añadir títulos y etiquetas
plt.title('Tiempo vs CH1, CH2, CH3')
plt.xlabel('Hora Local')
plt.ylabel('Valores de CH')

# Añadir leyenda
plt.legend()

# Mostrar el gráfico
plt.show()