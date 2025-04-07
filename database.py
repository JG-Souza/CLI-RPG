import sqlite3 as sq


def conectar_db():
    return sq.connect('jogadores.db') # Método que estabelece a conexão com o db que está no parâmetro                                            


def criar_tabelas(): # Cria as tabelas no banco de dados
    with conectar_db() as conn: # with é um gerenciador de contexto, ou seja, ao abrir a conexão, ele será fechada ao final do bloco, mesmo que ocorra um erro
        # conn é uma referência à conectar_db() e o método execute() executa comandos SQL
        conn.execute('''
            CREATE TABLE IF NOT EXISTS jogadores (
                nome TEXT PRIMARY KEY,
                mochila TEXT,
                hp_max INTEGER,
                hp_atual INTEGER,
                atk INTEGER,
                dfs INTEGER,
                spd INTEGER,
                exp INTEGER,
                exp_bar INTEGER,
                level INTEGER
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS monstros (
                nome TEXT PRIMARY KEY,
                hp_max INTEGER,
                hp_atual INTEGER,
                atk INTEGER,
                dfs INTEGER,
                spd INTEGER,
                level INTEGER
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS torres (
                nome TEXT PRIMARY KEY,
                monstro_nome TEXT,
                capanga_nome TEXT,
                recompensa TEXT
            )
        ''')


