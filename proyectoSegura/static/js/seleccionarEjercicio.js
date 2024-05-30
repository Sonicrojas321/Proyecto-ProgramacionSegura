$(function(){
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $('#seleccionar_ejercicio').click(function(){
       $.post("/verEjercicio/",
        {id_ejercicio: $('#ejercicio_id').val(),csrfmiddlewaretoken: csrftoken},
        function(data, status){
            if(status == "error"){
                if(data.status != "OK"){
                    alert("No se logró mandar los datos");
                }
            }
        }
       );
    });
});