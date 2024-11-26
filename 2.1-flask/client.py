import requests

#HOST = 'http://127.0.0.1:8000'
HOST = 'http://127.0.0.1:5002'


def post():
    post_data = {
        'title': 'Selling an aquarium fish',
        'description': 'Guppi fish, really cute',
        'owner': 'Mike'
    }

    response = requests.post(f'{HOST}/advertisements', json=post_data)
                         
    print(response.status_code)
    print(response.text)