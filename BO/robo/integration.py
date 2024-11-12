import json

import requests

import BO.robo.core


class Integration:
    def __init__(self, url=None, token=None):
        self.url = url
        self.header = {"Authorization": 'Bearer ' + token,
                       'Accept': '*/*'}

    def get(self, path=None):
        try:
            doc_itens = requests.get(self.url + path, headers=self.header)

            json_docs = json.loads(doc_itens.text)
            return json_docs
        except Exception as e:
            print('--- Erro ao buscar dados da integração ---')
            print(e)
            raise AttributeError
