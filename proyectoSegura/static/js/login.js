$(function(){
	$("#submit").click(function(evento){
		let mensajes = "";

		if($("#username").val() == ""){
			mensajes += "<li>El usuario no puede estar vacío</li>";
		}
		if($("#password").val() == ""){
			mensajes += "<li>La contraseña no puede estar vacía</li>";
		}
		
		if(mensajes != ""){
            		evento.preventDefault();
            		$("#errores").html("<ul>" + mensajes + "</ul>");
            		$("#errores").show();
        	}
	})
});