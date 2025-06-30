async function addPatientService(csrfToken, patientData, api) {
    let result = { success: false, message: '', data: null };

    try {
        // Hacer POST request a la API
        const response = await fetch(api, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(patientData), // Enviar directamente patientData
        });

        // si No tubo exito la respuesta
        if (!response.ok) {
  
             const errorData = await response.json().catch(() => ({}));
             result.message = errorData.message || `Error del servidor: ${response.status} - ${response.statusText}`;
             return result;
        }

        data_jsn = await response.json();
        if (data_jsn.success) {
             result.success = true;
             result.data = data_jsn.data;
        } else {
             result.message = 'Error del servidor al agregar paciente: \n' + data_jsn.message;
        }
        
        return result;

    } catch (error) {

        const errorMap = {
            400: 'Datos inválidos. Verifique la información ingresada',
            401: 'No autorizado. Inicie sesión nuevamente',
            403: 'No tiene permisos para realizar esta acción',
            404: 'Recurso no encontrado',
            409: 'El paciente ya existe en el sistema',
            422: 'Error de validación en los datos',
            500: 'Error interno del servidor. Intente nuevamente',
            0: 'Error de conexión. Verifique su conexión a internet'
        };
        
        // Determinar el mensaje de error apropiado
        if (error.status && errorMap[error.status]) {
            result.message = errorMap[error.status];
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
            result.message = errorMap[0]; // Error de conexión
        } else {
            result.message = error.message || 'Error desconocido al guardar paciente';
        }
      
        return result;
    
    }
}

    
