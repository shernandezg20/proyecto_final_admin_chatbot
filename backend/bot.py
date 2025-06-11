import requests
import time

TOKEN = 'xxx'
API_URL = 'http://localhost:8000'
URL = f'https://api.telegram.org/bot{TOKEN}/'
UPDATE_OFFSET = None

def get_updates(offset=None):
    params = {'timeout': 100, 'offset': offset}
    resp = requests.get(URL + 'getUpdates', params=params)
    return resp.json()

def send_message(chat_id, text, parse_mode=None):
    data = {'chat_id': chat_id, 'text': text}
    if parse_mode:
        data['parse_mode'] = parse_mode
    requests.post(URL + 'sendMessage', data=data)

def main():
    global UPDATE_OFFSET
    while True:
        result = get_updates(UPDATE_OFFSET)
        for item in result.get('result', []):
            UPDATE_OFFSET = item['update_id'] + 1
            msg = item['message']
            chat_id = msg['chat']['id']
            text = msg.get('text', '').strip()
            if not text:
                continue

            if text.lower() == '/start':
                send_message(chat_id, '¡Hola! Escribe el nombre de un producto y te mostraré resultados.')
                continue

            # Realizar búsqueda en el backend
            try:
                resp = requests.get(f'{API_URL}/productos/buscar', params={'q': text})
                resp.raise_for_status()
                productos = resp.json()
                if not productos:
                    send_message(chat_id, 'No se encontraron productos según tu búsqueda.')
                else:
                    for p in productos:
                        mensaje = f"*{p['nombre']}*\nPrecio Predicho: Q{p['precio_predicho']:.2f}\nPrecio Real: Q{p['precio_real']:.2f}\n{p['descripcion']}"
                        if p.get('imagen_url'):
                            send_message(chat_id, mensaje, parse_mode='Markdown')
                            # Opcional: enviar imagen
                            requests.post(URL + 'sendPhoto', data={'chat_id': chat_id, 'photo': p['imagen_url']})
                        else:
                            send_message(chat_id, mensaje, parse_mode='Markdown')
            except Exception as e:
                send_message(chat_id, 'Lo siento, ocurrió un error al buscar productos.')

        time.sleep(1)

if __name__ == '__main__':
    main()
