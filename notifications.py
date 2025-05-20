import requests

PUSHOVER_USER_KEY = 'umpfi2md1a6b91zk7pxu5wy2mb3bce'
PUSHOVER_API_TOKEN = 'aentxughcvabrvag556gcbpzejquyc'

def send_pushover_message(title, message, url=None):
    """Enviar mensaje al pushover"""

    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message,
        "url": url, 
        "url_title": "Atender solicitud de asistencia", 
        "html": 1,
        "priority": 2,  
        "sound": "persistent",  
        "retry": 30, # Frecuencia de repetición 
        "expire": 180 # Tiempo máximo de repetición 
    }
    
    response = requests.post("https://api.pushover.net/1/messages.json", data=data)
    return response.status_code == 200