document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mantenimiento-form');
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Previene el comportamiento por defecto del formulario

        const data = {
            ubicacion: document.getElementById('ubicacion').value,
            equipoId: document.getElementById('equipo-id').value,
            tipo: document.getElementById('tipo').value,
            modelo: document.getElementById('modelo').value,
            estado: document.getElementById('estado').value,
            notas: document.getElementById('notas').value
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/add_mantenimiento', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();
            if (response.ok) {
                document.getElementById('success-message').textContent = 'Mantenimiento registrado exitosamente.';
                form.reset();
            } else {
                throw new Error(result.error || 'Error desconocido'); // Manejo de errores
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('error-message').textContent = 'Error al registrar mantenimiento.';
        }
    });
});
