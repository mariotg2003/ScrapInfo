import json


def write_json(dic_objets, element):

    with open(f'datos_{element}.json', 'w', encoding='utf-8') as archivo:
        json.dump(dic_objets, archivo, indent=4, ensure_ascii=False)