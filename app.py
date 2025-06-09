# app.py
from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

class ConsultorClima:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def obtener_clima_actual(self, ciudad):
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": ciudad,
                "appid": self.api_key,
                "units": "metric",
                "lang": "es"
            }
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            if resp.status_code == 200:
                return self._formatear_clima_actual(data)
            else:
                return f"Error: {data.get('message', 'No se pudo obtener el clima')}"
        except requests.exceptions.RequestException as e:
            return f"Error de conexión: {str(e)}"
        except Exception as e:
            return f"Error inesperado: {str(e)}"
    
    def _formatear_clima_actual(self, data):
        ciudad = data['name']
        pais = data['sys']['country']
        temp = data['main']['temp']
        sensacion = data['main']['feels_like']
        humedad = data['main']['humidity']
        presion = data['main']['pressure']
        descripcion = data['weather'][0]['description'].title()
        viento = data['wind']['speed']
        timestamp = data['dt']
        hora_local = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        resultado = f"""
🌤️  CLIMA ACTUAL EN {ciudad.upper()}, {pais}
{'='*50}
📅 Fecha y hora: {hora_local}
🌡️  Temperatura: {temp}°C (Sensación térmica: {sensacion}°C)
☁️  Condición: {descripcion}
💧 Humedad: {humedad}%
🌪️  Presión: {presion} hPa
💨 Viento: {viento} m/s
        """
        return resultado.strip()

API_KEY = "66e8e227923985e194406900bd96e97d"  # Reemplazá con tu clave real
consultor = ConsultorClima(API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/clima_actual")
def clima_actual():
    ciudad = request.args.get("ciudad", "").strip()
    if not ciudad:
        return jsonify({"error": "Falta el parámetro 'ciudad'"}), 400
    resultado = consultor.obtener_clima_actual(ciudad)
    return jsonify({"resultado": resultado})

if __name__ == "__main__":
    app.run(debug=True)
