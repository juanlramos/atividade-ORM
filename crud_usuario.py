from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schema import Usuario

def criar_usuario(session: Session, username: str, email: str) -> Usuario:
    novo_usuario = Usuario(username=username, email=email)
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    return novo_usuario

def obter_usuario_por_id(session: Session, usuario_id: int) -> Usuario | None:
    usuario = session.get(Usuario, usuario_id)
   
    return usuario

def atualizar_email_usuario(session: Session, usuario_id: int, novo_email: str) -> Usuario | None:
    usuario = session.get(Usuario, usuario_id)
    if usuario:
        usuario.email = novo_email
        try:
            session.commit()
            session.refresh(usuario)
            return usuario
        
        except IntegrityError as e:
            session.rollback()
            return None
        
    return None

def excluir_usuario(session: Session, usuario_id: int) -> bool:
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        return False
    
    try:
        session.delete(usuario)
        session.commit()
        return True
    
    except IntegrityError as e:
        session.rollback()
        return False

