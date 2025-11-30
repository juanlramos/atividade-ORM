from database import SessionLocal
from schema import Artista, Musica, MusicaPlaylist, Playlist, Usuario
from sqlalchemy import select, func, desc
import pandas as pd

session = SessionLocal()

# Query 1
# Playlists de um Usuário Específico: Implemente uma função para listar todas as Playlists de um USUARIO específico, usando o username como filtro (ex: 'Pablo'). O retorno deve incluir o nome da Playlist e a data de criação.

def query1(username: str):
    query = (
        select(Playlist.nome, Playlist.data_criacao)
        .join(Usuario)
        .where(Usuario.username == username)
    )
    
    query_result = session.execute(query).all()

    return query_result

# Query 2
# Encontre todas as Músicas que pertencem a qualquer Playlist criada por um USUARIO específico (ex: 'Josue'), e cujo ARTISTA seja 'Queen'.

def query2(username: str, nome_artista: str):
    query = (
        select(Musica)
        .join(Musica.artista)
        .join(Musica.playlists_associadas)
        .join(MusicaPlaylist.playlist)
        .join(Playlist.usuario)
        .where(Usuario.username == username)
        .where(Artista.nome == nome_artista)
    )

    query_result = session.execute(query).all()

    return query_result

# Query 3
# Liste o nome de todas as Playlists e o número total de Músicas que cada uma contém. A listagem deve ser ordenada da Playlist mais longa para a mais curta.

def query3():
    query = (
        select(
            Playlist.nome, 
            func.count(MusicaPlaylist.musica_id).label('total_musicas')
        )
        .outerjoin(Playlist.musicas_associadas)
        .group_by(Playlist.playlist_id, Playlist.usuario_id, Playlist.nome)
        .order_by(desc('total_musicas'))
    )

    query_result = session.execute(query).all()

    return query_result

# Query 4
# Identifique e liste todos os Artistas que não possuem nenhuma de suas Músicas adicionadas a nenhuma Playlist no sistema.

def query4():
    query = (
        select(Artista)
        .where(Artista.id.not_in(
            (
                select(Musica.artista_id)
                .join(MusicaPlaylist, Musica.id == MusicaPlaylist.musica_id)
            )
        ))
    )

    query_result = session.execute(query).all()

    return query_result

result = query3()

df = pd.DataFrame(result, columns=["Nome", "total_musicas"])
print(df)