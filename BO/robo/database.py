import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, scoped_session


class SqlAlchemy:
    """
    Classe padrão de comandos SQL
    """
    def __init__(self, user, password, host, port, database, sgbd, driver):
        self.user = user
        self.senha = password
        self.host = host
        self.porta = port
        self.database = database
        self.sgbd = sgbd
        self.driver = driver
        self.engine = None
        self.conexao = None
        self.metadata = None
        self.session = None
        self.resultset = None
        self.scoped_session = None

        self.conectar()

    def conectar(self):
        """
        Função que conecta no banco de dados
        :return:
        """
        database_url = 'postgresql+psycopg2://{user}:{password}@{host}/{database_name}'.format(
            user=self.user,
            password=self.senha,
            host=self.host,
            database_name=self.database,
        )
        self.engine = db.create_engine(database_url, query_cache_size=0)
        self.conexao = self.engine.connect()
        self.metadata = db.MetaData()
        self.scoped_session = scoped_session(sessionmaker(bind=self.engine))


    def get_driver(self):
        """
        Função que retorna o driver usado na conexão
        :return:
        """
        if self.driver not in ['', None]:
            return f'?driver={self.driver}'
        return ''

    def get_sgbd(self):
        """
        Função que retorna qual a conexão do SGBD usado
        :return:
        """
        dict_sgbd = {
            'postgresql': f'postgresql+psycopg2',
            'sql-server': f'mssql+pyodbc'
        }
        try:
            return dict_sgbd[self.sgbd]
        except:
            return dict_sgbd['postgresql']

    def cria_sessao(self):
        """
        Função para criar sessão no banco
        """
        self.session = self.scoped_session()

    def remove_sessao(self):
        """
        Função que remove sessão no banco
        :return:
        """
        self.scoped_session.remove()

    def fazer_comando(self, query=None, tipo='select', parametros=None):
        """
        Função que faz o comando no banco
        :param query: Query a ser realizada
        :param tipo: Tipo de comando (Select, Insert, Delete, etc...)
        :param parametros: Parametros genéricos da query
        :return:
        """
        try:
            self.cria_sessao()
            with self.session.begin():
                self.resultset = self.session.execute(text(query), parametros).fetchall()
            self.remove_sessao()
            if tipo == 'select':
                cabecalho = list(self.resultset[0]._fields)
                dados = [list(row) for row in self.resultset]
                del self.resultset
                self.resultset = None
                return {'status': True, 'erro': None, 'dados': dados, 'cabecalho': cabecalho}
            else:
                return {'status': True, 'erro': None, 'dados': [], 'cabecalho': []}
        except Exception as e:
            print('erro do banco:')
            print(str(e))
            print(str(e)[:500])
            self.remove_sessao()
            return {'status': False, 'erro': str(e)[:500], 'dados': []}

    def bulk_insert(self, nm_tabela, lista_dict_coluna_valor, nm_pk='id'):
        if not lista_dict_coluna_valor:
            return None

        if len(nm_tabela.split('.')) == 1:
            nm_tabela = self.schema_cliente + '.' + nm_tabela

        colunas = ''
        valores = ''
        parametros = {}
        for contador, dict_coluna_valor in enumerate(lista_dict_coluna_valor):
            if not colunas:
                colunas = ','.join(dict_coluna_valor.keys())
            nm_valores = ''
            for chave, valor in dict_coluna_valor.items():
                parametros[f"{chave}_{contador}"] = valor
                nm_valores += f" :{chave}_{contador},"
            nm_valores = nm_valores[:-1]  # Removendo a última vírgula

            valores += f"({nm_valores}),"
        valores = valores[:-1]  # Removendo a última vírgula

        query = f'insert into {nm_tabela}({colunas}) values {valores} RETURNING {nm_pk};'

        retorno = self.__query(query=query, parametros=parametros)

        return retorno

    def buscar(self, query=None):
        with self.conexao.begin():
            self.resultset = self.conexao.execute(text(query))

        return self.resultset

    def __query(self, query=None, parametros=None):
        if parametros is None:
            parametros = {}

        self.parse_lista_para_tupla(parametros)

        with self.engine.begin() as conn:
            texto = text(query)
            self.resultset = conn.execute(texto, parametros)

        if self.resultset.returns_rows:
            return list(self.resultset)
        else:
            return None

    @staticmethod
    def parse_lista_para_tupla(parametros):
        for p in parametros:
            if isinstance(parametros[p], (list, set)):
                if len(parametros[p]) > 0:
                    parametros[p] = tuple(parametros[p])
                else:
                    parametros[p] = tuple([None])

            elif isinstance(parametros[p], tuple):
                if len(parametros[p]) < 0:
                    parametros[p] = tuple([None])
