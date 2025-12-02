from database import SessionLocal
from schema import Artista, Musica, MusicaPlaylist, Playlist, Usuario
from sqlalchemy import select, func, desc
import pandas as pd
import sys

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

if __name__ == "__main__":
    # Verifica se foi passado pelo menos um argumento, se não, exibe instruções de uso
    if len(sys.argv) < 2:
        print("Erro: Informe o número da query")
        print("Exemplo: python queries.py 3")
        sys.exit(1)

    escolha = sys.argv[1] # Pega o primeiro argumento após o nome do arquivo

    result = []
    colunas = []

    try:
        if escolha == "1":
            # Query 1 precisa de 1 argumento extra: username
            if len(sys.argv) < 3:
                print("Erro: Query 1 precisa do username. Ex: python queries.py 1 'Pablo'")
            else:
                username = sys.argv[2]
                result = query1(username)
                colunas = ["Nome Playlist", "Data Criação"]

        elif escolha == "2":
            # Query 2 precisa de 2 argumentos extras: username e artista
            if len(sys.argv) < 4:
                print("Erro: Query 2 precisa de user e artista. Ex: python queries.py 2 'Josue' 'Queen'")
            else:
                username = sys.argv[2]
                nome_artista = sys.argv[3]
                result = query2(username, nome_artista)
                colunas = ["Objeto Musica"] 

        elif escolha == "3":
            result = query3()
            colunas = ["Nome Playlist", "Total Musicas"]

        elif escolha == "4":
            result = query4()
            colunas = ["Objeto Artista"]
        
        else:
            print("Opção inválida!")
            sys.exit(1)

        # Exibição do Resultado
        if result:
            df = pd.DataFrame(result)
            if len(df.columns) == len(colunas):
                df.columns = colunas
            print(df)
        else:
            print("Nenhum resultado encontrado para esta consulta.")

    except Exception as e:
        print(f"Ocorreu um erro ao executar a query: {e}")