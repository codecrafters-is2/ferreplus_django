document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.register-barter-button').forEach(function(button) {
        button.addEventListener('click', function() {
            var form = button.closest('.register-barter-form');
            var barterId = form.querySelector('input[name="barter_id"]').value;
            var csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

            if (confirm('¿Desea registrar este trueque?')) {
                fetch(`/register_barter/${barterId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({
                        barter_id: barterId
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('El trueque ha sido registrado.');
                        location.reload();
                    } else {
                        alert('Hubo un problema al registrar el trueque.');
                    }
                });
            }
        });
    });
});
