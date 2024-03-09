import os

from flask import Flask, render_template, request

app = Flask(__name__)

color_names = {
    'BK': 'Negro',
    'BU': 'Azul',
    'BN': 'Marrón',
    'PU': 'Púrpura',
    'R': 'Rojo',
    'GY': 'Gris',
    'O': 'Naranja',
    'W': 'Blanco',
    'Y': 'Amarillo',
    'PK': 'Rosa',
    'GN': 'Verde',
    'T': 'Beige',
    'LGN': 'Verde Claro',
    'DGN': 'Gris Oscuro',
    'DO': 'Naranja Oscuro',
    'LBU': 'Celeste',
    'LBN': 'Cafe Claro',
'RB': 'Rojo'
}

# Ruta del archivo de datos
data_file = 'pinout_data.txt'

# Comprobar si el archivo de datos existe
if not os.path.exists(data_file):
    # Si no existe, crear un archivo en blanco
    with open(data_file, 'w', encoding='utf-8') as file:
        pass


# Función para leer los datos del archivo
def read_data():
    pin_data = []
    with open(data_file, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) == 7:  # Ahora esperamos 7 partes en lugar de 6
                pin, nombre, descripcion, instrumento, forma, valores, color = parts
                # Agregamos el atributo 'color' a los datos del pin
                pin_data.append({'pin': pin, 'nombre': nombre, 'descripcion': descripcion,
                                 'instrumento': instrumento, 'forma': forma, 'valores': valores,
                                 'color': color})
            elif "NOT USED" in line:
                # Si la línea contiene "NOT USED", conservar el valor del pin y del nombre y dejar los otros campos vacíos
                pin, nombre, *_ = parts  # Conservar solo el pin y el nombre
                # Agregamos el atributo 'color' con un valor predeterminado
                pin_data.append({'pin': pin, 'nombre': nombre, 'descripcion': '', 'instrumento': '',
                                 'forma': '', 'valores': '', 'color': ''})  # Por ejemplo, 'BK/OR' para negro/naranja
            else:
                print(f"Error: La línea '{line.strip()}' no tiene el formato correcto y será ignorada.")
    return pin_data


@app.route('/', methods=['GET', 'POST'])
def pinout():
    if request.method == 'POST':
        # Si se envía el formulario, obtener el número de pin a filtrar
        pin_to_filter = request.form['pin_to_filter']
    else:
        # Si es una solicitud GET, inicializar el número de pin a filtrar como vacío
        pin_to_filter = ''

    # Leer los datos del archivo
    pin_data = read_data()

    # Filtrar los datos si se proporciona un número de pin
    if pin_to_filter:
        pin_data = [item for item in pin_data if item['pin'] == pin_to_filter]

    return render_template('pinout.html', pin_data=pin_data, pin_to_filter=pin_to_filter, color_names=color_names)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
