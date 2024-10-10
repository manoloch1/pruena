document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('equipo-form'); // Verifica que este ID sea correcto
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Previene el comportamiento por defecto del formulario

        const data = {
            ubicacion: document.getElementById('ubicacion').value,
            equipoId: document.getElementById('equipo-id').value,
            tipo: document.getElementById('tipo').value,
            modelo: document.getElementById('modelo').value,
            estado: document.getElementById('estado').value,
            notas: document.getElementById('notas').value,
            tipo_conexion: document.getElementById('tipo-conexion').value,
            ip: document.getElementById('tipo-conexion').value === 'IP' ? document.getElementById('ip').value : '',
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/add_equipo', {
                // Asegúrate de que la URL sea correcta
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            console.log(result); // Para verificar la respuesta del servidor
            if (response.ok) {
                document.getElementById('success-message').textContent = 'Equipo agregado exitosamente.';
                form.reset(); // Limpia el formulario
            } else {
                throw new Error(result.error || 'Error desconocido'); // Manejo de errores
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('error-message').textContent = 'Error al agregar equipo.';
        }
    });

    // Lógica para mostrar u ocultar el campo de IP
    document.getElementById('tipo-conexion').addEventListener('change', function() {
        const ipField = document.getElementById('ip');
        if (this.value === 'IP') {
            ipField.style.display = 'block'; // Muestra el campo IP
        } else {
            ipField.style.display = 'none'; // Oculta el campo IP
            ipField.value = ''; // Limpia el campo IP
        }
    });

    // Inicializa el campo de IP como oculto al cargar la página
    document.getElementById('ip').style.display = 'none';
});
