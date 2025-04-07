import sqlite3 as sq
import json
from database import conectar_db
from glb import lista_torres, lista_personagens

class Personagem:
    def __init__(self, nome, mochila, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level):
        self.nome = nome
        self.mochila = mochila if mochila is not None else []
        self.hp_max = hp_max
        self.hp_atual = hp_atual
        self.atk = atk
        self.dfs = dfs
        self.spd = spd
        self.exp = exp
        self.exp_bar = exp_bar
        self.level = level
        self.carregar_do_db(nome)
        lista_personagens.append(self) # Adiciona o objeto Personagem atual à lista de personagens assim que é instanciado.
        self.salvar_no_db()


    @staticmethod # método estático, ou seja, não depende da instância da classe, e pode ser chamado diretamente na classe
    def conectar_db():
        return conectar_db()


    def salvar_no_db(self):
        if type(self) is Personagem: # verifica se a instância atual não é de uma subclasse (como Monstro)
            with self.conectar_db() as conn:
                conn.execute('''
                    INSERT OR REPLACE INTO jogadores (nome, mochila, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.nome, json.dumps(self.mochila), self.hp_max, self.hp_atual, self.atk, self.dfs, self.spd, self.exp, self.exp_bar, self.level)) # se já existir um registro com o mesmo nome, ele será atualizado com os novos valores


    def carregar_do_db(self, nome):
        with self.conectar_db() as conn:
            cursor = conn.execute('SELECT * FROM jogadores WHERE nome = ?', (nome,))
            row = cursor.fetchone() # obtem uma tupla com os dados do jogador.
            if row: # se row é diferente de None
                self.mochila = json.loads(row[1]) if row[1] else []  # Carrega a mochila como uma lista a partir da string JSON
                self.hp_max, self.hp_atual, self.atk, self.dfs, self.spd, self.exp, self.exp_bar, self.level = row[2:] # atribui os valores da linha obtida, aos atributos correspondentes do objeto (self)
                # está sendo feito um fatiamento acima, selecionando todos os elementos a partir do índice 1 até o final da tupla.


    @classmethod # método de classe que carrega todos os personagens do db
    def carregar_personagens_do_db(cls):
        with cls.conectar_db() as conn:
            cursor = conn.execute('SELECT nome, mochila, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level FROM jogadores')
            for row in cursor.fetchall(): # Cada row será uma tupla contendo os dados de um jogador
                nome, mochila, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level = row # é um desempacotamento

                # Deserializa a mochila de JSON para um objeto Python (lista de dicionários)
                mochila = json.loads(mochila) if mochila else []  # Se mochila for None ou uma string vazia, atribui uma lista vazia

                personagem = cls(nome, mochila, hp_max, hp_atual, atk, dfs, spd, exp, exp_bar, level) # cria uma instancia


    # Verifica se o item já existe na mochila
    def item_existe(self, novo_item):
        return any(item['Nome'] == novo_item['Nome'] for item in self.mochila)


    # Adiciona um novo item à mochila se ele não existir
    def adicionar_item(self, novo_item):
        if not self.item_existe(novo_item):
            if isinstance(novo_item, dict):  # Verifica se item é um dicionário
                self.mochila.append(novo_item)
                self.salvar_no_db()
            else:
                print(f'Item não pode ser adicionado à mochila: {novo_item}')
        else:
            print(f"Item {novo_item['Nome']} já está na mochila.")


    def visualizar_mochila(self):
        for item in self.mochila:
            print(f"Nome: {item['Nome']}, Descrição: {item['Descrição']}, Efeito: {item['Efeito']}")


    # Faz uma verificação de level up, para evitar repetição do próprio método level_up
    def verifica_level_up(self):
        if self.exp >= self.exp_bar:
            self.level_up()


    # Executa a lógica de subida de level
    def level_up(self):
        self.exp -= self.exp_bar
        self.exp_bar = int(round(self.exp_bar * 1.4))
        print('=' * 40)
        escolha = input('Onde você gostaria de colocar seu ponto de habilidade?\n1. Ataque\n2. Defesa\n3. Velocidade\n4. Max HP\n-> ')
        print('=' * 40)
        if escolha == '1':
            self.atk += 2
        elif escolha == '2':
            self.dfs += 2
        elif escolha == '3':
            self.spd += 2
        elif escolha == '4':
            self.hp_max += 3

        self.hp_max += 2
        self.level += 1
        self.salvar_no_db()

        print(f'Nome: {self.nome}\nMax HP: {self.hp_max}\nAtaque: {self.atk}\nDefesa: {self.dfs}\nVelocidade: {self.spd}\nNível: {self.level}')


    # Executa a lógica de um ataque
    def atacar(self, inimigo):
        dano = round(self.atk - (30 / 100 * inimigo.dfs))
        inimigo.hp_atual -= dano
        if inimigo.hp_atual < 0:
            inimigo.hp_atual = 0


    # Executa a lǵgica de uma luta
    def lutar(self, inimigo):
        atk_puro = self.atk
        for item in self.mochila:
            if item['Nome'] == 'Espada Alada':
                self.atk = atk_puro * 1.25

        if self.hp_atual == 0: # Verifica se você está apto para luta
            print('Você não possui HP suficiente, visite o médico')
            return

        # Atribui os pspéis de atacante e defensor
        atacante, defensor = (self, inimigo) if self.spd > inimigo.spd else (inimigo, self)

        while self.hp_atual > 0 and inimigo.hp_atual > 0: # Verifica se os dois estao vivos
            atacante.atacar(defensor)
            if defensor.hp_atual > 0:
                atacante, defensor = defensor, atacante # Troca os papéis

        # Lógica para caso de vitória
        if self.hp_atual > 0:
            self.exp += inimigo.level
            print('=' * 40)
            print(f'Você venceu a luta contra {inimigo.nome}, e ganhou {inimigo.level}xp')
            print(f'Você está com {self.exp}/{self.exp_bar} XP')
            self.verifica_level_up()
        
        # Lógica para caso de derrota
        else:
            print(f'Você foi derrotado por {inimigo}')
        self.atk = atk_puro
        self.salvar_no_db()
        inimigo.salvar_no_db()


    # Apresenta as informações sobre o personagem 
    def ver_status(self):
        print(f'Nome: {self.nome}\nHP: {self.hp_atual}/{self.hp_max}\nAtaque: {self.atk}\nDefesa: {self.dfs}\nVelocidade: {self.spd}\nNível: {self.level}\nEXP: {self.exp}/{self.exp_bar}')


    # Cria uma exibição com os nomes de oponentes disponíveis
    def escolhe_oponente(self):
        print('Oponentes Disponíveis: ')
        for personagem in lista_personagens:
            if personagem != self and type(personagem) is Personagem:
                print(personagem.nome)


    # Cria uma exibição com os nomes de todos os personagens disponíveis
    @staticmethod
    def escolhe_personagem():
        print('Personagens Disponíveis:')
        if not lista_personagens:
            print('Nenhum personagem disponível.')
        else:
            for personagem in lista_personagens:
                if type(personagem) is Personagem:
                    print(personagem.nome)


    # Lógica para resturar o HP do personagem
    def ir_ao_medico(self):
        self.hp_atual = self.hp_max
        print('Você restaurou seu HP com sucesso')
        self.salvar_no_db()


    # Lógica para enfrentar uma Torre
    def lutar_na_torre(self):
        for torre in lista_torres: # Cria uma exibição com todas as torres disponíveis
            print(f'{torre.nome}')

        escolha = input('Escolha uma torre: ')
        torre_escolhida = next((torre for torre in lista_torres if torre.nome.lower() == escolha.lower()), None) # Busca a torre escolhida na lista_torres com base no nome


        if torre_escolhida: # Verifica se a torre escolhida existe
            # Lógica da luta na torre
                self.lutar(torre.capanga) # Lutar contra o capanga
                if self.hp_atual > 0:
                    self.lutar(torre.monstro)
                    if self.hp_atual > 0:
                        print(f"Parabéns!!! Você venceu a {torre.nome} e ganhou a {torre.recompensa['Nome']}")
                        self.adicionar_item(torre.recompensa)

            # Recuperando o HP dos habitantes da torre
                torre.monstro.hp_atual = torre.monstro.hp_max
                torre.capanga.hp_atual = torre.capanga.hp_max
        else:
            print('Escolha inválida')
        

    # Cria um loop de ações que podem ser executadas por um personagem
    def acoes(self):
        while True:
            print('=' * 40)
            acao = input('Qual ação você quer tomar agora?\n1. Ver seus Stats\n2. Lutar (Treino)\n3. Ir ao médico\n4. Lutar na Torre\n5. Trocar de Personagem\n-> ')

            if acao == '1':
                self.ver_status()

            elif acao == '2':
                self.escolhe_oponente()
                oponente_nome = input('Com quem você quer lutar? ')
                oponente = next((p for p in lista_personagens if p.nome == oponente_nome), None) # Busca na lista_personagens o personagem cujo nome corresponde a oponente_nome
                if oponente:
                    self.lutar(oponente)
                else:
                    print('Personagem não encontrado!')
                    break

            elif acao == '3':
                self.ir_ao_medico()

            elif acao == '4':
                self.lutar_na_torre()

            elif acao == '5':
                break


    # Método para listar as torres
    @classmethod
    def listar_torres(cls):  
        for torre in lista_torres:
            print(f'{torre.nome}')

        escolha = input('Escolha uma torre: ')
        torre_escolhida = next((torre for torre in lista_torres if torre.nome.lower() == escolha.lower()), None) # Busca a torre escolhida na lista_torres com base no nome
        if torre_escolhida:
            cls.ver_torre(torre_escolhida) # Formata e exibe as informações da torre escolhida
        else:
            print('Escolha inválida')


    # Formata e exibe as informações da torre escolhida
    @classmethod
    def ver_torre(cls, torre):
        print(f'Nome: {torre.nome}\nMonstro: {torre.monstro.nome}\nHP: {torre.monstro.hp_atual}/{torre.monstro.hp_max}\nAtaque: {torre.monstro.atk}\nDefesa: {torre.monstro.dfs}\nVelocidade: {torre.monstro.spd}\nNível: {torre.monstro.level}')
        print(f'Capanga: {torre.capanga.nome}\nHP: {torre.capanga.hp_atual}/{torre.capanga.hp_max}\nAtaque: {torre.capanga.atk}\nDefesa: {torre.capanga.dfs}\nVelocidade: {torre.capanga.spd}\nNível: {torre.capanga.level}')


    # Cria um loop de "menu"
    @classmethod
    def inicio(cls):
        while True:
            print('=' * 40)
            acao_inicial = input('Qual ação você quer tomar agora?\n1. Ver personagens disponíveis\n2. Ver Torres\n3. Sentar e Descansar\n-> ')
            if acao_inicial == '1':
                cls.escolhe_personagem()
                personagem_nome = input('Com qual personagem você quer jogar? ')
                personagem = next((p for p in lista_personagens if p.nome == personagem_nome), None) # Busca na lista_personagens o personagem cujo nome corresponde a personagem_nome
                if personagem: # Se encontrar, então o personagem pode ser utilizado
                    personagem.acoes()
                else:
                    print('Personagem não encontrado!')
            elif acao_inicial == '2':
                cls.listar_torres() 
            elif acao_inicial == '3':
                break
            else:
                print('Opção inválida, tente novamente!')
