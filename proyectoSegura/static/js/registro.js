$(document).ready(function() {
    const form = $('#registroForm');

    if (form.length) {
        form.on('submit', function(event) {
            const password = $('#contrasenaAlumno').val();
            const confirmPassword = $('#contrasenaAlumno1').val();
            const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$/;

            if (!passwordPattern.test(password)) {
                alert('La contraseña no cumple con los requisitos. Debe tener al menos 10 caracteres, incluyendo mayúsculas, minúsculas, dígitos y al menos un carácter especial.');
                event.preventDefault();
                if (password !== confirmPassword) {
                    alert('Las contraseñas no coinciden.');
                    event.preventDefault();
                    return;
                }
            }
        });
    }
});


