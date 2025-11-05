from database import engine, SessionLocal
from schema import Base

from crud_usuario import (
    criar_usuario
)
from crud_artista import (
    criar_artista
)
from crud_musica import (
    criar_musica
)
from crud_playlist import (
    criar_playlist, adicionar_musica_playlist, 
    remover_musica_playlist, exibir_musicas_playlist
)

def main_demo():
    
    # Para testes
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as session:
        
        pablo = criar_usuario(session, "Pablo", "pablo@aluno.com")
        josue = criar_usuario(session, "Josué", "josue@aluno.com")
        alexandre = criar_usuario(session, "Alexandre", "alexandre@aluno.com")

        queen = criar_artista(session, "Queen", "Britânica")
        led_zeppelin = criar_artista(session, "Led Zeppelin", "Britânica") 
        ac_dc = criar_artista(session, "AC/DC", "Australiana")
        x = criar_artista(session, "Banda X (Pop)", "Brasileira")

        bohemian_rhapsody = criar_musica(session, "Bohemian Rhapsody", 354, queen.id)
        stairway_to_heaven = criar_musica(session, "Stairway To Heaven", 482, led_zeppelin.id)
        back_in_black = criar_musica(session, "Back In Black", 255, ac_dc.id)
        we_will_rock_you = criar_musica(session, "We Will Rock You", 160, queen.id)
        pop_brasileira = criar_musica(session, "Música Pop Brasileira", 180, x.id)
        thunderstruck = criar_musica(session, "Thunderstruck", 292, ac_dc.id)

        rock_pablo = criar_playlist(session, "Rock do Pablo", pablo.id)
        baladas_josue = criar_playlist(session, "Baladas do Josué", josue.id)
        heavy_riffs = criar_playlist(session, "Heavy Riffs", pablo.id)

        if rock_pablo:
            adicionar_musica_playlist(session, bohemian_rhapsody.id, rock_pablo, ordem=1)
            adicionar_musica_playlist(session, back_in_black.id, rock_pablo, ordem=2)
            adicionar_musica_playlist(session, we_will_rock_you.id, rock_pablo, ordem=3)
            # remover_musica_playlist(session, back_in_black.id, rock_pablo)
            exibir_musicas_playlist(session, rock_pablo)

        if baladas_josue:
            adicionar_musica_playlist(session, stairway_to_heaven.id, baladas_josue, ordem=1)
            exibir_musicas_playlist(session, baladas_josue)

        if heavy_riffs:
            adicionar_musica_playlist(session, back_in_black.id, heavy_riffs, ordem=1)
            adicionar_musica_playlist(session, thunderstruck.id, heavy_riffs, ordem=2)
            exibir_musicas_playlist(session, heavy_riffs)



if __name__ == "__main__":
    main_demo()

