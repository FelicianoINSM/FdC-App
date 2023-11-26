import requests

def send_request():
    target_ip = "192.168.35.123:8080"
    url = f'http://{target_ip}/test'
    json_data = {'id': 2, 'name': 'Lauti Puto'} 

    try:
        # Realiza la solicitud POST a la dirección IP especificada
        response = requests.post(url, json=json_data)

        # Verifica si la solicitud fue exitosa (código de estado 2xx)
        if response.ok:
            print(response.text)
        else:
            print(f'Error en la solicitud. Código de estado: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'Error durante la solicitud: {e}')

if __name__ == '__main__':
    send_request()