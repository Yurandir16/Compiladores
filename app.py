from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)


dato_store = []
# encontrado = []


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/procesar_archivo', methods=['POST'])
def procesar_archivo():
    archivo = request.files['archivo']
    df = pd.read_excel(
        archivo, names=['Clave', 'Nombre Contacto', 'Correo', 'Teléfono Contacto'])
    datos = df.to_dict(orient='records')
    for dato in datos:
        dato_store.append(dato)
    return render_template('buscar.html', datos=datos)


@app.route('/buscador', methods=['POST'])
def buscador():
    print(dato_store)
    encontrado = []
    palabra = request.form['palabra']
    # Crea un patrón de búsqueda que acepte caracteres especiales y busque nombres similares
    patron = '.*' + re.escape(str(palabra).casefold()) + '.*'
    for dato in dato_store:
        if re.match(patron, str(dato['Nombre Contacto']).casefold()):
            encontrado.append(dato)
    return render_template('resultado.html', encontrado=encontrado)


if __name__ == '__main__':
    app.run()
