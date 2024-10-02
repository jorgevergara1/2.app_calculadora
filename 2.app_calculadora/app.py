# importamos las clases y metodos
from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from datetime import datetime

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['Get',"POST"])
def aritmetica():
    if request.method == "POST":
        #Valores que recibo del form n1,n2 son pasados
        num1 =float(request.form.get('n1'))
        num2 =float(request.form.get('n2'))
        #Realizamos operaciones aritmeticas
        suma = num1 + num2
        resta = num1 -num2
        multiplicacion = num1 * num2
        division = num1 / num2
        return render_template('index.html', total_suma=suma,
                                             total_resta=resta,
                                             total_multiplicacion=multiplicacion,  
                                             total_division=division )
        
    return render_template('index.html')


@app.route('/divisas',methods=['GET', 'POST'])
def divisas():
    resultado = None
    cantidad = None
    divisa_destino = None
    error_message = None

    tipos_de_cambio = {
        'Dólar': 4184.21,  # Ejemplo: 1 USD = 4184.21COP
        'Euro': 4651.35,   # Ejemplo: 1 EUR = 4,651.35 COP
        'Peso': 1.0       # 1 COP = 1 COP
    }

    if request.method == "POST":
        cantidad_input = request.form.get('cantidad')
        divisa_destino_input = request.form.get('divisa_destino')

        if cantidad_input and divisa_destino_input:
            try:
                cantidad = float(cantidad_input)
                if cantidad < 0:
                    error_message = "La cantidad debe ser un número positivo."
                else:
                    resultado = convertir_divisas(cantidad, divisa_destino_input, tipos_de_cambio)
            except ValueError:
                error_message = "Por favor, ingresa un valor numérico válido para la cantidad."
            except KeyError:
                error_message = "Por favor, selecciona una divisa correcta."

    return render_template('divisas.html', resultado=resultado, cantidad=cantidad, tipos_de_cambio=tipos_de_cambio, error_message=error_message)

def convertir_divisas(cantidad, divisa_destino, tipos_de_cambio):
    tasa_destino = tipos_de_cambio[divisa_destino]
    return cantidad / tasa_destino  

@app.route('/fechas', methods=['GET', "POST"])
def calcular_edad():
    if request.method == "POST":
        fecha_nacimiento = request.form.get('fecha_nacimiento')

        # Validar que se haya ingresado una fecha
        if not fecha_nacimiento:
            flash('Por favor, ingrese su fecha de nacimiento.')
            return render_template('fechas.html')  # Cambiado a render_template

        try:
            # Convertir la fecha de nacimiento a un objeto datetime
            fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            hoy = datetime.now()

            # Calcular la edad
            edad = hoy.year - fecha_nacimiento_dt.year - ((hoy.month, hoy.day) < (fecha_nacimiento_dt.month, fecha_nacimiento_dt.day))

            return render_template('fechas.html', edad=edad)  # Retornar la plantilla con la edad
        except ValueError:
            flash('Formato de fecha inválido. Usa YYYY-MM-DD.')
            return render_template('fechas.html')  # Cambiado a render_template

    # Retornar la plantilla por defecto si es un GET
    return render_template('fechas.html')


    
if __name__=="__main__":
    app.run(debug=True)