from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schema import Artista

def criar_artista(session: Session, nome: str, nacionalidade: str) -> Artista:
    novo_artista = Artista(nome=nome, nacionalidade=nacionalidade)
    session.add(novo_artista)
    session.commit()
    session.refresh(novo_artista)

    return novo_artista

def obter_artista_por_id(session: Session, artista_id: int) -> Artista | None:
    artista = session.get(Artista, artista_id)
 
    return artista

def atualizar_nacionalidade_artista(session: Session, artista_id: int, nova_nacionalidade: str) -> Artista | None:
    artista = session.get(Artista, artista_id)
    if artista:
        artista.nacionalidade = nova_nacionalidade
        session.commit()
        session.refresh(artista)

    return artista

def excluir_artista(session: Session, artista_id: int) -> bool:
    artista = session.get(Artista, artista_id)

    if not artista:
        return False
    
    try:
        session.delete(artista)
        session.commit()
        return True
    
    except IntegrityError as e:
        session.rollback()
        return False