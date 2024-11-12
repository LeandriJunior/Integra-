from typing import Any


class Grupo:
    def __init__(self):
        pass

    def processar(self, data=None, filial_id=None) -> dict[str, Any]:
        return {
            'ativo': data.get('ativo'),
            'codigo': data.get('codigo'),
            'nome': data.get('nome')
        }


