import socket
import subprocess
def ejecutar_script(script):
    # Ejecutar el script usando subprocess
    subprocess.run(script, shell=True)

def recibir_signal(ip, puerto):
    # Crear un socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enlazar el socket a una dirección y puerto local
    direccion = (ip, puerto)
    sock.bind(direccion)

    #print(f"Esperando señales en {ip}:{puerto}")

    while True:
        # Recibir la señal
        data, address = sock.recvfrom(1024)

        # Cuando se recibe la señal, ejecutar el script
        if data.decode() == "Ejecutar":
            #print("Señal recibida. Ejecutando el script.")
            ejecutar_script("python evaluador.py respuesta.py entrada.txt")
            return 0

        else:
            #print("Señal recibida. Eliminar cron.")
            ejecutar_script("./eliminar.sh '" + data.decode() + "'")
            #print(data.decode()

# Uso del script
hostname = "tareas_segura"
puerto_local = 34343
recibir_signal(hostname, puerto_local)
