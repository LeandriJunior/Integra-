from typing import Any


class Categoria:
    def __init__(self):
        pass

    def processar(self, data=None, filial_id=None) -> dict[str, Any]:
        return {
            'codigo': data.get('codigo'),
            'nome': data.get('nome')
        }



