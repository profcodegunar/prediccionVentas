from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

# Inicializar la app Flask
app = Flask(__name__)

# Cargar el modelo entrenado
model = joblib.load('modelo_ventas_con_ciudades.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Obtener los datos del request
    data = request.get_json(force=True)
    
    # Convertir los datos en una lista
    year = data['años']
    city = data['ciudades']  # 'New York', 'Chicago', 'Boston', 'Miami', 'Los Angeles'
    
    # Preparar los datos de entrada para el modelo
    city_data = [0, 0, 0, 0]  # Chicago, Boston, Miami, Los Angeles (omitiendo New York)
    if city == 'Rio Negro':
        city_data[0] = 1
    elif city == 'Pichanaki':
        city_data[1] = 1
    elif city == 'Santa Ana':
        city_data[2] = 1
    elif city == 'La Merced':
        city_data[3] = 1
    
    # Crear el array para predecir
    prediction_data = [year] + city_data
    prediction_data = np.array([prediction_data])  # Convertir a formato numpy
    
    # Hacer la predicción
    predicted_sales = model.predict(prediction_data)
    
    # Retornar la respuesta en JSON
    return jsonify({'predicted_sales': predicted_sales[0]})

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
