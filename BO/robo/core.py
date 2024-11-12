import sys
import time
import json
from datetime import datetime, timedelta


class Core:
    def __init__(self):
        self.parametros = None
        self.configuracoes = None
        self.anomesdia_atual = None
        self.hora_atual = None

    @staticmethod
    def carregar_json(path=None):
        """
        Função para carregar um arquivo Json em variável
        :param path: Path do Json
        :return: Json convertido em dicionário
        """
        try:
            with open(path, 'r', encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            sys.exit(-4)
        except json.decoder.JSONDecodeError:
            sys.exit(-5)

    def debugar(self, mensagem=None):
        """
        Função que printa a mensagem, caso o debug esteja ativo
        :param mensagem: Mensagem a ser mostrada no terminal
        :return: True
        """
        if self.configuracoes.get('DEBUG'):
            print(mensagem)
        return True

    def rodar(self, funcao=None, nome=None, erro=-99):
        """
        Função generica que roda outras funções
        :return: True
        """
        ini = time.time()
        print(ini)
        self.debugar(mensagem=f'Inicio: {nome}')
        try:
            eval(funcao)
        except Exception as e:
            self.debugar(mensagem=f'Erro: {nome} - {e}')
            sys.exit(erro)
        self.debugar(mensagem=f'Fim: {nome}. Tempo: {time.time() - ini}')
        return True

    def tratar_parametros(self):
        """
        Função que trata os parâmetros padrões das queries
        :return:
        """
        self.anomesdia_atual = self.calcular_anomesdia()

        self.hora_atual = self.calcular_hora(is_hora=True)

        if not self.parametros.get('anomesdia'):
            self.parametros['anomesdia'] = self.calcular_anomesdia()

        if not self.parametros.get('dt_3'):
            self.parametros['dt_3'] = self.calcular_anomesdia(subtrair_dias=3)

        if not self.parametros.get('anomes'):
            self.parametros['anomes'] = self.calcular_anomesatual()

        self.parametros['ano'] = str(self.parametros.get('anomes'))[:4]
        self.parametros['mes'] = str(int(str(self.parametros.get('anomes'))[4:]))

        self.parametros['mes_str'] = self.parametros['mes'].zfill(2)

        prox_anomes = self.calcular_prox_anomes(anomes=self.parametros['anomes'])
        self.parametros['ano_prox'] = str(prox_anomes)[:4]
        self.parametros['mes_prox'] = str(prox_anomes)[4:]

        return True

    def calcular_prox_anomes(self, anomes=None):
        ano = int(str(anomes)[:4])
        mes = int(str(anomes)[4:])
        if mes == 12:
            mes = 1
            ano += 1
        else:
            mes += 1

        return f'{ano}{str(mes).zfill(2)}'

    def calcular_anomesdia(self, subtrair_dias=0, is_hora=False):
        """
        Função que constrói o anomesdia necessário
        :return: Anomesdia (YYYYMMDD)
        """
        agora = datetime.now()
        if subtrair_dias:
            agora = agora - timedelta(days=subtrair_dias)

        dia, mes, ano = agora.day, agora.month, agora.year

        retorno = ano * 10000 + mes * 100 + dia

        if is_hora:
            hora = agora.time().hour
            retorno = f'{retorno}_{hora}'

        return str(retorno)

    def calcular_hora(self, is_hora=False):
        """
        Função que calcula a hora
        :param is_hora: Se é para calcular hora atual ou 0
        :return: Hora
        """
        agora = datetime.now()
        hora = str(agora.time().hour) if is_hora else '0'
        return str(hora)

    def calcular_anomesatual(self):
        """
        Função que constrói o anomes atual
        :return: Anomes (YYYYMM)
        """
        agora = datetime.now()
        return agora.year * 100 + agora.month
