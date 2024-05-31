import math, random
import os
import requests
from db import models

#TOKEN = os.environ.get('TELE_TOKEN')
#CHAT_ID = os.environ.get('TELE_CHAT_ID')
URL = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s'

def obtener_bot(user:object) -> tuple:
    telegram_bot = models.TelegramBot.objects.get(usuario=user)
    return telegram_bot

def generate_otp() -> str:
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for _ in range(6) :
        OTP += string[math.floor(random.random() * length)]
 
    return OTP

def enviar_mensaje(mensaje: str, user: object) -> bool:
    """
    Envía el mensaje establecido al bot configurado en las
    variables constantes.

    mensaje: str
    returns: bool, True si se pudo mandar el mensaje, False de lo contrario
    """
    telegram_bot = obtener_bot(user)

    try: 
        respuesta = requests.get(URL %
                                 (telegram_bot.telegram_token, telegram_bot.telegram_chatID, mensaje))
        if respuesta.status_code != 200:
            return False
        return True
    except requests.RequestException:
        return False

    
