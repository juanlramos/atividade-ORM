from database import SessionLocal
from schema import Artista, Musica, MusicaPlaylist, Playlist, Usuario
from sqlalchemy import select, func, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload, aliased
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
        .join(Artista, Musica.artista_id == Artista.id)
        .join(MusicaPlaylist, Musica.id == MusicaPlaylist.musica_id)
        .join(Playlist, MusicaPlaylist.playlist_id == Playlist.playlist_id)
        .join(Usuario, Playlist.usuario_id == Usuario.id)
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
        .outerjoin(MusicaPlaylist, Playlist.playlist_id == MusicaPlaylist.playlist_id)
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

# Query 5
# Detalhes Completos da Música com Artista: Crie uma função para buscar uma Música por seu id e, 
# em uma única operação de consulta (evitando o problema N+1), carregue (fetch) automaticamente
# todos os detalhes do Artista relacionado. (Foco em Eager Loading ou Fetching Join).
def query5(musica_id: int):
    query = (
        select(Musica)
        .options(joinedload(Musica.artista)) # Eager loading do Artista associado
        .where(Musica.id == musica_id)
    )
    
    query_result = session.execute(query).scalar()

    return query_result

# Query 6
# Tempo Total de Reprodução da Playlist: Para cada PLAYLIST no sistema,
# calcule e retorne o tempo total de reprodução (soma de duracao_segundos de todas as músicas).
# A saída deve listar o nome da Playlist, o username do Dono e o tempo total de reprodução.
# (Foco em agregação SUM e GROUP BY sobre o N:N).
def query6():
    query = (
        select(
            Playlist.nome,
            Usuario.username,
            func.sum(Musica.duracao_segundos).label("tempo_total")
        )
        .join(Usuario, Playlist.usuario_id == Usuario.id)
        .outerjoin(MusicaPlaylist, Playlist.playlist_id == MusicaPlaylist.playlist_id)
        .outerjoin(Musica, MusicaPlaylist.musica_id == Musica.id)
        .group_by(Playlist.nome, Usuario.username)
        .order_by(desc("tempo_total"))
    )

    query_result = session.execute(query).all()
    
    return query_result

# Query 7
# Músicas Mais Curtas que a Média do Artista: Liste todas as Músicas cujo tempo de duração (duracao_segundos)
# é menor que o tempo de duração médio de todas as músicas do seu próprio Artista (ex: listar músicas do AC/DC
# que são mais curtas que a média do AC/DC). (Foco em subconsultas ou Window Functions se o ORM suportar).
def query7():
    MusicaInner = aliased(Musica)

    # Subconsulta que Calcula a média de duração das músicas do artista da linha atual
    media_artista_subquery = (
        select(func.avg(MusicaInner.duracao_segundos))
        .where(MusicaInner.artista_id == Musica.artista_id) 
        .scalar_subquery()
    )

    query = (
        select(
            Musica.titulo,
            Artista.nome.label("nome_artista"),
            Musica.duracao_segundos,
            media_artista_subquery.label("media_do_artista")
        )
        .join(Musica.artista)
        .where(Musica.duracao_segundos < media_artista_subquery)
        .order_by(Artista.nome)
    )

    query_result = session.execute(query).all()
    return query_result

# Query 8
# Busca em Tabela de Junção com Atributos Extras: Liste o título de todas as Músicas na playlist 'Rock do Pablo',
# incluindo a ordem_na_playlist de cada música.
def query8(nome_playlist: str):
    query = (
        select(Musica.titulo, MusicaPlaylist.ordem_na_playlist)
        .join(MusicaPlaylist, Musica.id == MusicaPlaylist.musica_id)
        .join(Playlist, (MusicaPlaylist.playlist_id == Playlist.playlist_id) & 
                        (MusicaPlaylist.usuario_id == Playlist.usuario_id))
        .where(Playlist.nome == nome_playlist)
        .order_by(MusicaPlaylist.ordem_na_playlist)
    )
    
    query_result = session.execute(query).all()
    return query_result

# Query 9
# Busca por Chave Composta Invertida: Encontre o username do Usuário que é o dono da Playlist
# que contém a MUSICA 'Bohemian Rhapsody'. O filtro deve começar pela MUSICA e navegar de volta para o USUARIO.
def query9(titulo_musica: str):
    query = (
        select(Usuario.username)
        .select_from(Musica)
        .join(MusicaPlaylist, Musica.id == MusicaPlaylist.musica_id)
        .join(Playlist, (MusicaPlaylist.playlist_id == Playlist.playlist_id) & 
                        (MusicaPlaylist.usuario_id == Playlist.usuario_id))
        .join(Usuario, Playlist.usuario_id == Usuario.id)
        .where(Musica.titulo == titulo_musica)
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
        .outerjoin(Musica, Artista.id == Musica.artista_id)
        .outerjoin(MusicaPlaylist, Musica.id == MusicaPlaylist.musica_id)
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
        .join(Artista, Musica.artista_id == Artista.id)
        .where(Artista.nome == 'Led Zeppelin')
        .where(Musica.duracao_segundos > 
                select(func.max(Musica.duracao_segundos))
                .join(Artista, Musica.artista_id == Artista.id)
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

    escolha = sys.argv[1]

    result = []
    colunas = []

    try:
        if escolha == "1":
            if len(sys.argv) < 3:
                print("Erro: Query 1 precisa do username. Ex: python queries.py 1 'Pablo'")
            else:
                username = sys.argv[2]
                result = query1(username)
                colunas = ["Nome Playlist", "Data Criação"]

        elif escolha == "2":
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

        elif escolha == "5":
            if len(sys.argv) < 3:
                print("Erro: Query 5 precisa do ID da música. Ex: python queries.py 5 1")
            else:
                musica_id = int(sys.argv[2])
                musica = query5(musica_id)
                
                if musica:
                    result = [{
                        "ID": musica.id,
                        "Música": musica.titulo,
                        "Artista": musica.artista.nome, 
                        "Nacionalidade do Artista": musica.artista.nacionalidade

                    }]
                else:
                    result = []
        elif escolha == "6":
            result = query6()
            colunas = ["Playlist", "Dono", "Tempo Total (s)"]

        elif escolha == "7":
            result = query7()
            colunas = ["Música", "Artista", "Duração", "Média do Artista"]

        elif escolha == "8":
            if len(sys.argv) < 3:
                print("Erro: Informe o nome da playlist. Ex: python queries.py 8 'Rock do Pablo'")
            else:
                nome_pl = sys.argv[2]
                result = query8(nome_pl)
                colunas = ["Música", "Ordem"]

        elif escolha == "9":
            if len(sys.argv) < 3:
                print("Erro: Informe o título da música. Ex: python queries.py 9 'Bohemian Rhapsody'")
            else:
                titulo = sys.argv[2]
                result = query9(titulo)
                colunas = ["Dono da Playlist"]

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