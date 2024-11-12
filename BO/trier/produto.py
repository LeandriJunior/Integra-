from typing import Any


class Produto:
    def __init__(self):
        pass

    def processar(self, data=None, filial_id=None) -> dict[str, Any]:

        tipo_codigo = None
        tipo_nome = None
        if data.get('tipo'):
            tipo_codigo = data.get('tipo').get('codigo')
            tipo_nome = data.get('tipo').get('nome')
        return {
            'codigo': data.get('codigo'),
            'nome': data.get('nome'),
            'valorVenda': data.get('valorVenda'),
            'valorCusto': data.get('valorCusto'),
            'valorCustoMedio': data.get('valorCustoMedio'),
            'quantidadeEstoque': data.get('quantidadeEstoque'),
            'unidade': data.get('unidade'),
            'codigoBarras': data.get('codigoBarras'),
            'codigoLaboratoria': data.get('codigoLaboratoria'),
            'nomeLaboratorio': data.get('nomeLaboratorio'),
            'codigoGrupo': data.get('codigoGrupo'),
            'nomeGrupo': data.get('nomeGrupo'),
            'codigoPrincipioAtivo': data.get('codigoPrincipioAtivo'),
            'nomePrincipioAtivo': data.get('nomePrincipioAtivo'),
            'codigoCategoria': data.get('codigoCategoria'),
            'nomeCategoria': data.get('nomeCategoria'),
            'codigoClassificacao': data.get('codigoClassificacao'),
            'nomeClassificacao': data.get('nomeClassificacao'),
            'ativo': data.get('ativo'),
            'percentualDesconto': data.get('percentualDesconto'),
            'percentualDescontoMax': data.get('percentualDescontoMax'),
            'tipoLista': data.get('tipoLista'),
            'tipo_codigo': tipo_codigo,
            'tipo_nome': tipo_nome,
            'observacaoVenda': data.get('observacaoVenda'),
            'tags': data.get('tags'),
            'integracaoEcommerce': data.get('integracaoEcommerce'),
            'nomeEcommerce': data.get('nomeEcommerce'),
            'descricaoEcommerce': data.get('descricaoEcommerce'),
            'valorVendaEcommerce': data.get('valorVendaEcommerce'),
            'quantidadeEstoqueEcommerce': data.get('quantidadeEstoqueEcommerce'),
            'larguraEcommerce': data.get('larguraEcommerce'),
            'alturaEcommerce': data.get('alturaEcommerce'),
            'pesoEcommerce': data.get('pesoEcommerce'),
            'corEcommerce': None,
            'tamanhoEcommerce': None,
        }




