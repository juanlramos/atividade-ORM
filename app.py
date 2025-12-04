from database import engine, SessionLocal
from schema import Base, Usuario, Artista, Musica, Playlist, MusicaPlaylist

def main_demo():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:

        pablo = Usuario(username="Pablo", email="pablo@aluno.com")
        josue = Usuario(username="Josué", email="josue@aluno.com")
        alexandre = Usuario(username="Alexandre", email="alexandre@aluno.com")

        session.add_all([pablo, josue, alexandre])
        session.flush()

        queen = Artista(nome="Queen", nacionalidade="Britânica")
        led_zeppelin = Artista(nome="Led Zeppelin", nacionalidade="Britânica")
        ac_dc = Artista(nome="AC/DC", nacionalidade="Australiana")
        x = Artista(nome="Banda X (Pop)", nacionalidade="Brasileira")

        session.add_all([queen, led_zeppelin, ac_dc, x])
        session.flush()

        bohemian_rhapsody = Musica(titulo="Bohemian Rhapsody", duracao_segundos=354, artista_id=queen.id)
        stairway_to_heaven = Musica(titulo="Stairway To Heaven", duracao_segundos=482, artista_id=led_zeppelin.id)
        back_in_black = Musica(titulo="Back In Black", duracao_segundos=255, artista_id=ac_dc.id)
        we_will_rock_you = Musica(titulo="We Will Rock You", duracao_segundos=160, artista_id=queen.id)
        pop_brasileira = Musica(titulo="Música Pop Brasileira", duracao_segundos=180, artista_id=x.id)
        thunderstruck = Musica(titulo="Thunderstruck", duracao_segundos=292, artista_id=ac_dc.id)

        session.add_all([
            bohemian_rhapsody, stairway_to_heaven,
            back_in_black, we_will_rock_you,
            pop_brasileira, thunderstruck
        ])
        session.flush()

        rock_pablo = Playlist(nome="Rock do Pablo", usuario_id=pablo.id)
        baladas_josue = Playlist(nome="Baladas do Josué", usuario_id=josue.id)
        heavy_riffs = Playlist(nome="Heavy Riffs", usuario_id=pablo.id)

        session.add_all([rock_pablo, baladas_josue, heavy_riffs])
        session.flush()

        if rock_pablo:
            rock_pablo.musicas_associadas.append(
                MusicaPlaylist(musica_id=bohemian_rhapsody.id, usuario_id=pablo.id, ordem_na_playlist=1)
            )
            rock_pablo.musicas_associadas.append(
                MusicaPlaylist(musica_id=back_in_black.id, usuario_id=pablo.id, ordem_na_playlist=2)
            )
            rock_pablo.musicas_associadas.append(
                MusicaPlaylist(musica_id=we_will_rock_you.id, usuario_id=pablo.id, ordem_na_playlist=3)
            )

        if baladas_josue:
            baladas_josue.musicas_associadas.append(
                MusicaPlaylist(musica_id=stairway_to_heaven.id, usuario_id=josue.id, ordem_na_playlist=1)
            )

        if heavy_riffs:
            heavy_riffs.musicas_associadas.append(
                MusicaPlaylist(musica_id=back_in_black.id, usuario_id=pablo.id, ordem_na_playlist=1)
            )
            heavy_riffs.musicas_associadas.append(
                MusicaPlaylist(musica_id=thunderstruck.id, usuario_id=pablo.id, ordem_na_playlist=2)
            )

        session.commit()

if __name__ == "__main__":
    main_demo()