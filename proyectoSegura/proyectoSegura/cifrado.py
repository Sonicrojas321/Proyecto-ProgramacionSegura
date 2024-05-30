import crypt
import base64
import os

def generar_salt(tamano = 12) -> str:
    """
    Genera salts aleatorios.

    tamano = 12
    returns: str, salt generado
    """
    aleatorio = os.urandom(tamano)
    return base64.b64encode(aleatorio).decode('utf-8')

def password_valido(pass_a_evaluar: str, shadow: str) -> bool:
    """
    Determina si pass_a_evaluar es un password válido de acuerdo a una cadena shadow de
    entrada:

    - pass_a_evaluar: str, password de interés
    - shadow: str, cadena con el formato completo del archivo shadow, esto es:
      - $algoritmo$
      - $salt$
      - hash
     Ejemplo:
       $6$wLn3hfSJdxalxrpH$PZbtfKfDbOU07UTorvtrao4.Rvlpj1lbKFOV6wiRISPmTWptpse9SdZU/d5jd9QYSxpR41z1cqbp2x9Z.IPa3/

    
    returns: bool, True si el password es válido
    """
    _, algoritmo, salt, resumen = shadow.split('$')
    configuracion = '$%s$%s$' % (algoritmo, salt)
    shadow_nuevo = crypt.crypt(pass_a_evaluar, configuracion)
    return shadow_nuevo == shadow    
