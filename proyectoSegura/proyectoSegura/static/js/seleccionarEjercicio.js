$(function(){
    $('#seleccionar_ejercicio').click(function(){
       $.post("/verEjercicio/",
        {id_ejercicio: $('#ejercicio_id').val()},
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