# 🌤️ Consultor del Clima

Una aplicación web moderna para consultar información meteorológica en tiempo real utilizando la API de OpenWeatherMap.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Características

- **🌍 Consulta global**: Obtén información meteorológica de cualquier ciudad del mundo
- **📱 Diseño responsive**: Interfaz adaptada para dispositivos móviles y escritorio
- **⚡ Tiempo real**: Datos actualizados directamente desde OpenWeatherMap
- **🎨 Interfaz moderna**: Diseño limpio con animaciones y efectos visuales
- **🛡️ Manejo de errores**: Validación robusta y mensajes de error informativos
- **📊 Información completa**: Temperatura, sensación térmica, humedad, presión y viento

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- Cuenta en [OpenWeatherMap](https://openweathermap.org/api) para obtener API Key

### Paso a paso

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/consultor-clima.git
   cd consultor-clima
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En macOS/Linux
   source venv/bin/activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**
   ```bash
   # Copia el archivo de ejemplo
   copy .env.example .env
   
   # Edita .env y agrega tu API Key
   API_KEY=tu_api_key_de_openweathermap
   ```

5. **Ejecuta la aplicación**
   ```bash
   python app.py
   ```

6. **Abre tu navegador**
   
   Visita: `http://127.0.0.1:5000`

## 📁 Estructura del Proyecto

```
consultor-clima/
├── app.py                 # Backend Flask principal
├── requirements.txt       # Dependencias del proyecto
├── .env                  # Variables de entorno (no incluir en git)
├── README.md             # Este archivo
├── templates/
│   └── index.html        # Template HTML principal
└── static/
    ├── styles.css        # Estilos CSS
    └── script.js         # Lógica JavaScript del frontend
```

## 🔧 Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
# REQUERIDA: API Key de OpenWeatherMap
API_KEY=tu_api_key_aqui

# OPCIONAL: Configuración de Flask
FLASK_DEBUG=True
SECRET_KEY=clave_secreta_para_sessions

# OPCIONAL: Configuración del servidor
HOST=127.0.0.1
PORT=5000
```

### Obtener API Key de OpenWeatherMap

1. Visita [OpenWeatherMap](https://openweathermap.org/api)
2. Crea una cuenta gratuita
3. Ve a "My API Keys" en tu dashboard
4. Copia tu API Key y agrégala al archivo `.env`

## 🛠️ Uso

### Interfaz Web

1. **Ingresa el nombre de una ciudad** en el campo de texto
2. **Haz clic en "Consultar clima"** o presiona Enter
3. **Visualiza la información** meteorológica completa

### API Endpoints

#### `GET /`
Página principal de la aplicación.

#### `GET /clima_actual?ciudad={nombre_ciudad}`
Obtiene información meteorológica de una ciudad específica.

**Parámetros:**
- `ciudad` (string, requerido): Nombre de la ciudad

**Respuesta exitosa:**
```json
{
  "resultado": "🌤️ CLIMA ACTUAL EN BUENOS AIRES, AR\n===================================\n📅 Fecha y hora: 2025-06-09 20:30:15\n🌡️ Temperatura: 18°C (Sensación térmica: 16°C)\n☁️ Condición: Parcialmente nublado\n💧 Humedad: 65%\n🌪️ Presión: 1013 hPa\n💨 Viento: 3.5 m/s"
}
```

**Respuesta de error:**
```json
{
  "error": "Ciudad 'XYZ' no encontrada"
}
```

#### `GET /health`
Endpoint de monitoreo para verificar el estado del servicio.

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-09T20:30:15.123456",
  "service": "Consultor del Clima"
}
```

## 🧪 Testing

### Ciudades de prueba sugeridas

- **Buenos Aires** - Argentina
- **Madrid** - España
- **Nueva York** - Estados Unidos
- **Tokio** - Japón
- **Londres** - Reino Unido
- **São Paulo** - Brasil

### Manejo de errores

La aplicación maneja los siguientes tipos de errores:

- ❌ **Ciudad no encontrada**: Verifica la ortografía
- ❌ **Error de conexión**: Problemas de red o API
- ❌ **Timeout**: La consulta tardó demasiado
- ❌ **API Key inválida**: Revisa tu configuración

## 🚀 Despliegue en Producción

### Usando Gunicorn

1. **Instala Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Ejecuta con Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Variables de entorno para producción

```bash
FLASK_DEBUG=False
SECRET_KEY=clave_secreta_muy_segura
HOST=0.0.0.0
PORT=5000
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Changelog

### v1.0.0 (2025-06-09)
- ✨ Primera versión estable
- 🎨 Interfaz web moderna y responsive
- 🌍 Soporte para consultas globales
- 🛡️ Manejo robusto de errores
- 📊 Información meteorológica completa
- 🔧 API REST bien documentada

## 🐛 Problemas Conocidos

- Las consultas pueden fallar si la API de OpenWeatherMap está saturada
- Algunas ciudades muy pequeñas pueden no estar en la base de datos
- La precisión de la ubicación depende de la base de datos de OpenWeatherMap

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias:

1. **Revisa los logs** del servidor para más información
2. **Verifica tu API Key** en el archivo `.env`
3. **Abre un issue** en el repositorio con detalles del problema

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [OpenWeatherMap](https://openweathermap.org/) por proporcionar la API meteorológica
- [Flask](https://flask.palletsprojects.com/) por el framework web
- [MDN Web Docs](https://developer.mozilla.org/) por la documentación de referencia

---

**Desarrollado con ❤️ para la comunidad**

¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!