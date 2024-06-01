document.addEventListener('DOMContentLoaded', function() {

    // Seleccionar todos los botones de "Responder"
    var buttons = document.querySelectorAll('.toggle-response-form');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            var questionId = this.getAttribute('data-question-id');
            var responseForm = document.getElementById('response-form-' + questionId);
            // Mostrar u ocultar el formulario de respuesta
            if (responseForm.style.display === 'none' || responseForm.style.display === '') {
                responseForm.style.display = 'block';
                this.textContent = 'Cancelar'; // Cambiar texto del botón a "Cancelar"
            } else {
                responseForm.style.display = 'none';
                this.textContent = 'Responder'; // Cambiar texto del botón a "Responder"
            }
        });
    });

    // Seleccionar el botón de eliminar publicación
    var deleteButton = document.getElementById('delete-post-button');
    if (deleteButton) {
        deleteButton.addEventListener('click', function(event) {
            var postStatus = deleteButton.getAttribute('data-post-status');
            var allowedStatuses = ['available', 'paused'];

            if (!allowedStatuses.includes(postStatus)) {
                event.preventDefault();
                alert("No se puede eliminar la publicación debido a que la misma se encuentra en un trueque confimado.");
            }
        });
    }
});

// Función para confirmar la eliminación de la respuesta
function confirmDeleteAnswer() {
    return confirm('¿Estás seguro de que deseas eliminar esta respuesta?');
}
// Función para confirmar la eliminación de la pregunta
function confirmDelete() {
    return confirm('¿Estás seguro de que deseas eliminar esta pregunta?');
}