from database import conectar_db
from personagem import Personagem


class Monstro(Personagem): # A classe Monstro está herdando os atributos e métodos da classe Personagem
    def __init__(self, nome, hp_max, hp_atual, atk, dfs, spd, level):
        super().__init__(nome, [], hp_max, hp_atual, atk, dfs, spd, 0, 0, level) # exp e exp_bar são atribuídos como 0 pois não são relevantes para monstros
        
        # Verifica se o monstro já existe no banco de dados antes de salvar
        if not self.existe_no_db():
            self.salvar_no_db()

    def __str__(self):
        return self.nome


    def existe_no_db(self):
        with self.conectar_db() as conn:
            cursor = conn.execute('SELECT COUNT(*) FROM monstros WHERE nome = ?', (self.nome,)) # é utilizada para contar o número de registros na tabela monstros onde a coluna nome é igual a um valor específico.
            count = cursor.fetchone()[0] # O método fetchone retorna uma tupla de valor único (a contagem de registros), e count recebe o primeiro (e único) valor dessa tupla
            return count > 0 # Retorna um valor booleano se já existir um monstro com o nome


    def salvar_no_db(self):
        with self.conectar_db() as conn:
            # insere um novo registro na tabela monstros ou substitui um registro existente se houver uma chave primária em conflito, ou seja, se já existir um monstro com o mesmo nome, ele será atualizado em vez de duplicado.
            conn.execute('''
                INSERT OR REPLACE INTO monstros (nome, hp_max, hp_atual, atk, dfs, spd, level)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.nome, self.hp_max, self.hp_atual, self.atk, self.dfs, self.spd, self.level))

