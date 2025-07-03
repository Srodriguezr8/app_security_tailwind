/**
 * Función auxiliar genérica para realizar llamadas a la API.
 * @param {string} url La URL de la API.
 * @param {string} method El método HTTP (ej. 'GET', 'POST').
 * @param {string} csrfToken El token CSRF para la autenticación.
 * @param {object} [body=null] El cuerpo de la solicitud para métodos como POST, PUT.
 * @param {object} [queryParams=null] Parámetros de consulta para la URL (solo para GET).
 * @returns {Promise<object>} Un objeto con { success: boolean, message: string, data: any }.
 */
async function apiService(url, method, csrfToken, body = null, queryParams = null) {
    let result = { success: false, message: '', data: null };
    const fullUrl = new URL(url, window.location.origin); // Construye URL absoluta

    // Añadir parámetros de consulta para GET
    if (queryParams && method === 'GET') {
        Object.keys(queryParams).forEach(key => {
            if (queryParams[key] !== undefined && queryParams[key] !== null) {
                fullUrl.searchParams.append(key, queryParams[key]);
            }
        });
    }

    const fetchOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
    };

    // Añadir cuerpo para métodos que lo requieren
    if (body && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        fetchOptions.body = JSON.stringify(body);
    }

    const errorMap = {
        400: 'Datos inválidos. Verifique la información ingresada.',
        401: 'No autorizado. Inicie sesión nuevamente.',
        403: 'No tiene permisos para realizar esta acción.',
        404: 'Recurso no encontrado.',
        409: 'El recurso ya existe en el sistema o hay un conflicto.', // Generalizado para 409
        422: 'Error de validación en los datos.',
        500: 'Error interno del servidor. Intente nuevamente más tarde.',
        0: 'Error de conexión. Verifique su conexión a internet.' // Para errores de red
    };

    try {
        const response = await fetch(fullUrl.toString(), fetchOptions);

        if (!response.ok) {
    const errorData = await response.json().catch(() => ({})); // Intenta parsear el cuerpo como JSON
            let statusCode = response.status;

            result.message = errorData.message || errorMap[statusCode] || `Error del servidor: ${statusCode} - ${response.statusText}`;
            
            // *** AQUÍ ESTÁ LA MODIFICACIÓN CLAVE ***
            // Si el errorData del backend contiene una propiedad 'data', la copiamos a nuestro 'result.data'
            if (errorData.data !== undefined) {
                result.data = errorData.data;
            }
            // También podemos copiar el estado de 'success' si el backend lo envía en un error
            if (errorData.success !== undefined) {
                result.success = errorData.success ;
            }
            
            return result; 
        }

        const responseData = await response.json(); // Data real del servidor

        // Si la API devuelve un campo 'success' (como en tu Django)
        if (responseData.success !== undefined) {
            result.success = responseData.success;
            result.data = responseData.data;
            result.message = responseData.message || (responseData.success ? 'Operación exitosa.' : 'Fallo en la operación.');
        } else {
            // Si la API no devuelve 'success', asumimos éxito si response.ok
            result.success = true;
            result.data = responseData; // A veces el data ya es el root del JSON
            result.message = 'Operación exitosa.';
        }
        
        return result;

    } catch (error) {
        // Manejo de errores de red o errores antes de recibir respuesta HTTP
        let message = errorMap[0]; // Por defecto, error de conexión
        if (error.name === 'AbortError') {
            message = 'La solicitud fue cancelada.';
        } else if (error.message) {
            // Capturar mensajes de error específicos de JavaScript si son útiles
            message = error.message;
        }
        
        result.message = message;
        return result;
    }
}



async function savePatientService(csrfToken, patientData, api) {
    // Asumimos POST para guardar/crear un nuevo paciente
    // Si necesitas PUT/PATCH para actualizar, puedes añadir un parámetro 'method' aquí
    return await apiService(api, 'POST', csrfToken, patientData);
}


async function getPatientsService(csrfToken, searchParams, api) {
    return await apiService(api, 'GET', csrfToken, null, searchParams);
}

async function saveAllAppointmentsService(csrfToken, appointmentsData, api) {
    return await apiService(api, 'POST', csrfToken, appointmentsData);
}

async function loadRealScheduleService(csrfToken, searchParams, api) {
    return await apiService(api, 'GET', csrfToken, null, searchParams);
}


async function getDoctorsService(csrfToken, searchParams, api) {
    return await apiService(api, 'GET', csrfToken, null, searchParams);
}

