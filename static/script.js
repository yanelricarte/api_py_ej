/**
 * Consultor del Clima - Cliente JavaScript
 * Maneja la interfaz de usuario y comunicación con el backend
 */

class ClimaApp {
    constructor() {
        this.form = document.getElementById("form-clima");
        this.resultado = document.getElementById("resultado");
        this.loading = document.getElementById("loading");
        this.submitButton = this.form.querySelector('button[type="submit"]');
        this.ciudadInput = document.getElementById("ciudad");
        
        this.init();
    }
    
    init() {
        this.form.addEventListener("submit", (e) => this.handleSubmit(e));
        this.ciudadInput.addEventListener("keypress", (e) => this.handleKeyPress(e));
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const ciudad = this.ciudadInput.value.trim();
        if (!ciudad) {
            this.showError("Por favor, ingresa el nombre de una ciudad");
            return;
        }
        
        await this.consultarClima(ciudad);
    }
    
    handleKeyPress(e) {
        if (e.key === 'Enter') {
            this.form.dispatchEvent(new Event('submit'));
        }
    }
    
    async consultarClima(ciudad) {
        try {
            this.showLoading();
            console.log("Consultando clima para:", ciudad);
            
            const response = await this.fetchClima(ciudad);
            const data = await response.json();
            
            console.log("Respuesta del servidor:", data);
            
            if (!response.ok) {
                this.showError(data.error || `Error del servidor: ${response.statusText}`);
                return;
            }
            
            if (data.error) {
                this.showError(data.error);
                return;
            }
            
            this.showSuccess(data.resultado);
            
        } catch (error) {
            console.error("Error en la consulta:", error);
            this.showError(`Error de conexión: ${error.message}`);
        }
    }
    
    async fetchClima(ciudad) {
        const url = `/clima_actual?ciudad=${encodeURIComponent(ciudad)}`;
        
        return await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            // Timeout personalizado
            signal: AbortSignal.timeout(15000) // 15 segundos
        });
    }
    
    showLoading() {
        this.setLoadingState(true);
        this.hideResult();
        this.loading.classList.remove("hidden");
    }
    
    showSuccess(mensaje) {
        this.setLoadingState(false);
        this.loading.classList.add("hidden");
        this.resultado.textContent = mensaje;
        this.resultado.className = "resultado success";
        this.resultado.scrollTop = 0; // Scroll al inicio
    }
    
    showError(mensaje) {
        this.setLoadingState(false);
        this.loading.classList.add("hidden");
        this.resultado.textContent = `❌ ${mensaje}`;
        this.resultado.className = "resultado error";
    }
    
    hideResult() {
        this.resultado.textContent = "";
        this.resultado.className = "resultado";
    }
    
    setLoadingState(isLoading) {
        this.submitButton.disabled = isLoading;
        this.ciudadInput.disabled = isLoading;
        
        if (isLoading) {
            this.submitButton.textContent = "Consultando...";
        } else {
            this.submitButton.textContent = "Consultar clima";
        }
    }
}

// Utilidades adicionales
class Utils {
    static capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    }
    
    static validateCityName(ciudad) {
        // Validación básica del nombre de ciudad
        const regex = /^[a-zA-ZÀ-ÿ\u00f1\u00d1\s\-\.\']+$/;
        return regex.test(ciudad) && ciudad.length >= 2 && ciudad.length <= 50;
    }
    
    static formatError(error) {
        // Formatea errores comunes para mostrar al usuario
        const errorMessages = {
            'city not found': 'Ciudad no encontrada. Verifica el nombre e intenta nuevamente.',
            'invalid api key': 'Error de configuración del servicio.',
            'timeout': 'La consulta tardó demasiado. Intenta nuevamente.',
            'network error': 'Error de conexión. Verifica tu conexión a internet.'
        };
        
        const lowerError = error.toLowerCase();
        for (const [key, message] of Object.entries(errorMessages)) {
            if (lowerError.includes(key)) {
                return message;
            }
        }
        
        return error;
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('Consultor del Clima iniciado');
    new ClimaApp();
});

// Manejo global de errores
window.addEventListener('error', (e) => {
    console.error('Error global capturado:', e.error);
});

// Manejo de errores de promesas no capturadas
window.addEventListener('unhandledrejection', (e) => {
    console.error('Promesa rechazada no manejada:', e.reason);
    e.preventDefault();
});