from database import conectar_db
import json
from monstro import Monstro
from glb import lista_torres

class Torre:
    def __init__(self, nome, monstro, capanga, recompensa):
        self.nome = nome
        self.monstro = monstro
        self.capanga = capanga
        self.recompensa = recompensa
        lista_torres.append(self) # Adiciona o objeto Torre atual à lista de torres assim que é instanciado.

    # Verifica se a torre já existe no banco de dados antes de salvar
        if not self.existe_no_db():
            self.salvar_no_db()


    def existe_no_db(self):
        with conectar_db() as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM torres WHERE nome = ?', (self.nome,))  # é utilizada para contar o número de registros na tabela torres onde a coluna nome é igual a um valor específico.
            count = cursor.fetchone()[0]  # O método fetchone retorna uma tupla de valor único (a contagem de registros), e count recebe o primeiro (e único) valor dessa tupla
            return count > 0  # Retorna um valor booleano se já existir uma torre com o nome


    def salvar_no_db(self):
        # insere um novo registro na tabela torres ou substitui um registro existente se houver uma chave primária em conflito, ou seja, se já existir uma torre com o mesmo nome, ela será atualizada em vez de duplicada.
        with conectar_db() as conn:
            conn.execute('''
                INSERT INTO torres (nome, monstro_nome, capanga_nome, recompensa) VALUES (?, ?, ?, ?)
            ''', (self.nome, self.monstro.nome, self.capanga.nome, json.dumps(self.recompensa))) # Converte o dicionário para JSON


    @classmethod # método de classe que carrega todas as torres do banco de dados
    def carregar_torres_do_db(cls):
        with conectar_db() as conn:
            cursor = conn.execute('SELECT nome, monstro_nome, capanga_nome, recompensa FROM torres')
            # Uma operação de desempacotamento será executada.
            for row in cursor.fetchall(): # cada row receberá uma tupla com os valores de cada coluna especificada na consulta
                nome, monstro_nome, capanga_nome, recompensa_json = row # cada variável receberá o valor correspondente na tupla row, na mesma ordem
                recompensa = json.loads(recompensa_json)
                
                # Busca o monstro e capanga pelos nomes armazenados
                monstro = cls.buscar_monstro(monstro_nome)
                capanga = cls.buscar_capanga(capanga_nome)

                # Cria a instância da torre após recuperar os dados
                cls(nome, monstro, capanga, recompensa)

    @staticmethod # método estático, ou seja, não depende da instância da classe, e pode ser chamado diretamente na classe
    def buscar_monstro(nome):
        with conectar_db() as conn:
            cursor = conn.execute('SELECT * FROM monstros WHERE nome = ?', (nome,))
            row = cursor.fetchone() # Recebe o resultado da consulta
            if row: # verifica se a tupla resultante da consulta possui um valor
                return Monstro(*row)  # O asterisco antes de row é um operador de desempacotamento. Isso significa que cada elemento da tupla row será passado como um argumento separado para o construtor da classe Monstro
            return None  # Funciona como um 'else'

    @staticmethod # método estático, ou seja, não depende da instância da classe, e pode ser chamado diretamente na classe
    def buscar_capanga(nome):
        with conectar_db() as conn:
            cursor = conn.execute('SELECT * FROM monstros WHERE nome = ?', (nome,))
            row = cursor.fetchone() # Recebe o resultado da consulta
            if row: # verifica se a tupla resultante da consulta possui um valor
                return Monstro(*row)  # O asterisco antes de row é um operador de desempacotamento. Isso significa que cada elemento da tupla row será passado como um argumento separado para o construtor da classe Monstro
            return None  # Funciona como um 'else'

