from flask import Flask, request, jsonify
from escpos.printer import File
from flask_cors import CORS

app = Flask(__name__)
PORT = 8000
CORS(app)  # Habilitar CORS para todas las rutas

def detectar_impresora(devfile):
    try:
        return File(devfile=devfile)
    except Exception as e:
        print(f"Error al conectar con la impresora: {e}")
        return None

def procesar_operaciones(printer, operaciones):
    for operacion in operaciones:
        if operacion['nombre'] == 'ImprimirTexto':
            texto = operacion['argumentos'][0]
            print(f"Imprimiendo texto: {texto}")
            printer.text(texto.encode('utf-8').decode('utf-8'))  # Asegurando el uso de UTF-8
        # Agrega más operaciones según sea necesario
    printer.cut()  # Realiza un corte del papel
    printer.close()  # Cierra la conexión

@app.route('/imprimir', methods=['POST'])
def imprimir():
    datos = request.get_json()
    devfile = datos.get('devfile')
    operaciones = datos.get('operaciones')
    
    if not devfile:
        return jsonify({"error": "El parámetro devfile es necesario"}), 400
    
    p = detectar_impresora(devfile)
    print("impresora", p)
    
    if p:
        try:
            procesar_operaciones(p, operaciones)
        except Exception as e:
            return jsonify({"error": f"Error al imprimir: {e}"})
        return jsonify({"success": "Impresión realizada con éxito"})
    else:
        return jsonify({"error": "No se pudo conectar con la impresora"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
