from database import criar_tabelas

from personagem import Personagem
from torre import Torre
from monstro import Monstro

# só executa se o script for executado diretamente (não se for importado como um módulo)
if __name__ == '__main__':
    criar_tabelas() # Garante que as tabelas sejam criadas antes de qualquer outra operação
    # Recuperam informações do db
    Personagem.carregar_personagens_do_db()
    Torre.carregar_torres_do_db()
    # Da inicio ao loop de ações do jogo
    Personagem.inicio()

    # Improvisação antes da atribuição da lógica de itens
    espada_alada = { "Nome": "Espada Alada", "Descricao": "Uma espada muito bela bla bla bla", "Efeito": "+25% de Ataque" }



    # Criando dois objetos da classe Monstro
    dragao = Monstro('Dragão', hp_max=50, hp_atual=50, atk=10, dfs=6, spd=4, level=10)
    esqueleto = Monstro('Esqueleto', hp_max=10, hp_atual=10, atk=2, dfs=2, spd=2, level=1)

    # Criando um objeto da classe Torre
    torre_do_poder = Torre(nome= 'torre do poder',monstro = dragao, capanga = esqueleto, recompensa= espada_alada)

    # Criando um objeto da classe Personagem
    jg = Personagem('jg', [], 20, 20, 4, 4, 4, 0, 20, 1)



        