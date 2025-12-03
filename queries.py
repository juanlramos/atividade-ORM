from database import SessionLocal
from schema import Artista, Musica, MusicaPlaylist, Playlist, Usuario
from sqlalchemy import select, func, desc
from sqlalchemy.exc import SQLAlchemyError
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
        select(Musica.id, Musica.titulo, Musica.duracao_segundos, Musica.artista_id)
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
        select(Artista.id, Artista.nome, Artista.nacionalidade)
        .where(Artista.id.not_in(
            (
                select(Musica.artista_id)
                .join(MusicaPlaylist, Musica.id == MusicaPlaylist.musica_id)
            )
        ))
    )

    query_result = session.execute(query).all()

    return query_result

# Query 10
# Liste todos os Artistas e seu ranking baseado no número de Playlists em que suas músicas estão presentes (o Artista com músicas na maior quantidade de playlists fica em 1º).

def query10():
    query = (
        select(
            Artista.nome,
            func.count(func.distinct(MusicaPlaylist.playlist_id)).label('total_playlists')
        )
        .outerjoin(Artista.musicas)
        .outerjoin(Musica.playlists_associadas)
        .group_by(Artista.id, Artista.nome)
        .order_by(desc('total_playlists'))
    )

    query_result = session.execute(query).all()

    return query_result

# Query 11
# Liste todas as Músicas do Artista 'Led Zeppelin' cuja duração é maior que a duração da música mais longa do Artista 'Queen'.

def query11():
    query = (
        select(Musica.titulo, Musica.duracao_segundos)
        .join(Artista)
        .where(Artista.nome == 'Led Zeppelin')
        .where(Musica.duracao_segundos > 
                select(func.max(Musica.duracao_segundos))
                .join(Artista)
                .where(Artista.nome == 'Queen')
                .scalar_subquery())
    )
    
    query_result = session.execute(query).all()

    return query_result

# Query 12
# Implemente uma função que mova uma MUSICA de uma PLAYLIST para outra PLAYLIST (ambas do mesmo USUARIO), garantindo que o processo seja Atômico (ou tudo acontece ou nada acontece).

def query12(usuario_id: int, id_playlist_origem: int,  id_playlist_destino: int, id_musica: int, nova_ordem: int) -> bool:
    try:
        playlists_encontradas = session.execute(
            select(Playlist).where(
                Playlist.playlist_id.in_([id_playlist_origem, id_playlist_destino]),
                Playlist.usuario_id == usuario_id
            )
            ).scalars().all()
        
        if len(playlists_encontradas) != 2:
            print("ERRO: Uma ou ambas as playlists não foram encontradas ou não pertencem ao usuário.")
            return False

        associacao_origem = session.execute(
            select(MusicaPlaylist).where(
                MusicaPlaylist.musica_id == id_musica,
                MusicaPlaylist.playlist_id == id_playlist_origem,
                MusicaPlaylist.usuario_id == usuario_id
            )
        ).scalar_one_or_none()
        
        if not associacao_origem:
            print(f"ERRO: A música de ID {id_musica} não está na playlist de origem.")
            return False
        
        session.delete(associacao_origem)
        
        nova_associacao = MusicaPlaylist(
            musica_id=id_musica,
            playlist_id=id_playlist_destino,
            usuario_id=usuario_id,
            ordem_na_playlist=nova_ordem
        )
        session.add(nova_associacao)

        session.commit()
        
        print(f"Música movida da playlist {id_playlist_origem} para {id_playlist_destino}.")
        return True

    except SQLAlchemyError as e:
        session.rollback()
        print(f"ERRO: Falha ao mover música. Revertendo operações.")
        print(f"Mensagem: {str(e)}")
        return False


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
                colunas = ["id", "titulo", "duracao", "id artista"] 

        elif escolha == "3":
            result = query3()
            colunas = ["Nome Playlist", "Total Musicas"]

        elif escolha == "4":
            result = query4()
            colunas = ["id", "nome", "nacionalidade"]

        elif escolha == "10":
            result = query10()
            colunas = ["nome artista", "total playlists"]

        elif escolha == "11":
            result = query11()
            colunas = ["título", "duração segundos"]

        elif escolha == "12":
            if len(sys.argv) < 7:
                print("Erro: query 12 precisa de usuario_id, id_playlist_origem, id_playlist_destino, id_musica, nova_ordem")
            else:
                usuario_id = int(sys.argv[2])
                id_playlist_origem = int(sys.argv[3])
                id_playlist_destino = int(sys.argv[4])
                id_musica = int(sys.argv[5])
                nova_ordem = int(sys.argv[6])
                query12(usuario_id, id_playlist_origem, id_playlist_destino, id_musica, nova_ordem)
        
        else:
            print("Opção inválida!")
            sys.exit(1)

        # Exibição do Resultado
        if result:
            df = pd.DataFrame(result)
            if len(df.columns) == len(colunas):
                df.columns = colunas
            print("\n\n", df)
        else:
            print("Nenhum resultado encontrado para esta consulta.")

    except Exception as e:
        print(f"Ocorreu um erro ao executar a query: {e}")