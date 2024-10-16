
import inyectar
import sys

CASE_BREAK = '$$$$$$'
INPUT_BREAK = '!!!!!!'

def evaluar(programa, ar_casos, max_time=5):
    """
    Programa ya es el compilado o script
    maxTime es para establecer en segundos el tiempo máximo de ejecución
    Cada caso se separa por la cadena especiasl $$$$$$$
    La entrada se separa de la salida por la cadena especial !!!!!!
    """
    entrada = '' #la cadena total que se enviara
    salida = [] #para tenerla declarada por si el scope
    salida_esperada = '' #para ir guardando lo que se lee en el archivo
    output_eval = False #se activa cuando se evalua el output
    res = []  #para guardar los resultados de cada caso
    for line in open(ar_casos):
        messy_line = line #no quitar saltos de línea ni nada, para comparar con salida esperada (tienen que ser exactametne iguales)
        line = line.strip() #quitar saltos de línea al final así como espacios extra, para evitar posibles errores en el input y facilitar el proceso

        if(line == CASE_BREAK and salida == []): #es la primera línea
            continue

        if(line == ''): #ignorar líneas vacías
            continue

        if line == INPUT_BREAK: #dejar de llenar la entrada he inyectar
            
            salida = inyectar.inyect(programa, entrada, max_time)
            output_eval = True
            entrada = '' #restart input

        elif line == CASE_BREAK: #cambiar banderas y evaluar
            output_eval = False
            if salida[1] != 0: # 0 es sin errores
                res.append(salida[0]) #el tipo de error
            elif salida[0] == salida_esperada or salida[0].strip() == salida_esperada.strip(): #sometimes the new lines must be preserved
                res.append(True)
            else:
                res.append(False)
            salida_esperada = '' #restart output

        elif output_eval:
            salida_esperada += messy_line

        else: #input reconstruction
            if line.strip().startswith('['): #si es una lista prolog no se quieren saltos de linea
                entrada += line + '\n'
            else:
                for elem in line.split(','):
                    entrada += elem + '\n'

    return res


if __name__ == '__main__':
    print(evaluar(sys.argv[1], sys.argv[2]))


