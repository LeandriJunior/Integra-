from typing import Any


class Estoque:
    def __init__(self):
        pass

    def processar(self, data=None, filial_id=None) -> dict[str, Any]:
        return {
            'codigoProduto': data.get('codigoProduto'),
            'quantidadeEstoque': data.get('quantidadeEstoque'),
            'valorCustoMedio': data.get('valorCustoMedio'),
            'dataUltimaEntrada': data.get('dataUltimaEntrada'),
            'valorUltimaEntrada': data.get('valorUltimaEntrada'),
            'filial_id': filial_id
        }




