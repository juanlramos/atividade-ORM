import datetime
from typing import List, Optional
from sqlalchemy import (
    CheckConstraint, ForeignKeyConstraint,
    Integer, String, UniqueConstraint, Identity,
    TIMESTAMP
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship, DeclarativeBase
)
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

class Artista(Base):
    __tablename__ = 'artista'
    
    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    nacionalidade: Mapped[Optional[str]] = mapped_column(String(100))
    
    musicas: Mapped[List["Musica"]] = relationship(back_populates="artista")

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    
    playlists: Mapped[List["Playlist"]] = relationship(back_populates="usuario", cascade="all, delete-orphan", passive_deletes=True)

class Musica(Base):

    __tablename__ = 'musica'
    
    __table_args__ = (
        CheckConstraint('duracao_segundos > 0', name='check_duracao_positiva'),
        ForeignKeyConstraint(['artista_id'], ['artista.id'], ondelete='RESTRICT', name='fk_artista')
    )
    
    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    duracao_segundos: Mapped[int] = mapped_column(Integer, nullable=False)
    artista_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
    artista: Mapped["Artista"] = relationship(back_populates="musicas")
    
    playlists_associadas: Mapped[List["MusicaPlaylist"]] = relationship(back_populates="musica", cascade="all, delete-orphan", passive_deletes=True)

class Playlist(Base):

    __tablename__ = 'playlist'

    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ondelete='CASCADE', name='fk_usuario'),
    )
    
    playlist_id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    data_criacao: Mapped[datetime.datetime] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    
    usuario: Mapped["Usuario"] = relationship(back_populates="playlists")
    
    musicas_associadas: Mapped[List["MusicaPlaylist"]] = relationship(back_populates="playlist", cascade="all, delete-orphan", passive_deletes=True)

class MusicaPlaylist(Base):

    __tablename__ = 'musica_playlist'
    
    musica_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    playlist_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ordem_na_playlist: Mapped[int] = mapped_column(Integer, nullable=False)
    
    __table_args__ = (
        ForeignKeyConstraint(['musica_id'], ['musica.id'], ondelete='CASCADE', name='fk_musica'),
        ForeignKeyConstraint(
            ['playlist_id', 'usuario_id'],
            ['playlist.playlist_id', 'playlist.usuario_id'], 
            ondelete='CASCADE', 
            name='fk_playlist_composta'
        ),
        UniqueConstraint('playlist_id', 'usuario_id', 'ordem_na_playlist')
    )

    musica: Mapped["Musica"] = relationship(back_populates="playlists_associadas")
    playlist: Mapped["Playlist"] = relationship(back_populates="musicas_associadas")