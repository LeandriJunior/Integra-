import importlib

import datetime
import BO.robo.database
import BO.robo.core
import BO.robo.integration


class Robo(BO.robo.core.Core):
    def __init__(self, parametro=None):
        super().__init__()
        self.parametro = parametro
        self.sql_conexao = None
        self.variaveis = None
        self.lojas = None
        self.data_atual = None
        self.data_inicio = None
        self.data_atual_sem_tz = None
        self.count = 0
        self.configuracoes = BO.robo.core.Core.carregar_json('integrations.json')[self.parametro]
        module = importlib.import_module(self.configuracoes['import'])
        self.Trier = getattr(module, self.configuracoes['classe'])
        self.get_conexao()
        self.get_variaveis()

    def processar(self):
        proximo = 0
        json_data = True
        lista = []
        bo_trier = self.Trier()
        try:
            for loja in self.lojas:
                while json_data:
                    try:
                        quantidade = 600
                        json_data = BO.robo.integration.Integration(
                            url=loja[2],
                            token=loja[0]
                        ).get(
                            path=self.configuracoes['path_todos'].format(proximo,
                                                                         quantidade)
                                if self.configuracoes['is_todos']
                                else self.configuracoes['path_data'].format(proximo,
                                                                            quantidade,
                                                                            self.data_inicio,
                                                                            self.data_atual)
                        )
                        if not isinstance(json_data, list):
                            print(json_data)
                            break
                        for data in json_data:

                            lista.append(
                                bo_trier.processar(data=data, filial_id=loja[1])
                            )
                            self.count = self.count + 1

                        self.sql_conexao.bulk_insert(
                            nm_tabela=self.configuracoes['tabela'],
                            lista_dict_coluna_valor=lista,
                            nm_pk=self.configuracoes['nm_pk']
                        )

                        lista = []
                        print(f'Mais 600 da loja {loja[1]}, já se foram: {self.count}')

                        proximo = proximo + 600
                        if len(json_data) < 600:
                            break
                    except:
                        self.get_conexao()
                        continue
                print(self.count)
                self.salvar_data()
        except Exception as e:
            print(e)

    def get_conexao(self):
        dados_db = BO.robo.core.Core().carregar_json('config.json')
        self.sql_conexao = BO.robo.database.SqlAlchemy(
            user=dados_db.get('USER'),
            password=dados_db.get('PASSWORD'),
            host=dados_db.get('HOST'),
            port=dados_db.get('PORT'),
            database=dados_db.get('NAME'),
            sgbd=dados_db.get('SGBD'),
            driver=dados_db.get('DRIVER')
        )

    def get_variaveis(self):
        self.variaveis = list(self.sql_conexao.buscar(
                query="""   
                            select * 
                            from stage.config_temporarias 
                            where integracao = 'produto' 
                            order by data_ini desc 
                            limit 1
                        """
            ))[0]
        query_lojas = """
                            select    senha
                                    , info_1
                                    , url as filial_id 
                            from sistema_chavesintegracao 
                            where nome='chave_trier'
                    """
        if self.configuracoes['is_first']:
            query_lojas += " and info_1 = '3'"
        self.lojas = self.sql_conexao.buscar(
                query=query_lojas
        )

        self.sql_conexao.buscar(query='truncate table stage.tmp_produto;')

        tz = datetime.timezone(datetime.timedelta(hours=-3))
        self.data_atual_sem_tz = datetime.datetime.now().replace(tzinfo=tz)
        self.data_atual = self.data_atual_sem_tz.isoformat(timespec='seconds').replace('-03:00', '-0300')
        self.data_inicio = self.variaveis[0].replace(tzinfo=tz).isoformat(timespec='seconds').replace('-03:00', '-0300')

    def salvar_data(self) -> None:
        self.get_conexao()
        self.sql_conexao.buscar(query=f"""
                  update stage.config_temporarias
                  set data_ini = '{self.data_atual_sem_tz}',
                      data_fim = '{datetime.datetime.now()}',
                      quantidade = {self.count}
                  where integracao = '{self.parametro}'
          """)