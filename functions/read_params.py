import json

def get_info(nombreJson):

    with open(f'./data/{nombreJson}.json', 'r', encoding='utf-8') as archivo:
        data = json.load(archivo)

    return data