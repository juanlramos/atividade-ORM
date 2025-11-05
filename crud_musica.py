from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schema import Musica

def criar_musica(session: Session, titulo: str, duracao: int, artista_id: int) -> Musica:
    nova_musica = Musica(titulo=titulo, duracao_segundos=duracao, artista_id=artista_id)
    session.add(nova_musica)
    session.commit()
    session.refresh(nova_musica)

    return nova_musica

def obter_musica_por_id(session: Session, musica_id: int) -> Musica | None:
    musica = session.get(Musica, musica_id)

    return musica

def atualizar_titulo_musica(session: Session, musica_id: int, novo_titulo: str) -> Musica | None:
    musica = session.get(Musica, musica_id)
    if musica:
        musica.titulo = novo_titulo
        session.commit()
        session.refresh(musica)

        return musica
    
    return None

def excluir_musica(session: Session, musica_id: int) -> bool:
    musica = session.get(Musica, musica_id)
    if not musica:
        return False
    
    try:
        session.delete(musica)
        session.commit()
        return True
    
    except IntegrityError as e:
        session.rollback()
        return False

