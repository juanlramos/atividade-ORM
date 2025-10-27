-- Base de dados

CREATE TABLE ARTISTA (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL UNIQUE,
    nacionalidade VARCHAR(100)
);

CREATE TABLE USUARIO (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE PLAYLIST (
    playlist_id SERIAL, 
    usuario_id INTEGER NOT NULL,
    nome VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (playlist_id, usuario_id),
    CONSTRAINT fk_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES USUARIO (id)
        ON DELETE CASCADE
);

CREATE TABLE MUSICA (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    duracao_segundos INTEGER NOT NULL CHECK (duracao_segundos > 0),
    artista_id INTEGER NOT NULL,
    
    CONSTRAINT fk_artista
        FOREIGN KEY (artista_id)
        REFERENCES ARTISTA (id)
        ON DELETE RESTRICT
);

CREATE TABLE MUSICA_PLAYLIST (
    musica_id INTEGER NOT NULL,
    playlist_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    ordem_na_playlist INTEGER NOT NULL,
    
    CONSTRAINT fk_musica
        FOREIGN KEY (musica_id)
        REFERENCES MUSICA (id)
        ON DELETE CASCADE,
    
    CONSTRAINT fk_playlist_composta
        FOREIGN KEY (playlist_id, usuario_id)
        REFERENCES PLAYLIST (playlist_id, usuario_id)
        ON DELETE CASCADE,
    
    PRIMARY KEY (musica_id, playlist_id, usuario_id),
    UNIQUE (playlist_id, usuario_id, ordem_na_playlist)
);

INSERT INTO ARTISTA (nome, nacionalidade) VALUES
('Queen', 'Britânica'),        -- ID 1
('Led Zeppelin', 'Britânica'),  -- ID 2
('AC/DC', 'Australiana'),       -- ID 3
('Banda X (Pop)', 'Brasileira'); -- ID 4

INSERT INTO USUARIO (username, email) VALUES
('Pablo', 'pablo@aluno.com'),       -- ID 1
('Josue', 'josue@aluno.com'),       -- ID 2
('Alexandre', 'alexandre@aluno.com'); -- ID 3

INSERT INTO MUSICA (titulo, duracao_segundos, artista_id) VALUES
('Bohemian Rhapsody', 354, 1),    -- ID 1 (Queen)
('Stairway to Heaven', 482, 2),   -- ID 2 (Led Zeppelin)
('Back In Black', 255, 3),        -- ID 3 (AC/DC)
('We Will Rock You', 160, 1),     -- ID 4 (Queen)
('Musica Pop Brasileira', 180, 4),-- ID 5 (Banda X)
('Thunderstruck', 292, 3);        -- ID 6 (AC/DC)

INSERT INTO PLAYLIST (playlist_id, usuario_id, nome) VALUES
(1, 1, 'Rock do Pablo'), 
(2, 2,'Baladas do Josue'), 
(3, 1, 'Heavy Riffs');  

-- MUSICA_PLAYLIST
-- Playlist (1, 1): 'Rock do Pablo'
INSERT INTO MUSICA_PLAYLIST (musica_id, playlist_id, usuario_id, ordem_na_playlist) VALUES
(1, 1, 1, 1), (3, 1, 1, 2), (4, 1, 1, 3); 

-- Playlist (2, 2): 'Baladas do Josue'
INSERT INTO MUSICA_PLAYLIST (musica_id, playlist_id, usuario_id, ordem_na_playlist) VALUES
(2, 2, 2, 1);

-- Playlist (3, 1): 'Heavy Riffs'
INSERT INTO MUSICA_PLAYLIST (musica_id, playlist_id, usuario_id, ordem_na_playlist) VALUES
(3, 3, 1, 1), (6, 3, 1, 2);
