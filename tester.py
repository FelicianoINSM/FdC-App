import requests
target_ip = "127.0.0.1:8080"
route = input('Ingresar ruta (vacio para usar la ruta /): ')
if route:
    url = f'http://{target_ip}/{route}'
else:
    url = f'http://{target_ip}/'

def post():
    json_data = {'code': 1234} 

    try:
        response = requests.post(url, json=json_data)

        if response.ok:
            print(response.text)
        else:
            print(f'Error en la solicitud. Código de estado: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'Error durante la solicitud: {e}')

def get():
    try:
        response = requests.get(url)

        if response.ok:
            print(response.text)
        else:
            print(f'Error en la solicitud. Código de estado: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'Error durante la solicitud: {e}')

if __name__ == '__main__':
    post()