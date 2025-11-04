from sqlalchemy.orm import Session
from sqlalchemy import select
from schema import Usuario, Musica, Playlist, MusicaPlaylist

def criar_playlist(session: Session, nome_playlist: str, usuario_id: int) -> Playlist | None:
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        return None
        
    nova_playlist = Playlist(nome=nome_playlist, usuario_id=usuario.id)
    
    session.add(nova_playlist)
    session.commit()
    session.refresh(nova_playlist)
    
    return nova_playlist


def adicionar_musica_playlist(session: Session, musica_id: int, playlist: Playlist, ordem: int) -> MusicaPlaylist | None:
    musica = session.get(Musica, musica_id)
    if not musica:
        return None
    
    if not playlist:
        return None

    nova_associacao = MusicaPlaylist(ordem_na_playlist=ordem, playlist=playlist, musica=musica)
    
    session.add(nova_associacao)
    session.commit()
    
    return nova_associacao


def remover_musica_playlist(session: Session, musica_id: int, playlist: Playlist) -> bool:

    stmt = select(MusicaPlaylist).where(
        MusicaPlaylist.musica_id == musica_id,
        MusicaPlaylist.playlist_id == playlist.playlist_id,
        MusicaPlaylist.usuario_id == playlist.usuario_id
    )
    
    associacao = session.execute(stmt).scalar_one_or_none()
    
    if associacao:
        session.delete(associacao)
        session.commit()
        return True
    else:
        return False

def exibir_musicas_playlist(session: Session, playlist: Playlist):
    print(f"\n--- Músicas em '{playlist.nome}' ({playlist.usuario.username}) ")
    
    session.refresh(playlist)
    
    if not playlist.musicas_associadas:
        print("   (Playlist vazia)")
        return

    associacoes_ordenadas = sorted(
        playlist.musicas_associadas,
        key=lambda assoc: assoc.ordem_na_playlist
    )

    for assoc in associacoes_ordenadas:
        print(f"   {assoc.ordem_na_playlist}. {assoc.musica.titulo} (Artista: {assoc.musica.artista.nome})")
    print("-------------------------------------------------")
