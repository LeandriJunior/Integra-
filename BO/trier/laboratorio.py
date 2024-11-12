from typing import Any


class Laboratorio:
    def __init__(self):
        pass

    def processar(self, data=None, filial_id=None) -> dict[str, Any]:
        return {
            'ativo': data.get('ativo'),
            'cnpj': data.get('cnpj'),
            'codigo': data.get('codigo'),
            'nome': data.get('nome')
        }



