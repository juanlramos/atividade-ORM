import os
import sys
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

load_dotenv()

app = Flask(__name__)

# Configuração do Banco
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Definição dos Modelos

class Artista(db.Model):
    __tablename__ = 'artista'

    # Colunas
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False, unique=True)
    nacionalidade = db.Column(db.String(100))

    # Relacionamentos
    musicas = db.relationship('Musica', back_populates='artista')


class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)

    playlists = db.relationship('Playlist', 
                                back_populates='usuario', 
                                cascade='all, delete-orphan')

class Musica(db.Model):
    __tablename__ = 'musica'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    duracao_segundos = db.Column(db.Integer, nullable=False)
    
    artista_id = db.Column(db.Integer, 
                           db.ForeignKey('artista.id', ondelete='RESTRICT'), 
                           nullable=False)
    
    __table_args__ = (
        db.CheckConstraint('duracao_segundos > 0', name='check_duracao_positiva'),
    )

    artista = db.relationship('Artista', back_populates='musicas')
    
    playlists_association = db.relationship('MusicaPlaylist',
                                            back_populates='musica',
                                            cascade='all, delete-orphan')


class Playlist(db.Model):
    __tablename__ = 'playlist'

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, 
                           db.ForeignKey('usuario.id', ondelete='CASCADE'), 
                           primary_key=True, 
                           nullable=False)
    
    nome = db.Column(db.String(255), nullable=False)
    
    data_criacao = db.Column(db.DateTime, 
                             server_default=db.func.current_timestamp())
    
    usuario = db.relationship('Usuario', back_populates='playlists')
    
    # --- AQUI ESTAVA O ERRO (AGORA CORRIGIDO) ---
    # Apontava para 'Playlist', agora aponta para 'MusicaPlaylist'
    musicas_association = db.relationship('MusicaPlaylist',
                                          back_populates='playlist',
                                          cascade='all, delete-orphan')



class MusicaPlaylist(db.Model):
    __tablename__ = 'musica_playlist'

    musica_id = db.Column(db.Integer, 
                          db.ForeignKey('musica.id', ondelete='CASCADE'), 
                          primary_key=True)
    
    playlist_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, primary_key=True)
    ordem_na_playlist = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['playlist_id', 'usuario_id'], 
            ['playlist.playlist_id', 'playlist.usuario_id'], 
            ondelete='CASCADE',
            name='fk_playlist_composta'
        ),
        db.UniqueConstraint('playlist_id', 'usuario_id', 'ordem_na_playlist', 
                            name='uq_playlist_ordem')
    )

    musica = db.relationship('Musica', back_populates='playlists_association')
    playlist = db.relationship('Playlist', back_populates='musicas_association')
