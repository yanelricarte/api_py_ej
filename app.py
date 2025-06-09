"""
Consultor del Clima - Aplicación Flask
API para consultar información meteorológica usando OpenWeatherMap
"""

import os
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests
from datetime import datetime
from typing import Dict, Any, Optional

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carga las variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la aplicación
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['JSON_AS_ASCII'] = False  # Para caracteres especiales en JSON


class ClimaError(Exception):
    """Excepción personalizada para errores del clima"""
    pass


class ConsultorClima:
    """Clase para consultar información meteorológica"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.timeout = 10
        
    def obtener_clima_actual(self, ciudad: str) -> str:
        """
        Obtiene el clima actual de una ciudad
        
        Args:
            ciudad (str): Nombre de la ciudad
            
        Returns:
            str: Información del clima formateada
            
        Raises:
            ClimaError: Si hay un error en la consulta
        """
        try:
            logger.info(f"Consultando clima para: {ciudad}")
            
            # Validar entrada
            if not self._validar_ciudad(ciudad):
                raise ClimaError("Nombre de ciudad inválido")
            
            # Realizar consulta a la API
            data = self._consultar_api(ciudad)
            
            # Formatear y retornar resultado
            resultado = self._formatear_clima_actual(data)
            logger.info(f"Clima obtenido exitosamente para: {ciudad}")
            return resultado
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout al consultar clima para: {ciudad}")
            raise ClimaError("La consulta tardó demasiado tiempo")
        except requests.exceptions.ConnectionError:
            logger.error(f"Error de conexión al consultar clima para: {ciudad}")
            raise ClimaError("Error de conexión con el servicio meteorológico")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red al consultar clima para {ciudad}: {str(e)}")
            raise ClimaError("Error de red al consultar el clima")
        except Exception as e:
            logger.error(f"Error inesperado al consultar clima para {ciudad}: {str(e)}")
            raise ClimaError("Error inesperado al consultar el clima")
    
    def _validar_ciudad(self, ciudad: str) -> bool:
        """Valida el nombre de la ciudad"""
        return (
            isinstance(ciudad, str) and
            len(ciudad.strip()) >= 2 and
            len(ciudad.strip()) <= 50
        )
    
    def _consultar_api(self, ciudad: str) -> Dict[str, Any]:
        """Realiza la consulta a la API de OpenWeatherMap"""
        url = f"{self.base_url}/weather"
        params = {
            "q": ciudad.strip(),
            "appid": self.api_key,
            "units": "metric",
            "lang": "es"
        }
        
        response = requests.get(url, params=params, timeout=self.timeout)
        data = response.json()
        
        if response.status_code == 200:
            return data
        else:
            error_msg = data.get('message', 'Error desconocido')
            if response.status_code == 404:
                raise ClimaError(f"Ciudad '{ciudad}' no encontrada")
            elif response.status_code == 401:
                raise ClimaError("Error de autenticación con el servicio")
            else:
                raise ClimaError(f"Error del servicio: {error_msg}")
    
    def _formatear_clima_actual(self, data: Dict[str, Any]) -> str:
        """Formatea los datos del clima en un string legible"""
        try:
            ciudad = data['name']
            pais = data['sys']['country']
            temp = data['main']['temp']
            sensacion = data['main']['feels_like']
            humedad = data['main']['humidity']
            presion = data['main']['pressure']
            descripcion = data['weather'][0]['description'].title()
            viento = data['wind']['speed']
            timestamp = data['dt']
            
            # Formatear fecha y hora
            hora_local = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            
            # Crear resultado formateado
            resultado = f"""🌤️  CLIMA ACTUAL EN {ciudad.upper()}, {pais}
{'='*50}
📅 Fecha y hora: {hora_local}
🌡️  Temperatura: {temp}°C (Sensación térmica: {sensacion}°C)
☁️  Condición: {descripcion}
💧 Humedad: {humedad}%
🌪️  Presión: {presion} hPa
💨 Viento: {viento} m/s"""
            
            return resultado.strip()
            
        except KeyError as e:
            logger.error(f"Datos faltantes en la respuesta de la API: {str(e)}")
            raise ClimaError("Datos incompletos del servicio meteorológico")


# Configuración de la aplicación
def crear_app() -> Flask:
    """Factory function para crear la aplicación Flask"""
    
    # Verificar API key
    api_key = os.getenv("API_KEY")
    if not api_key:
        logger.error("API_KEY no está definida en las variables de entorno")
        raise RuntimeError("La variable de entorno API_KEY no está definida")
    
    # Crear instancia del consultor
    consultor = ConsultorClima(api_key)
    
    # Registrar rutas
    @app.route("/")
    def index():
        """Página principal"""
        return render_template("index.html")
    
    @app.route("/clima_actual")
    def clima_actual():
        """Endpoint para consultar el clima actual"""
        try:
            ciudad = request.args.get("ciudad", "").strip()
            
            if not ciudad:
                logger.warning("Solicitud sin parámetro 'ciudad'")
                return jsonify({"error": "Falta el parámetro 'ciudad'"}), 400
            
            resultado = consultor.obtener_clima_actual(ciudad)
            return jsonify({"resultado": resultado})
            
        except ClimaError as e:
            logger.warning(f"Error de clima: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error inesperado en clima_actual: {str(e)}")
            return jsonify({"error": "Error interno del servidor"}), 500
    
    @app.route("/health")
    def health_check():
        """Endpoint de salud para monitoreo"""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "Consultor del Clima"
        })
    
    @app.errorhandler(404)
    def not_found(error):
        """Manejador de error 404"""
        return jsonify({"error": "Endpoint no encontrado"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Manejador de error 500"""
        logger.error(f"Error interno del servidor: {str(error)}")
        return jsonify({"error": "Error interno del servidor"}), 500
    
    return app


# Crear la aplicación
app = crear_app()

if __name__ == "__main__":
    # Configuración para desarrollo
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "127.0.0.1")
    
    logger.info(f"Iniciando servidor en {host}:{port} (debug={debug_mode})")
    app.run(host=host, port=port, debug=debug_mode)