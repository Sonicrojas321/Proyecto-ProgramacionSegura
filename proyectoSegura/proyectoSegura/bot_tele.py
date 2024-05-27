import math, random
import os
import requests
from db import models

#TOKEN = os.environ.get('TELE_TOKEN')
#CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'

def obtener_bot(user:str) -> list:
    usuario = models.Usuario.objects.get(username=user)
    user_token = usuario.telegram_token
    user_chat = usuario.telegram_chatID
    return user_token, user_chat

def generateOTP() -> str:
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6) :
        OTP += string[math.floor(random.random() * length)]
 
    return OTP

def enviar_mensaje(mensaje: str, token:str, chat_id:str) -> bool:
    """
    Envía el mensaje establecido al bot configurado en las
    variables constantes.

    mensaje: str
    returns: bool, True si se pudo mandar el mensaje, False de lo contrario
    """
    try: 
        respuesta = requests.get(URL %
                                 (token, chat_id, mensaje))       
        if not respuesta.status_code == 200:
            return False
        return True
    except:
        return False
