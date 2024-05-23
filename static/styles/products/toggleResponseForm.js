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
});
