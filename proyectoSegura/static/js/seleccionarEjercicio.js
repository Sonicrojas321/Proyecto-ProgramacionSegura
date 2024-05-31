$(function(){
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (const cookie of cookies) {
                const trimmedCookie = cookie.trim();
                // Does this cookie string begin with the name we want?
                if (trimmedCookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(trimmedCookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    $('#seleccionar_ejercicio').click(function(){
       $.post("/verEjercicio/",
        {csrfmiddlewaretoken: csrftoken},
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